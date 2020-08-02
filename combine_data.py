import pandas as pd
from datetime import datetime

counties_df = pd.read_csv("county_centers.csv")
population_df = pd.read_csv("covid_county_population_usafacts.csv")
deaths_df = pd.read_csv("covid_deaths_usafacts.csv")
cases_df = pd.read_csv("covid_confirmed_usafacts.csv")

counties_df = counties_df[['fips', 'pclon10', 'pclat10']]
deaths_df = deaths_df.drop(['County Name', 'State', 'stateFIPS'], axis=1)
cases_df = cases_df.drop(['County Name', 'State', 'stateFIPS'], axis=1)

def to_float(entry):
    entry = str(entry).replace('°', "")
    entry = entry.replace('–', '-')
    entry = entry.replace("+","")
    return entry

counties_df['pclat10'] = counties_df['pclat10'].apply(to_float)
counties_df['pclon10'] = counties_df['pclon10'].apply(to_float)

def cols(column):
    if str(column) != 'countyFIPS':
        start = datetime.strptime("1/1/20", "%m/%d/%y").timestamp()
        column = (datetime.strptime(column, "%m/%d/%y").timestamp() - start)/86400
        column = float(int(column))
    return column

cases_df = cases_df.rename(columns = cols)

def d_cols(column):
    if str(column) != 'countyFIPS':
        start = datetime.strptime("1/1/20", "%m/%d/%y").timestamp()
        column = (datetime.strptime(column, "%m/%d/%y").timestamp() - start)/86400
        column = float(int(column))
    return str(column) + 'd'

deaths_df = deaths_df.rename(columns = d_cols)

data = population_df.merge(counties_df, left_on = 'countyFIPS', right_on='fips')
data = data.drop(['fips'], axis=1)

data = data.drop(data[data.State == 'HI'].index)
data = data.drop(data[data.State == 'AK'].index)

deaths_data = data.merge(deaths_df, left_on = 'countyFIPS', right_on = 'countyFIPSd')
cases_data = deaths_data.merge(cases_df, left_on = 'countyFIPSd', right_on = 'countyFIPS')


cases_data.to_csv("cases_data.csv")
cases_data = pd.read_csv("cases_data.csv")


for i in range(22,208):
    cases_data[str(float(i)) + 'dc'] = cases_data[str(float(i))] - cases_data[str(float(i-1))]
    cases_data[str(float(i)) + 'dd'] = cases_data[str(float(i)) + 'd'] - cases_data[str(float(i-1)) + 'd']

cases_data.to_csv("cases_data.csv")

