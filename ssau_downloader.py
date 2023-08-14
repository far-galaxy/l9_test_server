# -*- coding: utf-8 -*-
import requests
from ast import literal_eval
import os
import time
import ssau_cleaner
from bs4 import BeautifulSoup

# Список групп и преподавателей для скачивания
# (при самостоятельном запуске модуля)
groups = ()
teachers = ()

# Скачивание расписания, очистка от лишнего (при желании) и сохранение в файл 
def download(isGroup, ID, week, clear=False):
    uri = "groupId" if isGroup else "staffId"
    folder = "groups" if isGroup else "teachers"
    site = requests.get(f'https://ssau.ru/rasp?{uri}={ID}&selectedWeek={week}')
    if site.status_code != 200:
        print(f'responce {site.status_code}')
        return
    print(f'Loaded {folder} shedule {ID}, week {week}')
    if not os.path.isdir(f'{folder}/{ID}/'):
        os.makedirs(f'{folder}/{ID}')
                
    path = os.path.abspath(f'{folder}/{ID}/week_{week}.html')        
    with open(path, 'w', encoding="utf-8") as f:
        f.write(str(site.text))
        print(f"Saved {folder} shedule {ID}, week {week}")
    if clear:
        ssau_cleaner.clear(path)
    # Задержка на всякий случай для защит от ботов
    time.sleep(0.5)

def findInRasp(req):
    rasp = requests.Session() 
    rasp.headers['User-Agent'] = 'Mozilla/5.0'
    hed = rasp.get("https://ssau.ru/rasp/")
    soup = BeautifulSoup(hed.text, 'lxml')
    csrf_token = soup.select_one('meta[name="csrf-token"]')['content']
    time.sleep(0.5)
    rasp.headers['Accept'] = 'application/json'
    rasp.headers['X-CSRF-TOKEN'] = csrf_token
	
    result = rasp.post("https://ssau.ru/rasp/search", data = {'text':req})
    if result.status_code == 200:
        return literal_eval(result.text)
    else:
        return []


if __name__ == "__main__":
    for groupId in groups:
        for week in range(1,17):
            download(True, groupId, week)
            
        
