from django.db import models
import uuid
from decimal import Decimal
from django.contrib.auth.models import User


class Post(models.Model):
    """Markers added by the users"""
    #id        = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user      = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    title     = models.CharField(max_length=50, default='')
    body      = models.TextField(default='')
    dateNtime = models.DateTimeField(auto_now_add=True, auto_now=False)
    latitude  = models.DecimalField(max_digits=22, decimal_places=18, default=Decimal(0.00))
    longitude = models.DecimalField(max_digits=22, decimal_places=18, default=Decimal(0.00))
    was_there = models.BooleanField(default=False)
    #slug     = models.SlugField(default='', max_length=150, unique=True)
    # attachments:
    youtube_url  = models.URLField(default='')
    attachment   = models.FileField(default='', upload_to='uploaded_files')

    def __str__(self):
        return self.title

    def __unicode__(self):  # what does this do?!
        return self.title


class Like(models.Model):
    """ Likes given to a Marker """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s' % (self.post.title, ':' ,self.user.username)


"""class Comment(models.Models):
    #Comments on a Marker
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(default='') """


#this was used when searched for a marker
"""class SearchQueries(models.Model):
    title = models.CharField(max_length=50, default='')
    latitude  = models.DecimalField(max_digits=22, decimal_places=18, default=Decimal(0.00))
    longitude = models.DecimalField(max_digits=22, decimal_places=18, default=Decimal(0.00))
    dateNtime = models.DateTimeField(auto_now_add=True, auto_now=False)
    youtube_url  = models.URLField(default='')
    body = models.TextField(default='')
    # attachments:
    youtube_url  = models.URLField(default='')
    # image = models.ImageField()
    # video = models.filefield()

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title
"""
