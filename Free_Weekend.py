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


#config = mw.addonManager.getConfig(__name__)
#a = config.get('days_week')
#tooltip(a, period=2000)

#-------------Configuration------------------
days_week   = [6]      #[0]=Monday|[1]=Tuesday|[2]=Wednesday|[3]=Thursday|[4]=Friday|[5]=Saturday|[6]=Sunday|[-1]=Ignore
log_tooltip = False    #True|False
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
        if (data.weekday() not in days_week):
        #if (data.weekday() not in days_week and data.strftime("%d/%m/%Y") not in datas_arquivo):
            removed_all=False
        else:
            IvlRange.remove(check_ivl)
            ignored_days.append(data.strftime("%Y/%m/%d"))

    ignored_days = ', '.join(ignored_days)

    if removed_all:
        best_ivl = choice(IvlRangeOri)
    else:
        best_ivl = choice(IvlRange)

    if  log_tooltip and removed_all:
        mensagem = 'Excluded week day used! Range Fuzz too small.'
        tooltip(mensagem, period=3000)
    elif log_tooltip and ignored_days:
        #mensagem = 'orig_ivl = ' + str(orig_ivl) + ' min_ivl = ' + str(min_ivl) + ' max_ivl = ' + str(max_ivl) + ' best_ivl = ' + str(best_ivl)
        mensagem = 'Ignored days: ' + str(ignored_days)
        tooltip(mensagem, period=2000)

    return best_ivl

# Patch Anki 2.0 and Anki 2.1 default scheduler
anki.sched.Scheduler._fuzzedIvl = load_balanced_ivl

# Patch Anki 2.1 experimental v2 scheduler
if version.startswith("2.1"):
    from anki.schedv2 import Scheduler
    anki.schedv2.Scheduler._fuzzedIvl = load_balanced_ivl
