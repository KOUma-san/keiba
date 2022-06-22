from bs4 import BeautifulSoup
import requests
from time import sleep

import os
import datetime

from decimal import Decimal
import json
import urllib.request
import urllib.parse

import pandas as pd
from pandas.errors import EmptyDataError

import glob
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np


# umamei scraping
def umamei_scraping(race_id):
    syutsubahyou = "https://race.netkeiba.com/race/shutuba.html?race_id={}&rf=race_list".format(race_id)
    res = requests.get(syutsubahyou)
    sleep(1)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, "html.parser")
    elems = soup.select('span a')
    elems2 = soup.select('div.RaceName')
    elems3 = soup.select('div.RaceData01')
    elems4 = soup.select('div.RaceData02')
    elems5 = soup.select('span.RaceNum')
    race_name = str(elems2[0].text).strip()
    race_time = str(elems3[0].text).strip()
    race_time = race_time.split('/')[0]
    race_time = race_time[0] + race_time[1] + race_time[3] + race_time[4]
    race_place = str(elems4[0].text).strip()
    race_place = race_place.splitlines()[1]
    race_num = str(elems5[0].text).strip()

    count = 0
    uma_list = []
    for uma in elems:
        count += 1
        uma_list.append(str(count) + ' ' + str(uma.text))

    color_list_5 = ["wheat", "black", "red", "blue", "yellow"]
    color_list_6 = ["wheat", "black", "red", "blue", "yellow", "green"]
    color_list_7 = ["wheat", "black", "red", "blue", "yellow", "green", "orange"]
    color_list_8 = ["wheat", "black", "red", "blue", "yellow", "green", "orange", "pink"]
    color_list_9 = ["wheat", "black", "red", "blue", "yellow", "green", "orange", "pink", "deeppink"]
    color_list_10 = ["wheat", "black", "red", "blue", "yellow", "green", "orange", "darkorange", "pink", "deeppink"]
    color_list_11 = ["wheat", "black", "red", "blue", "yellow", "green", "darkgreen", "orange", "darkorange", "pink", "deeppink"]
    color_list_12 = ["wheat", "black", "red", "blue", "yellow", "gold", "green", "darkgreen", "orange", "darkorange", "pink", "deeppink"]
    color_list_13 = ["wheat", "black", "red", "blue", "darkblue", "yellow", "gold", "green", "darkgreen", "orange", "darkorange", "pink", "deeppink"]
    color_list_14 = ["wheat", "black", "red", "darkred", "blue", "darkblue", "yellow", "gold", "green", "darkgreen", "orange", "darkorange", "pink", "deeppink"]
    color_list_15 = ["wheat", "black", "gray", "red", "darkred", "blue", "darkblue", "yellow", "gold", "green", "darkgreen", "orange", "darkorange", "pink", "deeppink"]
    color_list_16 = ["wheat", "silver", "black", "gray", "red", "darkred", "blue", "darkblue", "yellow", "gold", "green", "darkgreen", "orange", "darkorange", "pink", "deeppink"]
    color_list_17 = ["wheat", "silver", "black", "gray", "red", "darkred", "blue", "darkblue", "yellow", "gold", "green", "darkgreen", "orange", "darkorange", "pink", "deeppink", "magenta"]
    color_list_18 = ["wheat", "silver", "black", "gray", "red", "darkred", "blue", "darkblue", "yellow", "gold", "green", "darkgreen", "orange", "darkorange", "chocolate", "pink", "deeppink", "magenta"]
    if count == 18:
        color_list = color_list_18
    elif count == 17:
        color_list = color_list_17
    elif count == 16:
        color_list = color_list_16
    elif count == 15:
        color_list = color_list_15
    elif count == 14:
        color_list = color_list_14
    elif count == 13:
        color_list = color_list_13
    elif count == 12:
        color_list = color_list_12
    elif count == 11:
        color_list = color_list_11
    elif count == 10:
        color_list = color_list_10
    elif count == 9:
        color_list = color_list_9
    elif count == 8:
        color_list = color_list_8
    elif count == 7:
        color_list = color_list_7
    elif count == 6:
        color_list = color_list_6
    elif count == 5:
        color_list = color_list_5

    return race_name, race_time, race_place, race_num, uma_list, color_list


# create files
def create_files(race_name, race_place, race_num):
    now = datetime.datetime.now()
    racedate = now.strftime('%y%m%d')
    baken_list = ["tansyo", "fukusyo", "umaren", "wide", "sanfuku", "santan"]
    path = 'G:/マイドライブ/05_Keiba/' + race_place + '/' + racedate + '_' + race_place + race_num + '_' + race_name
    
    if not os.path.exists(path):
        os.mkdir(path)
        
    for i in range(len(baken_list)):
        path_i = path + '/' + baken_list[i] + '' 
        if not os.path.exists(path_i):
            os.mkdir(path_i)
    return path


