import requests, re
import xml.etree.ElementTree as ET

data_list = []
polyvision = {'Миасское': 'http://192.168.167.152/action/get?subject=diskinfo&id=0',
              'Коркино': 'http://192.168.156.120/action/get?subject=diskinfo&id=0',
              'Южноуральск': 'http://192.168.159.152/action/get?subject=diskinfo&id=0',
              'Копейск': 'http://192.168.158.152/action/get?subject=diskinfo&id=0'}

trassir = {'Верхнеуральск': 'http://192.168.168.100/cn/admin/SDset.asp',
           'Карталы': 'http://192.168.169.100/cn/admin/SDset.asp',
           'Калинина 9а': 'http://192.168.161.100/cn/admin/SDset.asp',
           'Карла Маркса 202': 'http://192.168.162.100/cn/admin/SDset.asp',
           'Карла Маркса 157': 'http://192.168.160.100/cn/admin/SDset.asp', }

for ip in polyvision:
    try:
        r = requests.get(polyvision[ip], auth=('admin', 'admin'))
        if '<status>3</status>' in r.text:
            match = re.search(r'<free>(.*)</free>', r.text)
            freespace = str(int(float(match.group(1)) / 2 ** 20))
            match = re.search(r'<size>(.*)</size>', r.text)
            freespace += '/' + str(int(float(match.group(1)) / 2 ** 20))
            print(ip + '(хорошо)' + 'свободное место: ' + freespace + '\n')
        else:
            print(ip + '(!!!!!!!!!!!!!ошибка диска!!!!!!!!!!!!!)' + '\n')
        possible_error = ip
    except:
        print(ip + ' - ошибка, проверьте подключение камеры' + '\n')

for ip in trassir:
    try:
        r = requests.get(trassir[ip], auth=('admin', 'admin'))
        data_list.append(r.text)
        data_list = ''.join(data_list).split('\n')
        search = 'firstChild.nodeValue=("normal")'
        for i in data_list:
            if search in i:
                disk_space = i
                disk_space = disk_space.split(';')
                match = re.search(r'"(.*)"', disk_space[4])
                if len(match.group(1)) != 0:
                    print(ip + '(хорошо)' + ' свободное место: ' + match.group(1) + '\n')
                else:
                    print(ip + '(!!!!!!!!!!!!!ошибка диска!!!!!!!!!!!!!)' + '\n')
                data_list.clear()
        possible_error = ip
    except:
        print(ip + ' - ошибка, проверьте подключение камеры' + '\n')
