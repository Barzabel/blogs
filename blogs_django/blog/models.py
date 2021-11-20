from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


class TimestampedModel(models.Model):
    """An abstract model with a pair of timestamps."""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Like_dislike(models.Model):

    def like(self):
        ClipLike.objects.create(clip=self)

    def dislike(self):
        ClipDislike.objects.create(clip=self)

    @classmethod
    def rates_for(cls, **kwargs) -> (int, int):
        """
        Returns a tuple of integers (likes, dislikes)
        for the clip(s) filtered by provided kwargs.
        """
        aggregate = cls.objects.filter(
            **kwargs,
        ).annotate(
            likes=models.Count('cliplike', distinct=True),
            dislikes=models.Count('clipdislike', distinct=True),
        ).aggregate(
            models.Sum('likes'),
            models.Sum('dislikes'),
        )
        return (
            aggregate['likes__sum'],
            aggregate['dislikes__sum'],
        )


class ClipLike(models.Model):
    clip = models.ForeignKey(Like_dislike, on_delete=models.CASCADE)


class ClipDislike(models.Model):
    clip = models.ForeignKey(Like_dislike, on_delete=models.CASCADE)


class Profile(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(max_length=500, blank=True)


class Tag(TimestampedModel):
    """A tag for the group of posts."""

    title = models.CharField(max_length=100)


class Post(TimestampedModel):
    """A blog post."""

    title = models.CharField(max_length=200)
    body = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    like_dislike = models.OneToOneField(Like_dislike, on_delete=models.CASCADE)


class PostComment(TimestampedModel):
    """A commentary to the blog post."""

    body = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    response_to = models.ForeignKey(
        'PostComment', on_delete=models.SET_NULL, null=True,
    )
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    like_dislike = models.OneToOneField(Like_dislike, on_delete=models.CASCADE)

@receiver(pre_save, sender=Post)
def create_Post(sender, instance, **kwargs):
    model = Like_dislike.objects.create()
    instance.like_dislike = model


@receiver(pre_save, sender=PostComment)
def create_Post(sender, instance, **kwargs):
    if instance.like_dislike is None:
        model = Like_dislike.objects.create()
        instance.like_dislike = model


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
