#!/usr/bin/env python
# -*- coding: utf-8 -*-

# File: wenshu/actions.py
# Author: Carolusian <https://github.com/carolusian>
# Date: 22.09.2018
# Last Modified Date: 22.09.2018
#
# Copyright 2018 Carolusian

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
from .utils import retry


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


def is_finished(browser):
    finish_text = '无符合条件的数据...'
    sleep_secs = 15
    time.sleep(sleep_secs)
    result_list = browser.find_element_by_id('resultList')
    # Refresh if no result found
    if finish_text in result_list.text:
        logger.info('Try refresh to reload content')
        browser.refresh()
        time.sleep(sleep_secs)

    # If still not result found, finish downloading
    result_list = browser.find_element_by_id('resultList')
    if finish_text in result_list.text:
        return True
    return False


def download_docs(browser, save_dir='./', click_next_page=False): 
    if click_next_page:
        next_page = browser.find_elements(By.XPATH, '//*[@id="pageNumber"]/a[contains(text(), "下一页")]')
        next_page[0].click()
        if is_finished(browser):
            logger.info('Finished downloading documents in this page.')
            return

    link_xpath = '//*[@class="dataItem"]'
    keywords_elems = browser.find_elements(By.XPATH, '//*[@class="contentCondtion"]')
    subfolder = '-'.join([el.text for el in keywords_elems])
    elems = browser.find_elements(By.XPATH, link_xpath)
    for el in elems:
        save_doc(browser, el, os.path.join(save_dir, subfolder))
        time.sleep(1)

    # Goto next page after this page is download
    download_docs(browser, save_dir, click_next_page=True)


@retry(times=5, delay=5, allowed_exceptions=IndexError)
def save_doc(browser, doc_elem, save_dir):
    doc_key = doc_elem.get_attribute('key')
    doc_title = doc_elem.get_attribute('title')
    logger.info('Found document %s.' % doc_title)

    unzipped_id = browser.execute_script('return unzip("%s")' % doc_key)
    doc_id = browser.execute_script('return com.str.Decrypt("%s")' % unzipped_id)
    doc_link = DOC_LINK_BASE % doc_id

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    p = re.compile('(var jsonHtmlData = ")(.+)(\\"}";)')
    
    resp = requests.get(doc_link, headers=headers)
    resp_text = resp.text

    resp_obj = p.findall(resp_text)[0][1].replace('\\', '') + '"}'
    resp_obj = json.loads(resp_obj)

    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, resp_obj['Title'] + '.html'), 'w') as f:
        f.write(resp_obj['Html'])
        logger.info('Downloaded %s.' % resp_obj['Title'])


    


