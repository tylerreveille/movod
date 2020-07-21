# -*- coding: utf-8 -*-
"""
Created on Thu May 14 11:09:09 2020

@author: Papi
"""

import os


def dtd_creator():
    text = '''<!-- DTD for Package-->
<!--CableLabs Asset Distribution Interface version 1.1 -->
<!-- <!ENTITY amp "&#38;#38;"> -->
<!ELEMENT ADI (Metadata, Asset* )>
<!ELEMENT Asset ( Metadata, Asset*, Content?)>
<!ELEMENT Metadata (AMS, App_Data*)>
<!ELEMENT AMS (#PCDATA)>
<!ATTLIST AMS
Asset_Name CDATA #REQUIRED
Asset_ID CDATA #REQUIRED
Asset_Class CDATA #REQUIRED
Provider CDATA #REQUIRED
Provider_ID CDATA #REQUIRED
Product CDATA #REQUIRED
Version_Minor CDATA #REQUIRED
Version_Major CDATA #REQUIRED
Description CDATA #REQUIRED
Creation_Date CDATA #REQUIRED
Verb CDATA #IMPLIED >
<!ELEMENT App_Data (#PCDATA)>
<!ATTLIST App_Data App CDATA #REQUIRED
Name CDATA #REQUIRED
Value CDATA #REQUIRED
>
<!ELEMENT Content (#PCDATA)>
<!ATTLIST Content Value CDATA #REQUIRED
>
    '''

    with open('C:\\Users\\Papi\\Desktop\\MOVOD\\files\\ADI.txt', 'w') as file:
        file.write(text)
        
    os.rename('C:\\Users\\Papi\\Desktop\\MOVOD\\files\\ADI.txt',
              'C:\\Users\\Papi\\Desktop\\MOVOD\\files\\ADI.dtd')
    print('adi created')



#dtd_creator()
