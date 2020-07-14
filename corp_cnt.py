# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 18:22:36 2020

@author: bbongsup
"""

import urllib.request

#url =  http://apis.data.go.kr/B553077/api/open/sdsc/storeZoneInRadius?radius=500&cx=127.004528&cy=37.567538&ServiceKey=[서비스키]&type=json 

# serviceKey = 'OURvkwMPCLqp0qa4wJ4Q5%2B03sKV9utK35BXu59ZCta06BHB7lDXSoaNpsCGByd2nzfUl6AL0fK8bnSj%2Fk9f%2BIA%3D%3D'

# url = http://apis.data.go.kr/1160100/service/GetCorpBasicInfoService/getCorpOutline?serviceKey=
# response = urllib.request.urlopen(url) json_str = response.read().decode("utf-8")

import requests
import cx_Oracle as ora
import pandas as pd

api_url1 = 'http://apis.data.go.kr/1160100/service/GetCorpBasicInfoService'
api_url2 = 'http://apis.data.go.kr/1160100/service/GetFinaStatInfoService'
service_key = 'OURvkwMPCLqp0qa4wJ4Q5%2B03sKV9utK35BXu59ZCta06BHB7lDXSoaNpsCGByd2nzfUl6AL0fK8bnSj%2Fk9f%2BIA%3D%3D'

page_no = 1
num_of_rows = 1

func_list1 = ['getCorpOutline', 'getAffiliate', 'getConsSubsComp']
func_list2 = ['getSummFinaStat', 'getBs', 'getIncoStat']

conn = ora.connect('crefin/crefin@localhost:1521/orcl')
cur = conn.cursor()

for func_nm1 in func_list1:
    for bas_dt in pd.date_range('20021128', '20200713').strftime('%Y%m%d'):
        sql1 = "INSERT INTO TOT_CNT_BAS_DT VALUES (:tbl_nm, :bas_dt, :tot_cnt)"
        url_format = '{api_url}/{func_nm}?serviceKey={service_key}&pageNo={page_no}&resultType={result_type}&numOfRows={num_of_rows}&basDt={bas_dt}'
        url = url_format.format(api_url=api_url1, func_nm=func_nm1, service_key=service_key, page_no='1', num_of_rows='10', result_type='json', bas_dt=bas_dt)
        print(url)
        response = requests.get(url)
        print(response.text)
        if response.status_code == 200 and response.text is not None:
            result_code = response.json()['response']['header']['resultCode']
            result_msg = response.json()['response']['header']['resultMsg']
            tot_cnt = response.json()['response']['body']['totalCount']
            print('func_nm, bas_dt, tot_cnt) = (%s, %s, %d)\n' % (func_nm1, bas_dt, tot_cnt))
            data = {"tbl_nm": func_nm1[3:].upper(), "bas_dt": bas_dt, "tot_cnt":tot_cnt }
            cur.execute(sql1, data)
            conn.commit()

for func_nm2 in func_list2:
    for biz_year in range(2020, 2021):
        sql1 = "INSERT INTO TOT_CNT_BIZ_YEAR VALUES (:tbl_nm, :biz_year, :tot_cnt)"
        url_format = '{api_url}/{func_nm}?serviceKey={service_key}&pageNo={page_no}&resultType={result_type}&numOfRows={num_of_rows}&bizYear={biz_year}'
        url = url_format.format(api_url=api_url2, func_nm=func_nm2, service_key=service_key, page_no='1', num_of_rows='10', result_type='json', biz_year=biz_year)
        print(url)
        response = requests.get(url)
        print(response.text)
        if response.status_code == 200 and response.text is not None:
            result_code = response.json()['response']['header']['resultCode']
            result_msg = response.json()['response']['header']['resultMsg']
            tot_cnt = response.json()['response']['body']['totalCount']
            print('func_nm, biz_year, tot_cnt) = (%s, %s, %d)\n' % (func_nm2, str(biz_year), tot_cnt))
            data = {"tbl_nm": func_nm2[3:].upper(), "biz_year": str(biz_year), "tot_cnt":tot_cnt }
            cur.execute(sql1, data)
            conn.commit()
            
cur.close()
conn.close()