# function of getting tansyo odds 
def tansyo(race_id):
    url = 'https://oldrace.netkeiba.com/?pid=show_ninkioddsgraph_js&raceid={0}&type={1}&offset=0&limit=5000'
    url = url.format(race_id, '1')
    try:
        with urllib.request.urlopen(url) as f:
            res =json.loads( f.read().decode('utf-8') )
        o1 = []
        for uma in res['showArray']:
            o1.append(uma['Kumi'])
        umalist = sorted(o1)
        o2 = []
        for odd in res['showArray']:
        # if cancel horses exist
            try:
                float(odd['tan'])
            except ValueError:
                o2.append(0)
            else:
                o2.append(Decimal(odd['tan']))        
        odds_list = [0] * len(umalist)
        for i, j in zip(o1, umalist):
            odds_list[i - 1] = o2[j - 1]  
        return umalist, odds_list
    except Exception as e:
        print(e)
        return [],[]


# function of getting fukusyo odds 
def fukusyo(race_id):
    url = 'https://oldrace.netkeiba.com/?pid=show_ninkioddsgraph_js&raceid={0}&type={1}&offset=0&limit=5000'
    url = url.format(race_id, '1')
    try:
        with urllib.request.urlopen(url) as f:
            res =json.loads( f.read().decode('utf-8') )
        o1 = []
        for uma in res['showArray']:
            o1.append(uma['Kumi'])
        o2 = []
        for odd in res['showArray']:
            fuku = odd['fuku'].split('@')
        # if cancel horses exist
            try:
                float(fuku[0])
            except ValueError:
                o2.append(0)
            else:          
                fuku1 = (Decimal(fuku[0])+Decimal(fuku[1]))/2
                o2.append(fuku1)
            
        umalist = sorted(o1)
        odds_list = [0] * len(umalist)
        for i, j in zip(o1, umalist):
            odds_list[i - 1] = o2[j - 1]
        return odds_list
    except Exception as e:
        print(e)
        return [],[]


# function of getting umaren odds 
def umaren(race_id, umalist):
    url = 'https://oldrace.netkeiba.com/?pid=show_ninkioddsgraph_js&raceid={0}&type={1}&offset=0&limit=5000'
    url = url.format(race_id, '4')
    try:
        with urllib.request.urlopen(url) as f:
            res =json.loads( f.read().decode('utf-8') )
        odds_list = [0] * len(umalist)
        for odd in res['showArray']:
            kumi = odd['Kumi'].split('-')
            umaren = odd['odds']
            odds_list[int(kumi[0]) - 1]+=Decimal(umaren)
            odds_list[int(kumi[1]) - 1]+=Decimal(umaren)
        return odds_list 
    except Exception as e:
        print(e)
        return []


# function of getting wide odds
def wide(race_id, umalist):
    url = 'https://oldrace.netkeiba.com/?pid=show_ninkioddsgraph_js&raceid={0}&type={1}&offset=0&limit=5000'
    url = url.format(race_id, '5')
    try:
        with urllib.request.urlopen(url) as f:
            res =json.loads( f.read().decode('utf-8') )
        odds_list = [0] * len(umalist)
        for odd in res['showArray']:
            kumi = odd['Kumi'].split('-')
            wide = odd['odds'].split('@')
            wide1 = (Decimal(wide[0])+Decimal(wide[1]))/2
            odds_list[int(kumi[0]) - 1]+=wide1
            odds_list[int(kumi[1]) - 1]+=wide1
        return odds_list
    except Exception as e:
        print(e)
        return []


# function of getting sanfuku odds
def sanfuku(race_id, umalist):
    url = 'https://oldrace.netkeiba.com/?pid=show_ninkioddsgraph_js&raceid={0}&type={1}&offset=0&limit=5000'
    url = url.format(race_id, '7')
    try:
        with urllib.request.urlopen(url) as f:
            res =json.loads( f.read().decode('utf-8') )
        odds_list = [0] * len(umalist)
        for odd in res['showArray']:
            kumi = odd['Kumi'].split('-')
            sanfuku = odd['odds']
            odds_list[int(kumi[0]) - 1]+=Decimal(sanfuku)
            odds_list[int(kumi[1]) - 1]+=Decimal(sanfuku)
            odds_list[int(kumi[2]) - 1]+=Decimal(sanfuku)
        return odds_list
    except Exception as e:
        print(e)
        return []


