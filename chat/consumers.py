import json
import logging
from channels import Group
from channels.auth import channel_session_user_from_http, channel_session_user
from .models import Room

log = logging.getLogger(__name__)


@channel_session_user_from_http
def ws_connect(message):
    label = 'chat'
    room = Room.objects.get_or_create(label=label)[0]

    Group('chat-' + label, channel_layer=message.channel_layer).add(
        message.reply_channel)

    message.channel_session['room'] = room.label


@channel_session_user
def ws_receive(message):
    try:
        label = message.channel_session['room']
        room = Room.objects.get(label=label)
    except KeyError:
        log.debug('no room in channel_session')
        return
    except Room.DoesNotExist:
        log.debug('recieved message, buy room does not exist label=%s', label)
        return

    data = json.loads(message['text'])
    if data:
        log.debug('chat message room=%s author=%s message=%s',
                  room.label, message.user, data['message'])
        m = room.messages.create(author=message.user, **data)
        print m.as_dict()
        Group('chat-' + label, channel_layer=message.channel_layer).send(
            {'text': json.dumps(m.as_dict())})


@channel_session_user
def ws_disconnect(message):
    try:
        label = message.channel_session['room']
        Group('chat-' + label, channel_layer=message.channel_layer).discard(
            message.reply_channel)
    except (KeyError, Room.DoesNotExist):
        pass
