import requests
import os
from bs4 import BeautifulSoup

#get all parsing archives
def get_archives():
    url = "https://xn--80aapkb3algkc.xn--j1afpl.xn--p1ai/.%d0%b0%d1%80%d1%85%d0%b8%d0%b2/"
    
    #get html and all time archive
    try:
        get = requests.get(url,timeout=5)
    except requests.ConnectionError:
        return "TimeOutError"
    
    get.encoding = "utf-8"
    soup = BeautifulSoup(get.text, "lxml")
    all_archive = soup.find("ul").find_all("a")
    
    return all_archive
    
#get all parsing archives
def get_groups(archive: str):
    
    #get html and list of groups
    try:
        get = requests.get(f"https://xn--80aapkb3algkc.xn--j1afpl.xn--p1ai{archive}/группы.html#заголовок", timeout=5)
    except requests.ConnectionError:
        return "TimeOutError"
        
    get.encoding = "utf-8"  
    soup = BeautifulSoup(get.text, "lxml")
    all_group = soup.find("div",class_="колонки-группы").find_all("a")
    
    return all_group
    
#get shedule
def get_shedule(archive: str, group: str) -> str:
    #get html and shedules
    try:
        get = requests.get(f"https://xn--80aapkb3algkc.xn--j1afpl.xn--p1ai{archive}/{group}", timeout=5)
    except requests.ConnectionError:
        return "TimeOutError"
    get.encoding = "utf-8"
    soup = BeautifulSoup(get.text, "lxml")
    schedule = soup.find("table",class_="расписание").find_all("tr")
    #output shedule
    output_shedule: str = ""
    for i in schedule:
        if i.find("td",colspan="5") != None:
            output_shedule += ("--" * 5) + '\n<u><b>' + i.text + '</b></u>\n'
        elif i.find("div",class_="пара-заголовок") != None:
            continue
        else:
            info = i.find_all("td")
            output_shedule += "<i><b>Пара - " + str(info[0].text) + " </b></i>" + str(info[2].text.replace("­","")) + '\n' \
            "Начало/конец: " + str((info[1].text)) + '\n' \
            "Преподователь: " + str(info[3].text.replace("­","")) + '\n' \
            "Кабинет: " + str(info[4].text) + '\n\n'
    return output_shedule