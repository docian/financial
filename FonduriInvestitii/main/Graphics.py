'''
Created on Jun 28, 2017

@author: dan
'''
import matplotlib.pyplot as plt
from pandas import DataFrame
from mpldatacursor import datacursor
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter, DayLocator

class Graphics(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''

if  __name__=='__main__':
    df = DataFrame().from_csv('../data/var_line_5var-122.csv', sep= ',')
    print df  
    months = MonthLocator()
    days = DayLocator()  
    datefmt = DateFormatter('%y-%m-%d')
    plt.plot_date(df.time, df.variation,fmt = '-')
    ax =  plt.subplot()
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(datefmt)
    ax.xaxis.set_minor_locator(days)
    ax.autoscale_view()
    plt.grid(True)
    plt.show()
    pass   