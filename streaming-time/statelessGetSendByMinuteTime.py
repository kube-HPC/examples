import time
from datetime import datetime

numberOfMsg = 0
sum = 0
active = True
sumFromStart = 0
lastWasEven = False


def getInputValue(args, input_name, default_value):
    if args['input'] and type(args['input'][0]) is dict and input_name in args['input'][0]:
        return args['input'][0][input_name]
    else:
        return default_value


def start(args, hkube_api):
    current_minute = datetime.now().minute
    global lastWasEven
    if current_minute % 2 == 0:
        process_time = getInputValue(args, 'even_minute_process_time', 1)
        if not lastWasEven:
            print(f"Process time is now {process_time}")
            lastWasEven = True
    else:
        process_time = getInputValue(args, 'odd_minute_process_time', 0.1)
        if lastWasEven:
            print(f"Process time is now {process_time}")
            lastWasEven = False
            
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



def main():
    print("starting algorithm runner")
    print(str(Algorunner))
    Algorunner.Debug('ws://dev.hkube.org/hkube/debug/stateless-time-statistics', start=start)
    
if __name__ == "__main__":
    main()
