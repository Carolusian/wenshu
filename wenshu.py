#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: wenshu.py
# Author: Carolusian <https://github.com/carolusian>
# Date: 22.09.2018
# Last Modified Date: 22.09.2018
#
# Copyright 2017 Carolusian

import os
import sys
from wenshu.config import get_logger
from wenshu.actions import open_website, download_docs 
try:
    from tkinter import *
    from tkinter.ttk import *
except ImportError:
    from Tkinter import *
    import Tkinter, Tkconstants, tkFileDialog



try:
    dirpath = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
except NameError:
    dirpath = os.path.dirname(os.path.abspath(sys.argv[0]))

os.environ['PATH'] += os.pathsep + dirpath
os.environ['PATH'] += os.pathsep + os.path.join(dirpath, 'bin')


WENSHU_WEBSITE = 'http://wenshu.court.gov.cn/Index'
SAVE_TO = os.path.join(dirpath, 'downloaded')


logger = get_logger(__name__)


class WenShuGui(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.ui()

    def ui(self):
        self.master.title('WenShu downloader')
        self.center_window()
        self.pack(fill=BOTH, expand=1)

        # buttons
        open_btn = Button(self, text='Open Website', command=self.open)
        open_btn.pack(side=TOP)
        ok_btn = Button(self, text='Download', command=self.download)
        ok_btn.pack(side=TOP)
        quit_btn = Button(self, text="Quit", command=self.quit)
        quit_btn.pack(side=TOP, padx=5, pady=5)

    def center_window(self):
        w = 200
        h = 80

        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()

        x = int((sw - w) / 2)
        y = int((sh - h) / 2)

        self.master.geometry('{}x{}+{}+{}'.format(
            w, h, x, y
        ))

    def open(self):
        self.brower = open_website(WENSHU_WEBSITE)

    def download(self):
        download_docs(self.brower, SAVE_TO)


if __name__ == '__main__':
    # fblikers entrypoint
    logger.debug('App started.')
    root = Tk()
    app = WenShuGui()
    root.mainloop()
