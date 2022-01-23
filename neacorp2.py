# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 16:46:49 2020

@author: bbongsup
"""
import requests
import cx_Oracle as ora
import sys
import numpy as np
import pandas as pd
import datetime as dt
import xml.etree.ElementTree as ET
from json.decoder import JSONDecodeError
    
class PublicData:
    conn = None
    def __init__(self):
        if PublicData.conn is None:
           PublicData.conn = self.conn2Oracle()
           if PublicData.conn is None:
               sys.exit()
    def __del__(self):
        pass
    def conn2Oracle(self):
        try:
            conn = ora.connect('crefin/moon6715!@localhost:1521/orcl')
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            if error.code == 1017:
                print('Please check your credentials.')
            else:
                print('Database connection error: %s'.format(e))
            return None
        else:
            return conn
    ##########################################################################################
    def getMaxBasDt(self, func_nm, start_date, end_date):
        sql1 = "SELECT NVL(MAX(BASDT),'{start_date}') FROM {tbl_nm} WHERE BASDT BETWEEN '{start_date}' AND '{end_date}'".format(tbl_nm=func_nm[3:], start_date=start_date, end_date=end_date)
        print(sql1)
        
        cur = PublicData.conn.cursor()
        cur.execute(sql1)
        max_bas_dt, = cur.fetchone()
        cur.close()
        return max_bas_dt
    ##########################################################################################
    def getMaxBizYear(self, func_nm, start_year, end_year):
        sql1 = "SELECT NVL(MAX(BIZYEAR),'{start_year}') FROM {tbl_nm} WHERE BIZYEAR BETWEEN '{start_year}' AND '{end_year}'".format(tbl_nm=func_nm[3:], start_year=start_year, end_year=end_year)
        print(sql1)
        
        cur = PublicData.conn.cursor()
        cur.execute(sql1)
        max_biz_year, = cur.fetchone()
        cur.close()
        return max_biz_year
    ##########################################################################################
    def getTotalRowsBasDt(self, func_nm, bas_dt):
        sql1 = "SELECT COUNT(*) AS TOT_ROWS FROM {tbl_nm} WHERE BASDT = :bas_dt".format(tbl_nm=func_nm[3:].upper())
        print(sql1)
        cur = PublicData.conn.cursor()
        cur.execute(sql1, bas_dt=bas_dt)
        tot_rows, = cur.fetchone()
        cur.close()
      
        return tot_rows
    ##########################################################################################
    def getTotalRowsBizYear(self, func_nm, biz_year):
        sql1 = "SELECT COUNT(*) AS TOT_ROWS FROM {tbl_nm} WHERE BIZYEAR = :biz_year".format(tbl_nm=func_nm[3:].upper())
        print(sql1)
        cur = PublicData.conn.cursor()
        cur.execute(sql1, biz_year=biz_year)
        tot_rows, = cur.fetchone()
        cur.close()
      
        return tot_rows
    ##########################################################################################
    def deleteIncompleteRows(self, func_nm, bas_dt):
        sql1 = "DELETE FROM {tbl_nm} WHERE BASDT = :bas_dt".format(tbl_nm=func_nm[3:].upper())
        print(sql1)
        cur = PublicData.conn.cursor()
        cur.execute(sql1, bas_dt=bas_dt)
        PublicData.conn.commit()
        cur.close()
    ##########################################################################################    
    def insertNewRows(self, func_nm, tuple_list):
        bind_vars = ""
        for i in np.arange(1, len(tuple_list[0])+1):
            if i == 1:
                bind_vars = ":1"
            else:
                bind_vars += ", :%s" % i
        
        sql1 = "INSERT INTO {tbl_nm} VALUES ({bind_vars})".format(tbl_nm=func_nm[3:].upper(), bind_vars=bind_vars)
        
        cur = PublicData.conn.cursor()
        cur.executemany(sql1, tuple_list)
        PublicData.conn.commit()
        cur.close()
    ########################################################################################## 
    def changeItems2Tuples(self, json_data):
        item_list = json_data['response']['body']['items']['item']
        tuple_list = []
        for row in item_list:
           new_row = [] 
           for val in row.values():
               new_row.append(val)
           tuple_list.append(tuple(new_row))
        # print(tuple_list)
        return tuple_list
    ########################################################################################## 
    def saveOneBasDt(self, api_url, func_nm, service_key, bas_dt):
        
        tot_rows = self.getTotalRowsBasDt(func_nm, bas_dt)
        print('tot_rows = ', tot_rows)
        
        url_format = api_url + '/{func_nm}?serviceKey={service_key}&pageNo={page_no}&resultType={result_type}&numOfRows={num_rows}&basDt={bas_dt}'
        url = url_format.format(func_nm=func_nm, service_key=service_key, page_no='1', num_rows='40', result_type='json', bas_dt=bas_dt)
        print(url)
        response = requests.get(url)
        #print(response.text)
        
        try:
            response.json()
            result_code = response.json()['response']['header']['resultCode']
            result_msg = response.json()['response']['header']['resultMsg']
        except JSONDecodeError as e:
            xmlroot = ET.fromstring(response.text)
            result_code = xmlroot.findall("./cmmMsgHeader/returnReasonCode")[0].text
            result_msg = xmlroot.findall("./cmmMsgHeader/returnAuthMsg")[0].text
            return (result_code, result_msg)

        if result_code != '00':
            return (result_code, resut_msg)
        
        tot_cnt = response.json()['response']['body']['totalCount']
        print("Total Count(%s): %s" % (bas_dt, tot_cnt))
        
        if tot_rows == tot_cnt or tot_cnt == 0:
            result_msg = 'No need to call (bas_dt, tot_rows, tot_cnt) = ({}, {}, {})\n'.foramt(bas_dt, tot_rows, tot_cnt)
            return ('00', result_msg)
        elif tot_rows > 0: # tot_rows < tot_cnt
            next_page_no = tot_rows // 40 + 1
        else:
            self.insertNewRows(func_nm, self.changeItems2Tuples(response.json()))
            next_page_no = 2
    
        tot_page_no = tot_cnt // 40 + (1 if tot_cnt % 40 > 0 else 0)
        for page_no in np.arange(next_page_no, tot_page_no+1):
            url = url_format.format(func_nm=func_nm, service_key=service_key, page_no=page_no, num_rows='40', result_type='json', bas_dt=bas_dt)
            print(url)
            response = requests.get(url)
            
            try:
                response.json()
                result_code = response.json()['response']['header']['resultCode']
                result_msg = response.json()['response']['header']['resultMsg']
            except JSONDecodeError as e:
                xmlroot = ET.fromstring(response.text)
                result_code = xmlroot.findall("./cmmMsgHeader/returnReasonCode")[0].text
                result_msg = xmlroot.findall("./cmmMsgHeader/returnAuthMsg")[0].text

            if result_code != '00':
                return (result_code, result_msg)
            
            self.insertNewRows(func_nm, self.changeItems2Tuples(response.json()))
            
        return ('00', "success")
    ########################################################################################## 
    def saveOneBizYear(self, api_url, func_nm, service_key, biz_year):
        
        tot_rows = self.getTotalRowsBizYear(func_nm, biz_year)
        print('tot_rows = ', tot_rows)
        
        url_format = api_url + '/{func_nm}?serviceKey={service_key}&pageNo={page_no}&resultType={result_type}&numOfRows={num_rows}&bizYear={biz_year}'
        url = url_format.format(func_nm=func_nm, service_key=service_key, page_no='1', num_rows='40', result_type='json', biz_year=biz_year)
        print(url)
        response = requests.get(url)
        # print(response)
        try:
            response.json()
            result_code = response.json()['response']['header']['resultCode']
            result_msg = response.json()['response']['header']['resultMsg']
        except JSONDecodeError as e:
            xmlroot = fromstring(response.text)
            result_code = xmlroot.findall("./cmmMsgHeader/returnReasonCode")[0].text
            result_msg = xmlroot.findall("./cmmMsgHeader/returnAuthMsg")[0].text
            return (result_code, result_msg)

        if result_code != '00':
            return (result_code, result_msg)
        
        tot_cnt = response.json()['response']['body']['totalCount']
        print("Total Count(%s): %s" % (biz_year, tot_cnt))
        
        if tot_rows == tot_cnt or tot_cnt == 0:
            result_msg = 'No need to call (biz_year, tot_rows, tot_cnt) = ({}, {}, {})\n'.format(biz_year, tot_rows, tot_cnt)
            return ('00', result_msg)
        elif tot_rows > 0: # tot_rows < tot_cnt
            next_page_no = tot_rows // 40 + 1
        else:
            self.insertNewRows(func_nm, self.changeItems2Tuples(response.json()))
            next_page_no = 2
    
        tot_page_no = tot_cnt // 40 + (1 if tot_cnt % 40 > 0 else 0)
        for page_no in np.arange(next_page_no, tot_page_no+1):
            url = url_format.format(func_nm=func_nm, service_key=service_key, page_no=page_no, num_rows='40', result_type='json', biz_year=biz_year)
            print(url)
            response = requests.get(url)
            try:
                response.json()
                result_code = response.json()['response']['header']['resultCode']
                result_msg = response.json()['response']['header']['resultMsg']
            except JSONDecodeError as e:
                xmlroot = ET.fromstring(response.text)
                result_code = xmlroot.findall("./cmmMsgHeader/returnReasonCode")[0].text
                result_msg = xmlroot.findall("./cmmMsgHeader/returnAuthMsg")[0].text
            return (result_code, result_msg)

            if result_code != '00':
                return (result_code, result_msg)
            
            self.insertNewRows(func_nm, self.changeItems2Tuples(response.json()))
        return ('00', "success")
    ##########################################################################################
    def getCorpBasicInfoService(self, start_date, end_date):
        api_url = 'http://apis.data.go.kr/1160100/service/GetCorpBasicInfoService'
        service_key = 'OURvkwMPCLqp0qa4wJ4Q5%2B03sKV9utK35BXu59ZCta06BHB7lDXSoaNpsCGByd2nzfUl6AL0fK8bnSj%2Fk9f%2BIA%3D%3D'
        #func_list = ['getAffiliate', 'getConsSubsComp']
        func_list = ['getCorpOutline']
        
        
        for func_nm in func_list:
            max_start_dt = self.getMaxBasDt(func_nm, start_date, end_date)
            for bas_dt in pd.date_range(max_start_dt, end_date).strftime('%Y%m%d'):
                result_code, result_msg = self.saveOneBasDt(api_url, func_nm, service_key, bas_dt)
                if result_code != '00':
                    print(result_msg)
                    return;
                
    ##########################################################################################
    def getFinaStatInfoService(self, start_year, end_year):
        api_url = 'http://apis.data.go.kr/1160100/service/GetFinaStatInfoService'
        service_key = 'OURvkwMPCLqp0qa4wJ4Q5%2B03sKV9utK35BXu59ZCta06BHB7lDXSoaNpsCGByd2nzfUl6AL0fK8bnSj%2Fk9f%2BIA%3D%3D'
        func_list = ['getSummFinaStat', 'getBs', 'getIncoStat']
        
        for func_nm in func_list:
            max_start_year = self.getMaxBizYear(func_nm, start_year, end_year)
            for biz_year in range(int(max_start_year), int(end_year)):
                result_code, result_msg = self.saveOneBizYear(api_url, func_nm, service_key, str(biz_year))
                if result_code != '00':
                    print(result_msg)
                    return;
if __name__ == "__main__":
    
    pcls = PublicData()
    
    
    
    #print('we created a Public Class')
    
    pcls.getCorpBasicInfoService('20200901', '20201231')
    #pcls.getFinaStatInfoService('2010', '2021')

    
    # max_bas_dt = pcls.getMaxBasDt('getConsSubsComp', '20210101', '20211231')
    # tot_rows = pcls.getTotalRows('getAffiliate', '20190101')
    # pcls.deleteIncompleteRows('getAffiliate', '20190102')
    # tuple_list = [('20190102', '1101111230012', '', '', 'N'),
    #               ('20190102', '1101111230013', '', '', 'N'),
    #               ('20190102', '1101111230014', '', '', 'N'),
    #               ('20190102', '1101111230015', '', '', 'N'),
    #               ('20190102', '1101111230016', '', '', 'N'),
    #               ('20190102', '1101111230017', '', '', 'N'),
    #               ('20190102', '1101111230018', '', '', 'N'),
    #               ('20190102', '1101111230019', '', '', 'N'),
    #               ('20190102', '1101111230020', '', '', 'N')]

    # pcls.insertNewRows('getAffiliate', tuple_list) 
  
'''
    url =  'http://apis.data.go.kr/1160100/service/GetCorpBasicInfoService'
    url += '/getAffiliate'
    url += '?serviceKey=OURvkwMPCLqp0qa4wJ4Q5%2B03sKV9utK35BXu59ZCta06BHB7lDXSoaNpsCGByd2nzfUl6AL0fK8bnSj%2Fk9f%2BIA%3D%3D'
    url += '&resultType=json'
    url += '&pageNo=1'
    url += '&numOfRows=1'
    url += '&basDt=20200703'

    print('url = ', url)

    response = requests.get(url)
    print(response.headers)
    print(response.json())
    if response.json()['response']['header'] == None:
        print("json is None")
    result_code = response.json()['response']['header']['resultCode']
    result_msg = response.json()['response']['header']['resultMsg']
'''

    # tt = pcls.changeItems2Tuples(response.json())
    # print(tt)
    # pcls.insertNewRows('getAffiliate', tt)
    
    # api_url = 'http://apis.data.go.kr/1160100/service/GetCorpBasicInfoService'
    # func_nm = 'getCorpOutline'
    # service_key = 'OURvkwMPCLqp0qa4wJ4Q5%2B03sKV9utK35BXu59ZCta06BHB7lDXSoaNpsCGByd2nzfUl6AL0fK8bnSj%2Fk9f%2BIA%3D%3D'
    # bas_dt = '20200703'
    
    # pcls.saveOneBasDt(api_url, func_nm, service_key, bas_dt)
    
    # pcls.getFinaStatInfoService('2010', '2021')

                
        
        
        
        

