import streamlit as st
import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup
import math

def getDataset1():    
    # web sracpe
    url = "https://www.worldometers.info/coronavirus/country/us/"
    res = requests.get(url)
    
    data = {}
    state_case_info = {}
    state_death_info = {}
    
    # find table contents
    soup = BeautifulSoup(res.content, 'html.parser')
    table_result = soup.find('tbody')
    trs = table_result.find_all('tr')
    
    # scrape data
    tr_cnt = 0
    
    for row in trs:
        tds = row.find_all('td')
        td_list = []
        for td in tds:
            td_list.append(td.text)
        
        if(tr_cnt != 0) :
            state = td_list[1][1:]
            total_case = td_list[2]
            new_case = td_list[3][2:]
            total_death = td_list[4][1:]
            new_death = td_list[5][1:]
            
            if(new_case == '' or new_case == ' ' or new_case ==  '\n'):
                new_case = '0'
                
            if(new_death == '' or new_death == ' ' or new_death ==  '\n'):
                new_death = '0'
            
            # export cleaned dataset
            data[state] = [int(total_case.replace(',', '')), int(new_case.replace(',', '')), int(total_death.replace(',', '')), int(new_death.replace(',', ''))]
            state_case_info[state] = int(total_case.replace(',', ''))
            state_death_info[state] = int(total_death.replace(',', ''))
        
        tr_cnt = tr_cnt + 1
        
    sorted_case = sorted(state_case_info.items(), key = lambda item: item[1], reverse = True)
    sorted_death = sorted(state_death_info.items(), key = lambda item: item[1], reverse = True)

    case_temp = []
    for case in sorted_case:
        case_temp.append([case[0], case[1]])
    
    case_tb = pd.DataFrame(case_temp)
    case_tb.columns = ["state", 'total_case']

    death_temp = []
    for death in sorted_death:
        death_temp.append([death[0], death[1]])
    
    death_tb = pd.DataFrame(death_temp)
    death_tb.columns = ["state", 'total_death']

    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    st.bar_chart(chart_data)

def getDataset2():
    # API Read
    # API key: e898e47cb4434fc6aa046f8881836e01
    url = "https://api.covidactnow.org/v2/states.csv?apiKey=e898e47cb4434fc6aa046f8881836e01"
    csvData = pd.read_csv(url, encoding='cp949')
    vaccineData = csvData[['state', 'actuals.vaccinesDistributed', 'actuals.vaccinationsInitiated', 'actuals.vaccinationsCompleted', 'metrics.vaccinationsInitiatedRatio', 'metrics.vaccinationsCompletedRatio']]
    
    # file open
    f_w = open('vaccinated_cleaned.csv', 'w', encoding="UTF-8", newline='')
    wr = csv.writer(f_w)
    
    # data cleaning
    # print('state', 'vaccineDistributed', 'vaccineInitiated', 'vaccineCompleted', 'vaccineInitiatedRatio', 'vaccineCompleteRatio')
    wr.writerow(['state', 'vaccineDistributed', 'vaccineInitiated', 'vaccineCompleted', 'vaccineInitiatedRatio', 'vaccineCompleteRatio'])
    
    for i in range(vaccineData.shape[0]):
        state = vaccineData.loc[i]['state']
        vaccineDistributed = vaccineData.loc[i]['actuals.vaccinesDistributed']
        vaccineInitiated = vaccineData.loc[i]['actuals.vaccinationsInitiated']
        vaccineCompleted = vaccineData.loc[i]['actuals.vaccinationsCompleted']
        vaccineInitiatedRatio = vaccineData.loc[i]['metrics.vaccinationsInitiatedRatio']
        vaccineCompleteRatio = vaccineData.loc[i]['metrics.vaccinationsCompletedRatio']
    
        if (math.isnan(vaccineData.loc[i]['actuals.vaccinesDistributed'])) :
            vaccineDistributed = 0
            
        if (math.isnan(vaccineData.loc[i]['actuals.vaccinationsInitiated'])) :
            vaccineInitiated = 0
        
        if (math.isnan(vaccineData.loc[i]['actuals.vaccinationsCompleted'])) :
            vaccineCompleted = 0
        
        if (math.isnan(vaccineData.loc[i]['metrics.vaccinationsInitiatedRatio'])) :
            vaccineInitiatedRatio = 0
            
        if (math.isnan(vaccineData.loc[i]['metrics.vaccinationsCompletedRatio'])) :
            vaccineCompleteRatio = 0
        
        # export cleaned dataset
        # print(state, vaccineDistributed, vaccineInitiated, vaccineCompleted, vaccineInitiatedRatio, vaccineCompleteRatio)
        wr.writerow([state, vaccineDistributed, vaccineInitiated, vaccineCompleted, vaccineInitiatedRatio, vaccineCompleteRatio])
    
    # print("Cleaned Dataset \"vaccinated_cleaned.csv\" is exported")

