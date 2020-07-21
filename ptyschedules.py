# -*- coding: utf-8 -*-
"""
Test the C&W Panama Schedule module in its own place, them import them individually?
Try to use the Panama_sched class and create a unique sqlite3 table...
"""
from airdates import date_finder, end_dates
from tkinter import *
import datetime
import sqlite3

def holdon():
    return

rightnow = datetime.datetime.now()

conn = sqlite3.connect('testdb.db')
c = conn.cursor()

### Fix this code later, classes may be smarter ways to create schedules:
class Panamasched:
    
    def __init__(self, master, chan_chosen, sched_mon_chosen, sched_yr_chosen):
        self.chan_chosen = chan_chosen
        self.sched_mon_chosen = sched_mon_chosen
        self.sched_yr_chosen = sched_yr_chosen
        self.enter_btn = Button(master, text='Create Schedule / Enter Data (first time)', command=self.enter_schedule_data).grid(row=1, column=0)
        self.load_btn = Button(master, text='Load Schedule', command=self.load_sched).grid(row=1, column=1)
        self.update_btn = Button(master, text='Update Schedule',  command=self.update_schedule).grid(row=1, column=2)
        self.clr_btn = Button(master, text='Clear Data/Cancel', command=self.clean_screen).grid(row=1, column=3)
        ##Add column labels and entry boxes, dropdowns, buttons, you name it    
        self.asset_ids_lbl = Label(master, text="Asset ID:")
        self.asset_ids_lbl.grid(row=2, column=0)
        self.asset_id1 = Entry(master, width=30)
        self.asset_id1.grid(row=3, column=0)
        self.asset_id2 = Entry(master, width=30)
        self.asset_id2.grid(row=4, column=0)
        self.asset_id3 = Entry(master, width=30)
        self.asset_id3.grid(row=5, column=0)
        self.asset_id4 = Entry(master, width=30)
        self.asset_id4.grid(row=6, column=0)
        self.asset_id5 = Entry(master, width=30)
        self.asset_id5.grid(row=7, column=0)
        self.asset_id6 = Entry(master, width=30)
        self.asset_id6.grid(row=8, column=0)
        self.brand_lbl = Label(master, text='Choose Brand')
        self.brand_lbl.grid(row=2, column=1)
        self.brand_opts = ['REVVOD']
        self.brand = StringVar()
        self.brand.set('Choose')
        self.brand_1  = OptionMenu(master, self.brand, *self.brand_opts)
        self.brand_1.grid(row=3, column=1)
        self.brand_2 = OptionMenu(master, self.brand, *self.brand_opts)
        self.brand_2.grid(row=4, column=1)
        self.brand_3  = OptionMenu(master, self.brand, *self.brand_opts)
        self.brand_3.grid(row=5, column=1)
        self.brand_4  = OptionMenu(master, self.brand, *self.brand_opts)
        self.brand_4.grid(row=6, column=1)
        self.brand_5  = OptionMenu(master, self.brand, *self.brand_opts)
        self.brand_5.grid(row=7, column=1)
        self.brand_6  = OptionMenu(master, self.brand, *self.brand_opts)
        self.brand_6.grid(row=8, column=1)
        ##category 1
        self.cat1_lbl = Label(master, text='Category 1')
        self.cat1_lbl.grid(row=2, column=2)
        self.cat_opts = ['Accion', 'Diversion', 'Exotico', 'Extremo', 'Cultura']
        self.chosen_cat1_1 = StringVar()
        self.chosen_cat1_1.set('Select Category')
        self.cat1_1  = OptionMenu(master, self.chosen_cat1_1, *self.cat_opts)
        self.cat1_1.grid(row=3, column=2)
        self.chosen_cat1_2 = StringVar()
        self.chosen_cat1_2.set('Select Category')
        self.cat1_2 = OptionMenu(master, self.chosen_cat1_2, *self.cat_opts)
        self.cat1_2.grid(row=4, column=2)
        self.chosen_cat1_3 = StringVar()
        self.chosen_cat1_3.set('Select Category')
        self.cat1_3  = OptionMenu(master, self.chosen_cat1_3, *self.cat_opts)
        self.cat1_3.grid(row=5, column=2)
        self.chosen_cat1_4 = StringVar()
        self.chosen_cat1_4.set('Select Category')
        self.cat1_4  = OptionMenu(master, self.chosen_cat1_4, *self.cat_opts)
        self.cat1_4.grid(row=6, column=2)
        self.chosen_cat1_5 = StringVar()
        self.chosen_cat1_5.set('Select Category')
        self.cat1_5  = OptionMenu(master, self.chosen_cat1_5, *self.cat_opts)
        self.cat1_5.grid(row=7, column=2)
        self.chosen_cat1_6 = StringVar()
        self.chosen_cat1_6.set('Select Category')
        self.cat1_6  = OptionMenu(master, self.chosen_cat1_6, *self.cat_opts)
        self.cat1_6.grid(row=8, column=2)
        ##cat2
        self.cat2_lbl = Label(master, text='Category 2')
        self.cat2_lbl.grid(row=2, column=3)
        self.chosen_cat2_1 = StringVar()
        self.chosen_cat2_1.set('Select Category')
        self.cat2_1  = OptionMenu(master, self.chosen_cat2_1, *self.cat_opts)
        self.cat2_1.grid(row=3, column=3)
        self.chosen_cat2_2 = StringVar()
        self.chosen_cat2_2.set('Select Category')
        self.cat2_2 = OptionMenu(master, self.chosen_cat2_2, *self.cat_opts)
        self.cat2_2.grid(row=4, column=3)
        self.chosen_cat2_3 = StringVar()
        self.chosen_cat2_3.set('Select Category')
        self.cat2_3  = OptionMenu(master, self.chosen_cat2_3, *self.cat_opts)
        self.cat2_3.grid(row=5, column=3)
        self.chosen_cat2_4 = StringVar()
        self.chosen_cat2_4.set('Select Category')
        self.cat2_4  = OptionMenu(master, self.chosen_cat2_4, *self.cat_opts)
        self.cat2_4.grid(row=6, column=3)
        self.chosen_cat2_5 = StringVar()
        self.chosen_cat2_5.set('Select Category')
        self.cat2_5  = OptionMenu(master, self.chosen_cat2_5, *self.cat_opts)
        self.cat2_5.grid(row=7, column=3)
        self.chosen_cat2_6 = StringVar()
        self.chosen_cat2_6.set('Select Category')
        self.cat2_6  = OptionMenu(master, self.chosen_cat2_6, *self.cat_opts)
        self.cat2_6.grid(row=8, column=3)
        ###licstart - do something creative with the date chooser
        self.licstart_lbl = Label(master, text='License Start Date')
        self.licstart_lbl.grid(row=2, column=4)
        self.dates_avail = date_finder(year=int(sched_yr_chosen), month=sched_mon_chosen)
        self.chosen_licdate1 = StringVar()
        self.chosen_licdate1.set('Select a date')
        self.licdate_asset1 = OptionMenu(master, self.chosen_licdate1, *self.dates_avail)
        self.licdate_asset1.grid(row=3, column=4)
        self.chosen_licdate2 = StringVar()
        self.chosen_licdate2.set('Select a date')
        self.licdate_asset2 = OptionMenu(master, self.chosen_licdate2, *self.dates_avail)
        self.licdate_asset2.grid(row=4, column=4)
        self.chosen_licdate3 = StringVar()
        self.chosen_licdate3.set('Select a date')
        self.licdate_asset3 = OptionMenu(master, self.chosen_licdate3, *self.dates_avail)
        self.licdate_asset3.grid(row=5, column=4)
        self.chosen_licdate4 = StringVar()
        self.chosen_licdate4.set('Select a date')
        self.licdate_asset4 = OptionMenu(master, self.chosen_licdate4, *self.dates_avail)
        self.licdate_asset4.grid(row=6, column=4)
        self.chosen_licdate5 = StringVar()
        self.chosen_licdate5.set('Select a date')
        self.licdate_asset5 = OptionMenu(master, self.chosen_licdate5, *self.dates_avail)
        self.licdate_asset5.grid(row=7, column=4)
        self.chosen_licdate6 = StringVar()
        self.chosen_licdate6.set('Select a date')
        self.licdate_asset6 = OptionMenu(master, self.chosen_licdate6, *self.dates_avail)
        self.licdate_asset6.grid(row=8, column=4)
        ###liceend - 
        self.end_dates_avail = end_dates(self.dates_avail)
        self.licend_lbl = Label(master, text='License End Date')
        self.licend_lbl.grid(row=2, column=5)
        self.chosen_licend1 = StringVar()
        self.chosen_licend1.set('Select a date')
        self.licend_asset1 = OptionMenu(master, self.chosen_licend1, *self.end_dates_avail)
        self.licend_asset1.grid(row=3, column=5)
        self.chosen_licend2 = StringVar()
        self.chosen_licend2.set('Select a date')
        self.licend_asset2 = OptionMenu(master, self.chosen_licend2, *self.end_dates_avail)
        self.licend_asset2.grid(row=4, column=5)
        self.chosen_licend3 = StringVar()
        self.chosen_licend3.set('Select a date')
        self.licend_asset3 = OptionMenu(master, self.chosen_licend3, *self.end_dates_avail)
        self.licend_asset3.grid(row=5, column=5)
        self.chosen_licend4 = StringVar()
        self.chosen_licend4.set('Select a date')
        self.licend_asset4 = OptionMenu(master, self.chosen_licend4, *self.end_dates_avail)
        self.licend_asset4.grid(row=6, column=5)
        self.chosen_licend5 = StringVar()
        self.chosen_licend5.set('Select a date')
        self.licend_asset5 = OptionMenu(master, self.chosen_licend5, *self.end_dates_avail)
        self.licend_asset5.grid(row=7, column=5)
        self.chosen_licend6 = StringVar()
        self.chosen_licend6.set('Select a date')
        self.licend_asset6 = OptionMenu(master, self.chosen_licend6, *self.end_dates_avail)
        self.licend_asset6.grid(row=8, column=5)


    @property
    def sched_var_name(self):
        return '{}_{}_{}'.format(self.chan_chosen, self.sched_mon_chosen, self.sched_yr_chosen)


    def load_sched(self):
        with conn:
                c.execute('SELECT * from panama_schedules WHERE name=?', (self.sched_var_name,))
                schedule_data = c.fetchall()
        
        self.asset_id1.delete(0, END)
        self.asset_id2.delete(0, END)
        self.asset_id3.delete(0, END)
        self.asset_id4.delete(0, END)
        self.asset_id5.delete(0, END)
        self.asset_id6.delete(0, END)
        self.brand.set('Choose')
        self.chosen_cat1_1.set('Select Category')
        self.chosen_cat2_1.set('Select Category')
        self.chosen_cat1_2.set('Select Category')
        self.chosen_cat2_2.set('Select Category')
        self.chosen_cat1_3.set('Select Category')
        self.chosen_cat2_3.set('Select Category')
        self.chosen_cat1_4.set('Select Category')
        self.chosen_cat2_4.set('Select Category')
        self.chosen_cat1_5.set('Select Category')
        self.chosen_cat2_5.set('Select Category')
        self.chosen_cat1_6.set('Select Category')
        self.chosen_cat2_6.set('Select Category')
        self.chosen_licdate1.set('Select a date')
        self.chosen_licdate2.set('Select a date')
        self.chosen_licdate3.set('Select a date')
        self.chosen_licdate4.set('Select a date')
        self.chosen_licdate5.set('Select a date')
        self.chosen_licdate6.set('Select a date')
        self.chosen_licend1.set('Select a date')
        self.chosen_licend2.set('Select a date')
        self.chosen_licend3.set('Select a date')
        self.chosen_licend4.set('Select a date')
        self.chosen_licend5.set('Select a date')
        self.chosen_licend6.set('Select a date')
        
        for rec in schedule_data:
            self.asset_id1.insert(0, rec[3])
            self.asset_id2.insert(0, rec[8])
            self.asset_id3.insert(0, rec[13])
            self.asset_id4.insert(0, rec[18])
            self.asset_id5.insert(0, rec[23])
            self.asset_id6.insert(0, rec[28])
            self.brand.set(str(rec[2]))
            self.chosen_cat1_1.set(str(rec[4]))
            self.chosen_cat2_1.set(str(rec[5]))
            self.chosen_cat1_2.set(str(rec[9]))
            self.chosen_cat2_2.set(str(rec[10]))
            self.chosen_cat1_3.set(str(rec[14]))
            self.chosen_cat2_3.set(str(rec[15]))
            self.chosen_cat1_4.set(str(rec[19]))
            self.chosen_cat2_4.set(str(rec[20]))
            self.chosen_cat1_5.set(str(rec[24]))
            self.chosen_cat2_5.set(str(rec[25]))
            self.chosen_cat1_6.set(str(rec[29]))
            self.chosen_cat2_6.set(str(rec[30]))
            self.chosen_licdate1.set(str(rec[6]))
            self.chosen_licdate2.set(str(rec[11]))
            self.chosen_licdate3.set(str(rec[16]))
            self.chosen_licdate4.set(str(rec[21]))
            self.chosen_licdate5.set(str(rec[26]))
            self.chosen_licdate6.set(str(rec[31]))
            self.chosen_licend1.set(str(rec[7]))
            self.chosen_licend2.set(str(rec[12]))
            self.chosen_licend3.set(str(rec[17]))
            self.chosen_licend4.set(str(rec[22]))
            self.chosen_licend5.set(str(rec[27]))
            self.chosen_licend6.set(str(rec[32]))
    
    
    def update_schedule(self):
        with conn:
            c.execute("""UPDATE panama_schedules SET
                      brand = :brand,
                      dateuploaded = :dateup,
                      asset1 = :asset_id1,
                      category1_1 = :cat1_1,
                      category2_1 = :cat2_1,
                      lic_start_1 = :chosen_licdate1,
                      lic_end_1 = :chosen_licend1,
                      asset2 = :asset_id2,
                      category1_2 = :cat1_2,
                      category2_2 = :cat2_2,
                      lic_start_2 = :chosen_licdate2,
                      lic_end_2 = :chosen_licend2,
                      asset3 = :asset_id3,
                      category1_3 = :cat1_3,
                      category2_3 = :cat2_3,
                      lic_start_3 = :chosen_licdate3,
                      lic_end_3 = :chosen_licend3,
                      asset4 = :asset_id4,
                      category1_4 = :cat1_4,
                      category2_4 = :cat2_4,
                      lic_start_4 = :chosen_licdate4,
                      lic_end_4 = :chosen_licend4,
                      asset5 = :asset_id5,
                      category1_5 = :cat1_5,
                      category2_5 = :cat2_5,
                      lic_start_5 = :chosen_licdate5,
                      lic_end_5 = :chosen_licend5,
                      asset6 = :asset_id6,
                      category1_6 = :cat1_6,
                      category2_6 = :cat2_6,
                      lic_start_6 = :chosen_licdate6,
                      lic_end_6 = :chosen_licend6
                      
                      WHERE name = :name""",
                      {
                        'brand': self.brand.get(),
                        'dateup': rightnow,
                        'asset_id1': self.asset_id1.get(),
                        'cat1_1': self.chosen_cat1_1.get(),
                        'cat2_1': self.chosen_cat2_1.get(),
                        'chosen_licdate1': self.chosen_licdate1.get(),
                        'chosen_licend1': self.chosen_licend1.get(),
                        'asset_id2': self.asset_id2.get(),
                        'cat1_2': self.chosen_cat1_2.get(),
                        'cat2_2': self.chosen_cat2_2.get(),
                        'chosen_licdate2': self.chosen_licdate2.get(),
                        'chosen_licend2': self.chosen_licend2.get(),
                        'asset_id3': self.asset_id3.get(),
                        'cat1_3': self.chosen_cat1_3.get(),
                        'cat2_3': self.chosen_cat2_3.get(),
                        'chosen_licdate3': self.chosen_licdate3.get(),
                        'chosen_licend3': self.chosen_licend3.get(),
                        'asset_id4': self.asset_id4.get(),
                        'cat1_4': self.chosen_cat1_4.get(),
                        'cat2_4': self.chosen_cat2_4.get(),
                        'chosen_licdate4': self.chosen_licdate4.get(),
                        'chosen_licend4': self.chosen_licend4.get(),
                        'asset_id5': self.asset_id5.get(),
                        'cat1_5': self.chosen_cat1_5.get(),
                        'cat2_5': self.chosen_cat2_5.get(),
                        'chosen_licdate5': self.chosen_licdate5.get(),
                        'chosen_licend5': self.chosen_licend5.get(),
                        'asset_id6': self.asset_id6.get(),
                        'cat1_6': self.chosen_cat1_6.get(),
                        'cat2_6': self.chosen_cat2_6.get(),
                        'chosen_licdate6': self.chosen_licdate6.get(),
                        'chosen_licend6': self.chosen_licend6.get(),
                        'name': self.sched_var_name
                        })

    
    def enter_schedule_data(self):
        with conn:
            c.execute("SELECT * FROM panama_schedules WHERE name=?", (self.sched_var_name,))
            verify_sched = c.fetchall()
            if verify_sched != []:
                print('schedule already exists, contact your database adminsitrator')
            else:
                with conn:
                    try:
                        c.execute("""INSERT INTO panama_schedules VALUES (:name, :dateuploaded, :brand, :asset1,
                                                            :category1_1, :category2_1, :lic_start_1, :lic_end_1,
                                                            :asset2, :category1_2, :category2_2, :lic_start_2, :lic_end_2,
                                                            :asset3, :category1_3, :category2_3, :lic_start_3, :lic_end_3,
                                                            :asset4, :category1_4, :category2_4, :lic_start_4, :lic_end_4,
                                                            :asset5, :category1_5, :category2_5, :lic_start_5, :lic_end_5,
                                                            :asset6, :category1_6, :category2_6, :lic_start_6, :lic_end_6
                                                            )""",
                                {
                                    'name': self.sched_var_name,
                                    'dateuploaded': rightnow,
                                    'brand': self.brand.get(),
                                    'asset1': self.asset_id1.get(),
                                    'category1_1': self.chosen_cat1_1.get(),
                                    'category2_1': self.chosen_cat2_1.get(),
                                    'lic_start_1': self.chosen_licdate1.get(),
                                    'lic_end_1': self.chosen_licend1.get(),
                                    'asset2': self.asset_id2.get(),
                                    'category1_2': self.chosen_cat1_2.get(),
                                    'category2_2': self.chosen_cat2_2.get(),
                                    'lic_start_2': self.chosen_licdate2.get(),
                                    'lic_end_2': self.chosen_licend2.get(),
                                    'asset3': self.asset_id3.get(),
                                    'category1_3': self.chosen_cat1_3.get(),
                                    'category2_3': self.chosen_cat2_3.get(),
                                    'lic_start_3': self.chosen_licdate3.get(),
                                    'lic_end_3': self.chosen_licend3.get(),
                                    'asset4': self.asset_id4.get(),
                                    'category1_4': self.chosen_cat1_4.get(),
                                    'category2_4': self.chosen_cat2_4.get(),
                                    'lic_start_4': self.chosen_licdate4.get(),
                                    'lic_end_4': self.chosen_licend4.get(),
                                    'asset5': self.asset_id5.get(),
                                    'category1_5': self.chosen_cat1_5.get(),
                                    'category2_5': self.chosen_cat2_5.get(),
                                    'lic_start_5': self.chosen_licdate5.get(),
                                    'lic_end_5': self.chosen_licend5.get(),
                                    'asset6': self.asset_id6.get(),
                                    'category1_6': self.chosen_cat1_6.get(),
                                    'category2_6': self.chosen_cat2_6.get(),
                                    'lic_start_6': self.chosen_licdate6.get(),
                                    'lic_end_6': self.chosen_licend6.get()
                                })
            
                        print('records created')
                    except sqlite3.OperationalError as e:
                        print(e)


    def clean_screen(self):
        self.asset_id1.delete(0, END)
        self.asset_id2.delete(0, END)
        self.asset_id3.delete(0, END)
        self.asset_id4.delete(0, END)
        self.asset_id5.delete(0, END)
        self.asset_id6.delete(0, END)
        self.brand.set('Choose')
        self.chosen_cat1_1.set('Select Category')
        self.chosen_cat2_1.set('Select Category')
        self.chosen_cat1_2.set('Select Category')
        self.chosen_cat2_2.set('Select Category')
        self.chosen_cat1_3.set('Select Category')
        self.chosen_cat2_3.set('Select Category')
        self.chosen_cat1_4.set('Select Category')
        self.chosen_cat2_4.set('Select Category')
        self.chosen_cat1_5.set('Select Category')
        self.chosen_cat2_5.set('Select Category')
        self.chosen_cat1_6.set('Select Category')
        self.chosen_cat2_6.set('Select Category')
        self.chosen_licdate1.set('Select a date')
        self.chosen_licdate2.set('Select a date')
        self.chosen_licdate3.set('Select a date')
        self.chosen_licdate4.set('Select a date')
        self.chosen_licdate5.set('Select a date')
        self.chosen_licdate6.set('Select a date')
        self.chosen_licend1.set('Select a date')
        self.chosen_licend2.set('Select a date')
        self.chosen_licend3.set('Select a date')
        self.chosen_licend4.set('Select a date')
        self.chosen_licend5.set('Select a date')
        self.chosen_licend6.set('Select a date')
        
        
###