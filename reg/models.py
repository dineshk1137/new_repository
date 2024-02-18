from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Rec(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    title = models.CharField(max_length = 50)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    address = models.CharField(max_length = 50)
    time = models.TimeField()
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank = True)
    rsvp_users = models.ManyToManyField(User, related_name='rsvps', blank=True)
    description = models.TextField(null=True, blank = True)

    def __str__(self):
        return(f"{self.title} , {self.address}")

