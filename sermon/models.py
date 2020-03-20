from django.db import models
# from django.contrib.auth.models import User


class Track(models.Model):
    title = models.CharField(max_length=250)
    url = models.URLField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=250)
    # author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title
