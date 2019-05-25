import os
import time


# show raspberry temperature,CPU,memory


def getCPUtemp():
    cpuTemp = os.popen('vcgencmd measure_temp').readline()
    cpuTemp = float(cpuTemp.replace('temp=', '').replace('\'C\n', ''))
    return cpuTemp


def getCPUusage():
    # calculate CPU with two short time, time2 - time1
    time1 = os.popen('cat /proc/stat').readline().split()[1:5]
    time.sleep(0.2)
    time2 = os.popen('cat /proc/stat').readline().split()[1:5]
    deltaUsed = int(time2[0]) - int(time1[0]) + int(time2[2]) - int(time1[2])
    deltaTotal = deltaUsed + int(time2[3]) - int(time1[3])
    cpuUsage = float(deltaUsed) / float(deltaTotal) * 100
    return cpuUsage


def getRAM():
    # get RAM as list,list[7],[8],[9]:total,used,free
    RAM = os.popen('free').read().split()[7:10]
    # convert kb in Mb for readablility
    RAM0 = float(RAM[0]) / 1024
    RAM1 = float(RAM[1]) / 1024
    percent = RAM1 / RAM0 * 100
    RAM2 = float(RAM[2]) / 1024
    return percent


def getInfo():
    cpuTemp = getCPUtemp()
    cpuUsage = getCPUusage()
    ramUsage = getRAM()
    print('-CPU: Temp={0:0.1f}`C  Use={1:0.1f}%  Ram={2:0.1f}%'.format(cpuTemp, cpuUsage, ramUsage))
    return cpuTemp, cpuUsage, ramUsage
