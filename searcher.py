from bs4 import BeautifulSoup as BS4
import urllib.request
import requests

kazan_complexes_url = "http://www.kazanopolis.ru/complexes"
kazan_schools_url = "https://akazan.com/schools/kazan"


def search_complexes_kazan():
    soup = BS4(urllib.request.urlopen(kazan_complexes_url), 'lxml')
    all_complexes_class = soup.find(attrs={'id': "gl-search-complexes"})
    list_of_complexes_tag = all_complexes_class.find_all("option")
    list_of_complexes = []
    for elem in list_of_complexes_tag:
        text = elem.text
        list_of_complexes.append(text)

    list_of_complexes_tag.clear()
    return list_of_complexes


def search_districts():
    soup = BS4(urllib.request.urlopen(kazan_complexes_url), 'lxml')
    all_district_class = soup.find(attrs={'id': "gl-search-districts"})
    list_of_districts_tag = all_district_class.find_all("option")
    list_of_districts = []
    for elem in list_of_districts_tag:
        text = elem.text
        list_of_districts.append(text)
    list_of_districts_tag.clear()
    return list_of_districts


def search_kazan_schools():
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'My User Agent 1.0',
    })
    r = requests.get(kazan_schools_url, headers=headers)
    soup = BS4(r.content, 'html5lib')
    all_schools_list_td = soup.find_all(attrs={'class': "ta-211"})
    all_schools_list = []
    for elem in all_schools_list_td:
        text = elem.text
        all_schools_list.append(text)

    all_schools_list_td.clear()
    return all_schools_list


def search_villages():
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'My User Agent 1.0',
    })
    r = requests.get("https://www.komandirovka.ru/countries/russia/respublika-tatarstan/", headers=headers)
    soup = BS4(r.content, 'html5lib')
    all_villages = soup.find_all(attrs={'class': "alpha__flag-txt"})
    # print(all_villages)
    all_villages_list = []
    for elem in all_villages:
        text = elem.find("strong").text
        # print(text)
        all_villages_list.append(text)

    return all_villages_list
