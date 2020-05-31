from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20)

    def __str__(self):
        return '<Profile:%s for %s>' %(self.nickname, self.user.username)


#给User类赋予的动态方法
def get_nickname(self):
    if Profile.objects.filter(user = self).exists:
        profile = Profile.objects.get(user = self)
        return profile.nickname
    else:
        return self.username

User.get_nickname = get_nickname