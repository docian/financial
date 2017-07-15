'''
Created on Jun 22, 2017

@author: docian
'''
import urllib2
import ast
# import matplotlib.pyplot as py
import numpy as np
import time
# import matplotlib.dates as mdates
import pandas as pd


if __name__ == '__main__':
    year_s = int(raw_input('din anul:'))
    year_e = int(raw_input('in anul:'))
    din_luna = int(raw_input('din_luna:'))
    din_ziua = int(raw_input('din ziua:'))
    la_luna = int(raw_input('pana in luna:'))
    la_ziua = int(raw_input('pana in ziua:'))
    fund = raw_input('nume fond:')
    start = (year_s,din_luna,din_ziua,3,0,0,0,0,-1)
    end = (year_e,la_luna,la_ziua,3,0,0,0,0,-1)
    start = int(time.mktime(start))*1000
    end = int(time.mktime(end))*1000
    print ('start:%s - end:%s'%(start,end))
#     u = 'https://www.nndirect.ro/clients/firstpagegraph?bl=1&timeFrame=ld&currency=lei&dateRangeFrom=1492586000000&dateRangeTo=1498078800000'
    u = 'https://www.nndirect.ro/clients/firstpagegraph?bl=1&timeFrame=ld&currency=lei&dateRangeFrom='+str(start)+'&dateRangeTo='+str(end)
    header = {}
    header['Content-Type'] = 'application/json'
    header['User-Agent']  = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    req = urllib2.Request(url = u, headers = header)
    resp = urllib2.urlopen(req)
    s = resp.read()
    print s
    s = s.split(':')
    s = s[1].split(';')
    for it in s:
        line = it.split('=')
        var = line[0].lstrip('"')
        if var == 'var line_5':
            values = line[1]
            values = values[3:][:-2]
            print values
            points = values.split('],[')
            t = []
            point_values = []
            no_points = 0
            for p in points:
                 t.append(time.strftime('%Y-%m-%d',time.gmtime(int(p.split(',')[0])/1000)))
                 point_values.append(p.split(',')[1])
                 no_points+=1
            print ('numarul de puncte:%d' %no_points)
#             ts = mdates.datestr2num(t)
#             py.figure(figsize = (10,6), facecolor = 'grey', edgecolor = 'green')
#             py.plot_date(t,point_values,'-')
#             py.xlabel('Data')
#             py.ylabel('Valoare')
#             py.show()
    pass
