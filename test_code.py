
import datetime
 
start_time = datetime.datetime.now()     #放在程序开始处
 
#doing thing 
 
end_time = datetime.datetime.now()      #放在程序结尾处
 
interval = (end_time-start_time).seconds    #以秒的形式
 
final_time = interval/60.0  #转换成分钟
 
print('final_name:\t', final_time)