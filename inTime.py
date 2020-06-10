#!/usr/bin/env python3
import click
import time
import json
import os

def strTime(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    return('{:02d}:{:02d}:{:02d}'.format(int(hours),int(mins), int(sec)))

def setStartTime(value):
    with open('data.json') as json_file:
        data = json.load(json_file)
        data['startTime']['value'] = '%f' % value

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

def getStartTime():
    with open('data.json') as json_file:
        data = json.load(json_file)
        return float(data['startTime']['value'])

def setWorkToday(value):
    with open('data.json') as json_file:
        data = json.load(json_file)
        data['workTime']['value'] = '%f' % value

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

def getWorkToday():
    with open('data.json') as json_file:
        data = json.load(json_file)
        workToday = float(data['workTime']['value'])
        return workToday

def getIsWorking():
    with open('data.json') as json_file:
        data = json.load(json_file)
        return int(data['isWorking']['value'])

def setIsWorking():
    with open('data.json') as json_file:
        data = json.load(json_file)
        data['isWorking']['value'] = '%i' % 1

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

def resetIsWorking():
    with open('data.json') as json_file:
        data = json.load(json_file)
        data['isWorking']['value'] = '%i' % 0

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

def setBankTime(value):
    with open('data.json') as json_file:
        data = json.load(json_file)
        data['bankTime']['value'] = '%f' % value

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

def getBankTime():
    with open('data.json') as json_file:
        data = json.load(json_file)
        return float(data['bankTime']['value'])

def saveAnUndo():
    with open('data.json') as json_file:
        data = json.load(json_file)

    with open('dataUndo.json', 'w') as outfile:
        json.dump(data, outfile)

@click.group()
def cli():
    path = '/home/nobel/Sync/python/workspace/inTime/'
    os.chdir(path)

@cli.command()  # @cli, not @click!
def status():
    if getIsWorking() == 1:
        print("Working!");
        startTime = getStartTime()
        time_lapsed = time.time()-startTime
        print("Total: " + strTime(time_lapsed))
    else:
        print("Not working!");

    print("Hours remaining: "+strTime(getWorkToday()))
    print("Bank time: "+strTime(getBankTime()))

@cli.command()  # @cli, not @click!
def start():
    if getIsWorking():
        print("Error: You are already working!")
        return

    saveAnUndo()
        
    setStartTime(time.time())
    setIsWorking()

@cli.command()  # @cli, not @click!
def stop():
    if getIsWorking() == 0:
        print("Error: You are not working!")
        return

    saveAnUndo()

    startTime = getStartTime()
    time_lapsed = time.time()-startTime
    print(strTime(time_lapsed))

    setWorkToday(getWorkToday() - time_lapsed)
    resetIsWorking()

@cli.command()  # @cli, not @click!
@click.option('--add','addtime',type=click.DateTime(formats=["%H:%M"]))
@click.option('--remove','removetime',type=click.DateTime(formats=["%H:%M"]))
@click.option('--reset/--no-reset',default=False)
def work(addtime,removetime,reset):

    saveAnUndo()

    if addtime:
        addtime = addtime.hour*3600+addtime.minute*60
        setWorkToday(getWorkToday()+addtime)
        print("Added " + strTime(addtime) + " to work today.")

    if removetime:
        removetime = removetime.hour*3600+removetime.minute*60
        setWorkToday(getWorkToday()-removetime)
        print("Removed " + strTime(removetime) + ".")

    if reset:
        setWorkToday(0.0)

    print("Hours remaining: "+strTime(getWorkToday()))

@cli.command()  # @cli, not @click!
def bank():

    saveAnUndo()

    setBankTime(getBankTime() - getWorkToday())
    setWorkToday(0.0)

@cli.command()  # @cli, not @click!
def workday():

    saveAnUndo()
    setWorkToday(5*60*60)

@cli.command()  # @cli, not @click!
def undo():
    with open('dataUndo.json') as json_file:
        data = json.load(json_file)

    saveAnUndo()

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

@cli.command()  # @cli, not @click!
def polybar():
    if getIsWorking():
        startTime = getStartTime()
        time_lapsed = time.time()-startTime
    else:
        time_lapsed = 0

    print("%s %s %s" % (
        strTime(time_lapsed),
        strTime(getWorkToday()),
        strTime(getBankTime()),
        ))

@cli.command()  # @cli, not @click!
@click.pass_context
def toggle(ctx):
    if getIsWorking():
        ctx.invoke(stop)
    else:
        ctx.invoke(start)

if __name__ == '__main__':
    cli(obj={})
