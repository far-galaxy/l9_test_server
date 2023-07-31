# -*- coding: utf-8 -*-
import requests
from ast import literal_eval
import os
import time

groups = (
    530996168,
    )

def download(isGroup, ID, week):
    uri = "groupId" if isGroup else "staffId"
    folder = "groups" if isGroup else "teachers"
    site = requests.get(f'https://ssau.ru/rasp?{uri}={ID}&selectedWeek={week}')
    print(f'Loaded {folder} shedule {ID}, week {week}')
    if not os.path.isdir(f'{folder}/{ID}/'):
        os.makedirs(f'{folder}/{ID}')
                
    path = os.path.abspath(f'{folder}/{ID}/week_{week}.html')        
    with open(path, 'w', encoding="utf-8") as f:
        f.write(str(site.text))
        print(f"Saved {folder} shedule {ID}, week {week}")
    time.sleep(0.5)

if __name__ == "__main__":
    for groupId in groups:
        for week in range(1,17):
            download(True, groupId, week)
            
        
