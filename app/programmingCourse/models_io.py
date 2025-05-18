from .models import *
from django.db.utils import IntegrityError
from django.contrib import messages
import time
from random import choice

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

def get_mission_completed(user, mission):
    try:
        return MissionCompleted.objects.get(user=user, mission=mission)
    except:
        return None

def set_mission_completed(user, mission, answer):
    try:
        userAnswer = get_mission_completed(user, mission)
        correct = mission.evaluate_answer(answer)
        if userAnswer != None: 
            completed = userAnswer.completed
        else:
            completed = False
        if correct and not completed:
            add_user_allTimeBalance(user,mission.maxPoints)
            completed = True
            if mission.reward:
                add_item(user,mission.reward)
        mission_completed, created = MissionCompleted.objects.update_or_create(
            mission=mission,
            user=user,
            defaults={
                "timestamp": int(time.time()),
                "answer": answer,
                "completed": completed,
                "correct": correct,})
        return mission_completed
    except:
        return None

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

def get_friend_request_senders(recipient) -> list:
    senders = [request.sender for request in FriendRequest.objects.filter(recipient=recipient)]
    return senders

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

def search_users(search, user) -> list:
    results = [x for x in User.objects.filter(username__icontains=search)]
    if user in results:
        results.remove(user)
    return results

def get_user_balance(user):
    try:
        return UserBalance.objects.get(user=user).balance
    except:
        try:
            UserBalance.objects.create(user=user, balance=0)
        except:
            return 0

def add_user_allTimeBalance(user, amount):
    try:
        newBalance = UserBalance.objects.get(user=user).balance + amount
    except:
        newBalance = amount
    try:
        UserBalance.objects.update_or_create(user=user, defaults={"balance": newBalance, "allTimeBalance": newBalance})
        return True
    except:
        return False

def add_user_balance(user, amount):
    try:
        newBalance = UserBalance.objects.get(user=user).balance + amount
    except:
        newBalance = amount
    try:
        try:
            UserBalance.objects.update_or_create(user=user, defaults={"balance": newBalance})
        except:
            UserBalance.objects.update_or_create(user=user, defaults={"balance": newBalance, "allTimeBalance": newBalance})
        return True
    except:
        return False

def get_user_inventory(user):
    try:
        return [x.item for x  in UserInventory.objects.filter(user=user).order_by("timestamp")][::-1]
    except:
        return None

def get_shop_items(user):
    try:
        if user == None: ownedItems = []; balance = 0
        else: ownedItems = [str(x.id) for x in get_user_inventory(user)]; balance = get_user_balance(user)
        return [{"category": category, "items": [{"item":x,"owned":str(x.id) in ownedItems, "afford": balance - x.price >= 0} for x in Item.objects.filter(shop=True, category=category)[::-1]]} for category in sorted(Item.objects.filter(shop=True).values_list("category", flat=True).distinct()) ]
    except:
        return None

def purchase_item(user, itemID):
    try:
        price = (Item.objects.get(id=itemID).price)*-1
        if get_user_balance(user) + price >= 0: 
            if itemID not in [str(x.id) for x  in get_user_inventory(user)] and itemID in [str(x.id) for x in Item.objects.filter(shop=True)]:
                    add_item(user, Item.objects.get(id=itemID))
                    add_user_balance(user, price)
                    return True
    except:
        return False

def get_inventory_items(user):
    try:
        userInventory = get_user_inventory(user)
        equippedItems = get_equipped_items(user)
        equippable = get_equippable_item_types()
        return [{"category": category, "items": [{"item":x,"active": x.id in equippedItems, "equippable": x.itemType in equippable} for x in [x for x in userInventory if x.category == category]]} for category in sorted(set([x.category for x in userInventory]))]
    except:
        return None

