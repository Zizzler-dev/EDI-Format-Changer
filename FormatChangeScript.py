from tabnanny import check
from typing import final
import streamlit as st
import pandas as pd
from datetime import date
import numpy as np
from datetime import datetime

st.image('zizzl health logo 22.png')

st.title("Format Changer")

st.subheader("Upload CSV Here:")
csv = st.file_uploader("Upload CSV:")


us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}

format_change = st.selectbox('Pick one' , ['DBS FSA', 'DBS HRA Funding', 'DBS HRA Enrollment', 'ECHO Import'])
if csv is not None:
    csv_df = pd.read_csv(csv)
    #st.write(csv_df)

    if(format_change == 'DBS FSA'):
        csv_df = csv_df.rename(columns = {"FEIN":"Client Federal ID", "EE SSN":"Participant Number","First Name":"Participant First Name","Middle Name":"Participant Middle Initial","Last Name":"Participant Last Name","Address Line 1":"Participant Address 1","Address Line 2":"Participant Address 2","City":"Participant City","State":"Participant State","Zip":"Participant Zip Code","EE Email":"Participant Email Address", "EE Date of Birth":"Participant Date of Birth", "Home Phone":"Participant Phone","Benefit Plan Name":"Plan Type Code","Coverage Effective Date":"Enrollment Effective Date","FSA Coverage Amount":"Pay Period Amount"})

        csv_df.insert(2, 'Participant Number Type', 1) #Participant Number Type
        csv_df.insert(13, 'Payroll Mode', 'M') #Payroll Mode
        csv_df.insert(17, 'Effective Posting  Date', csv_df['Enrollment Effective Date']) #Effective Posting Date
        csv_df.insert(20, 'Annual Election', csv_df['Pay Period Amount'].replace( '[\$,)]','', regex=True ).astype(float)) #Effective Posting Date
        csv_df.insert(21, 'Funding Type', 1) #Funding Type
        csv_df.insert(22, 'Employer Funding Code', ' ') #Funding Type
        csv_df.insert(23, 'COBRA Effective Date', ' ') #COBRA Effective Date
        csv_df.insert(24, 'COBRA Termination Date', ' ') #Funding Type
        csv_df.insert(25, 'Participant Other Number', ' ') #Participant Other Number
        csv_df.insert(26, 'Debit Card Enrollment', 0) #Debit Card Enrollmente
        csv_df.insert(27, 'Auto Reimbursement', 0) #Auto Reimbursement
        csv_df.insert(28, 'Direct Deposit - Bank Routing Number', ' ') #Funding Type
        csv_df.insert(29, 'Direct Deposit - Bank Account Number', ' ') #Funding Type
        csv_df.insert(30, 'Direct Deposit - Bank Account Type Code', ' ') #Funding Type
        csv_df.insert(31, 'Enrolled in HSA', ' ') #Funding Type
        csv_df.insert(32, 'Post Deductible Coverage', ' ') #Funding Type



        for i in csv_df.index: # FEIN

            if(csv_df["Annual Election"][i] > 999.99):
                csv_df["Pay Period Amount"][i] = csv_df["Annual Election"][i]

            csv_df['Annual Election'][i] = csv_df['Annual Election'][i] * 12

            if(csv_df["Annual Election"][i] <= 999.99):
                csv_df['Annual Election'][i] = '$' + str(csv_df['Annual Election'][i])


            csv_df['Client Federal ID'][i] = str(csv_df['Client Federal ID'][i]).translate({ord(i): None for i in '-'}) 


            csv_df['Participant Number'][i] = str(csv_df['Participant Number'][i]).translate({ord(i): None for i in '-'})


            if not(pd.isnull(csv_df['Participant Middle Initial'][i])):
                csv_df['Participant Middle Initial'][i] = str(csv_df['Participant Middle Initial'][i])[:1]


            csv_df['Participant Address 1'][i] = str(csv_df['Participant Address 1'][i]).translate({ord(i): None for i in ','})

            if not(pd.isnull(csv_df['Participant Middle Initial'][i])):
                csv_df['Participant Address 2'][i] = str(csv_df['Participant Address 2'][i]).translate({ord(i): None for i in ','})

            csv_df['Participant Date of Birth'][i] = str(csv_df['Participant Date of Birth'][i]).replace("0:00", "")

            newDate = ''.join(i.zfill(2) for i in csv_df['Participant Date of Birth'][i].split('/'))

            newDate = newDate[:2] + '/' + newDate[2:4] + '/' + newDate[4:]

            csv_df['Participant Date of Birth'][i] = newDate
            
            if(csv_df['Participant State'][i] in us_state_to_abbrev): 
                csv_df['Participant State'][i] = us_state_to_abbrev.get(csv_df['Participant State'][i])

        csv_df = csv_df.replace('nan', '').fillna('')
        #st.write(csv_df)

        

        st.download_button(
            label = "Download data as CSV",
            data = csv_df.to_csv(index = False).encode('utf-8'),
            file_name = 'DBS_FSA.csv',
            mime='text'
        )
    
    elif(format_change == 'DBS HRA Funding'):
        now = datetime.now()
        #new_date = str(now.month) + '/' + str(now.day) + '/' + str(now.year)
        new_date = [now.year, now.month, now.day ]
        csv_df = csv_df.rename(columns = {"FEIN":"Client Federal ID", "EE SSN":"Participant SSN","ICHRA Left Over Funds":"Funding Amounts","HSA Eligible":"Plan Code"})
        csv_df.insert(1, 'Benefit Plan Type', 105) 
        csv_df.insert(3, 'Participant Number Type', 1) 
        csv_df.insert(4, 'Funding Date', 1 ) 
        csv_df.insert(6, 'Funding Category', 1)
        del csv_df['Benefit Plan Name']
        del csv_df['Coverage Effective Date']
        del csv_df['Coverage End Date']
        

        for i in csv_df.index:
            csv_df['Client Federal ID'][i] = str(csv_df['Client Federal ID'][i]).translate({ord(i): None for i in '-'}) 
            csv_df['Participant SSN'][i] = str(csv_df['Participant SSN'][i]).translate({ord(i): None for i in '-'}) 
            csv_df['Funding Amounts'][i] = str(csv_df['Funding Amounts'][i])

            if (csv_df['Plan Code'][i] == True):
                csv_df['Plan Code'][i] = 2
            else:
                csv_df['Plan Code'][i] = 1

            if(new_date[2] != '01'):
                new_date[1] += 1
                if(new_date[1] > 12):
                    new_date[1] = 1
                new_date[2] = '01'

            csv_df["Funding Date"][i] = str(new_date[1]) + '/' + str(new_date[2]) + '/' + str(new_date[0])


        
        csv_df = csv_df.replace('nan', '').fillna('')
        st.write(csv_df)

        st.download_button(
            label = "Download data as CSV",
            data = csv_df.to_csv(index = False).encode('utf-8'),
            file_name = 'DBS_HRA_Funding.csv',
            mime='text'
        )
    
    elif(format_change == 'DBS HRA Enrollment'):
        csv_df = csv_df.rename(columns = {"FEIN":"Client Federal ID", "SSN":"Participant Number","Middle Name":"Middle Initial","Home Phone":"Participant Phone", "Address Line 1": "Participant Address 1", "Address Line 2": "Participant Address 2", "City": "Participant City", "State":"Participant State", "Zip": "Participant Zip Code", "EE Email": "Participant Email Address", "Coverage Effective Date": "Effective Date", "Termination Date": "Termination or Retirement Date"})
        csv_df.insert(2, 'Participant Number Type', 1)
        csv_df.insert(3, 'Dependent Number', '')
        csv_df.insert(15, 'Enroll Plan Type Code', '')
        csv_df.insert(16, 'Enroll Coverage Type Code', '')
        csv_df.insert(19, 'Cobra or Retirement Effective Date', '')
        csv_df.insert(20, 'Cobra or Retirement Termination Date', '')
        csv_df.insert(21, 'Other ID Number', '')
        csv_df.insert(23, 'Debit Card Enrollment', 0)
        csv_df.insert(24, 'Auto Reimbursement', 0)
        csv_df.insert(25, 'Medicare Eligible', '')
        csv_df.insert(26, 'ESRD', '')
        csv_df.insert(28, 'Relationship', 0)
        csv_df.insert(29, 'HIC Number', '')
        csv_df.insert(30, 'Coordination of Benefits', '')

        for i in csv_df.index:
            csv_df['Client Federal ID'][i] = str(csv_df['Client Federal ID'][i]).translate({ord(i): None for i in '-'}) 
            csv_df['Participant Number'][i] = str(csv_df['Participant Number'][i]).translate({ord(i): None for i in '-'}) 

            csv_df['Participant Address 1'][i] = str(csv_df['Participant Address 1'][i]).translate({ord(i): None for i in ','})
            csv_df['Participant Address 2'][i] = str(csv_df['Participant Address 2'][i]).translate({ord(i): None for i in ','})

            if(csv_df['Participant State'][i] in us_state_to_abbrev): 
                csv_df['Participant State'][i] = us_state_to_abbrev.get(csv_df['Participant State'][i])

            if not(pd.isnull(csv_df['Middle Initial'][i])):
                csv_df['Middle Initial'][i] = str(csv_df['Middle Initial'][i])[:1]

        csv_df = csv_df.replace('nan', '').fillna('')
        st.write(csv_df)

        st.download_button(
            label = "Download data as CSV",
            data = csv_df.to_csv(index = False).encode('utf-8'),
            file_name = 'DBS_HRA_Enrollment.csv',
            mime='text'
        )

    elif(format_change == 'ECHO Import'):
        csv_df = csv_df.rename(columns = {"Employee ID": "Employee Unique ID", "EE First Name": "First Name", "EE Last Name": "Last Name", "EE State": "State", "Coverage Effective Date": "Coverage Start Date", "Total Premium": "Premium", "Vendor Import Code": "Vendor Code", "Benefit Plan Name": "Plan"})
        
        for i in csv_df.index:
            csv_df['FEIN'][i] = str(csv_df['FEIN'][i]).translate({ord(i): None for i in '-'}) 

            if(csv_df['State'][i] in us_state_to_abbrev): 
                csv_df['State'][i] = us_state_to_abbrev.get(csv_df['State'][i])
        
        st.write(csv_df)
        st.download_button(
            label = "Download data as CSV",
            data = csv_df.to_csv(index = False).encode('utf-8'),
            file_name = 'ECHO_Import.csv',
            mime='text'
        )
