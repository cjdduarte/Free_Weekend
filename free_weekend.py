# -*- coding: utf-8 -*-

#Copyright(C)| Carlos Duarte
#Based on    | xquercus code, in add-on "Load Balanced Scheduler"
#License     | GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
#Source in   | https://github.com/cjdduarte/FreeWeekend

import sys
import anki
import datetime
from aqt import mw
from anki import version
from anki.sched import Scheduler

from aqt.utils import tooltip
#import os
from random import *

#-------------Configuration------------------
try:
    config = mw.addonManager.getConfig(__name__)
except AttributeError:
    config = dict(days_week=[6], log_tooltip=0, specific_days=["9999/12/31"])
'''
if getattr(mw.addonManager, "getConfig", None): #Anki 2.1
    config = mw.addonManager.getConfig(__name__)
    tooltip("Anki 2.1", period=3000)
else:  #Anki 2.0
    config = dict(days_week=[6], log_tooltip=0, specific_days=["9999/12/31"])
    tooltip("Anki 2.0", period=3000)
'''
#-------------Configuration (Anki 2.0) ------------------
#days_week      = [6]      #0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun, -1=Ignore
#log_tooltip    = 0        #"0=OFF, 1=Basic, 2=More"
#specific_days  = ["YYYY/MM/DD", "YYYY/MM/DD"] - Specific days must have quotation marks
#-------------Configuration (Anki 2.0) ------------------
days_week       = config['days_week']
log_tooltip     = config['log_tooltip']
specific_days   = config['specific_days']
#-------------Configuration------------------

seed()
'''
this_script_dir = os.path.dirname(__file__)
user_files_dir = os.path.join(this_script_dir, 'datas.txt')
with open(user_files_dir, 'r', encoding='utf-8') as f:
    datas_arquivo = [line.strip() for line in f]'''

def load_balanced_ivl(self, ivl):
    orig_ivl = int(ivl)
    min_ivl, max_ivl = self._fuzzIvlRange(orig_ivl)
    IvlRangeOri = []
    IvlRange = []
    ignored_days = []

    for k in range(min_ivl, max_ivl + 1):
        IvlRangeOri.append(k)
        IvlRange.append(k)

    best_ivl = randint(min_ivl, max_ivl)
    removed_all=True

    for check_ivl in range(min_ivl, max_ivl + 1):
        data = datetime.datetime.now() + datetime.timedelta(days=check_ivl)
        #if (data.weekday() not in days_week):
        if (data.weekday() not in days_week and data.strftime("%Y/%m/%d") not in specific_days):
            removed_all=False
        else:
            IvlRange.remove(check_ivl)
            ignored_days.append(data.strftime("%Y/%m/%d"))

    ignored_days = ', '.join(ignored_days)

    if removed_all:
        best_ivl = choice(IvlRangeOri)
    else:
        best_ivl = choice(IvlRange)

    '''if  log_tooltip and removed_all:
        mensagem = 'Excluded week day used! Range Fuzz too small.'
        tooltip(mensagem, period=3000)
    elif log_tooltip and ignored_days:
        #mensagem = 'orig_ivl = ' + str(orig_ivl) + ' min_ivl = ' + str(min_ivl) + ' max_ivl = ' + str(max_ivl) + ' best_ivl = ' + str(best_ivl)
        mensagem = 'Ignored days: ' + str(ignored_days)
        tooltip(mensagem, period=2000)'''
    #-------------Log------------------
    log_orig_ivl    = 'orig='    + (datetime.datetime.now() + datetime.timedelta(days=orig_ivl)).strftime("%Y/%m/%d") + '   '
    log_min_ivl     = 'min='     + (datetime.datetime.now() + datetime.timedelta(days=min_ivl)).strftime("%Y/%m/%d")  + '   '
    log_max_ivl     = 'max='     + (datetime.datetime.now() + datetime.timedelta(days=max_ivl)).strftime("%Y/%m/%d")  + '   '
    log_best_ivl    = 'sel='     + (datetime.datetime.now() + datetime.timedelta(days=best_ivl)).strftime("%Y/%m/%d") + '   '
    log_ign_days    = 'ignored=' + str(ignored_days)

    if  removed_all:
        if log_tooltip == 1:
            mensagem = 'ignored=All days used! Range Fuzz too small.'
            tooltip(mensagem, period=3000)
        elif log_tooltip == 2:
            mensagem = log_min_ivl + log_max_ivl + log_best_ivl + 'ignored=All days used! Range Fuzz too small.'
            tooltip(mensagem, period=4000)
    elif log_tooltip and ignored_days:
        if log_tooltip == 1:
            mensagem = log_ign_days
            tooltip(mensagem, period=3000)
        elif log_tooltip == 2:
            mensagem = log_min_ivl + log_max_ivl + log_best_ivl + log_ign_days
            tooltip(mensagem, period=4000)
    #-------------Log------------------

    return best_ivl

# Patch Anki 2.0 and Anki 2.1 default scheduler
anki.sched.Scheduler._fuzzedIvl = load_balanced_ivl

# Patch Anki 2.1 experimental v2 scheduler
if version.startswith("2.1"):
    from anki.schedv2 import Scheduler
    anki.schedv2.Scheduler._fuzzedIvl = load_balanced_ivl
