import numpy as np

def zellers_congruence(date, month, year):
    
    if month < 3:
        month = 12+ month
        year -= 1
    
    
    d= year % 100
    c = year // 100

    h= (date+(13*(month+1)//5)+d+(d//4)+(c//4)-2*c) % 7
    print(h)
    h = round(h)
    day = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    day = day[h]
    return day
