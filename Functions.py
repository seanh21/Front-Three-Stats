import requests
from bs4 import BeautifulSoup

def link_func(year):
    syear = str(year)
    syear1 = str(year + 1)
    test = requests.get('https://fbref.com/en/squads/53a2f082/' + syear + '-' + syear1 + '/Real-Madrid-Stats').text
    soup = BeautifulSoup(test, 'lxml')
    table = soup.find(id='matchlogs_for')
    links_list = []
    lists = table.find_all('td', class_="left group_start")
    for i in lists:
        links_list.append(i.__str__())
    proper_links = []
    for i in links_list:
        i = i.strip('''<td class="left group_start" data-stat="match_report"><a href''')
        i = i.rstrip('>Match Report</a></')
        i = i.rstrip('"')
        proper_links.append(i)
    return proper_links

def player_sub_info(player_name, soup2, soup3, soup4, list_times):
    if player_name in soup2: #finds the choosen player in the starting lineup
        count = 0
        for i in soup4:
            count += 1
            if player_name in str(i) and "Substitute" in str(i):  # finds the index at which the player is being substituted
                return '+' + list_times[count-1]
            else:
                return '90'
    elif player_name in soup3: #finds the choosen player being substituted
        count = 0
        for i in soup4:
            count += 1
            if player_name in str(i) and "Substitute" in str(i): #finds the index at which the player is being substituted
                return '-' + list_times[count-1]
    else:
        return '0'

# def players_played():
def headline(soup1, team):
    soup2 = soup1.find('h1').text
    if soup2.index(team) == 0:
        return soup1.find_all(class_="event a")
    else:
        return soup1.find_all(class_="event b")

def sub_info(player_name, soup4, sub_in_time, sub_off_time, list_times):
    for i in soup4:
        position = soup4.index(i)
        i = str(i)
        if "event_icon substitute_in" not in i:
            continue
        a = i.split('for ')
        if player_name in a[0]:
            return sub_in_time.append(list_times[position])
        elif player_name in a[1]:
            return sub_off_time.append(list_times[position])

def g_a_range(sub_in_time, sub_off_time, soup4, list_times):
    if len(sub_in_time) == 0 and len(sub_off_time) == 0:
        return soup4
    elif len(sub_in_time) == 0:
        upper = sub_off_time[0]
        upperi = list_times.index(upper)
        return soup4[:upperi]
    elif len(sub_off_time) == 0:
        lower = sub_in_time[-1]
        loweri = list_times.index(lower)
        return soup4[loweri:]
    else:
        upper = sub_off_time[0]
        upperi = list_times.index(upper)
        lower = sub_in_time[-1]
        loweri = list_times.index(lower)
        return soup4[loweri:upperi]

def Goal_and_Assist(player_name, soup5):
    Goals = 0
    Assists = 0
    for i in soup5:
        i = str(i)
        if "event_icon goal" in i and player_name in i:
            i = i.split("Assist")
            if player_name in i[0]:
                Goals += 1
                Goals
            elif player_name in i[1]:
                Assists += 1
                # print(Assists)
                Assists
            else:
                continue
        else:
            continue
    return [Goals, Assists]

def minutes_played(sub_in_time, sub_off_time, soup):
    if len(sub_in_time) == 0 and len(sub_off_time) == 0:
        if '990' in soup:
            return 90
        else:
            return 120
    elif len(sub_in_time) == 0:
        upper = sub_off_time[0]
        upper = upper.split('+')
        return int(upper[0])
    elif len(sub_off_time) == 0:
        lower = sub_in_time[-1]
        lower = lower.split('+')
        if '990' in soup:
            return 90 - int(lower[0])
        else:
            return 120 -int(lower[0])
    else:
        upper = sub_off_time[0]
        upper = upper.split('+')
        lower = sub_in_time[-1]
        lower = lower.split('+')
        return int(upper[0]) - int(lower[0])
