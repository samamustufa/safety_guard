
from django.db import models
from login.models import Login

class RestrictedAreaData(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    video_name = models.CharField(max_length=255)
    person_count = models.IntegerField()

    def __str__(self):
        return f"RestrictedAreaData(id={self.id}, user_id={self.user_id}, video_name={self.video_name}, person_count={self.person_count})"
