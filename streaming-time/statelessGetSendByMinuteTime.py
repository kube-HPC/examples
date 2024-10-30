import time
from datetime import datetime

numberOfMsg = 0
sum = 0
active = True
sumFromStart = 0
lastWasEven = false


def start(args, hkube_api):
    current_minute = datetime.now().minute
    global lastWasEven
    if current_minute % 2 == 0:
        process_time = 1
        if not lastWasEven:
            print("Minute is even")
            lastWasEven = true
    else:
        process_time = 0.1
        if lastWasEven:
            print("Minute is odd")
            lastWasEven = false

    if args['input']:
        if current_minute % 2 == 1:
            if type(args['input'][0]) is dict and 'odd_minute_process_time' in args['input'][0]:
                process_time = args['input'][0]['odd_minute_process_time']
        else:
            if type(args['input'][0]) is dict and 'even_minute_process_time' in args['input'][0]:
                process_time = args['input'][0]['even_minute_process_time']
    msg = args.get('streamInput')['message']
    global numberOfMsg
    global sum
    global sumFromStart
    numberOfMsg += 1
    msg['node'] = msg['node'] + 1
    msg["time" + str(msg['node'])] = time.time()
    deltaFromPrev = msg["time" + str(msg['node'])] - msg["time" + str(msg['node'] - 1)]
    fromStart = msg["time" + str(msg['node'])] - msg["time1"]
    sumFromStart += fromStart
    sum += deltaFromPrev
    if numberOfMsg % 40 == 1:
        print("Avg from prev node " + str(sum / numberOfMsg))
        print("Avg from start node " + str(sumFromStart / numberOfMsg))
    time.sleep(process_time)
    return msg



if __name__ == '__main__':
    start(args={'streamInput': {'message': "hi"}}, hkube_api="None")