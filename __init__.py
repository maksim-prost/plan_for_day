import openpyxl
from config import  LIST_WATH, TEMPLATE_WORKING_OUT

def load_data_from_exel_document():
    wb = openpyxl.load_workbook('расписание.xlsx')
    sheet = wb['Расписание занятий']
    hour_lesson = [(b.value.strip().split('\n'), c.value.split("\n1")[0] + f' ({ e.value.strip()}) проводит {f.value.strip()}') for (_,b,c,_,e,f) in list(sheet.rows)[1:]]
    sheet = wb['Отработка ктп и птп']
    working_out_dict = {}
    [ working_out_dict.setdefault( d.value, [] ).append(f'{c.value} {a.value} {b.value}') 
                                    for (a,b,c,d) in sheet.rows if d.value in LIST_WATH[0].current_interval()]
    return hour_lesson, working_out_dict 

def create_plan_for_day(hour_lesson, working_out_dict ):
    current_day_lesson = []
    lesson_hour_5 =''
    for hour,lesson in hour_lesson:
        for h in hour:
            if h == '14.00-15.30':
                lesson_hour_5 = lesson + '\n'
            else:
                current_day_lesson.append(lesson)
            if h == '21.00-21.20':
                for wath in LIST_WATH:
                    working_out = '\n'.join( working_out_dict.get( wath.cur_day,[] ) )
                    lesson_hour_5_all = (lesson_hour_5 and (lesson_hour_5 + working_out)) or (working_out and  f'ОТИ района выезда и охраняемых объектов:\n{working_out}') or TEMPLATE_WORKING_OUT
                    context = {
                        'date_of_approval': wath.view_prev_day(),
                        'date_of_event': wath.view_cur_day(),
                        'hour_5': lesson_hour_5_all,
                        'current_day_lesson':current_day_lesson,
                        }
                    wath.save_plan_day(context)
                    wath.next_day()                                
                lesson_hour_5 = ''
                current_day_lesson = []

if (__name__ == '__main__'):
    create_plan_for_day( *load_data_from_exel_document() )

