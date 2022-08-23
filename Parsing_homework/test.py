import sys
import argparse

#Парсим коммандную строку
def parse():
    parser = argparse.ArgumentParser(
        description='Парсит -n последних сообщений из каждого канала указанного канала, если ваше приложение на них подписанно')

    parser.add_argument('-t', action='store', type=str, required=False,
                        help='Целевые каналы')
    parser.add_argument('-n', action='store', type=int, required=False,
                        help='Кол-во сообщений')


    return parser.parse_args()

res = parse()
targets = res.t.split(',')
history_limit = res.n
print(targets)
print(type(targets))
print(history_limit)
print(type(history_limit))