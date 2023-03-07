import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

chrome = 'C:\Developer\chromedriver.exe'

driver = webdriver.Chrome(executable_path=chrome)


# Top cities in Florida
cities = ['Tampa', 'Gainesville', 'Jacksonville', 'Miami', 'Orlando', 'St. Petersburg']

df = pd.DataFrame()

url = f'https://www.zillow.com/professionals/real-estate-agent-reviews/'

for city in cities:
    for i in range(1, 4):
        driver.get(url + city + f'/?page={i}')
        time.sleep(3)
        if i <= 3:
            rd = []
            table = driver.find_element(By.CLASS_NAME, value='eSCkQe')
            for row in table.find_elements(by='tag name', value='tr'):
                col = row.find_elements(by='tag name', value='td')
                col = [element.text.split('\n') for element in col]
                rd.append(col)
            links = table.find_elements(By.CLASS_NAME, value='jMHzWg')
            final_links = []
            for link in links:
                ref = link.get_attribute('href')
                if ref not in final_links:
                    final_links.append(ref)
                else:
                    continue

            rd = rd[1:]
            df1 = pd.DataFrame(rd)
            df2 = pd.DataFrame(list(df1[0]))
            df2['Url'] = final_links
            df2['City'] = city
            df2 = df2.drop(columns=[1])
            df2[3] = df2[3].str.split(' ').str[0]
            df2[5] = df2[5].str.split(':').str[1]
            df2.rename(columns={0: 'Name', 2: 'Phone Number', 3: 'Reviews', 4: 'Company', 5: 'Agent Licence'},
                       inplace=True)
            df2 = df2[['City', 'Name', 'Company', 'Phone Number', 'Url', 'Agent Licence', 'Reviews']]
            df = df.append(df2, ignore_index=True)
            df.to_csv('Data.csv', mode='a', index=True, header=False)

driver.quit()
