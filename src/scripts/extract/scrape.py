#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import datetime as dt
import os
import time
from typing import List

import bs4
import pandas as pd
import requests
from tqdm import tqdm

import gravon.package as pkg

def _etiget(url: str, crawl_delay=0, headers={'User-agent': 'Custom'}, **kwargs) -> requests.Response:
    """
    Wrap requests.get() to conform to webscraping etiquette.
    """
    time.sleep(crawl_delay)
    return requests.get(url, headers=headers, **kwargs)

def _list_directory_contents(url: str) -> pd.DataFrame:
    response = _etiget(url)
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.content, 'lxml')
    table = soup.find('table')
    return (pd
        .read_html(str(table), parse_dates=[2])[0]
        .head(-1)
        .tail(-2)
        .reset_index(drop=True)
        .rename(columns=lambda c: c.lower())
        .rename(columns=lambda c: c.replace(' ', '_'))
        .assign(
            url           = url,
            last_modified = lambda r: r.last_modified.dt.date
        )
        .loc[:, [
            'url', 'name', 'last_modified'
        ]]
    )

def list_directory_contents_recursive(url: str) -> pd.DataFrame:
    isdir = 'name.str.endswith("/")'
    isfile = '~' + isdir
    result = pd.DataFrame()
    dirs = pd.DataFrame(data=[''], columns=['name'])
    while True:
        list = pd.concat([
            _list_directory_contents(os.path.join(url, dir.name))
            for dir in dirs.itertuples()
        ])
        result = result.append(list.query(isfile))
        dirs = list.query(isdir)
        if dirs.empty:
            break
    return (result
        .sort_values(['last_modified', 'name'])
        .reset_index(drop=True)
    )

def _copy(source: str, directory: str) -> None:
    response = _etiget(source)
    assert response.status_code == 200
    assert os.path.exists(directory)
    with open(os.path.join(directory, os.path.basename(source)), 'wb') as dst:
        dst.write(response.content)

def download(prefix: str, *urls: str) -> None:
    """
    wget -P prefix urls

    Example:
        >>> scrape.download(pkg.games_dir, pgk.player_url)
    """
    os.makedirs(prefix, exist_ok=True)
    for url in urls:
        _copy(url, prefix)

def mirror_no_directories(prefix: str, acclist: str, urls: pd.DataFrame) -> pd.DataFrame:
    """
    wget -m -nd -P prefix -A acclist urls

    Example:
        >>> scrape.mirror_no_directories(pkg.zip_dir, '*.zip', list_directory_contents_recursive(pkg.strados2_url))
    """
    files = urls.query('name.str.endswith(@acclist.split(".")[-1])')
    os.makedirs(prefix, exist_ok=True)
    for file in tqdm(files.itertuples(), total=files.shape[0]):
        _copy(os.path.join(file.url, file.name), prefix)
    return files

def _table(url: str, selector: str) -> pd.DataFrame:
    response = _etiget(url)
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.content, 'lxml')
    try:
        table = soup.select(selector)
        return pd.read_html(str(table), header=0)[0]
    except:
        return pd.DataFrame()

def _daily_results(date: dt.date) -> pd.DataFrame:
    return (_table(
            f'{pkg.stratego_url}/todays.jsp?year={date.year}&month={date.month}&day={date.day}',
            'body > table:nth-child(1) > tbody > tr > td > table:nth-child(13)'
        )
        .assign(Date = date)
    )

def results(prefix: str, start: dt.date, end: dt.date) -> List[str]:
    """
    Example:
        >>> scrape.results(pkg.daily_dir, '2003-06-01', pd.to_datetime('today').date())
    """
    dates = pd.date_range(start, end, closed='left')
    files = [
        f'results-{date.date()}.csv'
        for date in dates
    ]
    os.makedirs(prefix, exist_ok=True)
    for date, file in tqdm(zip(dates, files), total=len(dates)):
        _daily_results(date).to_csv(os.path.join(prefix, file), index=False)
    return files

def player_type(nick: str, type=0) -> pd.DataFrame:
    return (
        _table(
            f'{pkg.stratego_url}/player{type}.jsp?nick={nick.lower()}',
            'body > table:nth-child(1) > tbody > tr > td > table:nth-child(15)'
        )
        .assign(
            Nick = nick,
            Type = type
        )
    )

def player(nick: str) -> pd.DataFrame:
    return (pd
        .concat([
            player_type(nick, type)
            for type in [0, 1, 3, 4]
        ])
        .sort_values(['Time'])
        .reset_index(reset=True)
    )

def pvsp(nick1: str, nick2: str) -> pd.DataFrame:
    return _table(
        f'{pkg.stratego_url}/pvsp.jsp?nick1={nick1.lower()}&nick2={nick2.lower()}',
        'body > table:nth-child(1) > tbody > tr > td > table:nth-child(9)'
    )
