#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import bs4
import pandas as pd
import requests

def download_daily_results(year, month, day) -> pd.DataFrame:
    url = f'http://www.gravon.de/gravon/stratego/todays.jsp?year={year}&month={month}&day={day}'
    response = requests.get(url)
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.content, 'lxml')
    table = soup.find_all('table', {'width': '95%', 'align': 'center'})[1]
    df = pd.read_html(str(table), header=0)[0]
    df.columns = df.columns.str.replace(' ', '_')
    return df

def download_monthly_results(year, month) -> pd.DataFrame:
    return pd.concat([
        download_daily_results(year, month, day)
        for day in range(1, 29)
    ])

def download_kleier_tournament(eid: int) -> pd.DataFrame:
    url = f'https://www.kleier.net/cgi/tourn_table.php?eid={eid}'
    response = requests.get(url)
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.content, 'lxml')
    tables = soup.find_all('table')
    return [ 
        pd.read_html(str(table))[0].head(-1) 
        for table in tables 
    ]
