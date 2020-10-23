import uuid
import json

# STEP 1 - combine all info needed for persons and prepare a csv

def generate_uniqId_format():
    _uniqid = uuid.uuid4().hex
    indices = [0,8,12,16,20,32]
    parts = [_uniqid[i:j] for i,j in zip(indices, indices[1:])]
    uniqid = '-'.join(parts)
    return uniqid


with open('persons_at_sites_sebms.csv') as f:
    site_bookings = pd.read_csv(f)

with open('personal_data.csv') as f1:
    persons = pd.read_csv(f1)

uuids = []
for i in range(0, len(persons)):
    uuids.append(generate_uniqId_format())

persons['personId'] = uuids
persons.to_csv('persons_with_ids.csv') # use to create a json with persons to upload

df = pd.merge(persons, site_bookings, on="personid", how="inner")

df.to_csv('persons_with_sites.csv') # use this file for site booking - in combination with transect/transect_convert_sites.py