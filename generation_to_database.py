from entsoe import EntsoePandasClient
import sqlite3
import pandas as pd
from datetime import date, timedelta
import time


end_date = date.today()+timedelta(days=1)
current_date = end_date.strftime("%Y%m%d")

client = EntsoePandasClient(api_key='444fc771-5d0f-499f-9328-90c05c459219')

start = pd.Timestamp('20201109', tz='Europe/Brussels')
end = pd.Timestamp(current_date, tz='Europe/Brussels')
country_code = 'DE'


generation1 = client.query_generation(country_code, start=start, end=end, psr_type=None)

generation = generation1.iloc[:, generation1.columns.get_level_values(1)=='Actual Aggregated']

generation.columns = generation.columns.droplevel(level=1)
print(generation)

generation['Date'] = generation.index
generation.insert(0, 'id', range(0 , len(generation)))
generation['Total_Non_Renewables'] = generation['Fossil Brown coal/Lignite'] + generation['Fossil Gas'] + generation['Fossil Hard coal'] + generation['Fossil Oil'] + generation['Nuclear'] + generation['Other']
generation['Total_Renewables'] = generation['Biomass'] + generation['Geothermal'] + generation['Hydro Pumped Storage'] + generation['Hydro Run-of-river and poundage'] + generation['Hydro Water Reservoir'] + generation['Other renewable'] + generation['Solar'] + generation['Waste'] + generation['Wind Offshore'] + generation['Wind Onshore']
generation['Total'] = generation['Total_Renewables'] + generation['Total_Non_Renewables']
generation['Renewables_procentaqe'] = (generation['Total_Renewables'] / generation['Total'])*100
rounded_renewables = generation['Renewables_procentaqe'].round(decimals=1)
generation['Renewables_procentaqe'] =  rounded_renewables

print(generation)

is_NaN = generation.isnull()
row_has_NaN = is_NaN.any(axis=1)
rows_with_NaN = generation[row_has_NaN]
print(rows_with_NaN)

generation.drop(generation[row_has_NaN].index, inplace=True)

print(generation)

generation.rename(columns={"Fossil Brown coal/Lignite": "Fossil_Brown_coal_Lignite",
                            "Fossil Gas": "Fossil_Gas", "Fossil Hard coal": "Fossil_Hard_coal", "Fossil Oil": "Fossil_Oil", "Hydro Pumped Storage": "Hydro_Pumped_Storage",
                            "Hydro Run-of-river and poundage": "Hydro_Run_of_river_and_poundage", "Hydro Water Reservoir": "Hydro_Water_Reservoir", "Other renewable": "Other_renewable",
                            "Wind Offshore": "Wind_Offshore", "Wind Onshore": "Wind_Onshore"}, inplace = True)
print(generation.columns)

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
generation.to_sql('Stromzeiten_app_generation', conn, if_exists='replace', index = False)

c.execute('''  
SELECT * FROM Stromzeiten_app_generation
          ''')

for row in c.fetchall():
    print(row)

#time.sleep(900)


while True:
    latest_generation1 = client.query_generation(country_code, start=start, end=end, psr_type=None)

    latest_generation = latest_generation1.iloc[:, latest_generation1.columns.get_level_values(1) == 'Actual Aggregated']

    latest_generation.columns = latest_generation.columns.droplevel(level=1)
    latest_generation['Date'] = latest_generation.index
    latest_generation.insert(0, 'id', range(0, len(latest_generation)))
    latest_generation['Total_Non_Renewables'] = latest_generation['Fossil Brown coal/Lignite'] + latest_generation['Fossil Gas'] + \
                                                latest_generation['Fossil Hard coal'] +latest_generation['Fossil Oil'] + latest_generation[
                                              'Nuclear'] + latest_generation['Other']
    latest_generation['Total_Renewables'] = latest_generation['Biomass'] + latest_generation['Geothermal'] + latest_generation[
        'Hydro Pumped Storage'] + latest_generation['Hydro Run-of-river and poundage'] + latest_generation[
                                          'Hydro Water Reservoir'] + latest_generation['Other renewable'] + latest_generation[
                                          'Solar'] + latest_generation['Waste'] + latest_generation['Wind Offshore'] + latest_generation[
                                          'Wind Onshore']
    latest_generation['Total'] = latest_generation['Total_Renewables'] + latest_generation['Total_Non_Renewables']
    latest_generation['Renewables_procentaqe'] = (latest_generation['Total_Renewables'] / latest_generation['Total']) * 100
    print(latest_generation)

    is_NaN = latest_generation.isnull()
    row_has_NaN = is_NaN.any(axis=1)
    rows_with_NaN = latest_generation[row_has_NaN]
    print(rows_with_NaN)

    latest_generation.drop(latest_generation[row_has_NaN].index, inplace=True)
    latest_generation.rename(columns={"Fossil Brown coal/Lignite": "Fossil_Brown_coal_Lignite",
                                "Fossil Gas": "Fossil_Gas", "Fossil Hard coal": "Fossil_Hard_coal",
                                "Fossil Oil": "Fossil_Oil", "Hydro Pumped Storage": "Hydro_Pumped_Storage",
                                "Hydro Run-of-river and poundage": "Hydro_Run_of_river_and_poundage",
                                "Hydro Water Reservoir": "Hydro_Water_Reservoir", "Other renewable": "Other_renewable",
                                "Wind Offshore": "Wind_Offshore", "Wind Onshore": "Wind_Onshore"}, inplace=True)

    current_generation = latest_generation.tail(1)
    rounded_current_renewables = current_generation['Renewables_procentaqe'].round(decimals=1)
    current_generation['Renewables_procentaqe'] = rounded_current_renewables
    current_generation.round(1)

    SQL_Query = pd.read_sql_query('''  
        SELECT * FROM Stromzeiten_app_generation ORDER BY id DESC LIMIT 1
                  ''', conn)
    print(SQL_Query)
    df = pd.DataFrame(SQL_Query)

    df = df.reset_index(drop=True)
    current_generation = current_generation.reset_index(drop=True)
    print(current_generation)
    print(df)
    x = current_generation['id'].values[0]
    y = df['id'].values[0]
    print(x, y)
    if x == y:
        print("no new values")
    else:
        current_generation.to_sql('Stromzeiten_app_generation', conn, if_exists='append', index=False)



    c.execute('''  
    SELECT * FROM Stromzeiten_app_generation
              ''')

    for row in c.fetchall():
        print(row)

    time.sleep(60)