def getDataset3():
    # Public API Read
    url = "https://api.covidtracking.com/v1/states/current.csv"
    csvData = pd.read_csv(url, encoding='cp949')
    stateData = csvData[['state', 'positive', 'probableCases', 'negative', 'hospitalizedCurrently']]
    # file open
    f_w = open('state_metadata_cleaned.csv', 'w', encoding="UTF-8", newline='')
    wr = csv.writer(f_w)
    
    # data cleaning
    print('state', 'positive', 'probableCases', 'negative', 'hospitalizedCurrently')
    wr.writerow(['state', 'positive', 'probableCases', 'negative', 'hospitalizedCurrently'])
    
    for i in range(stateData.shape[0]):
        state = stateData.loc[i]['state']
        positive = stateData.loc[i]['positive']
        probableCases = stateData.loc[i]['probableCases']
        negative = stateData.loc[i]['negative']
        hospitalizedCurrently = stateData.loc[i]['hospitalizedCurrently']
    
        if (math.isnan(positive)) :
            positive = 0
            
        if (math.isnan(probableCases)) :
            probableCases = 0
        
        if (math.isnan(negative)) :
            negative = 0
        
        if (math.isnan(hospitalizedCurrently)) :
            hospitalizedCurrently = 0
            
        
        # export cleaned dataset
        print(state, positive, probableCases, negative, hospitalizedCurrently)
        wr.writerow([state, positive, probableCases, negative, hospitalizedCurrently])
    
    print("Cleaned Dataset \"state_metadata_cleaned.csv\" is exported")

def mergeDataset():
    state_abbr = {'CA' : 'California', 'TX' : 'Texas', 'FL' : 'Florida', 'NY' : 'New York', 'IL' : 'Illinois', 'PA' : 'Pennsylvania', 'OH' : 'Ohio', 'NC' : 'North Carolina', 'GA' : 'Georgia', 'MI' : 'Michigan', 'NJ' : 'New Jersey', 'TN' : 'Tennessee', 'AZ' : 'Arizona', 'MA' : 'Massachusetts', 'IN' : 'Indiana', 'VA' : 'Virginia', 'WI' : 'Wisconsin', 'WA' : 'Washington', 'SC' : 'South Carolina', 'MN' : 'Minnesota', 'MO' :  'Missouri', 'CO' : 'Colorado', 'KY' : 'Kentucky', 'AL' : 'Alabama', 'LA' : 'Louisiana', 'OK' : 'Oklahoma', 'MD' : 'Maryland', 'UT' : 'Utah', 'IA' : 'Iowa', 'AR' : 'Arkansas', 'MS' : 'Mississippi', 'KS' : 'Kansas', 'CT' : 'Connecticut', 'NV' : 'Nevada', 'OR' : 'Oregon', 'NM' : 'New Mexico', 'WV' : 'West Virginia', 'NE' : 'Nebraska', 'ID' : 'Idaho', 'RI' : 'Rhode Island', 'NH' : 'New Hampshire', 'MT' : 'Montana', 'DE' : 'Delaware', 'HI' : 'Hawaii', 'AK' : 'Alaska', 'ME' : 'Maine', 'ND' : 'North Dakota', 'SD' : 'South Dakota', 'WY' : 'Wyoming', 'DC' : 'District Of Columbia', 'VT' : 'Vermont'}

    f_r1 = open('web_scrape_states_covid_info_cleaned.csv', 'r', encoding="UTF-8")
    f_r2 = open('vaccinated_cleaned.csv', 'r', encoding="UTF-8")
    f_r3 = open('state_metadata_cleaned.csv', 'r', encoding="UTF-8")
    
    rdr1 = csv.reader(f_r1)
    rdr2 = csv.reader(f_r2)
    rdr3 = csv.reader(f_r3)

    state_info = {}
    for line in rdr1:
        if(line[0] != 'state'):
            total_case = int(line[1].replace(',',''))
            new_case = 0
            if (line[2] != '') :
                new_case = int(line[2].replace(',',''))
            total_death = int(line[3].replace(',',''))
            new_death = 0
            if (line[2] != '') :
                new_death = int(line[4].replace(',',''))

            death_rate = total_death / total_case * 100
            state_info[line[0]] = [total_case, new_case, total_death, new_death, death_rate]


    for line in rdr2:
        if line[0] in state_abbr:
            state_info[state_abbr[line[0]]+ " "].append(float(line[1]))
            state_info[state_abbr[line[0]]+ " "].append(float(line[2]))
            state_info[state_abbr[line[0]]+ " "].append(float(line[3]))
            state_info[state_abbr[line[0]]+ " "].append(float(line[4]) * 100)
            state_info[state_abbr[line[0]]+ " "].append(float(line[5]) * 100)

    for line in rdr3:
        if(line[0] != 'state' and line[0] != 'AS' and line[0] != 'GU' and line[0] != 'MP' and line[0] != 'PR' and line[0] != 'VI'):
            state_info[state_abbr[line[0]]+ " "].append(float(line[1]))
            state_info[state_abbr[line[0]]+ " "].append(float(line[2]))
            state_info[state_abbr[line[0]]+ " "].append(float(line[3]))
            state_info[state_abbr[line[0]]+ " "].append(float(line[4]))

    sorted_state = sorted(state_info.items(), key = lambda item: item[1], reverse = True)
    temp = []
    for state in sorted_state:
        if(state[0] != "USA Total") :
            temp.append([state[0], state[1][0], state[1][1], state[1][2], state[1][3], state[1][4], state[1][5], state[1][6], state[1][7], state[1][8], state[1][9], state[1][10], state[1][11], state[1][12], state[1][13]])
    
    tb = pd.DataFrame(temp)
    tb.columns = ["state", 'total_case', 'new_case', 'total_death', 'new_death', 'death_rate', 'vaccineDistributed','vaccineInitiated','vaccineCompleted','vaccineInitiatedRatio','vaccineCompleteRatio', 'positive','probableCases','negative','hospitalizedCurrently']
    # print("Sorted in Descending Order (Total Case)")
    # print(tb)
    tb.to_csv('Choi_Silvia_proj2.csv', sep=',')
         
    f_r1.close()
    f_r2.close()
    f_r3.close()

