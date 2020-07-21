# -*- coding: utf-8 -*-
""" A simple program to create, edit and delete movie IDs, add translations and other EPG info,
schedule these IDs (only one example: a central American
client that uses CableLabs compliant XMLs), then create metadata for the schedule (just XML files and
a planner excel sheet that contains the necessary info for ingest)
"""

from tkinter import *
#from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog

from airdates import date_finder, end_dates
from ptyschedules import Panamasched
from pty_planner import panama_planner
from pty_xmlgenerator import panama_xmls
from dtd_creator import dtd_creator

import sqlite3
import pandas as pd
import datetime
import calendar
import xml.etree.ElementTree as ET

root = Tk()
root.title('Welcome!')
root.iconbitmap('.\\ico\\movico.ico')
root.geometry("520x400")
#####

###SQLITE3 create DB and mroe:
conn = sqlite3.connect('testdb.db')
c = conn.cursor()


''' Beginning of the kinter application:'''
my_menu = Menu(root)
root.config(menu=my_menu)
###create menu widget
file_menu = Menu(my_menu)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=root.quit)


def warn_popup():
    messagebox.showwarning("WARNING", "This module is not complete")

def error_popup():
    messagebox.showwarning('!!!', "You need to make a schedule!")

def view_all():
    all_ids = Toplevel()
    all_ids.geometry("400x250")
    all_ids.title('All IDs')
    all_ids.iconbitmap('.\\ico\\searchico.ico')
    with conn:
        c.execute("SELECT *, oid FROM movieinfo")
        all_rec_query_res = c.fetchall()
        all_recs_list = []
        eg = 0
        for record in all_rec_query_res:
            recs = all_rec_query_res[eg][0]
            all_recs_list.append(recs)
            eg += 1
    
    text_lbl = Label(all_ids, text="Current Existing Asset IDs:").pack()
    all_rec_lbl = Label(all_ids, text=all_recs_list).pack()


def submit_movieinfo():
    conn = sqlite3.connect('testdb.db')
    c = conn.cursor()
    c.execute("""INSERT INTO movieinfo VALUES (:asset_id, :rating, :title, :actors,
                                                :studio, :director, :runtime, :prod_yr, :origin)""",
                    {
                        'asset_id': asset_id.get(),
                        'rating': rating.get(),
                        'title': title.get(),
                        'actors': actors.get(),
                        'studio': studio.get(),
                        'director': director.get(),
                        'runtime': runtime.get(),
                        'prod_yr': prod_yr.get(),
                        'origin': origin.get() 
                    })
    
    conn.commit()
    conn.close()
    asset_id.delete(0, END)
    rating.delete(0, END)
    title.delete(0, END)
    actors.delete(0, END)
    studio.delete(0, END)
    director.delete(0, END)
    runtime.delete(0, END)
    prod_yr.delete(0, END)
    origin.delete(0, END)
        


def query_record():
    query_top = Toplevel()
    query_top.title('ID info:')
    query_top.geometry("400x400")
    query_top.iconbitmap('.\\ico\\searchico.ico')
    global print_records
    with conn:
        try:
            c.execute("SELECT * FROM movieinfo WHERE asset_id = " + mov_id_query.get())
        except AttributeError:
            c.execute("SELECT *, oid FROM movieinfo")
    
    records = c.fetchall()
    if records == []:
        print_records = "ID does not exist"
    elif records:
        print_records = ''
    #print(records)
    #ex = 0
    for rec in records:
        print_records += ("Asset: " + str(rec[0]) + "\n" +"Rating: "
                          + str(rec[1]) + "\n"  + "Title: " + str(rec[2]) + "\n"
                          "Actors: " + str(rec[3]) + "\n" + "Director: " + str(rec[4]) + "\n" +
                          "Studio: " + str(rec[5]) + "\n" + "Runtime: " + str(rec[6]) + "\n" +
                          "Year Produced: " + str(rec[7]) + "\n" + "Country of Origin: " + str(rec[8]) + "\n"
                          )
        #ex += 0

    query_label = Label(query_top, text=print_records).grid(row=19, column=0)
    mov_id_query.delete(0, END)


def del_record():
    messagebox.askokcancel(title='Confirm Deletion', message='Are you sure you want to delete this?')
    with conn:
        c.execute("DELETE FROM movieinfo WHERE asset_id= " + del_id_ent.get())
        
    del_id_ent.delete(0, END)
    #
    

