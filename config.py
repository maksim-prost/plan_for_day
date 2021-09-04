import datetime
import os
import locale
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8') 
from docxtpl import DocxTemplate

begin_day = 1
begin_month = 9
begin_year = 2021

BEGIN_DAY = datetime.datetime( begin_year,begin_month,begin_day)

TEMPLATE_WORKING_OUT = "Повторение обязанностей, работа с документацией, изучение документацией предварительного планирования."


list_dict_wath = [
    { 
        'post' : "Помощник начальника караула",
        'post_usage' : "помощника начальника 1 караула",
        'name' : "А.В. Чикуров" ,
        'title' : "старшина внутренней службы",
        'number': 1,
    },
    { 
        'post' : "Командир отделения",
        'post_usage' : "командира отделения 2 караула",
        'name' : "В.В. Быков" ,
        'title' : '',
        'number': 2,
    },
    { 
        'post' : "Помощник начальника караула",
        'post_usage' : "помощника начальника 3 караула",
        'name' : "М.В. Корнев" ,
        'title' : "старший сержант внутренней службы",
        'number': 3,
    },
    { 
        'post' : "Командир отделения",# "Помощник начальника караула",
        'post_usage' : "командира отделения 4 караула",#помощника начальника 4 караула",
        'name' : "Гудков С.К.",#"А.И. Савченко" ,
        'title' : "",#"старший прапорщик внутренней службы",
        'number': 4,
    },
    
]

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
        if  not os.path.isdir( self.folder ):
            os.mkdir( self.folder )
    
    def next_day(self):
        self.prev_day =  self.cur_day
        self.cur_day = self.cur_day + datetime.timedelta( days=4)

    def view_cur_day(self):
        return self.cur_day.strftime('%d %B %Y')
    
    def view_prev_day(self):
        return self.prev_day.strftime('%d %B %Y')

    def save_plan_day (self, context):
        context.update(self.__dict__) 
        doc = DocxTemplate('план работы на сутки.docx')
        doc.render(context)
        doc.save(f"{self.folder}/план работы на {self.view_cur_day()}.docx")
    @classmethod
    def current_interval(cls):
        next_month = (BEGIN_DAY + datetime.timedelta(15)).month%12 +1
        cur_year = begin_year +1 if next_month==1 else  begin_year
        end_interval = datetime.datetime( cur_year,next_month,1)
        return (BEGIN_DAY + datetime.timedelta(i) for i in  range((end_interval-BEGIN_DAY).days))
        
LIST_WATH = [Wath(temp_wath) for temp_wath in list_dict_wath]

