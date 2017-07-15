'''
Created on Jul 10, 2017

@author: dan
'''
import urllib2 
import time 
import json 
import csv 
import pandas 
from pandas import DataFrame 

class BloombergDataMinning(object): 
    ''' 
    classdocs 
    ''' 


    def __init__(self, symbol = 'INGDXCH%3ALX'): 
        ''' 
        Constructor 
        ''' 
        self.url = 'https://www.bloomberg.com/markets/api/bulk-time-series/price/{s}?timeFrame=1_YEAR'.format(s = symbol) 
        self.symbol = symbol.split('%')[0] 
     
    def set_symbol(self,symbol):
        self.url = 'https://www.bloomberg.com/markets/api/bulk-time-series/price/{s}?timeFrame=1_YEAR'.format(s = symbol+'%3ALX') 
        self.symbol = symbol.split('%')[0]         
     
    def append_data_to_file(self): 
        req = urllib2.Request(self.url) 
        resp = urllib2.urlopen(req) 
        fjson = json.loads(resp.read()) 
        print fjson[0]['price'] 
#         fjson = json.loads(fjson[0]['price']) 
        fjson =  fjson[0]['price'] 
        fname =  self.symbol+'.csv' 
        with open(self.symbol+'.csv','a+')  as csv_file: 
            csv_writer = csv.writer(csv_file) 
            csv_writer.writerow(['date','value']) 
            for it in fjson: 
                csv_writer.writerow([it['date'],it['value']]) 
        df = pandas.read_csv(fname)   
        df.drop_duplicates(inplace = True, subset = 'date', keep = 'first') 
        df = df[df['date'] != 'date']
        df.to_csv(fname, index = False) 
        return df   

if __name__ == '__main__': 
    bdm = BloombergDataMinning()
    df = bdm.append_data_to_file()
    print  df
    bdm.set_symbol('INGROME')
    bdm.append_data_to_file()
    
    
       
       
         
       