def edit_record():
    with conn:
        c.execute("""UPDATE movieinfo SET
                  asset_id = :asset_id,
                  rating = :rating,
                  title = :title,
                  actors = :actors,
                  director = :director,
                  studio = :studio,
                  runtime = :runtime,
                  prod_year = :prod_yr,
                  origin = :origin
                  
                  WHERE asset_id = :asset_id""",
                  {'asset_id': asset_id_editor.get(),
                   'rating': rating_editor.get(),
                   'title': title_editor.get(),
                   'actors': actors_editor.get(),
                   'director': director_editor.get(),
                   'studio': studio_editor.get(),
                   'runtime': runtime_editor.get(),
                   'prod_yr': prod_yr_editor.get(),
                   'origin': origin_editor.get()
                          
                  })

    editor.destroy()
    
    

def open_editor():
    global editor
    editor = Tk()
    editor.title('Update A Record')
    editor.geometry("450x500")
    editor.iconbitmap('.\\ico\\movico.ico')
    #global record_to_edit_ent
    
    def get_rec_toupdate():
        rec_id = record_to_edit_ent.get()
        with conn:
            c.execute("SELECT * from movieinfo WHERE asset_id=" + rec_id)
            records = c.fetchall()
            
        ###CLEAR records beforehand
        asset_id_editor.delete(0, END)
        rating_editor.delete(0, END)
        title_editor.delete(0, END)
        actors_editor.delete(0, END)
        studio_editor.delete(0, END)
        director_editor.delete(0, END)
        runtime_editor.delete(0, END)
        prod_yr_editor.delete(0, END)
        origin_editor.delete(0, END)
        ### Now, insert data into the fields after query
        for rec in records:
            asset_id_editor.insert(0, rec[0])
            rating_editor.insert(0, rec[1])
            title_editor.insert(0, rec[2])
            actors_editor.insert(0, rec[3])
            studio_editor.insert(0, rec[4])
            director_editor.insert(0, rec[5])
            runtime_editor.insert(0, rec[6])
            prod_yr_editor.insert(0, rec[7])
            origin_editor.insert(0, rec[8])
    
    
    record_to_edit_lbl = Label(editor, text='Enter the Asset ID for the record to update:')
    record_to_edit_lbl.grid(row=0, column=0)
    record_to_edit_ent = Entry(editor, width=25)
    record_to_edit_ent.grid(row=0, column=1, padx=10, pady=10)
    
    record_to_edit_btn = Button(editor, text="Populate Fields", command=get_rec_toupdate)
    record_to_edit_btn.grid(row=1, column=1, padx=5, pady=5)
    
    global asset_id_editor, rating_editor, title_editor, actors_editor, studio_editor, director_editor
    global runtime_editor, prod_yr_editor, origin_editor
    
    asset_id_label_editor = Label(editor, text="Asset ID:")
    asset_id_label_editor.grid(row=2, column=0)
    asset_id_editor = Entry(editor, width=30)
    asset_id_editor.grid(row=2, column=1)
    rating_label_editor = Label(editor, text="Rating:")
    rating_label_editor.grid(row=3, column=0)
    rating_editor = Entry(editor, width=30)
    rating_editor.grid(row=3, column=1)
    title_label_editor = Label(editor, text="Title:")
    title_label_editor.grid(row=4, column=0)
    title_editor = Entry(editor, width=30)
    title_editor.grid(row=4, column=1)
    actors_label_editor = Label(editor, text="Actors:")
    actors_label_editor.grid(row=5, column=0)
    actors_editor = Entry(editor, width=30)
    actors_editor.grid(row=5, column=1)
    studio_label_editor = Label(editor, text="Studio:")
    studio_label_editor.grid(row=6, column=0)
    studio_editor = Entry(editor, width=30)
    studio_editor.grid(row=6, column=1)
    director_label_editor = Label(editor, text="Director:")
    director_label_editor.grid(row=7, column=0)
    director_editor = Entry(editor, width=30)
    director_editor.grid(row=7, column=1)
    runtime_label_editor = Label(editor, text="Runtime:")
    runtime_label_editor.grid(row=8, column=0)
    runtime_editor = Entry(editor, width=30)
    runtime_editor.grid(row=8, column=1)
    prod_yr_label_editor = Label(editor, text="Production Year:")
    prod_yr_label_editor.grid(row=9, column=0)
    prod_yr_editor = Entry(editor, width=30)
    prod_yr_editor.grid(row=9, column=1)
    origin_label_editor = Label(editor, text="Country of Origin:")
    origin_label_editor.grid(row=10, column=0)
    origin_editor = Entry(editor, width=30)
    origin_editor.grid(row=10, column=1)
    
    ## Edit button:
    edit_btn = Button(editor, text="Edit / Update Record", command=edit_record)
    edit_btn.grid(row=11, column=1)


