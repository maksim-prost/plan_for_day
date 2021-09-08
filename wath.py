import datetime
import os
import locale
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8') 
from docxtpl import DocxTemplate
from collections import Counter

from config import BEGIN_DAY, TEMPLATE_WORKING_OUT, list_dict_wath

class Wath():
    current_month = (BEGIN_DAY + datetime.timedelta( days=15)).strftime('%B')#расписание занятий может начинаться с последних чисел предыдущего месяца
    
    def __init__(self, template_wath) -> None:
        self.post = template_wath['post']
        self.post_usage = template_wath['post_usage']
        self.name = template_wath['name']
        self.title = template_wath['title']
        self.number = template_wath['number']
        self.cur_day = BEGIN_DAY + datetime.timedelta( days=self.number-1)
        self.prev_day = self.cur_day - datetime.timedelta( days=4)
        self.folder = f"планы работы на сутки {self.number} караула в {self.current_month}"
        
    def create_folder(self):
        os.path.isdir( self.folder ) or  os.mkdir( self.folder )
        os.path.isdir( f'{self.folder}/план конспекты' ) or  os.mkdir(f'{self.folder}/план конспекты'  )
     
    def next_day(self):
        self.prev_day =  self.cur_day
        self.cur_day = self.cur_day + datetime.timedelta( days=4)

    def view_cur_day(self):
        return self.cur_day.strftime('%d %B %Y')
    
    def view_prev_day(self):
        return self.prev_day.strftime('%d %B %Y')
    
    def create_template_report(self, list_lesson):
        
        count_hour_for_lesson = Counter((c,d,e,f) for c,d,e,f in list_lesson[:3])
        for (c,d,e,f) in count_hour_for_lesson:
            if 'пнк' not in f.lower(): continue
            template, *questions  = c.split('\n')
            [question_1, question_2] = questions and questions or ['','']
            subject_study = template.split(':')[0]
            theme = template.split('«')[1].split('»')[0]
            lecture = 'кл.гр' in e.lower()
            context = {
                        'date_of_approval': self.view_prev_day(),
                        'date_of_event': self.view_cur_day(),
                        'lecture': lecture,
                        'theme' :theme,
                        'question_1': question_1,
                        'question_2': question_2,
                        'list_of_sources':d or '',
                        'count_hour': count_hour_for_lesson[(c,d,e,f)],
                        'subject_study':subject_study
                        }
            self.save_in_docx(context, 'шаблон для план-конспекта на сутки.docx', 
                        f"{self.folder}/план конспекты/{self.view_cur_day()} {subject_study} {theme[:35]}.docx")
           
    def create_plan_for_day(self,current_day_lesson, lesson_hour_5, working_out):
        
        n_l_1, n_l = '\n1','\n'
        lesson = [f'{c.split(n_l_1)[0]} ({ e.strip()}) проводит {f.strip()}'
                            for (c,_,e,f) in current_day_lesson ]
        context = {
                    'date_of_approval': self.view_prev_day(),
                    'date_of_event': self.view_cur_day(),
                    'hour_5':   (lesson_hour_5 and '\n'.join([lesson_hour_5[0].split(n_l_1)[0]] + working_out) ) or
                                (working_out and  f'ОТИ района выезда и охраняемых объектов:\n{n_l.join(working_out)}') or
                                TEMPLATE_WORKING_OUT,
                    'current_day_lesson':lesson,
                    }
        self.save_in_docx(context,'план работы на сутки.docx',f"{self.folder}/план работы на {self.view_cur_day()}.docx")

    def save_in_docx (self, context, template, name_file):
        context.update(self.__dict__) 
        doc = DocxTemplate(template)
        doc.render(context)
        doc.save(name_file)
    


    @classmethod
    def current_interval(cls):
        next_month = (BEGIN_DAY + datetime.timedelta(15)).month%12 +1
        cur_year = BEGIN_DAY.year +1 if next_month==1 else  BEGIN_DAY.year 
        end_interval = datetime.datetime( cur_year,next_month,1)
        return (BEGIN_DAY + datetime.timedelta(i) for i in  range((end_interval-BEGIN_DAY).days))

LIST_WATH = [Wath(temp_wath) for temp_wath in list_dict_wath]