from decouple import config
import requests
import json
import urllib3
import psycopg2
import time
import logging
from parametrs import fields_and_types_Contacts, fields_and_types_Account, fields_and_types_Employee, fields_and_types_usr_type_partner, fields_and_types_usr_scroll_list_info
from parametrs import name_t, name_url


logging.basicConfig(
    filename='log.txt',  # Файл для запису логів
    level=logging.DEBUG,  # Рівень логування (може бути DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s [%(levelname)s]: %(message)s',  # Формат запису логів
    datefmt='%Y-%m-%d %H:%M:%S'  # Формат дати та часу
)


console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Рівень логування для консолі (може бути INFO, WARNING, ERROR, CRITICAL)
console_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s'))
logging.getLogger().addHandler(console_handler)


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


urlcrm = config('CREATIOURL', default = '' )
url_to_auth = config('URLTOAUTH', default = '')
usernamecrm = config('USERNAMECRM', default = '')
userpasswordcrm = config('USERPASSWORD', default = '')







name_f= []
name_f.append(fields_and_types_Contacts)
name_f.append(fields_and_types_Account)
name_f.append(fields_and_types_Employee)
name_f.append(fields_and_types_usr_scroll_list_info)
name_f.append(fields_and_types_usr_type_partner)
# print(name_f)

# print(name_t)


def connect_to_db():
    conn = psycopg2.connect(
        dbname=config("DBNAME"),
        user=config('DBUSERNAME'),
        password=config('DBPASSWORD'),
        host=config('DBHOST')
    )
    # print("maybe it`s ok")
    return conn


def create_table_db(table_name, fields_and_types):
    conn = connect_to_db()
    cursor = conn.cursor()

    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
    for field, field_type in fields_and_types.items():
        create_table_query += f"{field} {field_type}, "
    create_table_query = create_table_query.rstrip(", ")  # Видаляємо останню кому
    create_table_query += ");"

    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()
    # print("maybe it`s ok")


def auth_func():
    main_url = urlcrm + url_to_auth
    headers = {
        'Accept': 'application/json',
        'ForceUseSession': 'true',
        'Content-Type': 'application/json'

    }

    data = {
        'UserName': usernamecrm,
        'UserPassword': userpasswordcrm
    }

    response = requests.post(main_url, headers=headers, json=data, verify=False)

    if response.status_code == 200:
        # Опрацьовуйте відповідь, якщо код статусу 200 OK
        logging.info('Запит був успішним!')
        # print("Resoult response")
        # print(response.json())
        with open('response.json', 'w') as json_file:
            json.dump(response.json(), json_file, indent=4)
        logging.info('File response.json is written')
        logging.info(('File cookies.json in progres...'))
        cookies = {cookie.name: cookie.value for cookie in response.cookies}
        with open('cookies.json', 'w') as cookies_file:
            json.dump(cookies, cookies_file, indent=4)
        logging.info('File cookies was written')
        # print("Printed cookies")
        # for cookie in cookies:
        #     print(f'Cookie: {cookie}={cookies[cookie]}')

        logging.info("IF YOU SEE THIS MESSAGE, ALL OK")

    else:
        # Обробка помилок, якщо статус не 200
        logging.info(f'Помилка {response.status_code}: {response.text}')


#
# THIS METOD TO CREATE TABLES IN DB
#
def created_tables(name_table, name_fields):
    for i in range(0, len(name_table)):
        create_table_db(name_table[i], name_fields[i])
        logging.info(f'Table {name_table[i]} was records' )
    logging.info('All info was created')
#
# AFTER ALL TESTS IMPORTED THIS FUNC TO MAIN FUNC
# created_tables(name_t, name_f)


def record_to_db(name_url):
    url = config('CREATIOURL') + name_url
    cookies_filename = 'cookies.json'
    try:
        with open(cookies_filename, 'r') as cookies_file:
            cookies = json.load(cookies_file)

        response = requests.get(url, cookies=cookies, verify=False)
        return response.json()
    except Exception as e:
        logging.error(f"Помилка: {str(e)}")

        return None


def write_data_to_table(data, table_name):


    conn = connect_to_db()
    cursor = conn.cursor()

    for item in data:
        # Отримайте id для перевірки наявності запису
        id_to_check = item.get('Id')

        # Перевірте, чи існує запис з таким id в таблиці
        cursor.execute(f"SELECT id FROM {table_name} WHERE id = %s", (id_to_check,))
        existing_record = cursor.fetchone()

        if existing_record:
            # Запис із цим ідентифікатором вже існує, оновлюємо його
            update_query = f"UPDATE {table_name} SET ({', '.join(item.keys())}) = ({', '.join(['%s'] * len(item))}) WHERE id = %s"
            values_to_update = tuple(item.values()) + (id_to_check,)
            cursor.execute(update_query, values_to_update)
        else:
            # Запис із цим ідентифікатором не існує, створюємо новий запис
            keys = ', '.join(item.keys())
            values = ', '.join(['%s'] * len(item))
            insert_query = f"INSERT INTO {table_name} ({keys}) VALUES ({values})"
            values_to_insert = tuple(item.values())
            cursor.execute(insert_query, values_to_insert)

    # Збереження змін у базі даних
    conn.commit()

    # Закриття підключення до бази даних
    cursor.close()
    conn.close()


def full_write_data(ntable, nurl):
    for i in range(0, len(nurl)):

        start_time = time.time()
        data_to_insert = record_to_db(nurl[i])['value']
        # print(f'{ntable[i]}______{data_to_insert}')
        # print('_________________________________________')
        write_data_to_table(data_to_insert, ntable[i])
        end_time = time.time()
        execution_time = end_time - start_time
        logging.info(f"Час виконання: {execution_time} секунд")


def size_db():
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT pg_size_pretty(pg_database_size(current_database()));"
    cursor.execute(query)

    # Отримання результату запиту
    db_size = cursor.fetchone()[0]

    # Закриття курсора і з'єднання з базою даних
    cursor.close()
    conn.close()
    logging.info(f"Розмір бази даних: {db_size}")


#
# CODE WHAT UNDER THIS COMMENTS ARE READY TO UNCOMMENTED
#
while True:
    print(" Input 1. Записати куки для авторизації серверу на Creatio")
    print(" Input 2. Створити необхідні для заповнення таблиці в бд")
    print(" Input 3. Записати в таблиці дані з CRM")
    print(" Input 4. Вивести розмір БД")
    print(" Input 5. Exit")
    choice = input("Що ви хочете зробити?")
    if choice == '1':
        start_time = time.time()
        auth_func()
        end_time = time.time()
        execution_time = end_time - start_time
        logging.info(f"Час виконання: {execution_time} секунд")

    elif choice == '2':
        start_time = time.time()
        created_tables(name_t, name_f)
        end_time = time.time()
        execution_time = end_time - start_time
        logging.info(f"Час виконання: {execution_time} секунд")

    elif choice == '3':
        start_time = time.time()
        full_write_data(name_t, name_url)
        end_time = time.time()
        execution_time = end_time - start_time
        logging.info(f"Час виконання: {execution_time} секунд")

    elif choice == '4':
        start_time = time.time()
        size_db()
        end_time = time.time()
        execution_time = end_time - start_time
        logging.info(f"Час виконання: {execution_time} секунд")

    elif choice == '5':
        start_time = time.time()
        logging.info("Дякую за використання програми. Вихід.")
        end_time = time.time()
        execution_time = end_time - start_time
        logging.info(f"Час виконання: {execution_time} секунд")

        break
    else:
        print("Ви ввели невірний вибір. Будь ласка, виберіть 1, 2 або 3.")


