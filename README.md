##  Telegram-bot
***       
Этот Telegram-бот предназначен для поиска отелей по всему миру (на данный помент поиск по РФ недоступен) и вывода информации о них.

Данный Telegram-бот был разработан в рамках финальной работы [курса "Основы Python"](https://skillbox.ru/course/profession-python/) от [Skillbox](https://skillbox.ru) на языке программирования Python 3.10 c использованием фреймворка aiogram 3.0.0b7.


## 1. Создание Telegram-бота
***
Для создания бота в Telegram нужно написать боту [BotFather](https://t.me/BotFather), в диалоге с ним сначало нужно отправить команду ``/newbot`` для создания нового бота. Далее нужно ввести название и имя пользователя будущего бота, после чего BotFather отправит ссылку для доступа к боту и его токен.

## 2. Работа с кодом программы
***
Для работы с кодом программы необходимо скачать все прикреплённые файлы в папку проекта.
Запускающим файлом является ``main.py``.
Первым делом нужно установить все необходимые библиотеки. Их перечень находится в файле ``requirements.txt``: 
- aiogram 3.0.0b7
- python-dotenv 1.0.0
- requests 2.28.2
- pydantic 1.10.7
- aiosqlite 0.19.                   
```
pip install -r requirements.txt
```

После установки библиотек необходимо создать файл ``.env`` по образцу ``.env.template``, куда прописать ``BOT_TOKEN = ''`` полученный токен от BotFather, а также ключи для доступа к API сайтов 
``X_RAPID_API_KEY = ''`` <https://rapidapi.com/apidojo/api/hotels4> и ``CURRENCYCONVERTERAPI = ''`` <https://www.currencyconverterapi.com> 

## 3. Инструкция по использованию
***
Запустить программу на компьютере.
Запустите Telegram, нажмите на вкладку вашего бота, нажмите ``/start``. После этого Вам отправится приветственное сообщение от бота, после чего он запросит Ваше имя для внесения его в базу данных и отобразятся кнопки с выбором режима работы бота (эти команды доступны также в ``меню`` бота).

Бот поддерживает следующие режимы:
- поиск отелей по наименьшей стоимости (в порядке возрастания цены за номер)
- поиск отелей по наивысшей стоимости (в порядке убывания цены за номер)
- поиск отелей по параметрам пользователя
- отображения истории запросов пользователя
- помощь (список поддерживаемых команд ботом с их описанием)

После нажатия на одну из кнопок поиска, бот последовательно предлагает ввести необходимые данные для поиска, после которых выводит список отелей, нажимая на которые можно просмотреть фотографии отеля (если был выбран показ с фотографиями) и краткую информацию о самом отеле.

Конвертация валют рубль в доллар происходит по актуальному курсу через сервер <https://www.currencyconverterapi.com> на момент запроса.

### Скриншоты работы бота
***
![](images\scene1.png)

![](images\scene2.png)

![](images\scene3.png)

![](images\scene4.png)

## 4. Контактная информация
***
email: [eugene.3470541@gmail.com](https://mail.google.com/mail/)
