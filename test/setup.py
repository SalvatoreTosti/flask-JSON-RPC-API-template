from app import db
from app.models.user import User

# from app.models.event import Event


def afc(item):
    db.session.add(item)
    db.session.flush()
    db.session.commit()


def run():
    user1 = User(username="user-1", email="email1@test.com")
    user1.set_password("test1")
    user2 = User(username="user-2", email="email2@test.com")
    user2.set_password("test2")
    user3 = User(username="user-3", email="email3@test.com")
    user3.set_password("test3")
    afc(user1)
    afc(user2)
    afc(user3)

    # event1 = Event(user_id=user1.id, name="event 1", data={"a": "b"})
    # event2 = Event(user_id=user2.id, name="event 2", data={"c": "d"})
    # event3 = Event(user_id=user3.id, name="event 3", data={"e": "f"})
    # event4 = Event(user_id=user1.id, name="event 4", data={"g": {"h": "i"}})
    # afc(event1)
    # afc(event2)
    # afc(event3)
    # afc(event4)
