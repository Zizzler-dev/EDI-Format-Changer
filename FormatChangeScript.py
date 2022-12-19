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

def fill_date(date):
    newDate = ''.join(i.zfill(2) for i in date.split('/'))

    newDate = newDate[:2] + '/' + newDate[2:4] + '/' + newDate[4:]

    return str(newDate)

def keep_format(column):
    column = column.apply('="{}"'.format)
    #st.write(column)
    return column


format_change = st.selectbox('Pick one' , ['DBS FSA', 'DBS HRA Funding', 'DBS HRA Enrollment', 'DBS HSA'])
if csv is not None:
    csv_df = pd.read_csv(csv)
    

    if(format_change == 'DBS FSA'):
        csv_df = csv_df.rename(columns = {"FEIN":"Client Federal ID", "SSN":"Participant Number","First Name":"Participant First Name","Middle Name":"Participant Middle Initial","Last Name":"Participant Last Name","Address Line 1":"Participant Address 1","Address Line 2":"Participant Address 2","City":"Participant City","State":"Participant State","Zip":"Participant Zip Code","EE Email":"Participant Email Address", "EE Date of Birth":"Participant Date of Birth", "Home Phone":"Participant Phone","Pay Frequency": "Payroll Mode", "Benefit Plan Sub Code 1":"Plan Type Code","Coverage Effective Date":"Enrollment Effective Date","FSA Monthly Amount":"Pay Period Amount", "FSA Elected Amount": "Annual Election"})

        csv_df.insert(2, 'Participant Number Type', 1) #Participant Number Type
        csv_df.insert(2, 'Location', '') #Participant Number Type
        #csv_df.insert(14, 'Payroll Mode', 'M') #Payroll Mode
        csv_df.insert(18, 'Effective Posting  Date', None) #Effective Posting Date
        #csv_df.insert(20, 'Annual Election', csv_df['Pay Period Amount'].replace( '[\$,)]','', regex=True ).astype(float)) 
        csv_df.insert(21, 'Funding Type', 1) #Funding Type
        csv_df.insert(22, 'Employer Funding Code', '') #Funding Type
        csv_df.insert(24, 'COBRA Effective Date', '') #COBRA Effective Date
        csv_df.insert(25, 'COBRA Termination Date', '') #Funding Type
        csv_df.insert(26, 'Participant Other Number', '') #Participant Other Number
        csv_df.insert(27, 'Debit Card Enrollment', 0) #Debit Card Enrollment
        csv_df.insert(28, 'Auto Reimbursement', 0) #Auto Reimbursement
        csv_df.insert(29, 'Direct Deposit - Bank Routing Number', '') #Funding Type
        csv_df.insert(30, 'Direct Deposit - Bank Account Number', '') #Funding Type
        csv_df.insert(31, 'Direct Deposit - Bank Account Type Code', 0) #Funding Type
        csv_df.insert(32, 'Enrolled in HSA', 0) #Funding Type
        csv_df.insert(33, 'Post Deductible Coverage', 0) #Funding Type

        

        csv_df = csv_df.reindex(columns = ['Client Federal ID', 'Participant Number', 'Participant Number Type', 'Participant First Name', 'Participant Middle Initial', 'Participant Last Name', 'Participant Address 1', 'Participant Address 2', 'Participant City', 'Participant State', 'Participant Zip Code', 'Participant Email Address', 'Participant Date of Birth', 'Participant Phone', 'Payroll Mode', 'Location', 'Plan Type Code', 'Enrollment Effective Date', 'Effective Posting Date', 'Pay Period Amount', 'Annual Election', 'Funding Type', 'Employer Funding Code', 'Termination Date', 'COBRA Effective Date','COBRA Termination Date', 'Participant Other Number', 'Debit Card Enrollment', 'Auto Reimbursement', 'Direct Deposit - Bank Routing Number', 'Direct Deposit - Bank Account Number', 'Direct Deposit - Bank Account Type Code', 'Enrolled in HSA', 'Post Deductible Coverage' ])

        csv_df['Effective Posting Date'] = csv_df['Effective Posting Date'].fillna(csv_df['Enrollment Effective Date'])
       

        st.write(csv_df)
        for i in csv_df.index: # iterate through entire dataframe

            if(csv_df['Payroll Mode'][i] == 'Bi-Weekly (26 per year)'):                         #This if-else loop is used to calculate pay period amount
                csv_df['Payroll Mode'][i] = 'B'
                csv_df['Pay Period Amount'][i] = round(csv_df['Annual Election'][i] / 26, 2)
            elif(csv_df['Payroll Mode'][i] == 'Semi-Monthly (24 per year)'):
                csv_df['Payroll Mode'][i] = 'S'
                csv_df['Pay Period Amount'][i] = round(csv_df['Annual Election'][i] / 24, 2)
            elif(csv_df['Payroll Mode'][i] == 'Weekly (52 per year)'):
                csv_df['Payroll Mode'][i] = 'W'
                csv_df['Pay Period Amount'][i] = round(csv_df['Annual Election'][i] / 52, 2)
            elif(csv_df['Payroll Mode'][i] == 'Monthly (12 per year)'):
                csv_df['Payroll Mode'][i] = 'M'
                csv_df['Pay Period Amount'][i] = round(csv_df['Annual Election'][i] / 12, 2)

            if(csv_df['Plan Type Code'][i] == 2 or csv_df['Plan Type Code'][i] == 4):
                csv_df['Debit Card Enrollment'][i] = 1
            
            csv_df['Pay Period Amount'][i] = str(csv_df['Pay Period Amount'][i]).replace(',', '') #remove commas

            csv_df['Annual Election'][i] = str(csv_df['Annual Election'][i]).replace(',', '') #remove commas


            csv_df['Client Federal ID'][i] = str(csv_df['Client Federal ID'][i]).translate({ord(i): None for i in '-'}) 


            csv_df['Participant Number'][i] = str(csv_df['Participant Number'][i]).translate({ord(i): None for i in '-'})


            if not(pd.isnull(csv_df['Participant Middle Initial'][i])):
                csv_df['Participant Middle Initial'][i] = str(csv_df['Participant Middle Initial'][i])[:1]


            csv_df['Participant Address 1'][i] = str(csv_df['Participant Address 1'][i]).translate({ord(i): None for i in ','})

            if not(pd.isnull(csv_df['Participant Middle Initial'][i])):
                csv_df['Participant Address 2'][i] = str(csv_df['Participant Address 2'][i]).translate({ord(i): None for i in ','})

            csv_df['Participant Date of Birth'][i] = str(csv_df['Participant Date of Birth'][i]).replace("0:00", "")

            csv_df['Participant Date of Birth'][i] = fill_date(csv_df['Participant Date of Birth'][i])
            csv_df['Enrollment Effective Date'][i] = fill_date(csv_df['Enrollment Effective Date'][i])
            csv_df['Effective Posting Date'][i] = fill_date(csv_df['Effective Posting Date'][i])

            
            if(csv_df['Participant State'][i] in us_state_to_abbrev): 
                csv_df['Participant State'][i] = us_state_to_abbrev.get(csv_df['Participant State'][i])
            
            if(csv_df['Client Federal ID'][i] == '462655923'):
                csv_df['Client Federal ID'][i] = '391753459'
                csv_df['Location'][i] = 'Forest Grove'
            elif(csv_df['Client Federal ID'][i] == '411332521'):
                csv_df['Client Federal ID'][i] = '410627744'
                csv_df['Location'][i] = 'Wall Companies'

        csv_df = csv_df.replace('nan', '').fillna('')

        csv_df['Annual Election'] = csv_df['Annual Election'].astype(float)
        csv_df['Pay Period Amount'] = csv_df['Pay Period Amount'].astype(float)
        csv_df['Annual Election'] = csv_df['Annual Election'].map('{:.2f}'.format)
        csv_df['Pay Period Amount'] = csv_df['Pay Period Amount'].map('{:.2f}'.format)

        csv_df['Participant Date of Birth'] = keep_format(csv_df['Participant Date of Birth'])
        csv_df['Enrollment Effective Date'] = keep_format(csv_df['Enrollment Effective Date'])
        csv_df['Effective Posting Date'] = keep_format(csv_df['Effective Posting Date'])
        
        csv_df['Annual Election'] = keep_format(csv_df['Annual Election'])
        csv_df['Pay Period Amount'] = keep_format(csv_df['Pay Period Amount'])

        csv_df = csv_df.astype('str')
        st.write(csv_df)

        

        st.download_button(
            label = "Download data as CSV",
            data = csv_df.to_csv(index = False).encode('utf-8'),
            file_name = 'DBS_FSA.csv',
            mime='text'
        )
    
    elif(format_change == 'DBS HRA Funding'):
        #now = datetime.now()
        #new_date = [now.year, now.month, now.day ]
        #st.write(new_date[2])
        #if(new_date[2] != 1):
        #    new_date[1] = new_date[1] + 1
        #    if(new_date[1] > 12):
        #        new_date[1] = 1
        #    new_date[2] = 1
        #new_date = str(now.month) + '/' + str(now.day) + '/' + str(now.year)
        new_date = '01/01/2023'
        #st.write(keep_format(new_date))


        csv_df = csv_df.rename(columns = {"FEIN":"Client Federal ID", "EE SSN":"Participant SSN","ICHRA Left Over Funds":"Funding Amount","HSA Eligible":"Plan Code"})
        csv_df.insert(1, 'Benefit Plan Type', 105) 
        csv_df.insert(3, 'Participant Number Type', 1) 
        csv_df.insert(4, 'Funding Date', new_date) 
        csv_df.insert(6, 'Funding Category', 1)

        csv_df = csv_df[csv_df['Funding Amount'] > 0]    
        #st.write(csv_df['Funding Amount'][2])
        for i in csv_df.index:
            #if(csv_df['Funding Amount'][i] == 0):
            #    csv_df.drop([csv_df.index[i]])
            csv_df['Client Federal ID'][i] = str(csv_df['Client Federal ID'][i]).translate({ord(i): None for i in '-'}) 
            csv_df['Participant SSN'][i] = str(csv_df['Participant SSN'][i]).translate({ord(i): None for i in '-'}) 
            csv_df['Funding Amount'][i] = str(csv_df['Funding Amount'][i])

            if (csv_df['Plan Code'][i] == True):
                csv_df['Plan Code'][i] = 'HSA Plan'
            else:
                csv_df['Plan Code'][i] = 'Non HSA Plan'

            csv_df['Funding Date'][i] = fill_date(csv_df['Funding Date'][i])

            if(csv_df['Client Federal ID'][i] == '462655923'):
                csv_df['Client Federal ID'][i] = '391753459'
                csv_df['Location'][i] = 'Forest Grove'
            elif(csv_df['Client Federal ID'][i] == '411332521'):
                csv_df['Client Federal ID'][i] = '410627744'
                csv_df['Location'][i] = 'Wall Companies'


        csv_df['Participant SSN'] = csv_df['Participant SSN'].astype(str)
        csv_df['Client Federal ID'] = csv_df['Client Federal ID'].astype(str)
        csv_df['Funding Amount'] = csv_df['Funding Amount'].astype(float)
        csv_df['Funding Amount'] = csv_df['Funding Amount'].map('{:.2f}'.format)
        csv_df['Funding Amount'] = keep_format(csv_df['Funding Amount'])
        csv_df['Participant SSN'] = keep_format(csv_df['Participant SSN'])
        csv_df['Client Federal ID'] = keep_format(csv_df['Client Federal ID'])
        csv_df['Funding Date'] = keep_format(csv_df['Funding Date'])
        
        csv_df = csv_df.replace('nan', '').fillna('')
        st.write(csv_df)

        st.download_button(
            label = "Download data as CSV",
            data = csv_df.to_csv(index = False).encode('utf-8'),
            file_name = 'DBS_HRA_Funding.csv',
            mime='text'
        )
    
    elif(format_change == 'DBS HRA Enrollment'):
        csv_df = csv_df.rename(columns = {"FEIN":"Client Federal ID", "EE SSN":"Participant Number","Middle Name":"Middle Initial","Home Phone":"Participant Phone", "Address Line 1": "Participant Address 1", "Address Line 2": "Participant Address 2", "City": "Participant City", "State":"Participant State", "Zip": "Participant Zip Code", "EE Email": "Participant Email Address", "Coverage Effective Date": "Effective Date", "Termination Date": "Termination or Retirement Date", "HSA Eligible": "Enroll Plan Type Code", "Benefit Plan Type ID":"Enroll Coverage Type Code", "SSN": "Dependent Number"})
        csv_df.insert(2, 'Participant Number Type', 1)
        #csv_df.insert(3, 'Dependent Number', '')
        csv_df.insert(19, 'Cobra or Retirement Effective Date', '')
        csv_df.insert(20, 'Cobra or Retirement Termination Date', '')
        csv_df.insert(21, 'Other ID Number', '')
        csv_df.insert(23, 'Debit Card Enrollment', 0)
        csv_df.insert(24, 'Auto Reimbursement', 0)
        csv_df.insert(25, 'Medicare Eligible', '')
        csv_df.insert(26, 'ESRD', '')
        #csv_df.insert(28, 'Relationship', 0)
        csv_df.insert(29, 'HIC Number', '')
        csv_df.insert(30, 'Coordination of Benefits', 0)
        csv_df.insert(31, 'Termination Reason', '')

        csv_df['Participant Zip Code'] = csv_df['Participant Zip Code'].apply('{:0>5}'.format)
        st.write(csv_df)
        #st.write(csv_df['Participant Number'][3])

        for i in csv_df.index:
            
            csv_df['Client Federal ID'][i] = str(csv_df['Client Federal ID'][i]).translate({ord(i): None for i in '-'}) 
            csv_df['Participant Number'][i] = str(csv_df['Participant Number'][i]).translate({ord(i): None for i in '-'}) 
            csv_df['Dependent Number'][i] = str(csv_df['Dependent Number'][i]).translate({ord(i): None for i in '-'})

            csv_df['Participant Address 1'][i] = str(csv_df['Participant Address 1'][i]).translate({ord(i): None for i in ','})
            csv_df['Participant Address 2'][i] = str(csv_df['Participant Address 2'][i]).translate({ord(i): None for i in ','})

            if(csv_df['Client Federal ID'][i] == '391988565'):
                csv_df['Debit Card Enrollment'][i] = 1
            
            if(csv_df['Client Federal ID'][i] == '462655923'):
                csv_df['Client Federal ID'][i] = '391753459'
                csv_df['Location'][i] = 'Forest Grove'
            elif(csv_df['Client Federal ID'][i] == '411332521'):
                csv_df['Client Federal ID'][i] = '410627744'
                csv_df['Location'][i] = 'Wall Companies'
            elif(csv_df['Client Federal ID'][i] == '391753459'):
                csv_df['Location'][i] = 'Firstech, Inc'
            elif(csv_df['Client Federal ID'][i] == '410627744'):
                csv_df['Location'][i] = 'Highland Bank'
            
            

            if(csv_df['Participant State'][i] in us_state_to_abbrev): 
                csv_df['Participant State'][i] = us_state_to_abbrev.get(csv_df['Participant State'][i])

            if not(pd.isnull(csv_df['Middle Initial'][i])):
                csv_df['Middle Initial'][i] = str(csv_df['Middle Initial'][i])[:1]

            if(csv_df['Gender'][i] == 'Male'):
                csv_df['Gender'][i] = 'M'
            elif(csv_df['Gender'][i] == 'Female'):
                csv_df['Gender'][i] = 'F'

            if(csv_df['Relationship'][i] == 'Employee'):
                csv_df['Relationship'][i] = 0
                csv_df['Dependent Number'][i] = ''
            elif(csv_df['Relationship'][i] == 'Spouse'):
                csv_df['Relationship'][i] = 1
            elif(csv_df['Relationship'][i] == 'Child'):
                csv_df['Relationship'][i] = 2
            elif(csv_df['Relationship'][i] == 'Domestic Partner'):
                csv_df['Relationship'][i] = 3
            else:
                csv_df['Relationship'][i] = 4

            if(csv_df['Enroll Plan Type Code'][i] == True):
                csv_df['Enroll Plan Type Code'][i] = 'HSA Plan'
            elif(csv_df['Enroll Plan Type Code'][i] == False):
                csv_df['Enroll Plan Type Code'][i] = 'Non HSA Plan'
            
            csv_df['Date of Birth'][i] = fill_date(csv_df['Date of Birth'][i])
            csv_df['Effective Date'][i] = fill_date(csv_df['Effective Date'][i])
            
        
        for j in csv_df.index:
            x = csv_df['Participant Number'][j]
            #csv_df['Enroll Coverage Type Code'][i] = csv_df['Participant Number'].value_counts()[x]
            if(csv_df['Participant Number'].value_counts()[x] == 1):
                csv_df['Enroll Coverage Type Code'][j] = 1
            elif(csv_df['Participant Number'].value_counts()[x] == 2):
                csv_df['Enroll Coverage Type Code'][j] = 2
            elif(csv_df['Participant Number'].value_counts()[x] == 3):
                csv_df['Enroll Coverage Type Code'][j] = 3
            elif(csv_df['Participant Number'].value_counts()[x] >= 4):
                csv_df['Enroll Coverage Type Code'][j] = 4
        
        #for k in csv_df.index:
        #    y = csv_df['Participant Number'][k]
        #    if(csv_df['Relationship'][k] == 'Employee' and int(csv_df['Enroll Coverage Type Code'][k]) >=3):
        #        count = 0
        #        for l in csv_df.index:
        #            if(csv_df['Relationship'][l] == 'Child' and csv_df['Participant Number'][l] == y):
        #                count = count + 1
        #        csv_df['Location'][k] = count


        csv_df = csv_df.replace('nan', '').fillna('')
        csv_df['Participant Number'] = csv_df['Participant Number'].astype(str)
        csv_df['Participant Number'] = keep_format(csv_df['Participant Number'])

        csv_df['Dependent Number'] = csv_df['Dependent Number'].astype(str)
        csv_df['Dependent Number'] = keep_format(csv_df['Dependent Number'])

        csv_df['Client Federal ID'] = csv_df['Client Federal ID'].astype(str)
        csv_df['Client Federal ID'] = keep_format(csv_df['Client Federal ID'])

        csv_df['Participant Zip Code'] = csv_df['Participant Zip Code'].astype(str)
        csv_df['Participant Zip Code'] = keep_format(csv_df['Participant Zip Code'])

        csv_df['Date of Birth'] = keep_format(csv_df['Date of Birth'])
        csv_df['Effective Date'] = keep_format(csv_df['Effective Date'])

        st.write(csv_df)
        

        st.download_button(
            label = "Download data as CSV",
            data = csv_df.to_csv(index = False).encode('utf-8'),
            file_name = 'DBS_HRA_Enrollment.csv',
            mime='text'
        )

    elif(format_change == 'DBS HSA'):
        csv_df = csv_df.rename(columns = {"HSA Elected Amount": "Employee Contribution - Annual Election","FEIN":"Client Federal ID", "EE SSN":"Participant Number","Home Phone":"Participant Phone", "Address Line 1": "Participant Address 1", "Address Line 2": "Participant Address 2", "City": "Participant City", "State":"Participant State", "Zip": "Participant Zip Code", "Coverage Effective Date": "Enrollment Effective Date", "Termination Date": "Termination or Retirement Date", "Date of Birth": "Participant Date of Birth", "Home Phone":"Participant Phone", "Pay Frequency": "Payroll Mode", "First Name":"Participant First Name", "Last Name": "Participant Last Name"})
        
        csv_df.insert(2, 'Participant Number Type', 1)
        csv_df.insert(4, 'Participant Middle Initial', '')
        csv_df.insert(11, 'Participant Email Address', '')
        csv_df.insert(14, 'Location', '')
        csv_df.insert(15, 'Trustee Name', '')
        csv_df.insert(16, 'Insurance Carrier', '')
        csv_df.insert(18, 'Employer Coverage Type Code', 0)
        csv_df.insert(20, 'Employee Contribution - Pay Period Amount', 0)
        #csv_df.insert(21, 'Employee Contribution - Annual Election', 0)
        csv_df.insert(22, 'Termination Date', '')
        csv_df.insert(23, 'COBRA Effective Date', '')
        csv_df.insert(24, 'COBRA Termination Date', '')
        csv_df.insert(25, 'Participant Other Number', '')
        csv_df.insert(26, 'Direct Deposit - Bank Routing Number', '')
        csv_df.insert(27, 'Direct Deposit - Bank Account Number', '')
        csv_df.insert(28, 'Direct Deposit - Bank Account Type Code', 0)
        #csv_df.insert(29, 'Termination Date', '')

        st.write(csv_df)

        

        for i in csv_df.index:

            if(csv_df['Payroll Mode'][i] == 'Bi-Weekly (26 per year)'):                         #This if-else loop is used to calculate pay period amount
                csv_df['Payroll Mode'][i] = 'B'
                csv_df['Employee Contribution - Pay Period Amount'][i] = round(csv_df['Employee Contribution - Annual Election'][i] / 26 , 2)
                
            elif(csv_df['Payroll Mode'][i] == 'Semi-Monthly (24 per year)'):
                csv_df['Payroll Mode'][i] = 'S'
                csv_df['Employee Contribution - Pay Period Amount'][i] = round(csv_df['Employee Contribution - Annual Election'][i] / 24, 2)
                
            elif(csv_df['Payroll Mode'][i] == 'Weekly (52 per year)'):
                csv_df['Payroll Mode'][i] = 'W'
                csv_df['Employee Contribution - Pay Period Amount'][i] = round(csv_df['Employee Contribution - Annual Election'][i] / 52, 2)
                
            elif(csv_df['Payroll Mode'][i] == 'Monthly (12 per year)'):
                csv_df['Payroll Mode'][i] = 'M'
                csv_df['Employee Contribution - Pay Period Amount'][i] = round(csv_df['Employee Contribution - Annual Election'][i] / 12, 2)
                

            csv_df['Client Federal ID'][i] = str(csv_df['Client Federal ID'][i]).translate({ord(i): None for i in '-'}) 
            csv_df['Participant Number'][i] = str(csv_df['Participant Number'][i]).translate({ord(i): None for i in '-'}) 

            csv_df['Participant Address 1'][i] = str(csv_df['Participant Address 1'][i]).translate({ord(i): None for i in ','})
            csv_df['Participant Address 2'][i] = str(csv_df['Participant Address 2'][i]).translate({ord(i): None for i in ','})

            if(csv_df['Participant State'][i] in us_state_to_abbrev): 
                csv_df['Participant State'][i] = us_state_to_abbrev.get(csv_df['Participant State'][i])

            csv_df['Participant Date of Birth'][i] = str(csv_df['Participant Date of Birth'][i])
            csv_df['Client Federal ID'][i] = str(csv_df['Client Federal ID'][i])

            csv_df['Participant Date of Birth'][i] = fill_date(csv_df['Participant Date of Birth'][i])
            csv_df['Enrollment Effective Date'][i] = fill_date(csv_df['Enrollment Effective Date'][i])

            if(csv_df['Client Federal ID'][i] == '462655923'):
                csv_df['Client Federal ID'][i] = '391753459'
                csv_df['Location'][i] = 'Forest Grove'
            elif(csv_df['Client Federal ID'][i] == '411332521'):
                csv_df['Client Federal ID'][i] = '410627744'
                csv_df['Location'][i] = 'Wall Companies'

            

            #if(csv_df['Relationship'][i] == 'Child' or csv_df['Relationship'][i] == 'Spouse' or csv_df['Relationship'][i] == 'Domestic Partner'):
            #    st.write('check')
            #    csv_df.drop([csv_df.index[i]])

        for j in csv_df.index:
            x = csv_df['Participant Number'][j]
            #csv_df['Enroll Coverage Type Code'][i] = csv_df['Participant Number'].value_counts()[x]
            if(csv_df['Participant Number'].value_counts()[x] == 1):
                csv_df['Employer Coverage Type Code'][j] = 1
            elif(csv_df['Participant Number'].value_counts()[x] == 2):
                csv_df['Employer Coverage Type Code'][j] = 2
            elif(csv_df['Participant Number'].value_counts()[x] >= 3):
                csv_df['Employer Coverage Type Code'][j] = 3
        
        csv_df['Client Federal ID'] = csv_df['Client Federal ID'].astype(str)
        csv_df['Client Federal ID'] = keep_format(csv_df['Client Federal ID'])    
        #csv_df['Participant Number'] = csv_df['Participant Number'].astype(str)
        csv_df['Participant Number'] = keep_format(csv_df['Participant Number'])
        csv_df['Participant Date of Birth'] = keep_format(csv_df['Participant Date of Birth'])
        csv_df['Enrollment Effective Date'] = keep_format(csv_df['Enrollment Effective Date'])

        csv_df['Employee Contribution - Pay Period Amount'] = csv_df['Employee Contribution - Pay Period Amount'].astype(float)
        csv_df['Employee Contribution - Pay Period Amount'] = csv_df['Employee Contribution - Pay Period Amount'].map('{:.2f}'.format)
        csv_df['Employee Contribution - Pay Period Amount'] = keep_format(csv_df['Employee Contribution - Pay Period Amount'])

        csv_df['Employee Contribution - Annual Election'] = csv_df['Employee Contribution - Annual Election'].astype(float)
        csv_df['Employee Contribution - Annual Election'] = csv_df['Employee Contribution - Annual Election'].map('{:.2f}'.format)
        csv_df['Employee Contribution - Annual Election'] = keep_format(csv_df['Employee Contribution - Annual Election'])

        csv_df = csv_df.replace('nan', '').fillna('')
        csv_df = csv_df[csv_df['Relationship'] != 'Child'] 
        csv_df = csv_df[csv_df['Relationship'] != 'Spouse'] 
        csv_df = csv_df[csv_df['Relationship'] != 'Domestic Partner'] 
        
        csv_df.drop(['Relationship'], axis=1, inplace=True)

        st.write(csv_df)
        st.download_button(
            label = "Download data as CSV",
            data = csv_df.to_csv(index = False).encode('utf-8'),
            file_name = 'ECHO_Import.csv',
            mime='text'
        )