def epginfo():
    epgtop = Toplevel()
    epgtop.geometry("700x550")
    epgtop.title("Add summaries, translations and titles here")
    epgtop.iconbitmap('.\\ico\\movico.ico')

    ## Pick up here!! ##
    def epgquery():
        with conn:
            try:
                c.execute("SELECT * FROM epginfo WHERE asset_id =" + asset_id_epg.get())
                epgdatos = c.fetchall()
            except AttributeError:
                lbleg = Label(epginfo, text='No Record').grid(row=0, column=6)
              
        english_vod_title_ent.delete(0, END)  
        english_broadcast_title_ent.delete(0, END)
        english_synopsis_ent.delete(0, END)
        internet_title_ent.delete(0, END)
        spanish_vod_title_ent.delete(0, END)
        spanish_broadcast_title_ent.delete(0, END)
        spanish_synopsis_ent.delete(0, END)
        french_vod_title_ent.delete(0, END)
        french_broadcast_title_ent.delete(0, END)
        french_synopsis_ent.delete(0, END)
        portuguese_vod_title_ent.delete(0, END)
        portuguese_broadcast_title_ent.delete(0, END)
        portuguese_synopsis_ent.delete(0, END)
        
        for rec in epgdatos:
            english_vod_title_ent.insert(0, rec[1])
            english_broadcast_title_ent.insert(0, rec[2])
            english_synopsis_ent.insert(0, rec[3])
            internet_title_ent.insert(0, rec[4])
            spanish_vod_title_ent.insert(0, rec[5])
            spanish_broadcast_title_ent.insert(0, rec[6])
            spanish_synopsis_ent.insert(0, rec[7])
            french_vod_title_ent.insert(0, rec[8])
            french_broadcast_title_ent.insert(0, rec[9])
            french_synopsis_ent.insert(0, rec[10])
            portuguese_vod_title_ent.insert(0, rec[11])
            portuguese_broadcast_title_ent.insert(0, rec[12])
            portuguese_synopsis_ent.insert(0, rec[13])

     
    
    def addepg():
        with conn:
            c.execute("""INSERT INTO epginfo VALUES (:asset_id, :english_vod_title, :english_broadcast_title,
                                                           :english_synopsis, :internet_title, :spanish_vod_title,
                                                           :spanish_broadcast_title, :spanish_synopsis,
                                                           :french_vod_title, :french_broadcast_title, :french_synopsis,
                                                           :portuguese_vod_title, :portuguese_broadcast_title,
                                                           :portuguese_synopsis)""",
                    {
                        'asset_id': asset_id_epg.get(),
                        'english_vod_title': english_vod_title_ent.get(),
                        'english_broadcast_title': english_broadcast_title_ent.get(),
                        'english_synopsis': english_synopsis_ent.get(),
                        'internet_title': internet_title_ent.get(),
                        'spanish_vod_title': spanish_vod_title_ent.get(),
                        'spanish_broadcast_title': spanish_broadcast_title_ent.get(),
                        'spanish_synopsis': spanish_synopsis_ent.get(),
                        'french_vod_title': french_vod_title_ent.get(),
                        'french_broadcast_title': french_broadcast_title_ent.get(),
                        'french_synopsis': french_synopsis_ent.get(),
                        'portuguese_vod_title': portuguese_vod_title_ent.get(),
                        'portuguese_broadcast_title': portuguese_broadcast_title_ent.get(),
                        'portuguese_synopsis': portuguese_synopsis_ent.get()
                    })
    
    ##delete text boxes:
        asset_id_epg.delete(0, END)
        english_vod_title_ent.delete(0, END)
        english_broadcast_title_ent.delete(0, END)
        english_synopsis_ent.delete(0, END)
        internet_title_ent.delete(0, END)
        spanish_vod_title_ent.delete(0, END)
        spanish_broadcast_title_ent.delete(0, END)
        spanish_synopsis_ent.delete(0, END)
        french_vod_title_ent.delete(0, END)
        french_broadcast_title_ent.delete(0, END)
        french_synopsis_ent.delete(0, END)
        portuguese_vod_title_ent.delete(0, END)
        portuguese_broadcast_title_ent.delete(0, END)
        portuguese_synopsis_ent.delete(0, END)
        
            
    def editepg():
        with conn:
            c.execute("""UPDATE epginfo SET
                      asset_id = :asset_id,
                      english_vod_title = :english_vod_title,
                      english_broadcast_title = :english_broadcast_title,
                      english_synopsis = :english_synopsis,
                      internet_title = :internet_title,
                      spanish_vod_title = :spanish_vod_title,
                      spanish_broadcast_title = :spanish_broadcast_title,
                      spanish_synopsis = :spanish_synopsis,
                      french_vod_title = :french_vod_title,
                      french_broadcast_title = :french_broadcast_title,
                      french_synopsis = :french_synopsis,
                      portuguese_vod_title = :portuguese_vod_title,
                      portuguese_broadcast_title = :portuguese_broadcast_title,
                      portuguese_synopsis = :portuguese_synopsis                      
                      
                      WHERE asset_id = :asset_id""",
                      {'asset_id': asset_id_epg.get(),
                       'english_vod_title': english_vod_title_ent.get(),
                       'english_broadcast_title': english_broadcast_title_ent.get(),
                       'english_synopsis': english_synopsis_ent.get(),
                       'internet_title': internet_title_ent.get(),
                       'spanish_vod_title': spanish_vod_title_ent.get(),
                       'spanish_broadcast_title': spanish_broadcast_title_ent.get(),
                       'spanish_synopsis': spanish_synopsis_ent.get(),
                       'french_vod_title': french_vod_title_ent.get(),
                       'french_broadcast_title': french_broadcast_title_ent.get(),
                       'french_synopsis': french_synopsis_ent.get(),
                       'portuguese_vod_title': portuguese_vod_title_ent.get(),
                       'portuguese_broadcast_title': portuguese_broadcast_title_ent.get(),
                       'portuguese_synopsis': portuguese_synopsis_ent.get()
                       })
    
    
    asset_id_label = Label(epgtop, text="Asset ID:")
    asset_id_label.grid(row=0, column=0)
    asset_id_epg = Entry(epgtop, width=25)
    asset_id_epg.grid(row=0, column=1)
    english_vod_title_lbl = Label(epgtop, text="English VOD Title:")
    english_vod_title_lbl.grid(row=2, column=0)
    english_vod_title_ent = Entry(epgtop, width=25)
    english_vod_title_ent.grid(row=2, column=1)
    english_broadcast_title_lbl = Label(epgtop, text="English Broadcast Title:")
    english_broadcast_title_lbl.grid(row=3, column=0)
    english_broadcast_title_ent = Entry(epgtop, width=25)
    english_broadcast_title_ent.grid(row=3, column=1)
    english_synopsis_lbl= Label(epgtop, text="English Synopsis:")
    english_synopsis_lbl.grid(row=4, column=0)
    english_synopsis_ent = Entry(epgtop, width=25)
    english_synopsis_ent.grid(row=4, column=1, ipady=20)
    internet_title_lbl = Label(epgtop, text="Internet Title:")
    internet_title_lbl.grid(row=5, column=0)
    internet_title_ent = Entry(epgtop, width=25)
    internet_title_ent.grid(row=5, column=1)
    spanish_vod_title_lbl = Label(epgtop, text="Spanish VOD Title:")
    spanish_vod_title_lbl.grid(row=6, column=0)
    spanish_vod_title_ent = Entry(epgtop, width=25)
    spanish_vod_title_ent.grid(row=6, column=1)
    spanish_broadcast_title_lbl = Label(epgtop, text="Spanish Broadcast Title:")
    spanish_broadcast_title_lbl.grid(row=7, column=0)
    spanish_broadcast_title_ent = Entry(epgtop, width=25)
    spanish_broadcast_title_ent.grid(row=7, column=1)
    spanish_synopsis_lbl = Label(epgtop, text="Spanish Synopsis:")
    spanish_synopsis_lbl.grid(row=8, column=0)
    #### Test the size here:
    ##spanish_synopsis_ent.place(width=20, height=50)
    ##spanish_synopsis_ent = Entry(epgtop, width=20, font=('Arial', 24))
    spanish_synopsis_ent = Entry(epgtop, width=25)
    spanish_synopsis_ent.grid(row=8, column=1, ipady=20)
    french_vod_title_lbl = Label(epgtop, text="French VOD Title:")
    french_vod_title_lbl.grid(row=9, column=0)
    french_vod_title_ent = Entry(epgtop, width=25)
    french_vod_title_ent.grid(row=9, column=1)
    french_broadcast_title_lbl = Label(epgtop, text="French Broadcast Title:")
    french_broadcast_title_lbl.grid(row=10, column=0)
    french_broadcast_title_ent = Entry(epgtop, width=25)
    french_broadcast_title_ent.grid(row=10, column=1)
    french_synopsis_lbl = Label(epgtop, text="French Synopsis:")
    french_synopsis_lbl.grid(row=11, column=0)
    french_synopsis_ent = Entry(epgtop, width=25)
    french_synopsis_ent.grid(row=11, column=1, ipady=20)
    portuguese_vod_title_lbl = Label(epgtop, text="Portuguese VOD Title:")
    portuguese_vod_title_lbl.grid(row=12, column=0)
    portuguese_vod_title_ent = Entry(epgtop, width=25)
    portuguese_vod_title_ent.grid(row=12, column=1)
    portuguese_broadcast_title_lbl = Label(epgtop, text="Portuguese Broadcast Title:")
    portuguese_broadcast_title_lbl.grid(row=13, column=0)
    portuguese_broadcast_title_ent = Entry(epgtop, width=25)
    portuguese_broadcast_title_ent.grid(row=13, column=1)
    portuguese_synopsis_lbl = Label(epgtop, text="Portuguese Synopsis:")
    portuguese_synopsis_lbl.grid(row=14, column=0)
    portuguese_synopsis_ent = Entry(epgtop, width=25)
    portuguese_synopsis_ent.grid(row=14, column=1, ipady=20)
    def del_epg():
        messagebox.askokcancel(title='Confirm Deletion', message='Are you sure you want to delete this?')
        with conn:
            c.execute("DELETE FROM epginfo WHERE asset_id= " + asset_id_epg.get())
    ##buttons to perform actions
    query_epginfo_btn = Button(epgtop, text='Show EPG info', command=epgquery)
    query_epginfo_btn.grid(row=0, column=2)
    add_epginfo_btn = Button(epgtop, text='Add EPG Info', command=addepg)
    add_epginfo_btn.grid(row=0, column=3)
    edit_epginfo_btn = Button(epgtop, text='EDIT EPG info', command=editepg)
    edit_epginfo_btn.grid(row=0, column=4)
    del_epginfo_btn = Button(epgtop, text="DELETE EPG INFO??", command=del_epg)
    del_epginfo_btn.grid(row=0, column=5)

