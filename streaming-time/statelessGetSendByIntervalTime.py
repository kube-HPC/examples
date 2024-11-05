import time
from datetime import datetime

numberOfMsg = 0
sum = 0
active = True
sumFromStart = 0
currentlyFirst = None  # indicates if we are currently using the first process time


def get_input_value(args, input_name, default_value):
    if args['input'] and type(args['input'][0]) is dict and input_name in args['input'][0]:
        return args['input'][0][input_name]
    else:
        return default_value


def start(args, hkube_api):
    curr_time = time.time()
    change_occurred = False
    global currentlyFirst
    interval = get_input_value(args, 'interval', 60)
    
    currModelo = (curr_time // interval) % 2
        if currentlyFirst is None:  # Initial printing
        change_occurred = True
    else:
        change_occurred = (currentlyFirst != (currModelo == 0))
    currentlyFirst = (currModelo == 0)

    if currentlyFirst:
        process_time = get_input_value(args, 'first_process_time', 1)
    else:
        process_time = get_input_value(args, 'second_process_time', 0.1)

    if change_occurred:
        print(f"Process time is set to: {process_time}")

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
