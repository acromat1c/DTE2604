from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Group, GroupMember, GroupMessage, GroupJoinRequest

class GroupTests(TestCase):
    def setUp(self):
        # Create users

        self.owner = User.objects.create_user(username="owner", password="testpass")
        self.member = User.objects.create_user(username="member", password="testpass")

        # Create group
        self.group = Group.objects.create(groupOwner=self.owner, groupName="Test Group")

    def test_group_creation(self):
        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(self.group.groupOwner.username, "owner")

    def test_join_group(self):
        self.client.login(username="member", password="testpass")
        response = self.client.post(f"/groups/{self.group.groupName}", {"action": "join"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(GroupMember.objects.filter(group=self.group, user=self.member).exists())

    def test_chat_message_post(self):
        GroupMember.objects.create(group=self.group, user=self.member)
        self.client.login(username="member", password="testpass")
        response = self.client.post(f"/groups/{self.group.groupName}", {"message": "Hello!"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(GroupMessage.objects.count(), 1)
        msg = GroupMessage.objects.first()
        self.assertEqual(msg.message, "Hello!")
        self.assertEqual(msg.user.username, "member")

    def test_private_group_creates_join_request(self):
        self.group.is_private = True
        self.group.save()

        self.client.login(username="member", password="testpass")
        response = self.client.post(f"/groups/{self.group.groupName}", {"action": "join"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(GroupJoinRequest.objects.filter(group=self.group, user=self.member).exists())

    def test_owner_approves_join_request(self):
        GroupJoinRequest.objects.create(group=self.group, user=self.member)

        self.client.login(username="owner", password="testpass")
        response = self.client.post(f"/groups/{self.group.groupName}/requests", {
            "user_id": self.member.id,
            "action": "approve"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(GroupMember.objects.filter(group=self.group, user=self.member).exists())
        self.assertFalse(GroupJoinRequest.objects.filter(group=self.group, user=self.member).exists())

    def test_muted_user_cannot_chat(self):
        GroupMember.objects.create(group=self.group, user=self.member, is_muted=True)
        self.client.login(username="member", password="testpass")
        self.client.post(f"/groups/{self.group.groupName}", {"message": "Muted message"})
        self.assertEqual(GroupMessage.objects.count(), 0)

    def test_owner_can_kick_member(self):
        GroupMember.objects.create(group=self.group, user=self.member)
        self.client.login(username="owner", password="testpass")
        response = self.client.post(f"/groups/{self.group.groupName}", {
            "action": "kick",
            "target_id": self.member.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(GroupMember.objects.filter(group=self.group, user=self.member).exists())

    def test_kicked_user_cannot_post(self):
        # Member joins and gets kicked
        GroupMember.objects.create(group=self.group, user=self.member)
        self.client.login(username="owner", password="testpass")
        self.client.post(f"/groups/{self.group.groupName}", {
            "action": "kick",
            "target_id": self.member.id
        })

        self.client.login(username="member", password="testpass")
        response = self.client.post(f"/groups/{self.group.groupName}", {"message": "Should not send"})
        self.assertEqual(GroupMessage.objects.count(), 0)

    def test_unmute_user_can_chat(self):
        GroupMember.objects.create(group=self.group, user=self.member, is_muted=True)
        self.client.login(username="owner", password="testpass")
        self.client.post(f"/groups/{self.group.groupName}", {
            "action": "unmute",
            "target_id": self.member.id
        })

        self.client.login(username="member", password="testpass")
        self.client.post(f"/groups/{self.group.groupName}", {"message": "Now I can speak!"})
        self.assertEqual(GroupMessage.objects.count(), 1)

    def test_owner_cannot_be_kicked(self):
        # Try to kick the owner (shouldn't do anything)
        GroupMember.objects.create(group=self.group, user=self.owner)
        self.client.login(username="owner", password="testpass")
        response = self.client.post(f"/groups/{self.group.groupName}", {
            "action": "kick",
            "target_id": self.owner.id
        })
        # Owner should still be in the group
        self.assertTrue(GroupMember.objects.filter(group=self.group, user=self.owner).exists())

    def test_non_member_cannot_see_chat(self):
        self.client.login(username="member", password="testpass")
        response = self.client.get(f"/groups/{self.group.groupName}")
        # Should not see chat box HTML
        self.assertNotContains(response, '<h2>Group Chat')