import streamlit as st
import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup
import math
import numpy as np
import altair as alt

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

    case_state = []
    case_value = []
    for case in sorted_case:
        case_state.append(case[0])
        case_value.append(case[1])
    
    case_tb = pd.DataFrame(
       {"state": case_state, "total_case": case_value}
    )
    case_tb.columns = ["state", 'total_case']

    death_state = []
    death_value = []
    for death in sorted_death:
        death_state.append(death[0])
        death_value.append(death[1])
    
    death_tb = pd.DataFrame(
       {"state": death_state, "total_death": death_value}
    )
    death_tb.columns = ["state", 'total_death']

    case_chart = alt.Chart(case_tb).mark_bar().encode(
        x=alt.X('state', sort=None),
        y='total_case'
    )

    st.write("""Total Case Data (States)""")
    st.altair_chart(case_chart, use_container_width=True)

    death_chart = alt.Chart(death_tb).mark_bar().encode(
        x=alt.X('state', sort=None),
        y='total_death'
    )

    st.write("""Total Death Data (States)""")
    st.altair_chart(death_chart, use_container_width=True)


def getDataset2():
    state_abbr = {'CA' : 'California', 'TX' : 'Texas', 'FL' : 'Florida', 'NY' : 'New York', 'IL' : 'Illinois', 'PA' : 'Pennsylvania', 'OH' : 'Ohio', 'NC' : 'North Carolina', 'GA' : 'Georgia', 'MI' : 'Michigan', 'NJ' : 'New Jersey', 'TN' : 'Tennessee', 'AZ' : 'Arizona', 'MA' : 'Massachusetts', 'IN' : 'Indiana', 'VA' : 'Virginia', 'WI' : 'Wisconsin', 'WA' : 'Washington', 'SC' : 'South Carolina', 'MN' : 'Minnesota', 'MO' :  'Missouri', 'CO' : 'Colorado', 'KY' : 'Kentucky', 'AL' : 'Alabama', 'LA' : 'Louisiana', 'OK' : 'Oklahoma', 'MD' : 'Maryland', 'UT' : 'Utah', 'IA' : 'Iowa', 'AR' : 'Arkansas', 'MS' : 'Mississippi', 'KS' : 'Kansas', 'CT' : 'Connecticut', 'NV' : 'Nevada', 'OR' : 'Oregon', 'NM' : 'New Mexico', 'WV' : 'West Virginia', 'NE' : 'Nebraska', 'ID' : 'Idaho', 'RI' : 'Rhode Island', 'NH' : 'New Hampshire', 'MT' : 'Montana', 'DE' : 'Delaware', 'HI' : 'Hawaii', 'AK' : 'Alaska', 'ME' : 'Maine', 'ND' : 'North Dakota', 'SD' : 'South Dakota', 'WY' : 'Wyoming', 'DC' : 'District Of Columbia', 'VT' : 'Vermont'}
    # API Read
    # API key: e898e47cb4434fc6aa046f8881836e01
    url = "https://api.covidactnow.org/v2/states.csv?apiKey=e898e47cb4434fc6aa046f8881836e01"
    csvData = pd.read_csv(url, encoding='cp949')
    vaccineData = csvData[['state', 'actuals.vaccinesDistributed', 'actuals.vaccinationsInitiated', 'actuals.vaccinationsCompleted', 'metrics.vaccinationsInitiatedRatio', 'metrics.vaccinationsCompletedRatio']]

    state_vaccineInitiatedRatio_info = {}
    state_vaccineCompleteRatio_info = {}
    
    # data cleaning    
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

        if state in state_abbr:
            state_vaccineInitiatedRatio_info[state_abbr[state]] = vaccineInitiatedRatio
            state_vaccineCompleteRatio_info[state_abbr[state]] = vaccineCompleteRatio

    sorted_vaccineInitiatedRatio = sorted(state_vaccineInitiatedRatio_info.items(), key = lambda item: item[1], reverse = True)
    sorted_vaccineCompleteRatio = sorted(state_vaccineCompleteRatio_info.items(), key = lambda item: item[1], reverse = True)

    vaccineInitiatedRatio_state = []
    vaccineInitiatedRatio_value = []
    for vaccineInitiatedRatio in sorted_vaccineInitiatedRatio:
        vaccineInitiatedRatio_state.append(vaccineInitiatedRatio[0])
        vaccineInitiatedRatio_value.append(vaccineInitiatedRatio[1])
    
    vaccineInitiatedRatio_tb = pd.DataFrame(
       {"state": vaccineInitiatedRatio_state, "vaccine Initiated Ratio": vaccineInitiatedRatio_value}
    )
    vaccineInitiatedRatio_tb.columns = ["state", 'vaccine Initiated Ratio']

    vaccineCompleteRatio_state = []
    vaccineCompleteRatio_value = []
    for vaccineCompleteRatio in sorted_vaccineCompleteRatio:
        vaccineCompleteRatio_state.append(vaccineCompleteRatio[0])
        vaccineCompleteRatio_value.append(vaccineCompleteRatio[1])
    
    vaccineCompleteRatio_tb = pd.DataFrame(
       {"state": vaccineCompleteRatio_state, "vaccine Complete Ratio": vaccineCompleteRatio_value}
    )
    vaccineCompleteRatio_tb.columns = ["state", 'vaccine Complete Ratio']

    vaccineInitiatedRatio_chart = alt.Chart(vaccineInitiatedRatio_tb).mark_bar().encode(
        x=alt.X('state', sort=None),
        y='vaccine Initiated Ratio'
    )

    st.write("""vaccine Initiated Ratio (States)""")
    st.altair_chart(vaccineInitiatedRatio_chart, use_container_width=True)

    vaccineCompleteRatio_chart = alt.Chart(vaccineCompleteRatio_tb).mark_bar().encode(
        x=alt.X('state', sort=None),
        y='vaccine Complete Ratio'
    )

    st.write("""vaccine Complete Ratio (States)""")
    st.altair_chart(vaccineCompleteRatio_chart, use_container_width=True)    

