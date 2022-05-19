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
ANKI21 = version.startswith("2.1.")

try:  # 2.1.45+
    from anki.scheduler.v1 import Scheduler as SchedulerV1
    from anki.scheduler.v2 import Scheduler as SchedulerV2
    from anki.scheduler.v3 import Scheduler as SchedulerV3
except (ImportError, ModuleNotFoundError):
    from anki.sched     import Scheduler as SchedulerV1
    from anki.schedv2   import Scheduler as SchedulerV2

from aqt.utils import tooltip

import aqt
import aqt.deckconf
from anki.hooks import wrap

if ANKI21:
    from PyQt5 import QtCore, QtGui, QtWidgets
else:
    from PyQt4 import QtCore, QtGui as QtWidgets

from random import *

#-------------Configuration------------------
if getattr(getattr(mw, "addonManager", None), "getConfig", None): #Anki 2.1
    config = mw.addonManager.getConfig(__name__)
else:
    #(Anki 2.0) - you must change these values ​​based on the parameter table
    #----- Modify here ------
    config = dict(days_week=[6], log_tooltip=0, specific_days=["9999/12/31"])
    #----- Modify here ------

#-------------Parameter Table (Anki 2.0) ------------------
#days_week      = [6]      #0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun, -1=Ignore
#log_tooltip    = 0        #"0=OFF, 1=Basic, 2=More"
#specific_days  = ["YYYY/MM/DD", "YYYY/MM/DD"] - Specific days must have quotation marks
#-------------Parameter Table (Anki 2.0) ------------------

days_week       = config['days_week']
log_tooltip     = config['log_tooltip']
specific_days   = config['specific_days']
specific_days   = [ datetime.datetime.strftime(datetime.datetime.strptime(x, '%Y/%m/%d'), '%Y/%m/%d') for x in specific_days ] #Bug
#-------------Configuration------------------

seed()

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

def setup_ui(self, Dialog):

    r=self.gridLayout_3.rowCount()
    gridLayout_3 = QtWidgets.QGridLayout()

    self.DisableFW = QtWidgets.QCheckBox(self.tab_3)
    self.DisableFW.setObjectName(_fromUtf8("DisableFW"))
    self.DisableFW.setText(_('Disable Free Weekend (It will affect all decks that belong to this group of options)'))
    self.DisableFW.setDisabled(0)
    gridLayout_3.addWidget(self.DisableFW, r, 0, 1, 3)
    r+=1

    self.verticalLayout_4.insertLayout(1, gridLayout_3)

def load_conf(self):
    f = self.form
    c = self.conf
    f.DisableFW.setCheckState(c.get('DisableFW', 0))

def save_conf(self):
    f = self.form
    c = self.conf
    c['DisableFW'] = int(f.DisableFW.checkState())

def load_balanced_ivl(sched, ivl, _old):
    orig_ivl = int(ivl)
    min_ivl, max_ivl = sched._fuzzIvlRange(orig_ivl)
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

    #--------Deck ignored by parameter--------
    ignore_deck = False
    card = mw.reviewer.card
    if card:
        conf=sched.col.decks.confForDid(card.odid or card.did)
        if conf.get('DisableFW',0) == 2:
            ignore_deck = True
    #--------Deck ignored by parameter--------

    if removed_all or ignore_deck:
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
        if log_tooltip == 1 or log_tooltip == 2:
            mensagem = 'ignored=All days used! Range Fuzz too small.'
            tooltip(mensagem, period=3000)
        elif log_tooltip == 3:
            mensagem = log_min_ivl + log_max_ivl + log_best_ivl + 'ignored=All days used! Range Fuzz too small.'
            tooltip(mensagem, period=4000)
    elif  ignore_deck:
        if log_tooltip == 1 or log_tooltip == 2:
            mensagem = 'Disable Free Weekend in Options Group.'
            tooltip(mensagem, period=3000)
        elif log_tooltip == 3:
            mensagem = log_min_ivl + log_max_ivl + log_best_ivl + 'Disable Free Weekend in Options Group.'
            tooltip(mensagem, period=4000)
    elif log_tooltip and ignored_days:
        if log_tooltip == 2:
            mensagem = log_ign_days
            tooltip(mensagem, period=3000)
        elif log_tooltip == 3:
            mensagem = log_min_ivl + log_max_ivl + log_best_ivl + log_ign_days
            tooltip(mensagem, period=4000)
    #-------------Log------------------

    return best_ivl

aqt.forms.dconf.Ui_Dialog.setupUi   = wrap(aqt.forms.dconf.Ui_Dialog.setupUi, setup_ui, pos="after")
aqt.deckconf.DeckConf.loadConf      = wrap(aqt.deckconf.DeckConf.loadConf, load_conf, pos="after")
aqt.deckconf.DeckConf.saveConf      = wrap(aqt.deckconf.DeckConf.saveConf, save_conf, pos="before")

# Patch Anki 2.0 and Anki 2.1 default scheduler
SchedulerV1._fuzzedIvl = wrap(SchedulerV1._fuzzedIvl, load_balanced_ivl, 'around')

# Patch Anki 2.1 experimental v2 scheduler
if version.startswith("2.1"):
    SchedulerV2._fuzzedIvl = wrap(SchedulerV2._fuzzedIvl, load_balanced_ivl, 'around')