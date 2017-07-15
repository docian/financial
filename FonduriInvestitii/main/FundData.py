'''
Created on Jun 24, 2017

@author: dan
'''
import time
import urllib2
import pandas as pd
from pandas import DataFrame

class FundData(object):
    '''
    classdocs
    '''


    def __init__(self, year_s= None, din_luna = None, din_ziua = None,\
                  year_e = None,la_luna = None, la_ziua = None, fund = None ):
        '''
        Constructor
        '''
        if (year_s == None)|(year_e == None)|(din_luna == None)|(din_ziua == None)\
            |(la_luna == None)|(la_ziua == None)|(fund == None):
            year_s = int(raw_input('din anul:'))
            year_e = int(raw_input('in anul:'))
            din_luna = int(raw_input('din_luna:'))
            din_ziua = int(raw_input('din ziua:'))
            la_luna = int(raw_input('pana in luna:'))
            la_ziua = int(raw_input('pana in ziua:'))
            fund = raw_input('nume fond:')
        start = (year_s,din_luna,din_ziua,5,0,0,0,0,0)
        end = (year_e,la_luna,la_ziua,5,0,0,0,0,0)
        self.start = int(time.mktime(start))*1000
        self.end = int(time.mktime(end))*1000
        self.fund = fund
        print ('start:%s - end:%s'%(self.start,self.end))
    
    def fetch_data(self):
        u = 'https://www.nndirect.ro/clients/firstpagegraph?bl=1&timeFrame=ld&currency=lei&dateRangeFrom='\
            +str(self.start)+'&dateRangeTo='+str(self.end)
        header = {}
        header['Content-Type'] = 'application/json'
        header['User-Agent']  = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        req = urllib2.Request(url = u, headers = header)
        resp = urllib2.urlopen(req)
        s = resp.read()
        print s
        s = s.split(':')
        s = s[1].split(';')
        self.data = s[0].split('=')[1][3:-3].split('],[')
        for it in s:
            line = it.split('=')
            var = line[0].lstrip('"')
            if var == self.fund:
                values = line[1]
                values = values[3:][:-2]
                print values
                self.points = values.split('],[')
                self.t = []
                self.point_values = []
                self.no_points = 0
                for p in self.points:
                     self.t.append(time.strftime('%Y-%m-%d',time.gmtime(int(p.split(',')[0])/1000)))
                     self.point_values.append(p.split(',')[1])
                     self.no_points+=1
        self._create_dataframe()
                     
    def _create_dataframe(self):
        self.data = [it.split(',') for it in self.points]
        self.df = DataFrame(data = self.data, columns = ['time','value'])
        self.df.to_csv('../data/'+self.fund.replace(' ','_')+'-'+str(self.no_points)+'.csv', ',')
        pass    
        
