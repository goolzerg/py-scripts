#Python script
#Using API dadata.ru
#Get fias/oktmo/postal


import dbf, requests, os

table = dbf.Table(r'C:\Users\Chel-uirc\Desktop\Doc\Backup\821405.dbf')
table.open(mode=dbf.READ_WRITE)
bad_addresses = open(r'C:\Users\Chel-uirc\Desktop\Doc\BAD.txt', 'a')
fias = ''
postal_code = 0
oktmo = 0
count_bad = 0
count_good = 0
detail_level = 0
API_KEY = '69d7f18a43362c802eb5113dbe20a4bfe2e2954d'


def get_details(address):
    headers = {"Authorization": "Token {}".format(API_KEY), "Content-Type": "application/json"}
    json_data = {"query": address, "count": 1}
    resp = requests.post('https://dadata.ru/api/v2/suggest/address', json=json_data, headers=headers)
    global fias, postal_code, oktmo, detail_level
    fias = resp.json()['suggestions'][0]['data']['fias_id']
    postal_code = resp.json()['suggestions'][0]['data']['postal_code']
    oktmo = resp.json()['suggestions'][0]['data']['oktmo']
    detail_level = resp.json()['suggestions'][0]['data']['fias_level']


def FindDetails():
    for x in dbf.Process(table):
        try:
            if 'УЧАСТОК' in x[3].rstrip() or 'УЧ-К' in x[3].rstrip():
                bad_addresses.write(str(
                    x[0].rstrip() + ', ' + x[1].rstrip() + ', ' + x[3].rstrip() + ', ' + x[4].rstrip() + '\n').lower())
            else:
                prep_addr = x[0].rstrip() + ', ' + x[1].rstrip() + ', ' + x[3].rstrip() + ', ' + x[4].rstrip()
                get_details(prep_addr)

                if detail_level == '8':
                    if len(x[8].rstrip()) != 0:
                        count_good += 1
                        print('Found: ' + prep_addr.lower())
                        print('Count good :' + str(count_good))
                        x[7] = fias
                        x[6] = oktmo
                    else:
                        count_good += 1
                        print('Found: ' + prep_addr.lower())
                        print('Count good :' + str(count_good))
                        x[8] = postal_code
                        x[7] = fias
                        x[6] = oktmo
                else:
                    count_bad += 1
                    print('Not found: ' + prep_addr)
                    bad_addresses.write(str(x[0].rstrip() + ', ' + x[1].rstrip() + ', ' + x[3].rstrip() + ', ' + x[
                        4].rstrip() + '\n').lower())
                    print('Count bad: ' + str(count_bad))
        except IndexError:
            print('Error: ' + prep_addr)
            print('Count bad: ' + str(count_bad))
            count_bad += 1
            bad_addresses.write(
                str(x[0].rstrip() + ', ' + x[1].rstrip() + ', ' + x[3].rstrip() + ', ' + x[4].rstrip() + '\n').lower())
    table.close()


def FindPostal():
    global count_good, count_bad
    for x in dbf.Process(table):
        try:
            if len(x[8].rstrip()) == 0:
                if len(x[1].rstrip()) != 0:
                    prep_addr = x[0].rstrip() + ', ' + x[1].rstrip() + ', ' + x[3].rstrip() + ', ' + x[4].rstrip()
                    get_details(prep_addr)
                    x[8] = postal_code
                    count_good += 1
                    print('Count good: ' + str(count_good))
                    print(postal_code)
                else:
                    prep_addr = x[0].rstrip() + ', ' + x[3].rstrip() + ', ' + x[4].rstrip()
                    get_details(prep_addr)
                    x[8] = postal_code
                    count_good += 1
                    print('Count good: ' + str(count_good))
                    print(postal_code)
        except IndexError:
            print('Bad address: ' + prep_addr)
            count_bad += 1
            print('Count bad: ' + str(count_bad))
            bad_addresses.write(prep_addr + '\n')
    table.close()
    count_bad = 0
    count_good = 0


FindPostal()
