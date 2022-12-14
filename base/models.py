from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django_resized import ResizedImageField
from datetime import datetime
import time
# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True, blank=True)
    hackathon_participant = models.BooleanField(default=True, null=True)

    avatar =  ResizedImageField(size=[400,400], default='avatar.png')

    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    twitter = models.URLField(max_length=500, null=True, blank=True)
    linkedin = models.URLField(max_length=500, null=True, blank=True)
    website = models.URLField(max_length=500, null=True, blank=True)
    facebook = models.URLField(max_length=500, null=True, blank=True)
    github = models.URLField(max_length=500, null=True, blank=True)

    class Meta:
        ordering = ['avatar']



class Event(models.Model):
    name = models.CharField(max_length=200)
    preview = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, blank=True, related_name='events')
    date = models.DateTimeField()
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    registration_deadline = models.DateTimeField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-end_date']

    @property
    def event_status(self):
        status = None

        present = datetime.now().timestamp()
        deadline = self.registration_deadline.timestamp()
        past_deadline = (present > deadline)

        if past_deadline:
            status = 'Finished'
        else : 
            status = 'Ongoing'

        return status


class Submission(models.Model):
    participant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="submissions")
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    project_url = models.URLField(max_length=500, null=True, blank=True)
    details = models.TextField(null=True, blank=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)

    def __str__(self):
        return str(self.event) + ' --- ' + str(self.participant)