### Open diferent screens / module functions:
def open_movinfo():
    mov_tk = Toplevel()
    mov_tk.geometry("450x550")
    mov_tk.title("Create, Edit, Delete Movie IDs")
    mov_tk.iconbitmap('.\\ico\\movico.ico')
    global asset_id, rating, title, actors, studio, director, runtime, prod_yr, origin
    #### Create text boxes
    asset_id_label = Label(mov_tk, text="Asset ID:")
    asset_id_label.grid(row=0, column=0)
    asset_id = Entry(mov_tk, width=30)
    asset_id.grid(row=0, column=1)
    rating_label = Label(mov_tk, text="Rating:")
    rating_label.grid(row=1, column=0)
    rating = Entry(mov_tk, width=30)
    rating.grid(row=1, column=1)
    title_label = Label(mov_tk, text="Title:")
    title_label.grid(row=2, column=0)
    title = Entry(mov_tk, width=30)
    title.grid(row=2, column=1)
    actors_label = Label(mov_tk, text="Actors:")
    actors_label.grid(row=3, column=0)
    actors = Entry(mov_tk, width=30)
    actors.grid(row=3, column=1)
    studio_label = Label(mov_tk, text="Studio:")
    studio_label.grid(row=4, column=0)
    studio = Entry(mov_tk, width=30)
    studio.grid(row=4, column=1)
    director_label = Label(mov_tk, text="Director:")
    director_label.grid(row=5, column=0)
    director = Entry(mov_tk, width=30)
    director.grid(row=5, column=1)
    runtime_label = Label(mov_tk, text="Runtime:")
    runtime_label.grid(row=6, column=0)
    runtime = Entry(mov_tk, width=30)
    runtime.grid(row=6, column=1)
    prod_yr_label = Label(mov_tk, text="Production Year:")
    prod_yr_label.grid(row=7, column=0)
    prod_yr = Entry(mov_tk, width=30)
    prod_yr.grid(row=7, column=1)
    origin_label = Label(mov_tk, text="Country of Origin:")
    origin_label.grid(row=8, column=0)
    origin = Entry(mov_tk, width=30)
    origin.grid(row=8, column=1)
    #####Create submit button, data should go to sqlite database
    submit_btn = Button(mov_tk, text="Create Record", command=submit_movieinfo)
    submit_btn.grid(row=9, column=1, columnspan=2, pady=10)
    ####EPG info (translations, synopses, etc.)
    epg_info_btn  = Button(mov_tk, text='Add, View, or Edit EPG Info', command=epginfo)
    epg_info_btn.grid(row=10, column=1, columnspan=2, pady=15, padx=10)
    ### Query code:
    global mov_id_query
    lbl_mov_query = Label(mov_tk, text='Enter an ID to see info:')
    lbl_mov_query.grid(row=12, column=0)
    #mov_id_lbl = Label(mov_tk, text='Asset ID')
    #mov_id_lbl.grid(row=11, column=0)
    mov_id_query = Entry(mov_tk, width=25)
    mov_id_query.grid(row=12, column=1)
    ####
    show_id_btn = Button(mov_tk, text="Find Record",
                         command=query_record).grid(row=13, column=1, columnspan=2, padx=5, pady=10, ipadx=15)
    
    ### edit button (to new window):
    edit_rec_btn = Button(mov_tk, text="Edit Existing Movie Record", command=open_editor, bg="orange")
    edit_rec_btn.grid(row=11, column=1, columnspan=2, padx=5, pady=10, ipadx=15)
    #### Delete button (to delete a record here)
    ## try to have a confirmation button first?
    global del_id_ent
    del_id_lbl = Label(mov_tk, text='Asset ID to DELETE:')
    del_id_lbl.grid(row=17, column=0)
    del_id_ent = Entry(mov_tk, width=30)
    del_id_ent.grid(row=17, column=1)
    del_id_btn = Button(mov_tk, text="DELETE ID??",
                         command=del_record, bg='red').grid(row=18, column=1, padx=5, pady=10)



