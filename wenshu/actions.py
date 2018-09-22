#!/usr/bin/env python
# -*- coding: utf-8 -*-

# File: wenshu/actions.py
# Author: Carolusian <https://github.com/carolusian>
# Date: 22.09.2018
# Last Modified Date: 22.09.2018
#
# Copyright 2017 Carolusian

import time
import itertools
import re
import requests
import json
import os
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException
from .exceptions import UnsupportedPlatformException

from .config import get_logger, DOC_LINK_BASE


logger = get_logger(__name__)


def sleep(min_seconds=1, max_seconds=10):
    """Allow a browser instance to wait for a few seconds before do something"""
    time.sleep(randint(min_seconds, max_seconds))


def click(elem):
    try:
        elem.click()
    except ElementNotInteractableException:
        pass


def open_website(url):
    """
    Open website of target url
    """
    browser = webdriver.Firefox()
    browser.get(url)
    return browser


def download_docs(browser, save_dir='./'): 
    link_xpath = '//*[@class="dataItem"]'
    elems = browser.find_elements(By.XPATH, link_xpath)
    for el in elems:
        doc_key = el.get_attribute('key')
        doc_title = el.get_attribute('title')
        logger.info('Found document %s.' % doc_title)

        unzipped_id = browser.execute_script('return unzip("%s")' % doc_key)
        doc_id = browser.execute_script('return com.str.Decrypt("%s")' % unzipped_id)
        doc_link = DOC_LINK_BASE % doc_id
        save_doc(doc_link, doc_title, save_dir)
    logger.info('Finished downloading documents in this page.')


def save_doc(link, title, save_dir):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    p = re.compile('(var jsonHtmlData = ")(.+)(\\"}";)')
    
    resp = requests.get(link, headers=headers).text

    # A simple retry mechanism
    if not resp.find('jsonHtmlData'):
        secs = 10
        logger.info('Retrying %s %s seconds later...' % (title, secs))
        time.sleep(secs)
        resp = requests.get(link, headers=headers).text

    resp_obj = p.findall(resp)[0][1].replace('\\', '') + '"}'
    resp_obj = json.loads(resp_obj)

    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, resp_obj['Title'] + '.html'), 'w') as f:
        f.write(resp_obj['Html'])
        logger.info('Downloaded %s.' % resp_obj['Title'])
    time.sleep(10)


    


