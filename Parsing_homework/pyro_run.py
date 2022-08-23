from pyrogram import Client
import os
import sys
import argparse
import pandas as pd

path = os.path.dirname(os.path.abspath(__file__))

#Парсим коммандную строку
def parse():
    parser = argparse.ArgumentParser(
        description='Парсит -n последних сообщений из каждого указанного канала, если ваше приложение на них подписанно')

    parser.add_argument('-t', action='store', type=str, required=False,
                        help='Целевые каналы')
    parser.add_argument('-n', action='store', type=int, required=False,
                        help='Кол-во сообщений')
    parser.add_argument('-id', action='store', type=str, required=True,
                        help='api_id приложения')
    parser.add_argument('-hash', action='store', type=str, required=True,
                        help='api_hash приложения')
    return parser.parse_args()

#Получаем аргументы
targets = ['datajob',]
history_limit = 20
try:
    res = parse()
    targets = res.t.split(',')
    history_limit = res.n
    API_ID = res.id
    API_HASH = res.hash
except Exception as e:
    print('Error at parsing command line')
#print('Collect: ', targets)

#Получаем сообщения
all_messages = []
try:
    with Client("my_account", API_ID, API_HASH) as app:
        for target in targets:
            for message in app.iter_history(target, limit=history_limit):
                all_messages.append([message.sender_chat, message.message_id, message.date, message.text, message.entities])
    
    df = pd.DataFrame(all_messages)
    df.columns = ["chat", "message_id", "date", "text", "entities"]
    df.to_csv(path + '/telegram.csv', index=False)
    print('Success: ', path + '\\telegram.csv')
except Exception as e:
    print('Error: ', e)
