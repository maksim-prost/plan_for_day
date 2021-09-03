import datetime
import locale
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8') 

BEGIN_DAY = 1
BEGIN_MONTH = 9
BEGIN_YEAR = 2021

TEMPLATE_WORKING_OUT = "Повторение обязанностей, работа с документацией, изучение документацией предварительного планирования."


list_wath = [
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
begin_day = datetime.datetime( BEGIN_YEAR,BEGIN_MONTH,BEGIN_DAY )
for i,wath in enumerate( list_wath ):
    wath['cur_day'] = begin_day + datetime.timedelta( days=i)
    # print(wath['cur_day'].strftime('%d %B %Y'))