from django.db import models

# Create your models here
class Influencer(models.Model):
    username = models.CharField(max_length = 100, unique=True)
    full_name = models.CharField(max_length = 100, null=True, blank=True)

    def __str__(self):
        return self.username

class Post(models.Model):
    influencer = models.ForeignKey(Influencer, on_delete = models.CASCADE)
    post_id = models.CharField(max_length = 100, unique = True)
    caption = models.TextField(null=True, blank=True)
    media_url = models.URLField(max_length = 500)
    like_count = models.IntegerField()
    comment_count = models.IntegerField()
    created_at = models.DateTimeField()
    is_video = models.BooleanField(default=False)

    def __str__(self):
        return self.post_id


class Story(models.Model):
    influencer = models.ForeignKey(Influencer, on_delete = models.CASCADE)
    story_id = models.CharField(max_length = 100, unique = True)
    media_url = models.URLField(max_length = 500)
    created_at = models.DateTimeField()
    is_video = models.BooleanField(default=False)

    def __str__(self):
        return self.story_id

