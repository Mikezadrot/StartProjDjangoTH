from decouple import config

fields_and_types_Contacts = {
    "id": "UUID PRIMARY KEY",  # Id робітника
    "name": "VARCHAR(255)",  # Імя робітника
    "MobilePhone": "VARCHAR(20)",  # Номер телефону робітника
    "UsrEmployerLookupId": "UUID ",  # Id роботодавця
    "UsrAgencyLookupId": "UUID ",  # Id асенції яка надала інформацію про робітника(посередник)
    "UsrEmployeemanagerUkraineId": "UUID ",  # Id менеджера Україна
    "UsrEmployeeManagerEuropeId": "UUID ",  # Id менеджера Європа
    "UsrScrollLookupId": "UUID "  # Id вакансії
}

fields_and_types_Account = {
    "id": "UUID PRIMARY KEY",  # Id роботадавця(партнера)
    "name": "VARCHAR(255)",  # Імя роботодавця(партнера)
    "phone": "VARCHAR(20)",  # номер телефону для зв'язку з партнером
    "UsrPartnerTypeId": "UUID REFERENCES partnertype(id)",  # Id типу партнера(роботодавець або агенція)
    "UsrAgencyThatGiveUsEmployerId": "UUID"  # Id агенції яка надала інформацію про партнера
}

fields_and_types_Employee = {
    "id": "UUID PRIMARY KEY",  # Id менеджера
    "name": "VARCHAR(255)",  # Імя менеджера
    "FullJobTitle": "VARCHAR(255)"  # Назва посади менеджера

}

fields_and_types_usr_scroll_list_info = {
    "id": "UUID PRIMARY KEY",  # Id вакансії(посади) для робітника
    "name": "VARCHAR(255)"  # Назва вакансії(посади)
}

fields_and_types_usr_type_partner = {
    "id": "UUID PRIMARY KEY",  # Id типу партнера
    "name": "VARCHAR(255)"  # Назва типу партнера(роботодавець, агенція)
}

name_t = ['PartnerType', 'Profession', 'Employee', 'Account', 'Contacts']
name_url = [config('URLUSRTYPEPARTNER'), config('URLUSRSCROLLLIST'), config('URLEMPLOYEE'), config('URLACCOUNT'), config('URLCONTACT')]
