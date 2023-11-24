import xlsxwriter
from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient
from telethon import functions, types
import configparser

from bs4 import BeautifulSoup as BS4
import requests

config = configparser.ConfigParser()
config.read("config.ini")

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
phone = config['Telegram']['phone']
username = config['Telegram']['username']
client = TelegramClient(username, api_id, api_hash)
list_of_usernames = []
list_of_urls = ["https://tgram.me/tags/kazan?page=1", "https://tgram.me/tags/kazan?page=2",
                "https://tgram.me/tags/kazan?page=3", "https://tgram.me/tags/kazan?page=4",
                "https://tgram.me/tags/kazan?page=5", "https://tgram.me/tags/kazan?page=6",
                "https://tgram.me/tags/kazan?page=7", "https://tgram.me/tags/kazan?page=8",
                "https://tgram.me/tags/kazan?page=9", "https://tgram.me/tags/kazan?page=10",
                "https://tgram.me/tags/kazan?page=11", "https://tgram.me/tags/kazan?page=12",
                "https://tgram.me/tags/kazan?page=13"]

index = 1
list_of_found_ch = []
workbook = xlsxwriter.Workbook("all_channels.xlsx")
worksheet = workbook.add_worksheet(f"sheet")


def write_xlsx(index):
    for dictionary in list_of_found_ch:
        worksheet.write(index, 0, str(index))
        worksheet.write(index, 1, dictionary['district'])
        worksheet.write(index, 2, dictionary['name'])
        worksheet.write(index, 3, dictionary['participants'])
        worksheet.write(index, 4, dictionary['url'])
        index += 1


async def take_id(url):
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'My User Agent 1.0',
    })
    r = requests.get(url, headers=headers)
    soup = BS4(r.content, 'html5lib')
    all_usernames = soup.find_all(attrs={'class': 'text-truncate'})
    for usernames_id in all_usernames:
        await get_info(usernames_id.text)


async def get_info(username_id):
    result = await client(functions.contacts.SearchRequest(
        q=username_id,
        limit=100,
    ))
    dictionary = {}
    for elem in result.chats:
        dictionary['name'] = elem.title
        dictionary['participants'] = elem.participants_count
        dictionary['url'] = f'@{elem.username}'

        dictionary['district'] = "Казань"
        print(dictionary)
        if dictionary not in list_of_found_ch:
            list_of_found_ch.append(dictionary)


async def main():
    await client.start()
    # Ensure you're authorized
    for elem in list_of_urls:
        await take_id(elem)
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    write_xlsx(index)
    workbook.close()


with client:
    client.loop.run_until_complete(main())
