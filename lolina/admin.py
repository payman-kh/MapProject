from django .contrib import admin
from .models import Post, Comment, Like
from users.models import Profile

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
