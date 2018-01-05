"""
file to crawl music from website http://mr-vip.net/Music/load/Hindi%20Movie/Hindi%20Movie%20Albums/128kbps/
"""
import os
import urllib2
import urllib
import logging
import logging.handlers

from lxml import html

__author__ = 'Amit Pathak'

index_url = 'http://vipmunda.com/Music/load/Hindi%20Movie/Hindi%20Movie%20Albums/128kbps/'

BaseMusicFolder = '/home/amit/Music'


def write_to_local_disk(url):
    logging.info('download url is %s ' % url)

    temp_url = url.replace(index_url, '')
    folder_names = temp_url.split('/')
    filename = urllib.unquote(folder_names[-1])

    path = BaseMusicFolder + '/' + '/'.join(folder_names[:-1])
    path = urllib.unquote(path)

    if not os.path.exists(path):
        os.makedirs(path)

    if not os.path.exists(os.path.join(path, filename)):
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        file_buffer = response.read()
        with open(os.path.join(path, filename), 'wb') as temp_file:
            temp_file.write(file_buffer)

    return True


def read_urls(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)

    doc = html.parse(response)
    for elt in doc.iter('table'):
        for tr in elt.getchildren()[3:-1]:
            _, anchor_td, _, _, _ = tr.getchildren()
            anchor = anchor_td.getchildren()[0]
            href = anchor.attrib['href']
            new_href = str(anchor.base_url) + href

            if not (new_href.endswith('.mp3') or new_href.endswith('.jpg')):
                logging.info('iterating url %s '% new_href)
                read_urls(new_href)
            else:
                write_to_local_disk(new_href)
    return True


def main():
    """
    Main

    """
    logging.basicConfig(filename='/home/amit/scrap.log', level=logging.INFO)

    logging.debug('Started')
    read_urls(index_url)
    logging.debug('Finished')


if __name__ == '__main__':
    main()
