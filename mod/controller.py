import random

from pydantic import ValidationError

from mod import models
from mod import api
from mod import libhash
from mod import config


def save_userdata(username: str, password: str) -> None:
    """The function saves the user name and password to the database.
    There is no check for the data type.

    Args:
        username (str): required
        password (str): required

    Returns:
        None
    """
    userID = random.getrandbits(64)
    models.User(userID=userID, password=password, username=username)
    return


def get_userdata(username: str):
    """The function checks the presence of the user in the database.

    Args:
        username (str): required

    Returns:
        bool: True or False
    """
    dbdata = models.User.select(models.User.q.username == username)
    if dbdata.count() != 0:
        return dbdata[0].password
    else:
        return None


def save_message(message: dict) -> None:
    """The function stores the message in the database.

    Args:
        message (dict): [description]

    Returns:
        None
    """
    numbers = random.getrandbits(256)
    models.Message(messageID=numbers,
                   text=message['text'],
                   fromUserUsername=message['username'],
                   time=message['timestamp'])
    return


def get_messages() -> list:
    """The function receives all the messages
    from the database and converts them into a list.

    Args:
        No args.

    Returns:
        list: The list contains the following dictionary:
        {
            'mode': 'message',
            'username': str,
            'text': str,
            'time': int
        }
    """
    dbquery = models.Message.select(models.Message.q.id > 0)
    messages = []
    for data in dbquery:
        messages.append({
                    "mode": "message",
                    "username": data.fromUserUsername,
                    "text": data.text,
                    "timestamp": data.time
                        })
    return messages


async def auth_id() -> str:
    pass


async def register_user(data: dict) -> dict:
    try:
        data = await api.ValidJSON.parse_obj(data)
    except ValidationError as error:
        print(error)
    userID = random.getrandbits(64)
    dict_hash = libhash.password_hash(password=data.user.password)
    try:
        dbquery = models.User(userID=userID,
                              login=data.user.login,
                              password=dict_hash['hash_password'],
                              username=data.user.username,
                              authId=,
                              email=data.user.email,
                              salt=dict_hash['salt'],
                              key=dict_hash['key'])
    except EnvironmentError:
        print('Error')
    result = {
        'type': data.type,
        'data': {
            'time': time(),
            'user': {
                'id': userID,
                'auth_id': 'lkds89ds89fd98fd'
                },
            'meta': None
        },
        'errors': {
            'id': 25665546,
            'time': 1594492370.5225992,
            'status': 'OK',
            'code': 200,
            'detail': 'successfully'
            },
        'jsonapi': {
            'version': config.API_VERSION
            },
        'meta': None
        }
    return result

if __name__ == "__main__":
    print('Error! This module should be imported, not started.')