if __name__ == '__main__':
    fd = FundData(2017,1,1,2017,6,29,'var line_5')
    fd.fetch_data()
    daily_var = [[fd.df.iloc[k+1].time,\
                  (float(fd.df.iloc[k+1].value) - float(fd.df.iloc[k].value))*100/float(fd.df.iloc[k+1].value)]\
                  for k in range(0,len(fd.df)-1)]
    daily_var_df = DataFrame(data=daily_var, columns=['time','variation'])
    tmax =  daily_var_df.loc[daily_var_df['variation'].idxmax()][0]
    dvf = DataFrame(data=daily_var, columns=['time','variation'])
    dvf['time'] = dvf['time'].apply(lambda x: time.strftime('%Y-%m-%d',time.gmtime(float(x)/1000)))
    dvf.to_csv('../data/'+fd.fund.replace(' ','_')+'var-'+str(fd.no_points)+'.csv', ',')
    var_max = daily_var_df.loc[daily_var_df['variation'].idxmax()][1]
    dmax = time.strftime('%Y-%m-%d',time.gmtime(float(tmax)/1000))
    tmin = daily_var_df.loc[daily_var_df['variation'].idxmin()][0]
    var_min = daily_var_df.loc[daily_var_df['variation'].idxmin()][1]
    dmin = time.strftime('%Y-%m-%d',time.gmtime(float(tmin)/1000))
    start_day = time.strftime('%Y-%m-%d',time.gmtime(float(fd.start)/1000)) 
    end_day = time.strftime('%Y-%m-%d',time.gmtime(float(fd.end)/1000))                        
    print('\tintervalul:%s --- %s'%(start_day, end_day))
    print('max. variation:'+str(var_max)+' at date:'+dmax)
    print('min. variation:'+str(var_min)+' at date:'+dmin)    
    avrg_pos_var = daily_var_df.loc[daily_var_df['variation'] > 0].mean()
    avrg_neg_var = daily_var_df.loc[daily_var_df['variation'] < 0].mean()
    print('average positive :%f and negative:%f variation '%(avrg_pos_var['variation'],avrg_neg_var['variation']))

    print '---'
    two_days_var =[[daily_var[k+1][0],daily_var[k+1][1]+daily_var[k][1]] for k in range(0, len(daily_var)-2)]
    two_days_var_df = DataFrame(data=two_days_var, columns=['time','variation'])
    tmax =  two_days_var_df.loc[two_days_var_df['variation'].idxmax()][0]
    var_max = two_days_var_df.loc[two_days_var_df['variation'].idxmax()][1]
    dmax = time.strftime('%Y-%m-%d',time.gmtime(float(tmax)/1000))
    tmin = two_days_var_df.loc[two_days_var_df['variation'].idxmin()][0]
    var_min = two_days_var_df.loc[two_days_var_df['variation'].idxmin()][1]
    dmin = time.strftime('%Y-%m-%d',time.gmtime(float(tmin)/1000))  
    print('max. 2 days variation:'+str(var_max)+' at date:'+dmax)
    print('min. 2 days variation:'+str(var_min)+' at date:'+dmin)    
    avrg_pos_var = two_days_var_df.loc[two_days_var_df['variation'] > 0].mean()
    avrg_neg_var = two_days_var_df.loc[two_days_var_df['variation'] < 0].mean()
    print('2 days average positive :%f and negative:%f variation '%(avrg_pos_var['variation'],avrg_neg_var['variation']))
   
    print '---'
    three_days_var =[[daily_var[k+2][0],daily_var[k+2][1]+daily_var[k+1][1]+daily_var[k][1]] for k in range(0, len(daily_var)-3)]
    three_days_var_df = DataFrame(data=three_days_var, columns=['time','variation'])
    tmax =  three_days_var_df.loc[three_days_var_df['variation'].idxmax()][0]
    var_max = three_days_var_df.loc[three_days_var_df['variation'].idxmax()][1]
    dmax = time.strftime('%Y-%m-%d',time.gmtime(float(tmax)/1000))
    tmin = three_days_var_df.loc[three_days_var_df['variation'].idxmin()][0]
    var_min = three_days_var_df.loc[three_days_var_df['variation'].idxmin()][1]
    dmin = time.strftime('%Y-%m-%d',time.gmtime(float(tmin)/1000))  
    print('max. 3 days variation:'+str(var_max)+' at date:'+dmax)
    print('min. 3 days variation:'+str(var_min)+' at date:'+dmin)    
    avrg_pos_var = three_days_var_df.loc[three_days_var_df['variation'] > 0].mean()
    avrg_neg_var = three_days_var_df.loc[three_days_var_df['variation'] < 0].mean()
    print('3 days average positive :%f and negative:%f variation '%(avrg_pos_var['variation'],avrg_neg_var['variation']))
 
    print '---'
    four_days_var =[[daily_var[k+3][0],daily_var[k+3][1]+daily_var[k+2][1]+daily_var[k+1][1]+ daily_var[k][1]]\
                     for k in range(0, len(daily_var)-4)]
    four_days_var_df = DataFrame(data=four_days_var, columns=['time','variation'])
    tmax =  four_days_var_df.loc[four_days_var_df['variation'].idxmax()][0]
    var_max = four_days_var_df.loc[four_days_var_df['variation'].idxmax()][1]
    dmax = time.strftime('%Y-%m-%d',time.gmtime(float(tmax)/1000))
    tmin = four_days_var_df.loc[four_days_var_df['variation'].idxmin()][0]
    var_min = four_days_var_df.loc[four_days_var_df['variation'].idxmin()][1]
    dmin = time.strftime('%Y-%m-%d',time.gmtime(float(tmin)/1000))  
    print('max. 4 days variation:'+str(var_max)+' at date:'+dmax)
    print('min. 4 days variation:'+str(var_min)+' at date:'+dmin)    
    avrg_pos_var = four_days_var_df.loc[four_days_var_df['variation'] > 0].mean()
    avrg_neg_var = four_days_var_df.loc[four_days_var_df['variation'] < 0].mean()
    print('4 days average positive :%f and negative:%f variation '%(avrg_pos_var['variation'],avrg_neg_var['variation']))

    print '---'
    five_days_var =[[daily_var[k+4][0],daily_var[k+4][1]+daily_var[k+3][1]+daily_var[k+2][1]+ daily_var[k+1][1]+daily_var[k][1]]\
                     for k in range(0, len(daily_var)-5)]
    five_days_var_df = DataFrame(data=five_days_var, columns=['time','variation'])
    tmax =  five_days_var_df.loc[five_days_var_df['variation'].idxmax()][0]
    var_max = five_days_var_df.loc[five_days_var_df['variation'].idxmax()][1]
    dmax = time.strftime('%Y-%m-%d',time.gmtime(float(tmax)/1000))
    tmin = five_days_var_df.loc[five_days_var_df['variation'].idxmin()][0]
    var_min = five_days_var_df.loc[five_days_var_df['variation'].idxmin()][1]
    dmin = time.strftime('%Y-%m-%d',time.gmtime(float(tmin)/1000))  
    print('max. 5 days variation:'+str(var_max)+' at date:'+dmax)
    print('min. 5 days variation:'+str(var_min)+' at date:'+dmin)    
    avrg_pos_var = five_days_var_df.loc[five_days_var_df['variation'] > 0].mean()
    avrg_neg_var = five_days_var_df.loc[five_days_var_df['variation'] < 0].mean()
    print('5 days average positive :%f and negative:%f variation '%(avrg_pos_var['variation'],avrg_neg_var['variation']))

    print('--- last days variation ---')
    last_day = (float(fd.df.iloc[-1].value)-float(fd.df.iloc[-2].value))*100/float(fd.df.iloc[-1].value)
    last_two_days = last_day + (float(fd.df.iloc[-2].value)-float(fd.df.iloc[-3].value))*100/float(fd.df.iloc[-2].value)
    last_three_days = last_two_days +(float(fd.df.iloc[-3].value)-float(fd.df.iloc[-4].value))*100/float(fd.df.iloc[-3].value)
    last_four_days = last_three_days+(float(fd.df.iloc[-4].value)-float(fd.df.iloc[-5].value))*100/float(fd.df.iloc[-4].value)
    print('last day:%4.2f%% - last_two_days:%4.2f%% - last three days:%4.2f%% - last four days:%4.2f%%'\
           %(last_day,last_two_days,last_three_days,last_four_days))
#     print('max->%f time->%f')%(float(daily_var_df.loc(daily_var_df['variation'].idxmax())),\
#                                float(daily_var_df['variation'].idxmax()[0]))
#     print daily_var_df 
    
    
    
    