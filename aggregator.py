# -----------------------------------------------------------------------------
# Name:        aggregator.py
# Purpose:     CS 21A - implement a simple general purpose aggregator
#
# Author:      Jennifer Wong
# -----------------------------------------------------------------------------
"""
Implement a simple general purpose aggregator

Usage: aggregator.py filename topic
filename: input  file that contains a list of the online sources (urls).
topic:  topic to be researched and reported on
"""

import urllib.request
import urllib.error
import re
import sys


def write_file(filename, topic):
    """
    Write references to topic to output_file

    Parameters:
    filename (string) - name of file that contains list of urls
    topic (string) - word to find references of
    Return:
    none
    """
    output_file = topic + 'summary.txt'

    with open(output_file, 'w', encoding='utf-8') as file1:
        try:
            with open(filename, 'r', encoding='utf-8') as file2:
                for line in file2:      # iterate through urls
                    # write references to output_file
                    file1.write(open_url(line, topic))
        except IOError as error:        # filename cannot be opened
            print('Error opening file: ', filename, '\n', error)


def open_url(url, topic):
    """
    Open a url and decode page

    Parameters:
    url (string) - a url
    topic (string) - word to find references of
    Return:
    references (string) - references to topic
    """
    references = ''

    try:
        with urllib.request.urlopen(url) as url_file:   # open url
            page = url_file.read()
            decoded_page = page.decode('UTF-8')         # decode page
    except urllib.error.URLError as url_err:            # cannot open url
        print('Error opening url: ', url, url_err)
    except UnicodeDecodeError as decode_err:            # cannot decode url
        print('Error decoding url: ', url, decode_err)
    else:
        references = report_topic(url, decoded_page, topic)

    return references


def report_topic(url, page, topic):
    """
    Return source url and references, if any

    Parameters:
    url (string) - a url
    page (string) - HTML page
    topic (string) - word to find references of
    Return:
    references (string) - references to topic
    """
    references = ''

    if find_references(page, topic) != '':
        references = 'Source url:' + url + '\n'
        references = references + find_references(page, topic)
        references = references + '\n--------------------------------\n\n'

    return references


def find_references(page, topic):
    """
    Find references to topic in page

    Parameters:
    page (string) - HTML page
    topic (string) - word to find references of
    Return:
    all_references (string) - references to topic
    """
    all_references = ''

    # extract text inside angle brackets containing topic
    pattern = r'>([^<]*\b{}\b.*?)<'.format(topic)
    matches = re.findall(pattern, page, re.IGNORECASE | re.DOTALL)

    if matches:
        all_references = '\n'.join(matches)

    return all_references


def main():
    if len(sys.argv) != 3:      # if 3 command line arguments are not provided
        print('Error: invalid number of arguments')
        print('Usage: aggregator.py filename topic')
    else:
        filename = sys.argv[1]
        topic = sys.argv[2]
        write_file(filename, topic)


if __name__ == '__main__':
    main()
