import requests
from bs4 import BeautifulSoup
import Functions

link = Functions.link_func(2015) #gets all the links for each game that season
CR = []
KB = []
GB = []
Assists = 0
Goals = 0
Minutes_played = 0
for i in link:
    match = requests.get('https://fbref.com' + i).text
    soup1 = BeautifulSoup(match, 'lxml') #use continue for function in test
    soup = str(soup1.find_all(class_ = 'table_wrapper tabbed'))
    if 'Karim Benzema' not in soup or 'Cristiano Ronaldo' not in soup or 'Gareth Bale' not in soup:
        continue
    soup2 = str(soup1.find(id = "field")) #creates a string of the id field
    soup3 = str(Functions.headline(soup1, 'Real Madrid'))
    soup4 = Functions.headline(soup1, 'Real Madrid')
    times = []
    sub_in_time = []
    sub_off_time = []
    list_numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+"]
    list_times = []
    for i in soup4:
        i = str(i)
        times.append(i[33:37])
    for i in times:
        empty_str = ""
        for j in i:
            if j in list_numbers:
                empty_str = empty_str + j
        list_times.append(empty_str)
    Functions.sub_info("Cristiano Ronaldo", soup4, sub_in_time, sub_off_time, list_times)
    Functions.sub_info("Karim Benzema", soup4, sub_in_time, sub_off_time, list_times)
    Functions.sub_info("Gareth Bale", soup4, sub_in_time, sub_off_time, list_times)
    soup5 = Functions.g_a_range(sub_in_time,sub_off_time,soup4,list_times)
    Goals1 = 0
    Goals2 = 0
    Goals3 = 0
    Assists1 = 0
    Assists2 = 0
    Assists3 = 0
    Goals1 = Functions.Goal_and_Assist("Cristiano Ronaldo", soup5)[0]
    Goals2 = Functions.Goal_and_Assist("Karim Benzema", soup5)[0]
    Goals3 = Functions.Goal_and_Assist("Gareth Bale", soup5)[0]
    Assists1 = Functions.Goal_and_Assist("Cristiano Ronaldo", soup5)[1]
    Assists2 = Functions.Goal_and_Assist("Karim Benzema", soup5)[1]
    Assists3 = Functions.Goal_and_Assist("Gareth Bale", soup5)[1]
    Goals += Goals1 + Goals2 + Goals3
    Assists += Assists1 + Assists2 + Assists3
    mins = Functions.minutes_played(sub_in_time, sub_off_time, soup)
    Minutes_played += mins
print(str(Goals) + ' goals')
print(str(Assists) + ' assists')
print(str(Minutes_played) + ' mins')