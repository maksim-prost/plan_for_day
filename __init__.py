import os
import datetime
import openpyxl
from docxtpl import DocxTemplate
from config import  list_wath, TEMPLATE_WORKING_OUT


def load_data_from_exel_document():
    wb = openpyxl.load_workbook('расписание.xlsx')
    sheet = wb['Расписание занятий']

    list_hour = [ b.value.strip().split('\n') for b in sheet['b'] ]
    list_lesson = [ c.value.split("\n1")[0] + f' ({ e.value.strip()}) проводит {f.value.strip()}' for c,e,f in zip( sheet['c'],sheet['e'],sheet['f']  ) ]
    sheet = wb['Отработка ктп и птп']
    list_date_working_out = [ d.value for d in sheet['d'] ]
    list_location_working_out = [ f'{c.value} {a.value} {b.value}' for (a,b,c) in zip(sheet['a'],sheet['b'],sheet['c']) ]
    return list_hour, list_lesson, list_date_working_out, list_location_working_out


def create_plan_for_day(current_month, list_wath, list_hour, list_lesson, list_date_working_out, list_location_working_out):
    current_day_lesson = []
    hour_5_all =''
    for hour,lesson in zip(list_hour,list_lesson):
        for h in hour:
            if h == '14.00-15.30':
                hour_5_all = lesson + '\n'
            else:
                current_day_lesson.append(lesson)
            if h == '21.00-21.20':
                for wath in list_wath:
                    # cur_datetime = datetime.datetime(2021,8 , current_day)
                    indices = [ i for i, x in enumerate(list_date_working_out) if x == wath['cur_day'] ] 
                    working_out = '\n'.join( [ list_location_working_out[i] for i in indices ] )
                    
                    hour_5 = (hour_5_all and (hour_5_all + working_out)) or (working_out and  f'ОТИ района выезда и охраняемых объектов:\n{working_out}') or TEMPLATE_WORKING_OUT
                    context = {
                        'date_of_approval': ( wath['cur_day'] - datetime.timedelta(days=4) ).strftime('%d %B %Y г.'),
                        'date_of_event': wath['cur_day'].strftime('%d %B %Y г.'),
                        'hour_5': hour_5,
                        'current_day_lesson':current_day_lesson,
                        }
                    
                    context.update(wath) 

                    doc = DocxTemplate('план работы на сутки.docx')
                    doc.render(context)
                    folder = f"планы работы на сутки {wath['number']} караула в {current_month}"
                    doc.save(f"{folder}/план работы на {wath['cur_day'].strftime('%d %B %Y')}.docx")
                    
                    wath['cur_day'] =  wath['cur_day'] + datetime.timedelta(days=4) 
                hour_5_all = ''
                current_day_lesson = []

if (__name__ == '__main__'):
    current_month = list_wath[3]['cur_day'].strftime('%B')
    for wath in list_wath:
        folder = f"планы работы на сутки {wath['number']} караула в {current_month}"
        if  not os.path.isdir( folder ):
            os.mkdir( folder )
    create_plan_for_day( current_month, list_wath,*load_data_from_exel_document())
# os.system("libreoffice список.docx")