###Import commands for the buttons to make it function
### Builder Functions are here:
def scheduler():
    topsched = Toplevel()
    topsched.geometry("900x500")
    topsched.title("Schedule Creator Module")
    topsched.iconbitmap('.\\ico\\movico.ico')
    test_lbl = Label(topsched, text=chan_chosen.get() + ' ' + sched_mon_chosen.get() +
                                        ' ' + sched_yr_chosen.get()).grid(row=0, column=0)
    ###variables to note: chan_chosen, sched_mon_chosen, sched_yr_chosen
    sched_var_name = chan_chosen.get() + '_'  + sched_mon_chosen.get() +  '_' + sched_yr_chosen.get()
    '''The point here is to have different schedules modules that can be loaded and altered
    '''
    if chan_chosen.get() == 'Sample_Panama':
        run = Panamasched(topsched, chan_chosen.get(), sched_mon_chosen.get(), sched_yr_chosen.get())


def open_build():
    top2 = Toplevel()
    top2.geometry("400x400")
    top2.title("Schedule Creator Module")
    top2.iconbitmap('.\\ico\\movico.ico')
    global chan_chosen, sched_mon_chosen, sched_yr_chosen
    chan_chosen = StringVar()
    chan_chosen.set('Choose Channel')
    #chan_list_ = []
    drop_ex  = OptionMenu(top2, chan_chosen, 'Sample_Panama')
    drop_ex.pack()
    mons = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
            'September', 'October', 'November', 'December']
    yrs_ =['2020']
    sched_mon_chosen = StringVar()
    sched_mon_chosen.set('Select Month')
    sched_mon_build = OptionMenu(top2, sched_mon_chosen, *mons)
    sched_mon_build.pack()
    sched_yr_chosen = StringVar()
    sched_yr_chosen.set('Select Year')
    sched_yr_build = OptionMenu(top2, sched_yr_chosen, *yrs_)
    sched_yr_build.pack()
    bld_btn = Button(top2, text='View Schedule', command=scheduler).pack()



