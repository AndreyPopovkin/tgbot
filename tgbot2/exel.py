# -*- coding: utf-8 -*-

import xlrd
import xlwt
import time
import const

"""
1. Понедельник
2. Вторник
3. Среда
4. Четверг
5. Пятница
6. Суббота
7. Сегодня
8. Завтра
"""
def getTimeTable(group_name, exel_name, decision):
    workbook = xlrd.open_workbook(exel_name)
    try:
        #print group_name
        #print u"ВОД-2015-1"
        #print u"ВОД-2015-1" == group_name
        worksheet = workbook.sheet_by_name(group_name)
        #worksheet = workbook.sheet_by_name(u"ВОД-2015-1")
    except xlrd.biffh.XLRDError:
        print ("group_name_error")
        return "wrong group name, maybe this group isn't in new table, please write to support\n"
    dataLine = 14;
    dataColumn = 2;

    weeknum = "%U"
    week = int(time.strftime(weeknum))
    if (week % 2 == 0):
        dataLine += 1

    if decision == 7:
        daynum = "%w"
        day = int(time.strftime(daynum))
        decision = day
    elif decision == 8:
        daynum = "%w"
        day = int(time.strftime(daynum))
        decision = day + 1
        if (day == 0):
            week += 1

    ans = ""
    if 1 <= decision and decision <= 6:
        a = 1
        while (a <= 6):
            weekdayShift = 12 * (decision - 1)
            clock = worksheet.cell(dataLine + weekdayShift, dataColumn).value
            name = worksheet.cell(dataLine + weekdayShift, dataColumn + 2).value
            aud = worksheet.cell(dataLine + weekdayShift, dataColumn + 3).value
            ans += str(a) + u" пара:" \
                + clock + ' ' + \
                name + ' ' + aud + u"\n"
            a += 1
            dataLine += 2
    else:
        ans = "error, maybe wrong weekday index (found or calculated: {})".format(decision)
    return ans
