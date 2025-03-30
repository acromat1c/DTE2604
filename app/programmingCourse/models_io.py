from .models import *
from django.db.utils import IntegrityError

def get_course_list():
    try:
        return Course.objects.values_list("name", "description")
    except:
        return None

def get_course(nameCourse):
    try:
        return Course.objects.get(name=nameCourse)
    except:
        return None

def get_module_list(nameCourse):
    try:
        return Module.objects.filter(course__name=nameCourse).values_list("name", "description")
    except:
        return None

def get_module(nameCourse, nameModule):
    try:
        return Module.objects.get(name=nameModule, course__name=nameCourse)
    except:
        return None

def get_mission_list(nameCourse, nameModule):
    try:
        return Mission.objects.filter(module=Module.objects.get(name=nameModule, course__name=nameCourse)).values_list("name", "description")
    except:
        return None

def get_mission(nameCourse, nameModule, nameMission):
    try:
        return Mission.objects.get(name=nameMission, module=Module.objects.get(name=nameModule, course__name=nameCourse))
    except:
        return None

def get_mission_completed(mission, user):
    try:
        return MissionCompleted.objects.get(user=user, mission=mission)
    except:
        return None

def set_mission_completed(mission, user, time, answer):
    userAnswer = get_mission_completed(mission, user)
    if userAnswer != None: 
        completed = userAnswer.completed
    else:
        completed = False
    if answer == mission.answer and not completed:
        add_user_balance(user,mission.maxPoints)
        completed = True
    mission_completed, created = MissionCompleted.objects.update_or_create(
        mission=mission,
        user=user,
        defaults={
            "completionTime": time,
            "answer": answer,
            "completed": completed,})
    return mission_completed

def friend_request(sender, recipient):
    try:
        r = FriendRequest(sender = sender, recipient = recipient)
        r.save()
        return True
    except :
        return False

def undo_friend_request(sender, recipient):
    try:
        r = FriendRequest.objects.get(sender=sender, recipient=recipient)
        r.delete()
        return True
    except:
        return False

def accept_friend_request(accepter, sender):
    try:
        r = FriendRequest.objects.get(sender=sender, recipient=accepter)
        r.delete()
        try:
            f = Friend(user1=sender, user2=accepter)
            f.save()
        except IntegrityError:
            f = Friend(user1=accepter, user2=sender)
            f.save()
        return True
    except Exception as e:
        print(e)
        return False

def remove_friend(remover, friend):
    try:
        if Friend.objects.filter(user1=remover, user2=friend).exists():
            f = Friend.objects.get(user1=remover, user2=friend)
            f.delete()
            return True
        elif Friend.objects.filter(user1=friend, user2=remover).exists():
            f = Friend.objects.get(user1=friend, user2=remover)
            f.delete()
            return True
    except:
        return False
    

def decline_friend_request(recipient, sender):
    try:
        r = FriendRequest.objects.get(sender=sender, recipient=recipient)
        r.delete()
        return True
    except:
        return False

def get_friend_status(sender, recipient) -> int:
    NOT_FRIEND = 0
    SENT_REQUEST = 1
    RECIEVED_REQUEST = 2
    IS_FRIEND = 3
    if Friend.objects.filter(user1=sender, user2=recipient).exists():
        return IS_FRIEND
    elif Friend.objects.filter(user1=recipient, user2=sender).exists():
        return IS_FRIEND
    elif FriendRequest.objects.filter(sender=sender, recipient=recipient).exists():
        return SENT_REQUEST
    elif FriendRequest.objects.filter(sender=recipient, recipient=sender).exists():
        return RECIEVED_REQUEST
    else:
        return NOT_FRIEND

def get_friends(user) -> list:
    friends = [x.user2 for x in Friend.objects.filter(user1=user)]
    friends.extend([x.user1 for x in Friend.objects.filter(user2=user)])
    return friends

def get_user_balance(user):
    try:
        return UserBalance.objects.get(user=user).balance
    except:
        UserBalance.objects.create(user=user, balance=0)
        return 0

def add_user_balance(user, amount):
    try:
        newBalance = UserBalance.objects.get(user=user).balance + amount
    except:
        newBalance = amount
    model, created = UserBalance.objects.update_or_create(user=user, defaults={"balance": newBalance})
    return model, created

def get_user_inventory(user):
    try:
        return UserInventory.objects.filter(user=user)
    except:
        return None

def get_shop_items(user):
    try:
        if user == None: ownedItems = []; balance = 0
        else: ownedItems = [str(x.item.id) for x in get_user_inventory(user)]; balance = get_user_balance(user)
        return sorted([{"category": category, "items": [{"item":x,"owned":str(x.id) in ownedItems, "afford": balance - x.price >= 0} for x in Item.objects.filter(shop=True, category=category)[::-1]]} for category in Item.objects.filter(shop=True).values_list("category", flat=True).distinct() ], key=lambda i: i["category"])
    except:
        return None

def purchase_item(user, itemID):
    price = (Item.objects.get(id=itemID).price)*-1
    if get_user_balance(user) + price >= 0: 
        if itemID not in [str(x.item.id) for x  in get_user_inventory(user)] and itemID in [str(x.id) for x in Item.objects.filter(shop=True)]:
                UserInventory.objects.update_or_create(user=user, item=Item.objects.get(id=itemID))
                add_user_balance(user, price)


def get_inventory_items(user):
    return sorted([{"category": category, "items": [{"item":x,"active": False} for x in Item.objects.filter(category=category)[::-1] if str(x.id) in [str(x.item.id) for x  in get_user_inventory(user)]]} for category in Item.objects.filter().values_list("category", flat=True).distinct() ], key=lambda i: i["category"])
