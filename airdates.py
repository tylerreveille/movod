# -*- coding: utf-8 -*-

import datetime
import calendar

def date_finder(year, month):
    def allsaturdays(year):
       d = datetime.date(year, 1, 4)
       d += datetime.timedelta(days = 5 - d.weekday())
       while d.year == year:
          yield d
          d += datetime.timedelta(days = 7)
    ##vars: sched_mon_chosen, sched_yr_chosen, should be global in other script..
    #year_ = int(sched_yr_chosen.get())
    #mon_ = sched_mon_chosen.get()
    datelist = []
    for d in allsaturdays(year):
        datelist.append(d)
    
    year_ = year
    mon_  = month
    dates = []
    if mon_ == 'January':
        for fecha in datelist:
            if fecha.month == 1:
                dates.append(fecha)
                
    elif mon_ == 'February':
        for fecha in datelist:
            if fecha.month == 2:
                dates.append(fecha)
                
    elif mon_ == 'March':
        for fecha in datelist:
            if fecha.month == 3:
                dates.append(fecha)
                
    elif mon_ == 'April':
        for fecha in datelist:
            if fecha.month == 4:
                dates.append(fecha)
                
    elif mon_ == 'May':
        for fecha in datelist:
            if fecha.month == 5:
                dates.append(fecha)
                
    elif mon_ == 'June':
        for fecha in datelist:
            if fecha.month == 6:
                dates.append(fecha)
                
    elif mon_ == 'July':
        for fecha in datelist:
            if fecha.month == 7:
                dates.append(fecha)
                
    elif mon_ == 'August':
        for fecha in datelist:
            if fecha.month == 8:
                dates.append(fecha)
                
    elif mon_ == 'September':
        for fecha in datelist:
            if fecha.month == 9:
                dates.append(fecha)
                
    elif mon_ == 'October':
        for fecha in datelist:
            if fecha.month == 10:
                dates.append(fecha)
                
    elif mon_ == 'November':
        for fecha in datelist:
            if fecha.month == 11:
                dates.append(fecha)
                
    elif mon_ == 'December':
        for fecha in datelist:
            if fecha.month == 12:
                dates.append(fecha)

    return dates



#eg = date_finder(2020, 'January')
#print(eg)
#print(type(eg[0]))
#print(type(eg))

def end_dates(airdates):
    ended = []
    first = list(airdates)
    for dato in first:
        mas = dato + datetime.timedelta(weeks=10)
        ended.append(mas)
        
    return ended


#end_dates(eg)
#test = end_dates(eg)
#print(test)