# function of getting santan odds
def santan(race_id, umalist):
    url = 'https://oldrace.netkeiba.com/?pid=show_ninkioddsgraph_js&raceid={0}&type={1}&offset=0&limit=5000'
    url = url.format(race_id, '8')
    try:
        with urllib.request.urlopen(url) as f:
            res =json.loads( f.read().decode('utf-8') )

        odds_list = [0] * len(umalist)
        for odd in res['showArray']:
            kumi = odd['Kumi'].split('-')
            santan = odd['odds']
            odds_list[int(kumi[0]) - 1]+=(Decimal(santan)*Decimal("0.8"))
            odds_list[int(kumi[1]) - 1]+=(Decimal(santan)*Decimal("0.9"))
            odds_list[int(kumi[2]) - 1]+=Decimal(santan)
        return odds_list
    except Exception as e:
        print(e)
        return []


# calculate odds
def caluculate_odds(odds_list, kensyu, path):
    odds_csv_file = path + '/' + kensyu + '/matome.csv'
    if os.path.exists(odds_csv_file):
        df0 = pd.read_csv(odds_csv_file, encoding = 'shift-jis', index_col=0)
        df_before = df0.iloc[:, -1]
        before_list = df_before.to_list()
        for i, odds in enumerate(before_list):
            before_list[i] = Decimal(str(odds))
        diff_list = [x - y for (x, y) in zip(odds_list, before_list)]    
        for i, diff_odds in enumerate(diff_list):
            if diff_odds < 0:
                diff_list[i] = Decimal(str(diff_odds * Decimal(1.1)))
            else:
                diff_list[i] = Decimal(str(diff_odds))
    else:
        diff_list = [0] * len(odds_list)

    now = datetime.datetime.now()
    time = now.strftime('%m/%d %H:%M')
    df1 = pd.DataFrame(data={'umaban': uma_list, time: diff_list})
    diff_csv_file = path + '/' + kensyu + '/diff.csv'
    # df1.to_csv(diff_csv_file, encoding = 'shift-jis', header = True, index = True, errors='ignore')
    
    if not os.path.exists(diff_csv_file):
        diff_list = [0] * len(odds_list)
        df2 = pd.DataFrame(data={'umaban': uma_list, time: diff_list})
        df2.to_csv(diff_csv_file, encoding = 'shift-jis', header = True, index = True, errors='ignore')
    else:
        df3 = pd.read_csv(diff_csv_file, encoding = 'shift-jis', index_col=0)
        df4 = pd.concat([df3, df1], axis=1)
        df5 = df4.loc[:,~df4.columns.duplicated()]
        df5.to_csv(diff_csv_file, encoding = 'shift-jis', header = True, index = True, errors='ignore')
    
    
# create df and odds csv files
def dftocsv(uma_list, odds_list, kensyu, path):
    now = datetime.datetime.now()
    time = now.strftime('%m/%d %H:%M')
    odds_csv_file = path + '/' + kensyu + '/matome.csv'
    df0 = pd.DataFrame(data={'umaban': uma_list, time: odds_list})

    if not os.path.exists(odds_csv_file):
        df0.to_csv(odds_csv_file, encoding = 'shift-jis', header = True, index = True, errors='ignore')
    else:
        df1 = pd.read_csv(odds_csv_file, encoding = 'shift-jis', index_col=0)
        df2 = pd.concat([df1, df0], axis=1)
        df3 = df2.loc[:,~df2.columns.duplicated()]
        df3.to_csv(odds_csv_file, encoding = 'shift-jis', header = True, index = True, errors='ignore')


# odds rank
def rank_odds(path, kensyu):
    file = path + '/' + kensyu + '/diff.csv'
    df0 = pd.read_csv(file, encoding = 'shift-jis', index_col=0)
    df_sum = df0.iloc[:, :].sum(axis=1)
    df0.iloc[:, -1] = df_sum
    df_rank = df0.iloc[:, -1].rank().astype(int)
    return df_rank


# determin odds rank
def det_buy_list(path, file_rank):
    remaining_time = "15"
    file_last_rank = path + '/last_rank_' + remaining_time + 'min.csv'
    df = pd.read_csv(file_rank, encoding = 'shift-jis', index_col=0)
    df.to_csv(file_last_rank, encoding = 'shift-jis', header = True, index = True, errors='ignore')


