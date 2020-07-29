"""Docstring explaining the xml generator from sqlite3 database"""

## import the necessary modules
import datetime
import xml.etree.ElementTree as ET
import sqlite3
import re
from tkinter import filedialog
from dtd_creator import dtd_creator

def panama_xmls(schedule):
    ''' Connect to the database and query it '''
    #schedule = 'Sample_Panama_January_2020'
    sched_name = schedule
    
    conn = sqlite3.connect('testdb.db')
    c = conn.cursor()
    c.execute("SELECT asset1, asset2, asset3, asset4, asset5, asset6 FROM panama_schedules WHERE name=?", (sched_name,))
    scheduled_ids = c.fetchall()
    ###execute select statements for all values, loop through to create entire dataframe then export it
    asset_list = []
    for id_ in scheduled_ids:
        for var in id_:
                asset_list.append(var)
    
    
    def get_asset_names(j):
        with conn:
            c.execute("SELECT spanish_vod_title FROM epginfo WHERE asset_id=:movid", {'movid':asset_list[j]} )
            assetname = c.fetchone()
            #print(assetname)
            asset_name_var = assetname[0]
            asset_name_var = re.sub(' ', '_', asset_name_var)
            return asset_name_var
        
    
    def get_title_var(j):
        c.execute("SELECT spanish_vod_title FROM epginfo WHERE asset_id=:movid", {'movid':asset_list[j]} )
        span_title = c.fetchone()
        span_title = span_title[0]
        return span_title
    
    
    def get_span_summary(j):
        c.execute("SELECT spanish_synopsis FROM epginfo WHERE asset_id=:movid", {'movid':asset_list[j]})
        summary_span_var = c.fetchone()
        summary_span_var = summary_span_var[0]
        return summary_span_var
    
    
    def get_rating(j):
        c.execute("SELECT rating FROM movieinfo WHERE asset_id=:movid", {'movid':asset_list[j]})
        rating = c.fetchone()
        rating = rating[0]
        return rating
        
    
    def get_durations(j):
        c.execute("SELECT runtime FROM movieinfo WHERE asset_id=:movid", {'movid':asset_list[j]})
        timecode = c.fetchone()
        duration_var = timecode[0]
        duration_vars = [duration_var, duration_var[:5]]
        return duration_vars
    
    
    def get_year(j):
        c.execute("SELECT prod_year FROM movieinfo WHERE asset_id=:movid", {'movid':asset_list[j]})
        prod_year = c.fetchone()
        yr = prod_year[0]
        return yr
    
    
    def get_studio_name(j):
        c.execute("SELECT studio FROM movieinfo WHERE asset_id=:movid", {'movid':asset_list[j]})
        studio_name  = c.fetchone()
        studio = studio_name[0]
        return studio
    
    
    def get_actors(j):
        c.execute("SELECT actors FROM movieinfo WHERE asset_id=:movid", {'movid':asset_list[j]})
        actors_from_db = c.fetchall()
        actor_tup = actors_from_db[0]
        #print(actor_tup)
        actores = actor_tup[0]
        actores = actores.split(",")
        #print(actores)
        all_actor_vars = [actor_tup[0]]
        act_str = actor_tup[0]
        #print(act_str)
        actor1 = act_str.split(" ")
        #print(actor1)
        try:
            first_actor = str(actor1[1] + " " + actor1[0])
        except IndexError:
            first_actor = ''
        #print(first_actor)
        try:
            act2= actores[1]
        except IndexError:
            act2 = ''
        actor2= act2.split(" ")
        try:
            second_actor = str(actor2[2] + ", " + actor2[1])
        except IndexError:
            second_actor = ''
        all_actor_vars.append(first_actor)
        all_actor_vars.append(second_actor)
        return all_actor_vars
    

    def get_director(j):
        c.execute("SELECT director FROM movieinfo WHERE asset_id=:movid", {'movid':asset_list[j]})
        director = c.fetchone()[0]
        return director
    
    
    def get_cats(sched_name, j):
            c.execute("""SELECT category1_1, category2_1, category1_2, category2_2, 
                              category1_3, category2_3, category1_4, category2_4,
                              category1_5, category2_5, category1_6, category2_6
                              FROM panama_schedules WHERE name=?""", (sched_name,))
            cats = c.fetchall()
            categories = cats[0]
            if j == 0:
                category1and2 = [categories[0],categories[1]]
            elif j == 1:
                category1and2 = [categories[2],categories[3]]
            elif j == 2:
                category1and2 = [categories[4],categories[5]]
            elif j == 3:
                category1and2 = [categories[6],categories[7]]
            elif j == 4:
                category1and2 = [categories[8],categories[9]]
            elif j == 5:
                category1and2 = [categories[10],categories[11]]
            else:
                print('out of index')
            return category1and2
    

    def lic_dates(sched_name, j):
        c.execute("""SELECT lic_start_1, lic_end_1, lic_start_2, lic_end_2, lic_start_3,
                      lic_end_3, lic_start_4, lic_end_4, lic_start_5, lic_end_5, lic_start_6,lic_end_6 
                      FROM panama_schedules WHERE name=?    
                      """, (sched_name,))
        lic_dates = c.fetchall()
        if j == 0:
            lic_start = lic_dates[0][0]
            lic_start = datetime.datetime.strptime(lic_start, '%Y-%m-%d')
            lic_start = lic_start.strftime('%Y-%m-%d')
            lic_end = lic_dates[0][1]
            lic_end = datetime.datetime.strptime(lic_end, '%Y-%m-%d')
            lic_end = lic_end.strftime('%Y-%m-%d')
            lics = [lic_start, lic_end]
        elif j == 1:
            lic_start = lic_dates[0][2]
            lic_start = datetime.datetime.strptime(lic_start, '%Y-%m-%d')
            lic_start = lic_start.strftime('%Y-%m-%d')
            lic_end = lic_dates[0][3]
            lic_end = datetime.datetime.strptime(lic_end, '%Y-%m-%d')
            lic_end = lic_end.strftime('%Y-%m-%d')
            lics = [lic_start, lic_end]
        elif j == 2:
            lic_start = lic_dates[0][4]
            lic_start = datetime.datetime.strptime(lic_start, '%Y-%m-%d')
            lic_start = lic_start.strftime('%Y-%m-%d')
            lic_end = lic_dates[0][5]
            lic_end = datetime.datetime.strptime(lic_end, '%Y-%m-%d')
            lic_end = lic_end.strftime('%Y-%m-%d')
            lics = [lic_start, lic_end]
        elif j == 3:
            lic_start = lic_dates[0][6]
            lic_start = datetime.datetime.strptime(lic_start, '%Y-%m-%d')
            lic_start = lic_start.strftime('%Y-%m-%d')
            lic_end = lic_dates[0][7]
            lic_end = datetime.datetime.strptime(lic_end, '%Y-%m-%d')
            lic_end = lic_end.strftime('%Y-%m-%d')
            lics = [lic_start, lic_end]
        elif j == 4:
            lic_start = lic_dates[0][8]
            lic_start = datetime.datetime.strptime(lic_start, '%Y-%m-%d')
            lic_start = lic_start.strftime('%Y-%m-%d')
            lic_end = lic_dates[0][9]
            lic_end = datetime.datetime.strptime(lic_end, '%Y-%m-%d')
            lic_end = lic_end.strftime('%Y-%m-%d')
            lics = [lic_start, lic_end]
        elif j == 5:
            lic_start = lic_dates[0][10]
            lic_start = datetime.datetime.strptime(lic_start, '%Y-%m-%d')
            lic_start = lic_start.strftime('%Y-%m-%d')
            lic_end = lic_dates[0][11]
            lic_end = datetime.datetime.strptime(lic_end, '%Y-%m-%d')
            lic_end = lic_end.strftime('%Y-%m-%d')
            lics = [lic_start, lic_end]
        return lics
    
    
    ##hold='%m/%d/%Y'
    ## get creation date for the creation_date tag in the XML:
    todaysdate = datetime.datetime.now()
    today = todaysdate.strftime('%Y-%m-%d')
    
    ## prettify is a function that was found online: it makes XMLs "pretty printed"
    def prettify(element, indent='  '):
        queue = [(0, element)]  ## (level, element)
        while queue:
            level, element = queue.pop(0)
            children = [(level + 1, child) for child in list(element)]
            if children:
                element.text = '\n' + indent * (level+1)  ## for child open
            if queue:
                element.tail = '\n' + indent * queue[0][0]  ## for sibling open
            else:
                element.tail = '\n' + indent * (level-1)  ## for parent close
            queue[0:0] = children  ## prepend so children come before siblings
    
    
    ## Now we have the xmlcreator function --
    def xmlcreator(j, sched_name):
        asset_name_var = get_asset_names(j)
        title_var = get_title_var(j)
        summary_span_var = get_span_summary(j)
        rating_var = get_rating(j)
        ###be wary of the next two lines:
        duration_var = get_durations(j)[0]
        display_rt_var = get_durations(j)[1]
        year_var = get_year(j)
        studio_var = get_studio_name(j)
        actor_list = get_actors(j)
        director = get_director(j)
        categories = get_cats(sched_name, j)
        lic_start_date = lic_dates(sched_name, j)
        lic_end_date = lic_dates(sched_name, j)
        contract_name = asset_name_var
        ## FINALLY THIS PART CREATES THE XML
        ADIdoc = ET.Element('ADI')
        metadata1 = ET.SubElement(ADIdoc, 'Metadata')
        ET.SubElement(metadata1, 'AMS', Provider="REVVOD", Product="MOD",
                      Asset_Name=str(asset_name_var + "_HD_Package"),
                      Version_Major="1", Version_Minor="0",  Description= str(asset_name_var + ' HD'),
                      Creation_Date=str(today), Provider_ID="REV.com", 
                      Asset_ID=str("REV0520046500" + asset_list[j]), Asset_Class="package")
        ET.SubElement(metadata1, 'App_Data', Name="Metadata_Spec_Version", App="MOD", Value="CableLabsVOD1.1")
        Asset = ET.SubElement(ADIdoc, 'Asset')
        metadata2 = ET.SubElement(Asset, "Metadata")
        ET.SubElement(metadata2, "AMS", Provider="REVVOD", Product="MOD",
                      Asset_Name=str(asset_name_var + "_HD_Title"), Version_Major="1", Version_Minor="0",
                      Description= str(asset_name_var + ' HD'), Creation_Date=str(today),
                      Provider_ID="tylerreveille.com", Asset_ID=str("R3V0520046500" + asset_list[j]), Asset_Class="title")
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Type", Value="Title")
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Title_Sort_Name", Value=title_var)
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Title_Brief", Value=title_var)
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Title", Value=title_var)
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Summary_Medium", Value= summary_span_var)
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Summary_Short", Value= summary_span_var)
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Rating", Value=rating_var)
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Closed_Captioning", Value="N")
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Run_Time", Value=duration_var)
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Display_Run_Time", Value=display_rt_var)
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Year", Value=year_var)
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Studio", Value=studio_var)
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Studio_Name", Value=studio_var)
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Actors", Value= actor_list[1])
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Actors", Value= actor_list[2])
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Actors_Display", Value= actor_list[0])
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Director", Value= director)
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Category", Value= categories[0])
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Category", Value= categories[1])
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Genre", Value="Adulto")
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Box_Office", Value="0")
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Billing_ID", Value="0")
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Licesning_Window_Start",
                      Value = str(lic_start_date[0] + "T00:00:00"))
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Licensing_Window_End",
                      Value= str(lic_end_date[1] + 'T23:59:59'))
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Preview_Period", Value="0")
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Maximum_Viewing_Length", Value="00:24:00")
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Provider_QA_Contact", Value="vodoperations@company.com")
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Contract_Name", Value= contract_name)
        ET.SubElement(metadata2, 'App_Data', App="MOD", Name="Suggested_Price", Value="0.00")
        Asset2 = ET.SubElement(Asset, 'Asset')
        metadata3 = ET.SubElement(Asset2, 'Metadata')
        ET.SubElement(metadata3, "AMS", Provider="REVVOD", Product="MOD", Asset_Name=str(asset_name_var + "_HD_Movie"),
                      Version_Major="1", Version_Minor="0",
                      Description= str(asset_name_var + ' HD'), Creation_Date=str(today),
                      Provider_ID="tylerreveille.com",
                      Asset_ID=str("R3V0520046500" + asset_list[j]), Asset_Class="movie")
        ET.SubElement(metadata3, 'App_Data', App="MOD", Name="Type", Value="movie")
        ET.SubElement(metadata3, 'App_Data', App="MOD", Name="Screen_Format", Value="Widescreen")
        ET.SubElement(metadata3, 'App_Data', App="MOD", Name="HDContent", Value="Y")
        ET.SubElement(metadata3, 'App_Data', App="MOD", Name="Audio_Type", Value="Stereo")
        ET.SubElement(metadata3, 'App_Data', App="MOD", Name="Viewing_Can_Be_Resumed", Value="Y")
        ET.SubElement(metadata3, 'App_Data', App="MOD", Name="Watermarking", Value="N")
        ET.SubElement(metadata3, 'App_Data', App="MOD", Name="Copy_Protection", Value="N")
        ET.SubElement(metadata3, 'App_Data', App="MOD", Name="Content_Format", Value="MPEG2")
        ET.SubElement(metadata3, 'App_Data', App="MOD", Name="Content_FileSize", Value="")
        ET.SubElement(metadata3, 'App_Data', App="MOD", Name="Content_CheckSum", Value="")
        ET.SubElement(Asset2, 'Content', Value=str("HUTL0520046500" + asset_list[j] + ".ts"))
        Asset3 = ET.SubElement(Asset, 'Asset')
        metadata4 = ET.SubElement(Asset3, 'Metadata')
        ET.SubElement(metadata4, 'AMS', Provider="REVVOD", Product="MOD", Asset_Name=str(asset_name_var + "_HD_Poster"),
                      Version_Major="1",  Version_Minor="0", Description= str(asset_name_var + ' HD'),
                      Creation_Date=str(today), Provider_ID="tylerreveille.com",
                      Asset_ID=("R3V05200465" + asset_list[j] ), Asset_Class="poster")
        ET.SubElement(metadata4, 'App_Data', App="MOD", Name="Type", Value="poster")
        ET.SubElement(metadata4, 'App_Data', App="MOD", Name="Image_Aspect_Ratio", Value="640x960")
        ET.SubElement(metadata4, 'App_Data', App="MOD", Name="Content_FileSize", Value="")
        ET.SubElement(metadata4, 'App_Data', App="MOD", Name="Content_CheckSum", Value="")
        ET.SubElement(Asset3, 'Content', Value=str("HUTL05200465" + asset_list[j]  + ".jpg"))
        ## final steps: call prettify to make it look good and export the ADI element
        prettify(ADIdoc)
        tree = ET.ElementTree(ADIdoc)
        #"C:\\Users\\Papi\\Desktop\\MOVOD\\files\\EX00"
        tree.write(dirvar + '\\' + 'EX00' + str(asset_list[j]) + '_HD_test' + '.xml',
                   xml_declaration=True, encoding='iso-8859-1')
        
    
    ## Production:
    dirvar = filedialog.askdirectory(initialdir='/', title='')
    num = 0
    for num in range(6):
        xmlcreator(num, schedule)
        num += 1
    
    conn.commit()
    conn.close()
    dtd_creator(dirvar)
    
#panama_xmls('Sample_Panama_January_2020')
