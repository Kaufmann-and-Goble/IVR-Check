#!/usr/local/bin/python3

import time
import os
print('\nVersion 0.2')
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
filelocation = '/Volumes/Shared/Apps/IVR_USAGE/output/kandglog_20130829.txt'
savelocation = '/Volumes/Shared/Apps/IVR_USAGE/logs/'
holder = []
final = []
success = 0
plans = []
total = []
data = []
print(x, y, z)

print('Opening File')

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
    print('Adjusting for dates entered')
    count = 0
    print('Month: ' + month)
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
    name = str(curtime) + '-IVR-output.txt'
    print('Output saved to: ' + savelocation + name)
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
    print('# Removed: ' + str(numberRemoved))


def tally():
    count = 0
    while count < len(holder):
        if 'PlanID=' in holder[count]:
            location = str(holder[count]).find('=')
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
    print('TOTAL= ' + str(totalcount))
    output(holder)
    return totalcount


def log(tallytotal):
    print('Log saved to:' + savelocation + curtime + '.txt')
    count = 0
    file = open(savelocation + curtime + '.txt', 'a')
    file.write('Year Specified: [' + str(x) + ']\n')
    file.write('Batch Start Specified: [' + str(y) + ']\n')
    file.write('Batch End Specified: [' + str(z) + ']\n\n')
    while count < len(data):
        file.write(str(data[count] + '\n'))
        count += 1
    file.write('\nTotal: [' + str(tallytotal) + ']\n')
    file.close()


def finalask():
    asks = input('Would you like to open the output files? (y/n) : ')
    print(str(asks))
    if str(asks) is 'y':
        os.system('open /Volumes/Shared/Apps/IVR_USAGE/logs/' + str(curtime) + '.txt')
        os.system('open /Volumes/Shared/Apps/IVR_USAGE/logs/' + str(curtime) + '-IVR-output.txt')
    else:
        print('[DONE]')

timeframe()
doublecheck()
log(tally())
#finalask()
os.system('open /Volumes/Shared/Apps/IVR_USAGE/logs/' + str(curtime) + '.txt')
# os.system('open /Volumes/Shared/Apps/IVR_USAGE/logs/' + str(curtime) + '-IVR-output.txt')



