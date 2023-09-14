from decouple import config


fields_and_types_Contacts = {
    "id": "UUID PRIMARY KEY",
    "name": "VARCHAR(255)",
    "MobilePhone": "VARCHAR(20)",
    "UsrEmployerLookupId": "UUID",
    "UsrAgencyLookupId": "UUID",
    "UsrEmployeemanagerUkraineId": "UUID",
    "UsrEmployeeManagerEuropeId": "UUID",
    "UsrScrollLookupId": "UUID"
}

fields_and_types_Account = {
    "id": "UUID PRIMARY KEY",
    "name": "VARCHAR(255)",
    "phone": "VARCHAR(20)",
    "UsrPartnerTypeId": "UUID",
    "UsrAgencyThatGiveUsEmployerId": "UUID"
}

fields_and_types_Employee = {
    "id": "UUID PRIMARY KEY",
    "name": "VARCHAR(255)",
    "FullJobTitle": "VARCHAR(255)"

}


fields_and_types_usr_scroll_list_info = {
    "id": "UUID PRIMARY KEY",
    "name": "VARCHAR(255)"
}


fields_and_types_usr_type_partner = {
    "id": "UUID PRIMARY KEY",
    "name": "VARCHAR(255)"
}



name_t = ['Contacts', 'Account', 'Employee', 'Profession', 'PartnerType']
name_url = [config('URLCONTACT'), config('URLACCOUNT'), config('URLEMPLOYEE'), config('URLUSRSCROLLLIST'), config('URLUSRTYPEPARTNER')]
