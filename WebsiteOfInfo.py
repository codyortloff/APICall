# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 15:40:50 2024

@author: COrtloff
"""
import json
import requests
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup

data = requests.get('https://moaapi.net/v2/mall_hours')

json_string = data.text[1:-1]
parsed_json = json.loads(json_string)

day_id = []
day = []
open = []
close = []

for i in parsed_json['hours']['regular']:
    for j in i:
        if j == 'day_id':
            day_id.append(i[j])
        elif j == 'day':
            day.append(i[j])
        elif j == 'open':
            open.append(i[j])
        elif j == 'close':
            close.append(i[j])

reg_hours = pd.DataFrame({'DayID' : day_id, 'Day' : day, 'Open' : open, 'Close' : close}).sort_values('DayID')


day_id = []
day = []
open = []
close = []
date = []

for i in parsed_json['hours']['upcoming']:
    for j in i:
        if j == 'day_id':
            day_id.append(i[j])
        elif j == 'day':
            day.append(i[j])
        elif j == 'open':
            open.append(i[j])
        elif j == 'close':
            close.append(i[j])
        elif j == 'date':
            date.append(i[j])

upcoming_hours = pd.DataFrame({'DayID' : day_id, 'Day' : day, 'Open' : open, 'Close' : close, 'Date' : date}).sort_values('Date')



st.write(f'This file contains the {parsed_json[list(parsed_json.keys())[0]]} for the Mall of America')
st.write('The regular hours are:')
for i in reg_hours.values:
    st.write(f'\t{i[1]}: {i[2]} - {i[3]}')


st.write('However, sometimes the upcoming hours can be a little bit different than the regular hours.')

count = 0
for i in upcoming_hours.values:
    if count == 0:
        st.write(f"Today ({i[1]}, {i[4]}), the mall is open from {i[2]} to {i[3]}")
    elif count == 1:
        st.write(f"Tomorrow ({i[1]}, {i[4]}), the mall is open from {i[2]} to {i[3]}")
    else: 
        st.write(f"This upcoming {i[1]} ({i[4]}), the mall is open from {i[2]} to {i[3]}")
    count += 1
    
    
    
## Tenant INFO:
data = requests.get('https://moaapi.net/v2/tenants/include-tags')

json_string = data.text
parsed_json = json.loads(json_string)

for i in parsed_json:
    tenant_str = ''
    try:
        tenant_str += f"{i['name'].strip()}"
    except KeyError:
        st.write()

    try: 
        tenant_str += f" is located on level {i['level']} of the mall. "
    except KeyError:
        st.write()

    try:
        tenant_str += BeautifulSoup(i['teaser'], 'html.parser').text.strip().replace('.\n', '. ').replace('\n', ': ')
        tenant_str += ' '
    except:
        st.write()

    try:
        count = 1
        for j in i['type']:
            if count == 1:
                tenant_str += f"{i['name'].strip()} is a "
            tenant_str += j['name']
            if count < len(i['type']):
                tenant_str += ', '
                count += 1
            tenant_str += ' location. '
    except KeyError:
        st.write()

    try:
        tenant_str += f"The best place to park to go to {i['name'].strip()} is in the {i['best_parking']['name']} "
        if i['best_parking']['name'] in ['East', 'West']:
            tenant_str += 'ramp. '
        else:
            tenant_str += 'lot. '
    except KeyError:
        st.write()

    try:
        tenant_str += f"{i['name'].strip()} is a good place to go if you are looking for any of the following: {i['keywords']}. "
    except KeyError:
        st.write()

    try: 
        day_id = []
        day = []
        open = []
        close = []
        
        test_str = f"The regular hours for {i['name']} are: "
        for j in i['hours']['regular']:
            day_id.append(j['day_id'])
            day.append(j['day'])
            if j['status']['name'] == 'Closed':
                open.append('Closed')
                close.append('Closed')
            else:
                open.append(j['open'])
                close.append(j['close'])
        
        df = pd.DataFrame({'DayID' : day_id, 'Day' : day, 'Open' : open, 'Close' : close}).sort_values('DayID')
        
        count = 1
        for k in df.values:
            test_str += f"{k[1]}: "
            if k[2] == 'Closed':
                test_str += 'Closed'
            else: 
                test_str += f'{k[2]} - {k[3]}'
            if count < len(df):
                test_str += ', '
            count += 1
        test_str += f'. However, sometimes the upcoming hours can be a little bit different than the regular hours for a variety of reasons (events, holidays, etc.). The upcoming hours this next week for {i["name"].strip()} are: '
        
        day_id = []
        day = []
        open = []
        close = []
        date = []
        
        for j in i['hours']['upcoming']:
            day_id.append(j['day_id'])
            day.append(j['day'])
            if j['status']['name'] == 'Closed':
                open.append('Closed')
                close.append('Closed')
            else:
                open.append(j['open'])
                close.append(j['close'])
            date.append(j['date'])
        
        df2 = pd.DataFrame({'DayID' : day_id, 'Day' : day, 'Open' : open, 'Close' : close, 'Date' : date}).sort_values('Date')
        
        count = 1
        for k in df2.values:
            if count == 1:
                test_str += f'Today ({k[1]}, {k[4]}): '
                if k[2] == 'Closed':
                    test_str += 'Closed'
                else: 
                    test_str += f'{k[2]} - {k[3]}'
            elif count == 2:
                test_str += f"Tomorrow ({k[1]}, {k[4]}): "
                if k[2] == 'Closed':
                    test_str += 'Closed'
                else: 
                    test_str += f'{k[2]} - {k[3]}'
            else:
                test_str += f"{k[1]} ({k[4]}): "
                if k[2] == 'Closed':
                    test_str += 'Closed'
                else: 
                    test_str += f'{k[2]} - {k[3]}'
            if count < len(df2):
                test_str += ', '
            count += 1
        test_str += '. '

        tenant_str += test_str
    except KeyError:
        st.write()

    try:
        tenant_str += f"If you would like to call {i['name'].strip()}, their phone number is: {i['phone'].replace('.', '-')}"
    except KeyError:
        st.write()
        
    st.write(tenant_str)

