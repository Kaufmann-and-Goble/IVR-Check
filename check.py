

import time

curtime = time.strftime("%Y-%m-%d")
print('\n###########################################################################################')
print('    -This is a program that will take the IVR log located in * and open / read it to      \t\n    output successful IVR connections and count the total number of connections per Plan. \t')
print('    -The program goes from the beginning of the specified month, to the end.\t\t\t\t')
print('###########################################################################################\n')
print('----------EXAMPLE----------')
print('[YEAR]: 2017')
print('[STARTING MONTH]: 8\t *This is for if we want to start the batch in August(8)')
print('[ENDING MONTH]: 9\t *This is for if we want to end the batch in September(9)')
print('--------END EXAMPLE--------\n')
x = input('[YEAR]: ')
y = input('[STARTING MONTH]: ')
z = input('[ENDING MONTH]: ')
filelocation = '/Volumes/Shared/Andrew/Apps/IVR_USAGE/output/kandglog_20130829.txt'
savelocation = '/Volumes/Shared/Andrew/Apps/IVR_USAGE/logs/'
holder = []
final = []
success = 0
hour = ''
minute = ''
hourminute = [0]*24
hours = list(range(24))
plans = []
total = []
data = []
display = []

print('\nOpening File\n')

with open(filelocation) as a:
    storage = a.readlines()
    a.close()


def success_check(place):
    count = 0
    success = 0
    while count < len(place):
        if 'kgaSuccess' in place[count]:
            final.append(place[count - 1])
            print(place[count - 1])
            final.append(place[count] + '\n')
            print(place[count])
            success += 1
        count += 1
    output(final)
    print('# of Successful connections: ' + str(success))


def date_check(month):
    count = 0
    while count < len(storage):
        if 'kgaSuccess' in storage[count] and str(x) + '-' + str(month) in storage[count]:
            holder.append(storage[count - 1])
            holder.append(storage[count])
        count += 1


def timeframe():
    start = int(y)
    end = int(z)
    current = start
    while int(current) <= int(end):
        current = '{:0>2}'.format(current)
        date_check(current)
        current = int(current) + 1


def output(export):
    name = str(curtime) + '-IVR-output''.txt'
    print('\nOutput saved to: \t\t' + savelocation + name)
    file = open(savelocation + name, 'w')
    for line in export:
        b = str(line)
        file.write(b + '\n')
    file.close()


def doublecheck():
    count = 0
    numberRemoved = 0
    while count < len(holder):
        if 'kgaFailure' in holder[count]:
            holder.pop(count)
            holder.pop(count - 1)
            holder.pop(count + 1)
            numberRemoved += 1
        count += 1
    print('# Removed: ' + str(numberRemoved) + '\n')


def tally():
    count = 0
    hold = 0
    tallys = 1
    file = open(savelocation + str(curtime) + '-TOTAL.csv', 'w')
    while count < len(holder):
        if 'PlanID=' in holder[count]:
            location = str(holder[count]).find('=')
            month = str(holder[count][5])+str(holder[count][6])
            day = holder[count][8:10]
            timestamp(count)
            when = (str(month) + ('-' + (str(day))))
            if len(display) >= 2:
                line = display[hold - 1]
                oldwhen = str(line[0:5])
                if str(oldwhen) == str(when):
                    tallys += 1
                else:
                    display.append(str(when) + ',' + str(tallys))
                    file.write(str(when) + ',' + str(tallys) + '\n')
                    tallys = 1
                    hold += 1
            if len(display) <= 1:
                display.append(when)
                file.write(str(when) + '\n')
                hold += 1
            ids = (str(holder[count])[location + 1:location + 4])
            total.append(ids)
            if ids not in plans:
                plans.append(ids)
        count += 1
    plans.sort()
    totalcount = 0
    number = 0
    while number < len(plans):
        data.append('# of [' + str(plans[number]) + '] uses = ' + str(total.count(str(plans[number]))))
        print('# of [' + str(plans[number]) + '] uses = ' + str(total.count(str(plans[number]))))
        totalcount += total.count(str(plans[number]))
        number += 1
    print('\nTOTAL= ' + str(totalcount))
    output(holder)
    file.close()
    print('Total Usage saved to: \t' + savelocation + curtime + '-TOTAL.csv')
    return display


def log(tallytotal):
    print('Log saved to: \t\t\t' + savelocation + curtime + '.txt')
    count = 0
    file = open(savelocation + curtime + '.txt', 'w')
    file.write('Year Specified: [' + str(x) + ']\n')
    file.write('Batch Start Specified: [' + str(y) + ']\n')
    file.write('Batch End Specified: [' + str(z) + ']\n\n')
    while count < len(data):
        file.write(str(data[count] + '\n'))
        count += 1
    file.write('\nTotal: [' + str(tallytotal) + ']\n')
    file.close()


def timestamp(count):
    hour = int(holder[count][11:13])
    hourminute[hour] = hourminute[hour] + 1


def csv():
    file = open(savelocation + curtime + '-HOURLY.csv', 'w')
    for line in hours:
        file.write(str(hours[line]) + ',' + str(hourminute[line]) + '\n')
    file.close()
    print('Hourly saved to: \t\t' + savelocation + curtime + '-HOURLY.csv')





timeframe()
doublecheck()
log(tally())
csv()




