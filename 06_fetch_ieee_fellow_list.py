import requests
from bs4 import BeautifulSoup
import time

def fetch(url):
    # d = BeautifulSoup(open(url,encoding='utf-8'),features='html.parser')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0',
        'Cookie': 'GSP=CF=4'
    }
    while True:
        try:
            resp = requests.get(url, headers=headers)
            break
        except Exception as e:
            print(e)
            pass
    time.sleep(2)
    d = BeautifulSoup(resp.content, "html.parser")
    main_table = d.find(name="table", attrs={"class": "wikitable"})
    trs = main_table.findAll(name="tr")
    fellow_list = []
    for tr in trs:
        tds = tr.findAll(name="td")
        if len(tds) == 3:
            fellow_list.append(tds[1].text)
    print(url, len(fellow_list))
    return fellow_list

    # print(len(fellow_table))

urls = [
    "https://en.wikipedia.org/wiki/List_of_fellows_of_IEEE_Aerospace_and_Electronic_Systems_Society",
    "https://en.wikipedia.org/wiki/List_of_fellows_of_IEEE_Broadcast_Technology_Society",
    "https://en.wikipedia.org/wiki/List_of_fellows_of_IEEE_Circuits_and_Systems_Society",
    "https://en.wikipedia.org/wiki/List_of_fellows_of_IEEE_Communications_Society",
    "https://en.wikipedia.org/wiki/List_of_fellows_of_IEEE_Computational_Intelligence_Society",
    "https://en.wikipedia.org/wiki/List_of_fellows_of_IEEE_Consumer_Electronics_Society",
    "https://en.wikipedia.org/wiki/List_of_fellows_of_IEEE_Control_Systems_Society",
    "https://en.wikipedia.org/wiki/List_of_fellows_of_IEEE_Dielectrics_%26_Electrical_Insulation_Society",
    "https://en.wikipedia.org/wiki/List_of_fellows_of_IEEE_Education_Society",
    "https://en.wikipedia.org/wiki/List_of_fellows_of_IEEE_Electromagnetic_Compatibility_Society",
    "https://en.wikipedia.org/wiki/List_of_fellows_of_IEEE_Electron_Devices_Society",
    "https://en.wikipedia.org/wiki/IEEE_Antennas_%26_Propagation_Society",
    "https://en.wikipedia.org/wiki/List_of_fellows_of_IEEE_Engineering_in_Medicine_and_Biology_Society",
    "https://en.wikipedia.org/wiki/List_of_fellows_of_IEEE_Power_%26_Energy_Society",
    "https://en.wikipedia.org/wiki/List_of_fellows_of_IEEE_Power_Electronics_Society"
]

fellow_list = []
for url in urls:
    fellow_list.extend(fetch(url))

with open("fellow/IEEE fellow list new.txt", "w", encoding='utf-8') as f:
    for fellow in fellow_list:
        f.write(fellow)
        f.write("\n")
