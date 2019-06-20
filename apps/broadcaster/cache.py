from asgiref.sync import sync_to_async
from redis import Redis

redis_connection = Redis()

from settings import (
    CACHE_CONNECTION_PREFIX,
)


def get_user_cache_key(connection_id):
    return f'{CACHE_CONNECTION_PREFIX}:{connection_id}'


@sync_to_async
def add_connection(connection_id, channel_name):
    redis_connection.set(
        get_user_cache_key(connection_id), channel_name
    )


@sync_to_async
def remove_connection(connection_id):
    redis_connection.delete(
        get_user_cache_key(connection_id)
    )


@sync_to_async
def list_connected():
    _, connected = redis_connection.scan(
        match=f'{CACHE_CONNECTION_PREFIX}:*'
    )
    connected = [c.decode('utf-8').split(':')[1] for c in connected]
    return connected


def get_connection_channel(connection_id):
    channel = redis_connection.get(connection_id)
    return channel.decode('utf-8')