def getDataset3():
    state_abbr = {'CA' : 'California', 'TX' : 'Texas', 'FL' : 'Florida', 'NY' : 'New York', 'IL' : 'Illinois', 'PA' : 'Pennsylvania', 'OH' : 'Ohio', 'NC' : 'North Carolina', 'GA' : 'Georgia', 'MI' : 'Michigan', 'NJ' : 'New Jersey', 'TN' : 'Tennessee', 'AZ' : 'Arizona', 'MA' : 'Massachusetts', 'IN' : 'Indiana', 'VA' : 'Virginia', 'WI' : 'Wisconsin', 'WA' : 'Washington', 'SC' : 'South Carolina', 'MN' : 'Minnesota', 'MO' :  'Missouri', 'CO' : 'Colorado', 'KY' : 'Kentucky', 'AL' : 'Alabama', 'LA' : 'Louisiana', 'OK' : 'Oklahoma', 'MD' : 'Maryland', 'UT' : 'Utah', 'IA' : 'Iowa', 'AR' : 'Arkansas', 'MS' : 'Mississippi', 'KS' : 'Kansas', 'CT' : 'Connecticut', 'NV' : 'Nevada', 'OR' : 'Oregon', 'NM' : 'New Mexico', 'WV' : 'West Virginia', 'NE' : 'Nebraska', 'ID' : 'Idaho', 'RI' : 'Rhode Island', 'NH' : 'New Hampshire', 'MT' : 'Montana', 'DE' : 'Delaware', 'HI' : 'Hawaii', 'AK' : 'Alaska', 'ME' : 'Maine', 'ND' : 'North Dakota', 'SD' : 'South Dakota', 'WY' : 'Wyoming', 'DC' : 'District Of Columbia', 'VT' : 'Vermont'}
    # Public API Read
    url = "https://api.covidtracking.com/v1/states/current.csv"
    csvData = pd.read_csv(url, encoding='cp949')
    stateData = csvData[['state', 'positive', 'probableCases', 'negative', 'hospitalizedCurrently']]

    state_hospitalizedCurrently_info = {}
    
    # data cleaning
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
        if state in state_abbr:
            state_hospitalizedCurrently_info[state_abbr[state]] = hospitalizedCurrently

    sorted_hospitalizedCurrently = sorted(state_hospitalizedCurrently_info.items(), key = lambda item: item[1], reverse = True)

    hospitalizedCurrently_state = []
    hospitalizedCurrently_value = []
    for hospitalizedCurrently in sorted_hospitalizedCurrently:
        hospitalizedCurrently_state.append(hospitalizedCurrently[0])
        hospitalizedCurrently_value.append(hospitalizedCurrently[1])
    
    hospitalizedCurrently_tb = pd.DataFrame(
       {"state": hospitalizedCurrently_state, "currently hospitalized": hospitalizedCurrently_value}
    )
    hospitalizedCurrently_tb.columns = ["state", 'currently hospitalized']

    hospitalizedCurrently_chart = alt.Chart(hospitalizedCurrently_tb).mark_bar().encode(
        x=alt.X('state', sort=None),
        y='currently hospitalized'
    )

    st.write("""currently hospitalized (States)""")
    st.altair_chart(hospitalizedCurrently_chart, use_container_width=True)

