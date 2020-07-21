# -*- coding: utf-8 -*-
"""
Creates planners used in VOD services for ingest, metadata, and reporting.
This demo is for a Panamanian client
"""

import sqlite3
import pandas as pd
import os
from tkinter import filedialog

def panama_planner(schedule):
    conn = sqlite3.connect('testdb.db')
    c = conn.cursor()
    c.execute("SELECT asset1, asset2, asset3, asset4, asset5, asset6 FROM panama_schedules WHERE name=?", (schedule,))
    scheduled_ids = c.fetchall()
    ###execute select statements for all values, loop through to create entire dataframe then export it
    idlist = []
    for id_ in scheduled_ids:
        for var in id_:
            idlist.append(var)
    
    #print('ID list: {}'.format(idlist))
    #print('\n')
    
    def get_title(sched_id):
        c.execute('SELECT title FROM movieinfo WHERE asset_id=?', (sched_id,))
        eng_title = c.fetchone()
        eng_title = eng_title[0]
        return eng_title
    
    
    def get_span_title(sched_id):
        c.execute('SELECT spanish_vod_title FROM epginfo WHERE asset_id=?', (sched_id,))
        span_title = c.fetchone()
        span_title = span_title[0]
        return span_title
    
    
    def get_genre(sched_name):
        c.execute("""SELECT category1_1, category2_1, category1_2, category2_2, 
                  category1_3, category2_3, category1_4, category2_4,
                  category1_5, category2_5, category1_6, category2_6
                  FROM panama_schedules WHERE name=?""", (sched_name,))
        cats = c.fetchall()
        categories = cats[0]
        ##cat_1 = categories[0]
        ##cat_2 = categories[1]
        ##categories = str(cat_1 + ', ' + cat_2)
        #### REMEMBER THIS RETURNS A TUPLE
        return categories
    
    
    def get_brand(sched_id):
        c.execute('SELECT brand FROM panama_schedules')
        brand = c.fetchone()
        brand = brand[0]
        return brand
    
    
    def get_synopsis(sched_id):
        c.execute('SELECT english_synopsis FROM epginfo WHERE asset_id=?', (sched_id,))
        syn = c.fetchone()
        syn = syn[0]
        return syn
        
    
    def get_span_synopsis(sched_id):
        c.execute('SELECT spanish_synopsis FROM epginfo WHERE asset_id=?', (sched_id,))
        spansyn = c.fetchone()
        spansyn = spansyn[0]
        return spansyn
        
    
    def get_studio(sched_id):
        c.execute('SELECT studio FROM movieinfo WHERE asset_id=?', (sched_id,))
        stud = c.fetchone()
        studio = stud[0]
        return studio
    
    
    def get_actors(sched_id):
        c.execute('SELECT actors FROM movieinfo WHERE asset_id=?', (sched_id,))
        actores = c.fetchone()
        actors = actores[0]
        return actors
        
    
    
    def get_lic_dates(sched_name):
        c.execute("""SELECT lic_start_1, lic_end_1, lic_start_2, lic_end_2, lic_start_3,
                  lic_end_3, lic_start_4, lic_end_4, lic_start_5, lic_end_5, lic_start_6,lic_end_6 
                  FROM panama_schedules WHERE name=?    
                  """, (sched_name,))
        lic_dates = c.fetchall()
        return lic_dates
        
    
    ex = idlist[0]
    ex2 = idlist[1]
    ex3 = idlist[2]
    ex4 = idlist[3]
    ex5 = idlist[4]
    ex6 = idlist[5]
    sched =  'Sample_Panama_January_2020'
    values1 = [ex, get_title(ex), get_span_title(ex), get_genre(sched)[0], get_genre(sched)[1], get_brand(ex),
               get_synopsis(ex), get_span_synopsis(ex), get_actors(ex),
              ##second bracket values change based on asset:
              get_lic_dates(sched)[0][0],get_lic_dates(sched)[0][1]
            ]
    
    values2 = [ex2, get_title(ex2), get_span_title(ex2), get_genre(sched)[2], get_genre(sched)[3], get_brand(ex2),
              get_synopsis(ex2), get_span_synopsis(ex2), get_actors(ex2),
              get_lic_dates(sched)[0][2], get_lic_dates(sched)[0][3]]
    
    values3 = [ex3, get_title(ex3), get_span_title(ex3), get_genre(sched)[4], get_genre(sched)[5], get_brand(ex3),
               get_synopsis(ex3), get_span_synopsis(ex3), get_actors(ex3),
              ##second bracket values change based on asset:
              get_lic_dates(sched)[0][4],get_lic_dates(sched)[0][5]
            ]
    
    values4 = [ex4, get_title(ex4), get_span_title(ex4), get_genre(sched)[6], get_genre(sched)[7], get_brand(ex4),
               get_synopsis(ex4), get_span_synopsis(ex4), get_actors(ex4),
              ##second bracket values change based on asset:
              get_lic_dates(sched)[0][6],get_lic_dates(sched)[0][7]
            ]
    
    values5 = [ex5, get_title(ex5), get_span_title(ex5), get_genre(sched)[8], get_genre(sched)[9], get_brand(ex5),
               get_synopsis(ex5), get_span_synopsis(ex5), get_actors(ex5),
              ##second bracket values change based on asset:
              get_lic_dates(sched)[0][8],get_lic_dates(sched)[0][9]
            ]
    
    values5 = [ex6, get_title(ex6), get_span_title(ex6), get_genre(sched)[8], get_genre(sched)[9], get_brand(ex6),
               get_synopsis(ex6), get_span_synopsis(ex6), get_actors(ex5),
              ##second bracket values change based on asset:
              get_lic_dates(sched)[0][10],get_lic_dates(sched)[0][11]
            ]
    
    
    all_values = [values1, values2, values3, values4, values5]
    #print('\n')
    #print(all_values)
    #print(len(all_values))
    #### Fix this code below to make this function more pythonic:
    #def get_values(sched_id, sched_name):
        ## returns a list
        #ex = sched_id
        #values = [ex, get_title(ex), get_span_title(ex), get_genre(ex), get_brand(ex), get_synopsis(ex),
        #      get_span_synopsis(ex), get_actors(ex), get_lic_dates(ex)[0], get_lic_dates(ex)[1]]
        #return values
    
    #####
    cols = ['ID', 'TITLE','Spanish Title', 'Genre', 'Genre', 'Brand', 'SYNOPSIS', 'Spanish Synopsis',
            'ACTORS', 'License Start' , 'License End']
    
    #all_values  = []
    ## a list of lists for the pandas DF created below, shoudl work well in a for loop
    #a = 0
    #for mov in idlist:
    #    hdid = idlist[a]
    #    values = get_values(hdid)
    #    all_values.append(values)
    #    a += 1
    
    #print(all_values)
    
    ###### Create the DataFrame:
    ####just need the May 20 and formatting...
    mtp_df = pd.DataFrame(all_values, columns=cols)
    #print(mtp_df)
    mtp_df = mtp_df.set_index('ID', drop=True)
    #print(mtp_df)
    mtp_df.to_csv('mtp.csv')
    
    ### import the csv, add it to the top df + columns in one row
    top_ = ['May 2020', '','','','','','','','','']
    top = pd.DataFrame([top_])
    #print(top)
    ##
    mtp_data = pd.read_csv('mtp.csv', header=None)
    #print(mtp_data)
    ##
    new_df = top.append(mtp_data)
    new_df = new_df.set_index(0, drop=True)
    new_df = new_df.rename(columns={0:'', 1:'', 2:'', 3:'',4:'', 5:'',6:'', 7:'', 8:'', 9:'', 10:''})
    new_df = new_df[1:]
    #print(new_df)
    os.remove('mtp.csv')
    dirvar = filedialog.askdirectory(initialdir='/', title='')
    new_df.to_excel(dirvar + '\\' + str(sched) + '.xls')
    ## need to drop the top row (column index)
    conn.commit()
    conn.close()
    

#panama_planner('Sample_Panama_January_2020')