from django.db import models
from login.models import Login

class RestrictedAreaData(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='restricted_area_data')
    video_name = models.CharField(max_length=255)
    person_count = models.IntegerField()

    def __str__(self):
        return f"RestrictedAreaData(id={self.id}, user={self.user.user_name}, video_name={self.video_name}, person_count={self.person_count})"
