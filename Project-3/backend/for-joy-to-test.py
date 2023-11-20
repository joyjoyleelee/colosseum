from datetime import datetime

now = str(datetime.now()).split(" ")
current_date = now[0].split('-')
current_time = now[1].split(':')
print(f'Current date: {current_date}')
print(f'Current time: {current_time}')