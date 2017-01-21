#!/usr/bin/python
# -*- coding:utf-8 -*-
# modified from gen_pass_by_web(author:Peter Kim)
# author:junmoxiao

import urllib2
import re

site_list_file = 'site_list.txt'
words_file_name = 'words.txt'


def _remove_html_tags(html):
    text = html
    rules = [
        {r'>\s+': u'>'},  # Remove spaces after a tag opens or closes.
        {r'\s+': u' '},  # Replace consecutive spaces.
        {r'\s*<br\s*/?>\s*': u'\n'},  # Newline after a <br>.
        {r'</(div)\s*>\s*': u'\n'},  # Newline after </p> and </div> and <h1/>.
        {r'</(p|h\d)\s*>\s*': u'\n\n'},  # Newline after </p> and </div> and <h1/>.
        {r'<head>.*<\s*(/head|body)[^>]*>': u''},  # Remove <head> to </head>.
        {r'<a\s+href="([^"]+)"[^>]*>.*</a>': r'\1'},  # Show links instead of texts.
        {r'[ \t]*<[^<]*?/?>': u''},  # Remove remaining tags.
        {r'^\s+': u''}  # Remove spaces at the beginning.
    ]
    for rule in rules:
        for k, v in rule.items():
            regex = re.compile(k)
            try:
                text = regex.sub(v, text)
            except:
                pass
    special = {
        '&nbsp;': ' ',
        '&amp;': '&',
        '&quot;': '"',
        '&lt;': '<',
        '&gt;': '>'
    }
    for k, v in special.items():
        text = text.replace(k, v)
    text = re.sub('[^A-Za-z0-9]+', ' ', text)
    return text


def get_site_list():
    print 'get site list......'
    global site_list_file
    file_list = open(site_list_file, 'r')
    sites = file_list.read().split(',')
    return sites


def get_sites_content(sites):
    words_last = []
    for site in sites:
        site = site.strip()
        print 'download the %s......' % site
        headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0'}
        req = urllib2.Request(url=site, headers=headers)
        response = urllib2.urlopen(req)
        contents = _remove_html_tags(response.read())
        words = contents.split(' ')
        words_last.extend(words)
    return words_last


def write_words(words):
    words = set(words)
    words_file = open(words_file_name, 'wb')
    words_content = '\n'.join(words)[1:]
    words_file.write(words_content)
    words_file.close()


if __name__ == '__main__':
    sites = get_site_list()
    words = get_sites_content(sites)
    write_words(words)
