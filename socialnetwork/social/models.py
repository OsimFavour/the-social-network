from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Post(models.Model):
    body = models.TextField()
    image = models.ImageField(upload_to='uploads/post_photos', blank=True, null=True)
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')

    def __str__(self):
        return f"{self.author.username} Post Page"



class Comment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='comment_dislikes')

    # the related name as + takes away the reverse mapping, so we can't
    # necessarily get the children from this field. Instead we'll create
    # a separate property to handle that
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')

    # A property method allows us to access a function within the 
    # actual template itself
    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-created_on').all()
    
    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
    

# create a foreignkey relationship between the user profile model
# and the user model, one user can have one profile and one 
# profile can have one user
class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name="user", related_name="profile", on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to='uploads/profile_pictures', default='uploads/profile_pictures/default.png')
    followers = models.ManyToManyField(User, blank=True, related_name='followers')

    def __str__(self):
        return f"{self.user.username} Profile"

# All we need to use django signals
# sender -> User
# receiver -> decorator (@receiver)
# instance -> User object being saved
# created -> true/false


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """To create the user profile instantly with django signals"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the user profile with django signals"""
    instance.profile.save()


class Notification(models.Model):
    # 1 = Like, 2 = Comment, 3 = Follow
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(User, related_name="notification_to", on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, related_name="notification_from", on_delete=models.CASCADE, null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name="+", blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)


class ThreadModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

class MessageModel(models.Model):
    thread = models.ForeignKey('ThreadModel', related_name='+', on_delete=models.CASCADE, blank=True, null= True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    body = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='uploads/message_photos', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)