# import os
# import datetime
import openpyxl

from config import  LIST_WATH, TEMPLATE_WORKING_OUT


def load_data_from_exel_document():
    wb = openpyxl.load_workbook('расписание.xlsx')
    sheet = wb['Расписание занятий']
    list_hour = [ b.value.strip().split('\n') for b in sheet['b'] ]
    list_lesson = [ c.value.split("\n1")[0] + f' ({ e.value.strip()}) проводит {f.value.strip()}' for c,e,f in zip( sheet['c'],sheet['e'],sheet['f']  ) ]
    
    sheet = wb['Отработка ктп и птп']
    list_date_working_out = [ d.value for d in sheet['d'] ]
    list_location_working_out = [ f'{c.value} {a.value} {b.value}' for (a,b,c) in zip(sheet['a'],sheet['b'],sheet['c']) ]
    
    return list_hour, list_lesson, list_date_working_out, list_location_working_out


def create_plan_for_day(list_hour, list_lesson, list_date_working_out, list_location_working_out):
    current_day_lesson = []
    hour_5_all =''
    for hour,lesson in zip(list_hour,list_lesson):
        for h in hour:
            if h == '14.00-15.30':
                hour_5_all = lesson + '\n'
            else:
                current_day_lesson.append(lesson)
            if h == '21.00-21.20':
                for wath in LIST_WATH:
                    indices = [ i for i, x in enumerate(list_date_working_out) if x == wath.cur_day ] 
                    working_out = '\n'.join( [ list_location_working_out[i] for i in indices ] )
                    
                    hour_5 = (hour_5_all and (hour_5_all + working_out)) or (working_out and  f'ОТИ района выезда и охраняемых объектов:\n{working_out}') or TEMPLATE_WORKING_OUT
                    context = {
                        'date_of_approval': wath.view_prev_day(),
                        'date_of_event': wath.view_cur_day(),
                        'hour_5': hour_5,
                        'current_day_lesson':current_day_lesson,
                        }
                    wath.save_plan_day(context)
                    wath.next_day()               
                    
                hour_5_all = ''
                current_day_lesson = []

if (__name__ == '__main__'):
    create_plan_for_day( *load_data_from_exel_document())

