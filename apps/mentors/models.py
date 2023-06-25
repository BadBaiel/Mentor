from django.db import models
from static.image import *
from apps.users.models import User

class Skills(models.Model):
    text = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.text}'

    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'


class Employment(models.Model):
    weekday = models.CharField(max_length=20)
    weekend = models.CharField(max_length=20)

    def __str__(self):
        return f'Weekday: {self.weekday}' \
               f'Weekend: {self.weekend}'


class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False, blank=True)
    image = models.ImageField(blank=True, upload_to='mentors/', default='mentors/default.jpg')
    group = models.CharField(max_length=20)
    name = models.CharField(max_length=15)
    about_me = models.TextField()
    contact = models.URLField()
    directions = models.CharField(max_length=255)
    month = models.CharField(max_length=255)
    skills = models.ManyToManyField(Skills)
    employment = models.ForeignKey(Employment, on_delete=models.CASCADE)
    time_create = models.DateTimeField(auto_now_add=True, null=True)
    time_update = models.DateTimeField(auto_now=True, null=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')
    is_mentor = models.BooleanField(default=False)


    @property
    def likes_count(self):
        return self.likes.count()

    #@classmethod
    #def get_mentors_by_rating(cls):
    #    return cls.objects.annotate(likes_count=models.Count('likes')).order_by('-likes_count')

    @property
    def dislikes_count(self):
        return self.dislikes.count()

    @property
    def students_count(self):
        return self.dislikes_count + self.likes_count

    class Meta:
        verbose_name = 'Mentor'
        verbose_name_plural = 'Mentors'

    def __str__(self):
        return f'{self.name}'







