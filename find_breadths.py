import requests
import erpcreds
import iitkgp_erp_login.erp as erp
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
import argparse
from tabulate import tabulate

def parse_args():
    parser = argparse.ArgumentParser(description='Get breadth electives from ERP')
    parser.add_argument('-o', '--overwrite', action='store_true', help='Overwrite existing electives.csv file')
    parser.add_argument('--notp', action='store_true', help='Enter OTP manually')
    parser.add_argument('--slots', nargs='+', help='Slots to register for')
    return parser.parse_args()

def save_electives(args):
    headers = {
    'timeout': '20',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36'
    }

    session = requests.Session()

    if args.notp:
        erp.login(headers, session, ERPCREDS=erpcreds, LOGGING=True, SESSION_STORAGE_FILE=".session")
    else:
        erp.login(headers, session, ERPCREDS=erpcreds, OTP_CHECK_INTERVAL=2, LOGGING=True, SESSION_STORAGE_FILE=".session")
    

    ERP_ELECTIVES_URL = "https://erp.iitkgp.ac.in/Acad/central_breadth_tt.jsp"

    response = session.get(ERP_ELECTIVES_URL, headers=headers)

    soup = bs(response.text, 'html.parser')

    # each "tr" contains a course
    rows = soup.find_all('tr')

    courses = []

    for row in rows:
        # Extract the data within the 'td' tags
        cells = row.find_all('td')
        if len(cells) >= 8:
            course = {}
            course_code_input = cells[0].find('input', {'name': 'subno'})
            course_code = course_code_input['value']
            course['Course Code'] = course_code.strip()

            course['Name'] = cells[1].text.strip()

            course['LTP'] = cells[2].text.strip()

            prereq_str = ''
            for i in range(3, 6):
                if cells[i].text.strip() != '':
                    prereq_str += cells[i].text.strip() + ', '
            
            # remove trailing comma and space
            if prereq_str != '':
                course['Prerequisites'] = prereq_str[:-2]
            else:
                course['Prerequisites'] = 'No prerequisites'

            dep_input = cells[0].find('input', {'name': 'dept'})
            dep = dep_input['value']
            course['Department'] = dep.strip()

            # slots is of the form {X}, we need just X
            if cells[7].text.strip() == '':
                course['Slot'] = 'Not alloted yet'
            else:
                course['Slot'] = cells[7].text.strip()[1:-1]
            
            if cells[8].text.strip() == '':
                course['Venue'] = 'Not alloted yet'
            else:
                course['Venue'] = cells[8].text.strip()

            courses.append(course)


    # Create a pandas DataFrame with the scraped data
    df = pd.DataFrame(data=courses)

    # for some reason, some empty slots are not being replaced
    df['Slot'].replace('', 'Not alloted yet', inplace=True)

    df.to_csv('breadth_electives.csv', index=False)

def main():
    args = parse_args()

    if args.overwrite or not os.path.exists('breadth_electives.csv'):
        save_electives(args)

    df = pd.read_csv('breadth_electives.csv') 

    # filter the df
    df_available = pd.DataFrame()
    for slot in args.slots:    
        df_available = pd.concat([df_available, df[df['Slot'].str.contains(slot)]], ignore_index=True)
    df_available.set_index('Course Code', inplace=True)

        
    # save available electives
    with open('available_breadths.txt', 'w') as f:
        f.write(tabulate(df_available, headers='keys', tablefmt='fancy_grid'))

    print("Available electives saved to available_breadths.txt")

if __name__ == '__main__':
    main()