# create odds gragh
def odds_graph(path, kensyu, ymin, ymax, ystep, color_list):
    path_graph = path + '/graph' 
    if not os.path.exists(path_graph):
        os.mkdir(path_graph)
    
    now = datetime.datetime.now()
    racedate = now.strftime('%y'+'/'+'%m'+'/'+'%d')
    time = now.strftime('%m%d_%H%M')
    file = path + '/' + kensyu + '/matome.csv'
    df_baken   = pd.read_csv(file, index_col=0, encoding = 'shift-jis')
    df_baken = df_baken.set_index('umaban')
    graph_title = str(racedate) + ' ' + race_name + ' ' + kensyu
    
    fig, ax = plt.subplots(figsize=(18,10))
    plt.title(graph_title, {"fontsize": 20}, fontname="MS Gothic")
    plt.xlabel('Date')
    plt.ylabel("Odds")
    plt.minorticks_on()
    plt.xticks(rotation=75)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.ylim([ymin, ymax])
    plt.yticks(np.arange(ymin, ymax+ystep, step=ystep))
    plt.grid(linestyle='dotted', linewidth=1)
    
    for i in range(0, len(color_list), 1):
        baken_i_list = df_baken.iloc[i]
        if i % 2 == 0:
            plt.plot(df_baken.columns, baken_i_list, color=color_list[i], marker='o', label=str(df_baken.index[i]))
        else:
            plt.plot(df_baken.columns, baken_i_list, color=color_list[i], marker='^', label=str(df_baken.index[i]))
    ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    plt.legend(bbox_to_anchor=(0, 1), loc='upper left', borderaxespad=1, prop={'family':'Yu Gothic'})
    
    for file in glob.glob(path_graph+'/'+kensyu+'_graph*.png'):
        os.remove(file)  
    plt.savefig(path_graph+'/'+kensyu+'_graph_'+time+'.png', dpi=300)


if __name__ == '__main__':
    race_id_from_netkeiba = 2022050306
    for i in range(1, 13, 1):
        race_id = str(race_id_from_netkeiba) + str(i).zfill(2)
        race_name, race_time, race_place, race_num, uma_list, color_list = umamei_scraping(race_id)
        path = create_files(race_name, race_place, race_num)

        umalist, tansyo_odds_list = tansyo(race_id)
        fukusyo_odds_list = fukusyo(race_id)
        umaren_odds_list = umaren(race_id, umalist)
        wide_odds_list = wide(race_id, umalist)
        sanfuku_odds_list = sanfuku(race_id, umalist)
        santan_odds_list = santan(race_id, umalist)
    
        caluculate_odds(tansyo_odds_list, "tansyo", path)
        caluculate_odds(fukusyo_odds_list, "fukusyo", path)
        caluculate_odds(umaren_odds_list, "umaren", path)
        caluculate_odds(wide_odds_list, "wide", path)
        caluculate_odds(sanfuku_odds_list, "sanfuku", path)
        caluculate_odds(santan_odds_list, "santan", path)

        dftocsv(uma_list, tansyo_odds_list, "tansyo", path)
        dftocsv(uma_list, fukusyo_odds_list, "fukusyo", path)
        dftocsv(uma_list, umaren_odds_list, "umaren", path)
        dftocsv(uma_list, wide_odds_list, "wide", path)
        dftocsv(uma_list, sanfuku_odds_list, "sanfuku", path)
        dftocsv(uma_list, santan_odds_list, "santan", path)
        
        df_tan_rank = rank_odds(path, "tansyo")
        df_fuku_rank = rank_odds(path, "fukusyo")
        df_umaren_rank = rank_odds(path, "umaren")
        df_wide_rank = rank_odds(path, "wide")
        df_sanfuku_rank = rank_odds(path, "sanfuku")
        df_santan_rank = rank_odds(path, "santan")

        file_rank = path + '/rank.csv'

        df_rank = pd.concat([df_tan_rank, df_fuku_rank, df_umaren_rank, df_wide_rank, df_sanfuku_rank, df_santan_rank], axis=1)
        df_rank_sum0 = df_rank.iloc[:, 0:6].sum(axis=1).astype(int)
        df_rank_sum = df_rank.iloc[:, 0:6].sum(axis=1).rank().astype(int)
        df_rank = pd.concat([df_rank, df_rank_sum], axis=1)
        columns_list = ["tansyo", "fukusyo", "umaren", "wide", "sanfuku", "santan", "sum"]
        df_rank.columns = columns_list
        df_rank.insert(0, 'umaban', uma_list)
        df_rank.to_csv(file_rank, encoding = 'shift-jis', header = True, index = True, errors='ignore')
        
        now = datetime.datetime.now()
        now_time = now.strftime("%H%M")
        now_time1 = int(now_time[:2])
        now_time2 = int(now_time[2:])/60
        now_time = now_time1 + now_time2
        race_time1 = int(race_time[:2])
        race_time2 = int(race_time[2:])/60
        race_time = race_time1 + race_time2
        diff_time = race_time - now_time

        if 0.2 < diff_time < 0.3:
            det_buy_list(path, file_rank)
            odds_graph(path, "tansyo", 0, 70, 5, color_list)
            odds_graph(path, "fukusyo", 1, 15, 1, color_list)
        else:
            pass