def show_intro():
    st.write("""
    Introduction
    """)
def show_explorer():
    st.write("""
    Explorer
    """)
    getDataset1()
def show_conclusions():
    st.write("""
    conclusion
    """)
def show_research_objectives():
    st.write("""
    4. The objective of my project was to explore the effectiveness of vaccinations in influencing mortality rates due to COVID-19 across different states. The datasets I chose included:

    Dataset 1: Total cases and deaths per state.
    Dataset 2: Vaccination data by state.
    Dataset 3: Positive/negative case rates and hospitalization durations by state.
    I aimed to investigate whether there was a correlation between vaccination rates and total deaths, suggesting the effectiveness of vaccines in reducing mortality rates from COVID-19.
    
    5. The analysis revealed that vaccination does not have a significant effect on the death rate from COVID-19. This finding suggests that while vaccines are critical in controlling the spread of the disease and reducing severe outcomes, other factors may also significantly influence mortality rates.
    
    6. The project was quite challenging as it was my first experience working through such a structured data science workflow from data acquisition to deploying a web application. Identifying and integrating three different datasets that were relevant to my research question proved particularly difficult. Additionally, building a web application to showcase the results was a new and challenging task.
    
    7. Throughout the project, I felt that stronger coding skills, particularly in data manipulation and web application development, would have made the process smoother. Additionally, more experience in selecting and utilizing datasets that support specific research topics would have been beneficial.
    
    8. To expand the project, I would like to incorporate datasets on the economic aspects of vaccination, such as the cost of vaccines. Analyzing whether financial factors influence vaccination rates could provide deeper insights into public health strategies and vaccine uptake.
    """)

# Main app structure
st.title("Corona Virus Data Explorer")
page = st.sidebar.selectbox("Choose a page", ["Introduction", "Data Explorer", "Conclusions", "Research Objectives"])

if page == "Introduction":
    show_intro()
elif page == "Data Explorer":
    show_explorer()
elif page == "Conclusions":
    show_conclusions()
elif page == "Research Objectives":
    show_research_objectives()

# getDataset1()
# getDataset2()
# getDataset3()

# mergeDataset()

# st.write("""# Author Information
# name: Silvia Choi
# """)
