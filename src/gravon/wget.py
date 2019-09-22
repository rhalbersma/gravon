#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import collections
import os

import bs4
import requests

def mirror_no_directories(prefix: str, acclist: str, *urls) -> None:
    """
    wget -m -nd -P prefix -A acclist urls

    Examples:
        >>> Wget.mirror_no_directories('downloads', '*.zip', 'http://www.gravon.de/strados2/files/')
    """
    os.makedirs(prefix, exist_ok=True)
    urls = collections.deque(urls)
    while urls:
        top = urls.popleft()
        response = requests.get(top)
        assert response.status_code == 200
        soup = bs4.BeautifulSoup(response.content, 'lxml')
        for link in soup.find_all('a'):
            filename = link.get('href')
            if filename.endswith('/') and not filename.startswith('/'):
                urls.append(top + filename)
                continue
            if not filename.endswith(acclist.split('.')[-1]):
                continue
            response = requests.get(os.path.join(top, filename))
            assert response.status_code == 200
            with open(os.path.join(prefix, filename), 'wb') as dst:
                dst.write(response.content)

def download(prefix: str, *urls) -> None:
    """
    wget -P prefix urls

    Examples:
        >>> Wget.download('viewer', 'https://www.gravon.de/webstart/strados2/strados2.jnlp')
    """
    os.makedirs(prefix, exist_ok=True)
    for url in urls:
        response = requests.get(url)
        assert response.status_code == 200
        filename = url.split('/')[-1]
        with open(os.path.join(prefix, filename), 'wb') as dst:
            dst.write(response.content)
