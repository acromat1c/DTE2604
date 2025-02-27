from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=45)
    nameDiscriminator = models.IntegerField()
    passwordHash = models.CharField(max_length=45)
    passwordSalt = models.CharField(max_length=45)
    email = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return f"{self.name}#{self.nameDiscriminator}"


class Friend(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_user2")

    class Meta:
        unique_together = ('user1', 'user2')


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_requests_sent")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_requests_received")


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
        unique_together = ('user', 'achievement')


class Group(models.Model):
    groupOwner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_groups")
    groupName = models.CharField(max_length=45)

    def __str__(self):
        return self.groupName


class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('group', 'user')


class Course(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Module(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=1000)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Mission(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=1000)
    maxPoints = models.IntegerField()
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class MissionCompleted(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField()
    completionTime = models.DateField()