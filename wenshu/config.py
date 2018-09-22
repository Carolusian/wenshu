import logging


DOC_LINK_BASE = 'http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID=%s'


def get_logger(name):
    logging.basicConfig(level=logging.INFO, filename='wenshu.log')
    return logging.getLogger(name)
