<b>Bug Report:</b> https://github.com/cjdduarte/FreeWeekend<br>
<b>Warning:</b> this addon may conflict with other addons that use Anki's scheduler.
<b>Important:</b> The addon does not change past schedules, only new schedules.
<b>About:</b>

Select Sunday if you do not want to study on this day or any other day of the week and this addon will select another day in the rescheduling.
You will leave this day free for other tasks or rest.

<img src="https://i.ibb.co/c60sYf3/statistic.jpg" alt="Statistic">	

An Anki Fuzz based range will be used to avoid impacting Anki's algorithm as described in the <a href="https://apps.ankiweb.net/docs/manual.html#what-spaced-repetition-algorithm-does-anki-use">manual</a>:

<i>"After you select an ease button, Anki also applies a small amount of random “fuzz” to prevent cards that were introduced at the same time and given the same ratings from sticking together and always coming up for review on the same day. This fuzz does not appear on the interval buttons, so if you’re noticing a slight discrepancy between what you select and the intervals your cards actually get, this is probably the cause"</i>

<b>Fuzz example:</b>
- Review less than 3 days: will not choose another day.
- Review in 3 days: Choose between days 2 and 4.
- Review in 7 days: Choose between days 5 and 9.
- Review in 90 days: Choose between days 86 and 94.
- Cards you forgot, and return within 2 days it does not choose another day.

If the fuzz range is too small or does not exist (review less than 3 days) to satisfy the parameter condition, the day of the week may be selected for review of the card.

<b>Configuration:</b>

Change the values ​​in the source code for your need.

The default installation value is to skip <b>Sunday</b> and the log message is <b>disabled</b>.

You can enter more than one day of the week, separated by commas, but <b>remember</b> that this can overwhelm the other days.

<code>#-------------Configuration------------------

days_week   = [6]       #[0]=Monday|[1]=Tuesday|[2]=Wednesday|[3]=Thursday|[4]=Friday|[5]=Saturday|[6]=Sunday|[-1]=Ignore

log_tooltip = False     #True or False

#-------------Configuration------------------</code>

Enabling log, the addon will show on the screen which days are being ignored when replying to the card.

Or it will display a message that the fuzz range has not met the required minimum condition.

<img src="https://i.ibb.co/h9HX2FX/ignored-days.png" alt="ignored-days">

Copyright(C)| Carlos Duarte

Based on | xquercus code, in add-on "Load Balanced Scheduler"

License | GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

Source in | https://github.com/cjdduarte/FreeWeekend

<b> #### Change Log:</b>

v1.2 - 2018-12-04
- Added new log message when fuzz does not satisfy required condition

v1.1  - 2018-12-04
- Added log to show ignored days

v1.0 - 2018-12-03
- Initial Release

<b> #### To Do:</b>

- implement text file to select specific days (Example: holidays, trips, etc ...):

- to implement parameterization in Anki: