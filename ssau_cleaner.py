from bs4 import BeautifulSoup
import glob
head = """
<!DOCTYPE html>
<html lang="ru">

<head>
    <meta charset="utf-8" />
    <meta name="csrf-token" content="thisIsCSRFtoken" />
    <title>Расписание</title>
    <meta property="og:image:secure_url" content="https://ssau.ru/i/logo/ssau_preview.jpg" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
    <link rel="stylesheet" type="text/css" href="/styles/app.css" />
</head>
<body>

"""

# Очистка файла расписания от шапок, подвалов и прочих лишних элементов,
# не используемых при парсинге
def clear(file_name):
    with open(file_name, 'r+', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')

        div = soup.find('div', class_='container timetable')
        buttons = div.find('div', class_='info-block__buttons')
        if buttons != None:
            buttons.extract()
        
        legend = div.find('div', class_='timetable__legend')
        if legend != None:
            legend.extract()
            
        search = div.find('select', class_='d-block')
        if search != None:
            search.extract()

        if div is not None:
            file.seek(0)
            file.truncate()
            file.write(head+str(div)+"\n</body>\n</html>")
          
if __name__ == "__main__":
    folder = './groups/530992489'
    for i in glob.glob(f'{folder}/week_*.html'):
        clear(i)