def open_mtpgen():
    top3 = Toplevel()
    top3.geometry("550x400")
    top3.title("Metadata Sheet Module")
    lbl3 = Label(top3, text='VOD Planner Creator').grid(row=0,column=0)
    chan_chosenMTP = StringVar()
    chan_chosenMTP.set('Choose Channel')
    drop_ex3  = OptionMenu(top3, chan_chosenMTP,  'Sample_Panama')
    drop_ex3.grid(row=1,column=0)
    mons = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
            'September', 'October', 'November', 'December']
    yrs_ = ['2020']
    sched_mon_chosenMTP = StringVar()
    sched_mon_chosenMTP.set('Select Month')
    sched_mon_MTP = OptionMenu(top3, sched_mon_chosenMTP, *mons)
    sched_mon_MTP.grid(row=1,column=1)
    sched_yr_chosenMTP = StringVar()
    sched_yr_chosenMTP.set('Select Year')
    sched_yr_MTP = OptionMenu(top3, sched_yr_chosenMTP, *yrs_)
    sched_yr_MTP.grid(row=1,column=2)
    schedule_planner = chan_chosenMTP.get() + '_' + sched_mon_chosenMTP.get() +  '_' + sched_yr_chosenMTP.get()
    #global schedule_planner
    def planner():
        plannertime = chan_chosenMTP.get() + '_' + sched_mon_chosenMTP.get() +  '_' + sched_yr_chosenMTP.get()
        if chan_chosenMTP.get() == 'Sample_Panama':
            try:
                panama_planner(plannertime)
                newlbl = Label(top3, text=plannertime).grid(row=2,column=0)
            except IndexError as issue:
                error_popup()
    #lbltest = Label(top3, text=schedule_planner).grid(row=2,column=0)
    ### CHANGE COMMAND:
    run_mtpgen = Button(top3, text="RUN", command=planner).grid(row=1,column=3)


