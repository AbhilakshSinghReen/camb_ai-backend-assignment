from json import dumps as json_dumps
from random import choice as random_choice
from time import time
from uuid import uuid4


usernames = ["user1", "user2", "user3", "user4", "user5"]
names = ["John", "Alice", "Bob", "Jane", "Michael"]
statuses = ["Awake", "Sleeping", "Programming",]


def generate_unique_key():
    return str(uuid4()) + "--" + str(time())


def generate_random_value():
    user_details = {
        'username': random_choice(usernames),
        'name': random_choice(names),
        'status': random_choice(statuses),
    }
    return json_dumps(user_details)
