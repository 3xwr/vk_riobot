import vk_api
import requests
import json
import urllib.request
from urllib.parse   import quote

vk_session = vk_api.VkApi(token='1101549996d1a40ba59078cae8183c2f4c894030ecf97d536123661494b56f6646112674cb449fb978f13')

from vk_api.longpoll import VkLongPoll, VkEventType
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
commands = ['рио','помощь', 'фарк']

def send_rio_message(char_name):
    if string_list[0] == commands[0]:
        rq_string = 'https://raider.io/api/v1/characters/profile?region=eu&realm=soulflayer&name=' + quote(char_name) + '&fields=mythic_plus_scores_by_season%3Acurrent'
        request = requests.get(rq_string)
        json_data = json.loads(request.text)
        if 'statusCode' in json_data:
            vk.messages.send(
            user_id=event.user_id,
            random_id=event.random_id,
            message='Неверно указано имя персонажа'
            )
            return
        vk.messages.send(
            user_id=event.user_id,
            random_id=event.random_id,
            message=json_data['mythic_plus_scores_by_season'][0]['scores']['all']
        )
    else:
        vk.messages.send(
            user_id=event.user_id,
            random_id=event.random_id,
            message='Неверный формат запроса'
        )

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if commands[0] in event.text:
            string_list = event.text.split(' ')
            current_char_name = 'Имя персонажа не указано'
            if len(string_list)>1:
                current_char_name = string_list[1].capitalize()
                if event.from_user:
                    send_rio_message(current_char_name)
                elif event.from_chat:
                    send_rio_message(current_char_name)
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=event.random_id,
                    message='Неверный формат запроса'
                )
        if event.text == commands[1]:
            vk.messages.send(
                    user_id=event.user_id,
                    random_id=event.random_id,
                    message='Список команд: рио <имя персонажа>, помощь, фарк'
                )




