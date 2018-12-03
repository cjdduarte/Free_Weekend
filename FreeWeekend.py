# -*- coding: utf-8 -*-
# Copyright (C) 2018 Carlos Duarte
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import sys
import anki
import datetime
from aqt import mw
from anki import version
from anki.sched import Scheduler

from aqt.utils import tooltip
import os
from random import *

dias_semana = [6] #0=SEG, 1=TER ...6=DOM (-1 ANULA)
log_tooltip = True

seed()

this_script_dir = os.path.dirname(__file__)
user_files_dir = os.path.join(this_script_dir, 'datas.txt')
with open(user_files_dir, 'r', encoding='utf-8') as f:
    datas_arquivo = [line.strip() for line in f]
#-------------------------------------------

def load_balanced_ivl(self, ivl):
    """Return the (largest) interval that has the least number of cards and falls within the 'fuzz'"""
    orig_ivl = int(ivl)
    min_ivl, max_ivl = self._fuzzIvlRange(orig_ivl)
    IvlRangeOri = []
    IvlRange = []

    for k in range(min_ivl, max_ivl + 1):
        IvlRangeOri.append(k)
        IvlRange.append(k)

    best_ivl = randint(min_ivl, max_ivl)

    removed_all=True
    for check_ivl in range(min_ivl, max_ivl + 1):
        data = datetime.datetime.now() + datetime.timedelta(days=check_ivl)
        if (data.weekday() not in dias_semana and data.strftime("%d/%m/%Y") not in datas_arquivo):
            removed_all=False
        else:
            IvlRange.remove(check_ivl)

    if removed_all:
        best_ivl = choice(IvlRangeOri)
    else:
        best_ivl = choice(IvlRange)

    if log_tooltip:
        mensagem = 'orig_ivl = ' + str(orig_ivl) + ' min_ivl = ' + str(min_ivl) + ' max_ivl = ' + str(max_ivl) + ' best_ivl = ' + str(best_ivl)
        tooltip(mensagem, period=5000)

    return best_ivl


# Patch Anki 2.0 and Anki 2.1 default scheduler
anki.sched.Scheduler._fuzzedIvl = load_balanced_ivl


# Patch Anki 2.1 experimental v2 scheduler
if version.startswith("2.1"):
    from anki.schedv2 import Scheduler
    anki.schedv2.Scheduler._fuzzedIvl = load_balanced_ivl
