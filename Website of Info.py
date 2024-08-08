# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 15:40:50 2024

@author: COrtloff
"""
import streamlit as st
import json
import requests
import pandas as pd

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
    
    

