# **Телеграм-бот для турагенства "Too Easy Travel"**
___

Данный проект создавался для обучения и практики программирования на языке Python.
Основной функционал бота - отвечать на запросы пользователя информацией об отелях из API.


## Описание архитектуры проекта
___

+ :file_folder: **config_data** - *папка, содержащая конфигурационные файлы бота*
  + `__init__.py` - *файл, инициализирующий импорты файлов в папке*
  + `config.py` - *файл, содержащий код для конфигурации меню телеграм-бота*

+ :file_folder: **database** - *папка с файлами, связанными с отладкой работы базы данных*
  + `__init__.py` - *файл, инициализирующий импорты файлов в папке*
  + `history_base.py` - *файл, класса структуры базы данных*
  + `history_record.py` - *функция, для внесения записи в базу данных*

+ :file_folder: **handlers** - *папка с подкаталогами, которые содержат файлы с функциями бота*
  + :file_folder: **custom_handlers** - *подкаталог, содержит файлы пользовательских функций бота*
    + `__init__.py` - *файл, инициализирующий импорты файлов в папке*
    + `bestdeal.py` - *файл, содержащий скрипт работы функции бота отвечающей на команду "bestdeal"*
    + `hello.py` - *файл, содержащий скрипт работы функции бота отвечающий на сообщение пользователя "привет"*
    + `highprice.py` - *файл, содержащий скрипт работы функции бота отвечающей на команду "highprice"*
    + `history.py` - *файл, содержащий скрипт работы функции бота отвечающей на команду "history"*
    + `lowprice.py` - *файл, содержащий скрипт работы функции бота отвечающей на команду "lowprice"*
  + :file_folder: **default_handlers** - *подкаталог, содержит файлы стандартных функций бота*
    + `__init__.py` - *файл, инициализирующий импорты файлов в папке*
    + `hellow_world.py` - *файл, содержащий скрипт работы функции бота отвечающей на команду "hellow_world"*
    + `help.py` - *файл, содержащий скрипт работы функции бота отвечающей на команду "help"*
    + `start.py` - *файл, содержащий скрипт работы функции бота отвечающей на команду "start"*
  + `__init__.py` - *файл, инициализирующий импорты файлов и подкаталогов в папке*

+ :file_folder: **keyboards** - *папка содержит файлы, связанные с работой клавиатуры телеграм бота*
  + `__init__.py` - *файл, инициализирующий импорты файлов и подкаталогов в папке*
  + :file_folder: **reply** - *подкаталог содержит файлы, связанные с работой кнопок-ответов*
    + `__init__.py` - *файл, инициализирующий импорты файлов в папке*
    + `agreement_request.py` - *файл, содержащий код создающий кнопки ДА, НЕТ в телеграм боте*

+ :file_folder: **states** - *папка содержит файлы, связанные с работой состояний пользователя в скриптах*
  + `__init__.py` - *файл, инициализирующий импорты файлов в папке*
  + `userstate_bestdeal.py` - *файл, содержащий класс состояний объекта для скрипта функции "bestdeal"*
  + `userstate_highprice.py` - *файл, содержащий класс состояний объекта для скрипта функции "highprice"*
  + `userstate_lowprice.py` - *файл, содержащий класс состояний объекта для скрипта функции "lowprice"*

+ :file_folder: **utils** - *папка, содержащая общие вспомогательные функции для скриптов*
  + `__init__.py` - *файл, инициализирующий импорты файлов в папке*
  + `API_details.py` - *файл, содержащий функцию запроса деталей отеля из API по id отеля*
  + `API_id.py` - *файл, содержащий функцию запроса id запрашиваемой локации из API*
  + `API_list.py` - *файл, содержащий функцию запроса списка отелей по id локации из API*
  + `general_functions.py` *файл, содержащий все общие функции импортируемые в основные скрипты бота*
  + `set_bot_commands.py` *файл, содержащий функцию отладки меню команд телеграм бота*

+ `.env.tempate`
+ `.gitignore`
+ `loader.py`
+ `main.py`
+ `REAMDE.md`
+ `requirements.txt`

## Описание функционала телеграм-бота
___
### Функция команды lowprice

После ввода команды у пользователя запрашивается:
1. Город, где будет проводиться поиск.
2. Количество отелей, которые необходимо вывести в результате (не больше
заранее определённого максимума).
3. Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”)
a. При положительном ответе пользователь также вводит количество
необходимых фотографий (не больше заранее определённого
максимума)

<img height="100" src="https://gitlab.skillbox.ru/iurii_shilov/PA_Python_DPO_bot/-/raw/sixth_step/image/lowprice_dialog.png" width="150"/>

<img height="100" src="https://gitlab.skillbox.ru/iurii_shilov/PA_Python_DPO_bot/-/raw/sixth_step/image/lowprice_result1.png" width="150"/>

<img height="100" src="https://gitlab.skillbox.ru/iurii_shilov/PA_Python_DPO_bot/-/raw/sixth_step/image/lowprice_result2.png" width="150"/>


### Функция команды highprice

После ввода команды у пользователя запрашивается:
1. Город, где будет проводиться поиск.
2. Количество отелей, которые необходимо вывести в результате (не больше
заранее определённого максимума).
3. Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”)
a. При положительном ответе пользователь также вводит количество
необходимых фотографий (не больше заранее определённого
максимума)

<img height="100" src="https://gitlab.skillbox.ru/iurii_shilov/PA_Python_DPO_bot/-/raw/sixth_step/image/highprice_dialog.png" width="150"/>

<img height="100" src="https://gitlab.skillbox.ru/iurii_shilov/PA_Python_DPO_bot/-/raw/sixth_step/image/lowprice_result1.png" width="150"/>


### Функция команды bestdeal

После ввода команды у пользователя запрашивается:
1. Город, где будет проводиться поиск.
2. Диапазон цен.
3. Диапазон расстояния, на котором находится отель от центра.
4. Количество отелей, которые необходимо вывести в результате (не больше
заранее определённого максимума).
5. Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”)
a. При положительном ответе пользователь также вводит количество
необходимых фотографий (не больше заранее определённого
максимума)

<img height="100" src="https://gitlab.skillbox.ru/iurii_shilov/PA_Python_DPO_bot/-/raw/sixth_step/image/bestdeal_dialog.png" width="150"/>

<img height="100" src="https://gitlab.skillbox.ru/iurii_shilov/PA_Python_DPO_bot/-/raw/sixth_step/image/bestdeal_dialog2.png" width="150"/>

<img height="100" src="https://gitlab.skillbox.ru/iurii_shilov/PA_Python_DPO_bot/-/raw/sixth_step/image/bestdeal_result.png" width="150"/>


### Функция команды history

После ввода команды пользователю выводится история поиска отелей. Сама история
содержит:
1. Команду, которую вводил пользователь.
2. Дату и время ввода команды.
3. Отели, которые были найдены.

<img height="100" src="https://gitlab.skillbox.ru/iurii_shilov/PA_Python_DPO_bot/-/raw/sixth_step/image/history.png" width="150"/>