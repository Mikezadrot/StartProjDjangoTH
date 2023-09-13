from decouple import config
import requests
import json
import urllib3
import psycopg2

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


urlcrm = config('CREATIOURL', default = '' )
url_to_auth = config('URLTOAUTH', default = '')
usernamecrm = config('USERNAMECRM', default = '')
userpasswordcrm = config('USERPASSWORD', default = '')





fields_and_types_Contacts = {
    "id": "UUID PRIMARY KEY",
    "name": "VARCHAR(255)",
    "mobile_phone": "VARCHAR(20)",
    "usr_employer_lookup_id": "UUID",
    "usr_agency_lookup_id": "UUID",
    "usr_employeemanager_ukraine_id": "UUID",
    "usr_employee_manager_europe_id": "UUID",
    "usr_scroll_lookup_id": "UUID"
}

fields_and_types_Account = {
    "id": "UUID PRIMARY KEY",
    "name": "VARCHAR(255)",
    "phone": "VARCHAR(20)",
    "usr_partner_type_id": "UUID",
    "usr_agency_that_give_us_employer_id": "UUID"
}

fields_and_types_Employee = {
    "id": "UUID PRIMARY KEY",
    "name": "VARCHAR(255)",
    "full_job_title": "UUID"

}

fields_and_types_Employee = {
    "id": "UUID PRIMARY KEY",
    "name": "VARCHAR(255)",
    "full_job_title": "UUID"

}



fields_and_types_usr_scroll_list_info = {
    "id": "UUID PRIMARY KEY",
    "name": "VARCHAR(255)"
}


fields_and_types_usr_type_partner = {
    "id": "UUID PRIMARY KEY",
    "name": "VARCHAR(255)"
}


name_f= []
name_f.append(fields_and_types_Contacts)
name_f.append(fields_and_types_Account)
name_f.append(fields_and_types_Employee)
name_f.append(fields_and_types_usr_scroll_list_info)
name_f.append(fields_and_types_usr_type_partner)
# print(name_f)


name_t = ['Contacts', 'Account', 'Employee', 'Profession', 'PartnerType']
# print(name_t)


def connect_to_db():
    conn = psycopg2.connect(
        dbname=config("DBNAME"),
        user=config('DBUSERNAME'),
        password=config('DBPASSWORD'),
        host=config('DBHOST')
    )
    print("maybe it`s ok")
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
    print("maybe it`s ok")



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
        print('Запит був успішним!')
        # print("Resoult response")
        # print(response.json())
        with open('response.json', 'w') as json_file:
            json.dump(response.json(), json_file, indent=4)
        print('File response.json is written')
        print(('File cookies.json in progres...'))
        cookies = {cookie.name: cookie.value for cookie in response.cookies}
        with open('cookies.json', 'w') as cookies_file:
            json.dump(cookies, cookies_file, indent=4)
        print('File cookies was written')
        print("Printed cookies")
        # for cookie in cookies:
        #     print(f'Cookie: {cookie}={cookies[cookie]}')

        print("IF YOU SEE THIS MESSAGE, ALL OK")

    else:
        # Обробка помилок, якщо статус не 200
        print(f'Помилка {response.status_code}: {response.text}')


#
# THIS METOD TO CREATE TABLES IN DB
#
def created_tables(name_table, name_fields):
    for i in range(0, len(name_table)):
        create_table_db(name_table[i], name_fields[i])
        print(f'Table {name_table[i]} was records' )
    print('All info was created')
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
        print(f'An error occurred: {str(e)}')
        return None


# auth_func()

def write_to_current_tableDB(table_name):
    elm_mass = record_to_db(config('URLCONTACT'))['value']
    res_mass = []
    for i in elm_mass:
        print("Element")
        prom_mass = []
        mass = list(i)

        for k in mass:
            # print(i[k])

            prom_mass.append(i[k])
            # print(prom_mass)
        res_mass.append(prom_mass)
    # print(res_mass)
    conn = connect_to_db()
    cursor = conn.cursor()

    for item in res_mass:
        id_to_check = item[0]  # Отримайте ідентифікатор для перевірки
        cursor.execute(f"SELECT id FROM {table_name} WHERE id = %s", (id_to_check,))
        existing_record = cursor.fetchone()

        if existing_record:
            # Запис із цим ідентифікатором вже існує, оновлюємо його
            update_query = f'''
                UPDATE {table_name} SET
                    name = %s,
                    mobile_phone = %s,
                    usr_employer_lookup_id = %s,
                    usr_agency_lookup_id = %s,
                    usr_employeemanager_ukraine_id = %s,
                    usr_employee_manager_europe_id = %s,
                    usr_scroll_lookup_id = %s
                WHERE id = %s
            '''
            cursor.execute(update_query, (item[1], item[2], item[3], item[4], item[5], item[6], item[7], id_to_check))
        else:
            # Запис із цим ідентифікатором не існує, створюємо новий запис
            insert_query = f'''
                INSERT INTO {table_name} (
                    id, name, mobile_phone, usr_employer_lookup_id, usr_agency_lookup_id, usr_employeemanager_ukraine_id, usr_employee_manager_europe_id, usr_scroll_lookup_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_query, item)

    # Збереження змін у базі даних
    conn.commit()

    # Закриття підключення до бази даних
    cursor.close()
    conn.close()


# write_to_current_tableDB('Contacts')

while True:
    print(" Input 1. Записати куки для авторизації серверу на Creatio")
    print(" Input 2. Створити необхідні для заповнення таблиці в бд")
    print(" Input 3. Записати в таблиці дані з CRM")
    print(" Input 4. Exit")

    choice = input("Що ви хочете зробити?")
    if choice == '1':
        auth_func()
    elif choice == '2':
        created_tables(name_t, name_f)
    elif choice == '3':
        write_to_current_tableDB('Contacts')
    elif choice == '4':
        print("Дякую за використання програми. Вихід.")
        break
    else:
        print("Ви ввели невірний вибір. Будь ласка, виберіть 1, 2 або 3.")




# print(record_to_db()['value'])

#
# # print(res_mass)
#
# def write_to_current_tableDB(table_name):
#
#
#     insert_query = f'''
#         INSERT INTO {table_name} (
#             id, name, mobile_phone, usr_employer_lookup_id, usr_agency_lookup_id, usr_employeemanager_ukraine_id, usr_employee_manager_europe_id, usr_scroll_lookup_id
#         ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#         '''
#     conn = connect_to_db()
#     cursor = conn.cursor()
#
#     for item in res_mass:
#         cursor.execute(insert_query, item)
#
#     # Збереження змін у базі даних
#     conn.commit()
#
#     # Закриття підключення до бази даних
#     cursor.close()
#     conn.close()
#
# write_to_current_tableDB("contacts_info")
#
#
