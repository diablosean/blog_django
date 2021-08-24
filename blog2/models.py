from django.db import models
from django.urls import reverse


# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField()
    timestamp = models.DateTimeField()

    def get_absolute_url(self):
        return reverse('blog2:post_detail', args=[self.title])