def open_xmlgen():
    top4 = Toplevel()
    top4.geometry("550x400")
    top4.title("XML Generator Module")
    top4.iconbitmap('.\\ico\\xmlico.ico')
    lbl4 = Label(top4, text='XML Generator').grid(row=0,column=0)
    ### CHANGE COMMAND:
    chan_chosenXML = StringVar()
    chan_chosenXML.set('Choose Channel')
    drop_ex4 = OptionMenu(top4, chan_chosenXML, 'Sample_Panama')
    drop_ex4.grid(row=1,column=0)
    mons = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
            'September', 'October', 'November', 'December']
    yrs_ = ['2020']
    sched_mon_chosenXML = StringVar()
    sched_mon_chosenXML.set('Select Month')
    sched_mon_XML = OptionMenu(top4, sched_mon_chosenXML, *mons)
    sched_mon_XML.grid(row=1,column=1)
    sched_yr_chosenXML = StringVar()
    sched_yr_chosenXML.set('Select Year')
    sched_yr_XML = OptionMenu(top4, sched_yr_chosenXML, *yrs_)
    sched_yr_XML.grid(row=1,column=2)
    def run_xmls():
        pitch = plannertime = chan_chosenXML.get() + '_' + sched_mon_chosenXML.get() + '_' + sched_yr_chosenXML.get()
        if chan_chosenXML.get() == 'Sample_Panama':
            try:
                panama_xmls(pitch)
                dtd_creator()
            except IndexError as issue:
                error_popup()
    
    run_xmlgen = Button(top4, text="Create XMLs", command=run_xmls).grid(row=1,column=4)


#Home buttons, call function above
btn1 = Button(root, text="Movie ID Module", command=open_movinfo)
btn1.grid(row=1, column=0)
btn2 = Button(root, text="Schedule Builder", command=open_build)
btn2.grid(row=2, column=0)
btn3 = Button(root, text="Metadata Excel Sheet Module", command=open_mtpgen)
btn3.grid(row=3, column=0, padx=10)
btn4 = Button(root, text="XML Generator", command=open_xmlgen)
btn4.grid(row=4, column=0)
btn5 = Button(root, text="View All IDs", command=view_all)
btn5.grid(row=5, column=0)
btn6 = Button(root, text='Excel XML Generator(future)', command=warn_popup)
btn6.grid(row=6, column=0)
button_quit = Button(root, text='Exit Program Now', command=root.quit, bg="red")
button_quit.grid(row=7, column=0, pady=10)

nexttask = Label(root, text="")
nexttask.grid(row=8, column=0, pady=15)

### end of program:
mainloop()
#root.mainloop()
#mov_tk.mainloop()
