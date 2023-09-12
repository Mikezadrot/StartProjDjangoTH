#Code special to POST&GET to Creatio
from decouple import config
import requests
import json
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

urlcrm = config('CREATIOURL', default = '' )
url_to_auth = config('URLTOAUTH', default = '')
usernamecrm = config('USERNAMECRM', default = '')
userpasswordcrm = config('USERPASSWORD', default = '')

#
# print(urlcrm)
# print(url_to_auth)
# print(usernamecrm)
# print(userpasswordcrm)

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

def send_get_request_with_cookies(url_odata, namefile):
    url = config('CREATIOURL') + url_odata
    cookies_filename = 'cookies.json'
    response_filename = f'{namefile}.json'
    try:
        # Зчитати куки з файлу
        with open(cookies_filename, 'r') as cookies_file:
            cookies = json.load(cookies_file)

        # Відправити GET-запит з кукісами
        response = requests.get(url, cookies=cookies, verify=False)

        # Вивести відповідь на екран
        with open(response_filename, 'w') as response_file:
            json.dump(response.json(), response_file,ensure_ascii=False, indent=4)
        print(f'ALL INFO WAS WRITTEN IN {response_filename} file')
        return response

    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return None


# send_get_request_with_cookies()

list_of_urls = [config('URLACCOUNT'), config('URLCONTACT'), config('URLUSRLEADS')]
modified_strings = [s.replace("/0/odata/", "") for s in list_of_urls]


# THIS CODE WAS FIRST TRY TO RECORD INTO JSON FILE DIFFERENT INFO FROM CREATIO

# auth_func()
#
# for i in range(0, len(modified_strings)):
#     print('Start written to JSON ')
#
#     send_get_request_with_cookies(list_of_urls[i], modified_strings[i])
#     print(f'{modified_strings[i]} file was written')
#
#
# print("ALL IS OK")
# print(" Input 1. Записати куки для авторизації серверу на Creatio")
# print(" Input 2. Виконати запити по протоколу odata v4 to Creatio")
# print(" Input 3. Exit")
#
# print("Що ви хочете зробити?")

# END CODE

while True:
    print(" Input 1. Записати куки для авторизації серверу на Creatio")
    print(" Input 2. Виконати запити по протоколу odata v4 to Creatio")
    print(" Input 3. Exit")

    choice = input("Що ви хочете зробити?")
    if choice == '1':
        auth_func()
    elif choice == '2':
        for i in range(0, len(modified_strings)):
            print('Start written to JSON ')

            send_get_request_with_cookies(list_of_urls[i], modified_strings[i])
            print(f'{modified_strings[i]} file was written')
    elif choice == '3':
        print("Дякую за використання програми. Вихід.")
        break
    else:
        print("Ви ввели невірний вибір. Будь ласка, виберіть 1, 2 або 3.")








# TESTING CODE UNDER THIS COMMENT IS NOT INTERESTING FOR ANOTHER PEOPLE



# test_str_mass = [config('URLACCOUNT'), config('URLCONTACT'), config('URLUSRLEADS')]
# modified_strings = [s.replace("/0/odata/", "") for s in test_str_mass]
# for s in modified_strings:
#     print(s)
# test_str = config('URLCONTACT')
# mod_s = test_str.replace('/0/odata/', '')
# print(test_str)
# print(mod_s)
# print(new_str)


# END BULLSHIT