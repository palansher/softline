import requests

from bs4 import BeautifulSoup

# def get_url_images(url="https://lenta.ru"):
#     try:
#         response = requests.get(url,timeout=20) #ждем полной загрузки страницы не более 20 секунд
#         soup = BeautifulSoup(response.text,"html.parser")
#         images = soup.find_all("img") #получим все тэги img
#         list_src = []
#         for image in images:
#             list_src.append(image["src"])
#         return set(list_src)
#     except Exception as e:
#         print(e)
#         return set()
# for i,img in enumerate(get_url_images(),1):
#     print(f"{i}) {img}")

# Практика - извлекаем значение из тэга. Допустим найти все ссылки и вывести их названия
# <a href="адрес ссылки">текст ссылки</a>

def get_links(url="https://lenta.ru"):
    try:
        response = requests.get(url,timeout=20) #ждем полной загрузки страницы не более 20 секунд
        soup = BeautifulSoup(response.text,"html.parser")
        links = soup.find_all("a") #получим все тэги img
        list_links = {}
        for a in links:
            list_links[a["href"]] = a.text

        return list_links
    except Exception as e:
        print(e)
        return {}
for key,value in get_links().items():
    print(f"{key}: {value}")