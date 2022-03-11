import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate


base_url = 'https://results.eci.gov.in/ResultAcGenMar2022/ConstituencywiseS2443.htm?ac='

seats = {
    'Meerut Cantt': 47,
    'Meerut South': 49,
    'Siwalkhas': 43,
    'Hastinapur': 45,
    'Kithore': 46,
    'Sirathu': 251,
}


def get_results(v):
    url = f'https://results.eci.gov.in/ResultAcGenMar2022/ConstituencywiseS24{v}.htm?ac={v}'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    link = soup.find('div', id='div1')
    table = link.find('table')

    headers = []
    for i in table.find_all('th'):
        title = i.text
        headers.append(title)

    mydata = pd.DataFrame(columns=headers)
    for j in table.find_all('tr')[1:]:
        row_data = j.find_all('td')
        if len(row_data) == len(headers):
            row = [i.text for i in row_data]
            length = len(mydata)
            mydata.loc[length] = row
    mydata['Total Votes'] = mydata['Total Votes'].astype(int)
    mydata.sort_values('Total Votes')
    parties = [
        'Samajwadi Party',
        'Bharatiya Janata Party',
        'Rashtriya Lok Dal',
    ]
    final_data = mydata[mydata.Party.isin(parties)]
    column = final_data['Total Votes']
    max_value = column.max()
    min_value = column.min()
    print('Margin:', max_value - min_value)
    print(tabulate(final_data, headers='keys', tablefmt='psql'))
    mydata.drop(mydata.index, inplace=True)


if __name__ == '__main__':
    for k, v in seats.items():
        print('Seat:', k)
        get_results(v)