def get_gatcha_items(user):
    try:
        if user == None: ownedItems = []
        else: ownedItems = [str(x.id) for x in get_user_inventory(user)]
        return [x for x in [{"category": category, "items": len([x for x in Item.objects.filter(gatcha=True, category=category)[::-1] if str(x.id) not in ownedItems])} for category in sorted(Item.objects.filter(gatcha=True).values_list("category", flat=True).distinct()) ] if x["items"]!=0]
    except:
        return None
        
def play_gatcha(user, price):
    try:
        balance = get_user_balance(user)
        if balance < price: return None
        ownedItems = [str(x.id) for x in get_user_inventory(user)]
        items = [x for x in Item.objects.filter(gatcha=True) if str(x.id) not in ownedItems]
        if items == []: return None
        item = choice(items)
        add_item(user, item)
        add_user_balance(user, price*-1)
        return item
    except:
        return None


def add_item(user, item):
    try:
        UserInventory.objects.update_or_create(user=user, item=item, defaults={"timestamp":int(time.time())})
        return True
    except:
        return False

def add_starter_items(user):
    default_theme = Item.objects.get(name="Default Theme")
    no_title = Item.objects.get(name="No title")
    no_border = Item.objects.get(name="No Profile Border")
    try:
        UserInventory.objects.update_or_create(user=user, item=default_theme, defaults={"timestamp":int(time.time())})
        UserInventory.objects.update_or_create(user=user, item=no_title, defaults={"timestamp":int(time.time())})
        UserInventory.objects.update_or_create(user=user, item=no_border, defaults={"timestamp":int(time.time())})
        set_user_theme(user=user, item=default_theme)
        set_user_title(user=user, item=no_title)
        set_user_border(user=user, item=no_border)
        return True
    except:
        return False

def get_equipped_items(user):
    l = []
    try: 
        l.append(UserTheme.objects.get(user=user).item.id)
        p = Profile.objects.get(user=user)
        l.append(p.title.id)
        l.append(p.border.id)
    except: pass
    return l

def get_equippable_item_types(): 
    return ["theme", "title", "border"]

def equip_item(user, itemID):
    try:
        # Validate that the item is owned by the user
        owned_item_ids = [x.item.id for x in UserInventory.objects.filter(user=user)]
        if int(itemID) not in owned_item_ids:
            return False
        if int(itemID) > 0:
            item = Item.objects.get(id=itemID)
            match item.itemType:
                case "theme": 
                    set_user_theme(user, item)
                case "title": 
                    set_user_title(user, item)
                case "border": 
                    set_user_border(user, item)
        else:
            match itemID:
                case "-1":
                    set_user_theme_unequip(user)
        return True
    except: return False


def get_user_theme(user):
    try:
        theme = UserTheme.objects.get(user=user).item
        if theme:
            return theme.content
        else:
            return None
    except:
        try: 
            UserTheme.objects.update_or_create(user=user, defaults={"item":None})
        except: 
            return None

def set_user_theme(user, item):
    try:
        if item.itemType == "theme":
            UserTheme.objects.update_or_create(user=user, defaults={"item":item})
        return True
    except:
        return False

def set_user_title(user, item):
    try:
        if item.itemType == "title":
            Profile.objects.update_or_create(user=user, defaults={"title":item})
        return True
    except:
        return False

def set_user_border(user, item):
    try:
        if item.itemType == "border":
            Profile.objects.update_or_create(user=user, defaults={"border":item})
        return True
    except:
        return False

def set_user_theme_unequip(user):
    try:
        UserTheme.objects.update_or_create(user=user, defaults={"item":None})
        return True
    except:
        return False

def get_group_leaderboard(group):
    members = GroupMember.objects.filter(group=group).values_list("user", flat=True)

    leaderboard_raw = (
        MissionCompleted.objects
        .filter(user__in=members, completed=True, correct=True)
        .values('user')
        .annotate(score=models.Count('id'))
        .order_by('-score')
    )

    results = []
    for entry in leaderboard_raw:
        user = User.objects.get(id=entry['user'])
        results.append({
            'user': user,
            'score': entry['score']
        })

    return results
