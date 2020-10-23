import json
import math
import pandas as pd

with open('persons_with_ids.csv') as f1:
    persons = pd.read_csv(f1)

projects = ["809245f8-63d3-41b4-ad52-1e9a67cc965a"]

persons_list = []
for index, row in persons.iterrows():

    # these fields might be nan
    email = persons.loc[index]['email']
    mobileNum = persons.loc[index]['mobile']
    address1 =  persons.loc[index]['address1']
    town = persons.loc[index]['town']
    lastName = persons.loc[index]['lastName']
    birthYear =  persons.loc[index]['birthYear']

    # perform a check for nan - if there is a nan it won't be converted into correct JSON format
    # (nans are floats)
    if (type(email) == float):
        email = ""
    if (type(mobileNum) == float):
        mobileNum = ""
    if (type(address1) == float):
        address1 = ""
    if (type(town) == float):
        town = ""
    if (type(lastName) == float):
        lastName = ""
    if (math.isnan(birthYear)):
        birthYear = ""
    else :
        birthYear = str(int(birthYear))

    person = {
        "firstName": persons.loc[index]['firstName'],
        "lastName":lastName,
        "email": email,
        "personCode": str(persons.loc[index]['personCode']),
        "personId" : persons.loc[index]['personId'],
        "projects" : projects,
        "address1" : address1,
        "town" : town,
        "gender":  persons.loc[index]['gender'],
        "mobileNum": mobileNum,
        "birthYear": birthYear
    }
    persons_list.append(person)

with open('persons_upload_test.json', 'w') as f:
    json.dump(persons_list, f, ensure_ascii=False)