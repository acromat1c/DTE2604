from django.db import models
from django.contrib.auth.models import User




class Friend(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_user2")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user1', 'user2'], name='unique_friends'),
            models.CheckConstraint(
                check=models.Q(user1__lt=models.F('user2')),
                name='user1_smaller_than_user2'
            ),
        ]

class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_requests_sent")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_requests_received")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sender', 'recipient'], name='unique_friend_request')
        ]

class Achievement(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    time = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'achievement'], name='unique_user_achievement')
        ]

class Group(models.Model):
    groupOwner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_groups")
    groupName = models.CharField(max_length=45)

    def __str__(self):
        return self.groupName

class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['group', 'user'], name='unique_group_member')
        ]

class GroupMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)

itemTypes = ["collectible", "other", "theme"]

class Item(models.Model):
    name = models.CharField(max_length=1000)
    category = models.CharField(max_length=1000)
    itemType = models.CharField(max_length=1000, choices=[[x,x] for x in itemTypes])
    price = models.IntegerField()
    shop = models.BooleanField()
    description = models.CharField(max_length=10000)
    image = models.ImageField(upload_to='item_pic/')
    content = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    text = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_course')
        ]

    def __str__(self):
        return self.name

class Module(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    text = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'course'], name='unique_module')
        ]

    def __str__(self):
        return f"{self.name} | {self.course}"

class Mission(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    text = models.TextField()
    answer = models.CharField(max_length=1000)
    maxPoints = models.IntegerField()
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    reward = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL, default=None)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'module'], name='unique_Mission')
        ]

    def __str__(self):
        return f"{self.name} | {self.module}"

class MissionCompleted(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.IntegerField()
    answer = models.CharField(max_length=1000)
    completed = models.BooleanField()

    class Meta:
            constraints = [
                models.UniqueConstraint(fields=['user', 'mission'], name='unique_complete')
            ]

    def __str__(self):
        return f"{self.user} | {self.mission}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return f'{self.user} Profile'

class UserBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField()
    allTimeBalance = models.IntegerField()

    def __str__(self):
        return str(self.user)

class UserInventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    timestamp = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'item'], name='unique_item')
        ]

    def __str__(self):
        return f"{self.user} | {self.item}"

class UserTheme(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.user} | {self.item}"