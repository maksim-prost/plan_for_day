import openpyxl

from wath import  LIST_WATH
def load_data_from_exel_document():
    wb = openpyxl.load_workbook('расписание.xlsx')
    sheet = wb['Расписание занятий']
    
    hour_lesson = [ ( b.value.strip().split('\n'), 
                    [ c.value.strip(), d.value and d.value.strip(), e.value.strip(), f.value.strip() ] )
                                                    for (_,b,c,d,e,f) in list(sheet.rows)[1:] ]
    sheet = wb['Отработка ктп и птп']
    working_out_dict = {}
    [ working_out_dict.setdefault( d.value, [] ).append(f'{c.value} {a.value} {b.value}') 
                                    for (a,b,c,d) in sheet.rows if d.value in LIST_WATH[0].current_interval()]
    return hour_lesson, working_out_dict 

def create_plan_for_day(hour_lesson, working_out_dict ):
    
    for wath in LIST_WATH: wath.create_folder()
    current_day_lesson = []
    lesson_hour_5 = None
    for hour,lesson in hour_lesson:
        for h in hour:
            if h == '14.00-15.30':
                lesson_hour_5 = lesson 
            else:
                current_day_lesson.append(lesson)
            if h == '21.00-21.20':
                for wath in LIST_WATH:
                    wath.create_plan_for_day(current_day_lesson, lesson_hour_5, working_out_dict.get( wath.cur_day, []) )
                    wath.create_template_report(current_day_lesson)                               
                    wath.next_day() 
                lesson_hour_5 = None
                current_day_lesson = []

if (__name__ == '__main__'):
    create_plan_for_day( *load_data_from_exel_document() )

