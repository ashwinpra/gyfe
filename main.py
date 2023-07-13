import requests
import erpcreds
import iitkgp_erp_login.erp as erp
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
import argparse
from tabulate import tabulate

def parse_args():
    parser = argparse.ArgumentParser(description='Get electives from ERP')
    parser.add_argument('-o', '--overwrite', action='store_true', help='Overwrite existing electives.csv file')
    parser.add_argument('--slots', nargs='+', help='Slots to register for')
    return parser.parse_args()

def save_electives():
    headers = {
    'timeout': '20',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36'
    }

    session = requests.Session()

    sessionToken, ssoToken = erp.login(headers, erpcreds, 2, session)

    ERP_ELECTIVES_URL = "https://erp.iitkgp.ac.in/Acad/central_breadth_tt.jsp"

    response = session.get(ERP_ELECTIVES_URL, headers=headers)

    soup = bs(response.text, 'html.parser')

    # each "tr" contains a course
    rows = soup.find_all('tr')

    course_codes = []
    course_names = []
    credits = []
    prereqs = []
    venues = []
    depts = []
    slots = []

    for row in rows:
        # Extract the data within the 'td' tags
        cells = row.find_all('td')
        if len(cells) >= 8:
            course_code_input = cells[0].find('input', {'name': 'subno'})
            course_code = course_code_input['value']
            course_codes.append(course_code.strip())

            course_names.append(cells[1].text.strip())

            credits.append(cells[2].text.strip())

            prereq_str = ''
            for i in range(4, 6):
                if cells[i].text.strip() != '':
                    prereq_str += cells[i].text.strip() + ', '
            
            # remove trailing comma and space
            if prereq_str != '':
                prereqs.append(prereq_str[:-2])
            else:
                prereqs.append('No prerequisites')

            dep_input = cells[0].find('input', {'name': 'dept'})
            dep = dep_input['value']
            depts.append(dep.strip())

            # slots is of the form {X}, we need just X
            if cells[7].text.strip() == '':
                slots.append('Not alloted yet')
            else:
                slots.append(cells[7].text.strip()[1:-1])

            if cells[8].text.strip() == '':
                venues.append('Not alloted yet')
            else:
                venues.append(cells[8].text.strip())


    # Create a pandas DataFrame with the scraped data
    data = {
        'Course Code': course_codes,
        'Course Name': course_names,
        'Credits': credits,
        'Department': depts,
        'Prerequisites': prereqs,
        'Venue': venues,
        'Slot': slots

    }

    df = pd.DataFrame(data)

    # for 

    df.to_csv('electives.csv', index=False)

def main():
    args = parse_args()

    if args.overwrite or not os.path.exists('electives.csv') :
        save_electives()

    df = pd.read_csv('electives.csv')   
    # filter the dataframe to only include the slots the user wants to register for
    df = df[df['Slot'].isin(args.slots)].reset_index(drop=True)
    
    # save the available electives to a text file
    with open('available_electives.txt', 'w') as f:
        f.write(tabulate(df, headers='keys', tablefmt='fancy_grid'))

    print("Available electives saved to available_electives.txt")

if __name__ == '__main__':
    main()