def show_intro():
    st.write("""
    Welcome to our data exploration webapp! My name is Silvia Choi, and in this project, I have analyzed the impact of vaccination on COVID-19 death rates across various states. This webapp is designed to allow users to explore the relationships between state-wide vaccination rates, case outcomes, and mortality data. By navigating through this interactive platform, you can gain insights into how these variables interact across different regions and times.
    """)
def show_explorer():
    st.write("""
    Explore the impact of COVID-19 through interactive bar charts in this section of our webapp. Each dataset used in the study is visualized as follows:
    """)
    st.subheader("""
    Data1: Web Scrape
    """)
    st.write("""
    Bar charts display the total number of COVID-19 cases and deaths per state, offering insights into the overall impact of the pandemic across the country.
    """)
    getDataset1()

    st.subheader("""
    Data2: API
    """)
    st.write("""
    Bar charts show vaccination data by state, illustrating the progression and geographical distribution of vaccination efforts.
    """)
    getDataset2()

    st.subheader("""
    Data3: Public API
    """)
    st.write("""
    Bar charts detail positive and negative case rates along with hospitalization durations by state, providing a deeper understanding of the healthcare burden and outcome severity.
    """)
    getDataset3()
    st.write("""
    These interactive bar charts allow you to select specific states and time frames, helping you examine how vaccination rates correlate with case outcomes and death rates. By manipulating these visualizations, you can uncover trends and patterns, gaining a comprehensive understanding of the dynamics at play in the pandemic response.
    """)
def show_conclusions():
    st.write("""
    The analysis conducted in this project reveals that there is no significant correlation between vaccination rates and death rates from COVID-19 across the states studied. Despite the critical role of vaccines in preventing severe illness and controlling the spread of the virus, our findings suggest that other factors may also significantly influence mortality rates. This conclusion is crucial for policymakers and health professionals as it highlights the complexity of managing a pandemic and the need for multifaceted public health strategies.
    """)
def show_research_objectives():
    st.write("""
    4. Q: What did you set out to study?
    
    A: The objective of my project was to explore the effectiveness of vaccinations in influencing mortality rates due to COVID-19 across different states. The datasets I chose included:

    Dataset 1: Total cases and deaths per state.
    Dataset 2: Vaccination data by state.
    Dataset 3: Positive/negative case rates and hospitalization durations by state.
    I aimed to investigate whether there was a correlation between vaccination rates and total deaths, suggesting the effectiveness of vaccines in reducing mortality rates from COVID-19.

    5. Q: What did you discover/what were your conclusions?

    A: The analysis revealed that vaccination does not have a significant effect on the death rate from COVID-19. This finding suggests that while vaccines are critical in controlling the spread of the disease and reducing severe outcomes, other factors may also significantly influence mortality rates.

    6. Q: What difficulties did you have in completing the project?

    A: The project was quite challenging as it was my first experience working through such a structured data science workflow from data acquisition to deploying a web application. Identifying and integrating three different datasets that were relevant to my research question proved particularly difficult. Additionally, building a web application to showcase the results was a new and challenging task.

    7. Q: What skills did you wish you had while you were doing the project?
    
    A: Throughout the project, I felt that stronger coding skills, particularly in data manipulation and web application development, would have made the process smoother. Additionally, more experience in selecting and utilizing datasets that support specific research topics would have been beneficial.

    8. Q: What would you do "next" to expand or augment the project?
    
    A: To expand the project, I would like to incorporate datasets on the economic aspects of vaccination, such as the cost of vaccines. Analyzing whether financial factors influence vaccination rates could provide deeper insights into public health strategies and vaccine uptake.
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
