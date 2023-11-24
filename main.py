import asyncio
import configparser
import sys

from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient
from telethon import functions, types
from searcher import search_districts, search_kazan_schools, search_complexes_kazan, search_villages

import xlsxwriter

config = configparser.ConfigParser()
config.read("config.ini")

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

phone = config['Telegram']['phone']
username = config['Telegram']['username']
client = TelegramClient(username, api_id, api_hash)

list_of_found_ch = []


def write_xlsx(integer):
    workbook = xlsxwriter.Workbook("all_channels.xlsx")
    worksheet = workbook.add_worksheet(f"{integer}sheet")
    worksheet.write(0, 0, "#")
    worksheet.write(0, 1, "district")
    worksheet.write(0, 2, "name")
    worksheet.write(0, 3, "participants")
    worksheet.write(0, 4, "url")
    index = 1
    for elem in list_of_found_ch:
        worksheet.write(index, 0, str(index))
        worksheet.write(index, 1, elem['district'])
        worksheet.write(index, 2, elem['name'])
        worksheet.write(index, 3, elem['participants'])
        worksheet.write(index, 4, elem['url'])
        index += 1
    workbook.close()


async def parse_list(result, search):
    dictionary = {}
    for elem in result.chats:
        dictionary['name'] = elem.title
        dictionary['participants'] = elem.participants_count
        dictionary['url'] = f'@{elem.username}'
        if len(search.split(' ')) == 1:
            dictionary['district'] = "Казань"
        else:
            dictionary['district'] = search.split(' ')[0]
        print(dictionary)
        if dictionary not in list_of_found_ch:
            list_of_found_ch.append(dictionary)


async def search_channels(list, keyword):
    for list_elem in list:
        if keyword != "":
            search = f'{list_elem} {keyword}'
        else:
            search = f'Казань {list_elem}'
        result = await client(functions.contacts.SearchRequest(
            q=search,
            limit=100,
        ))
        await parse_list(result, search)


async def main():
    await client.start()

    # Ensure you're authorized
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    list_of_kazan_complexes = search_complexes_kazan()
    list_of_kazan_districts = search_districts()
    list_of_schools = search_kazan_schools()
    # # await search_channels(list_of_schools, "")
    # await search_channels(list_of_kazan_complexes, "")
    # await search_channels(list_of_kazan_districts, "Казань")
    await search_channels(search_villages(), " ")
    write_xlsx(4)


with client:
    client.loop.run_until_complete(main())
