import time
from datetime import datetime

numberOfMsg = 0
sum = 0
active = True
sumFromStart = 0
currentlyFirst = None
lastModelo = 0


def get_input_value(args, input_name, default_value):
    if args['input'] and type(args['input'][0]) is dict and input_name in args['input'][0]:
        return args['input'][0][input_name]
    else:
        return default_value


def start(args, hkube_api):
    curr_time = time.time()
    change_occurred = False
    interval = get_input_value(args, 'interval', 60)
    global currentlyFirst
    global lastModelo
    if currentlyFirst is None:  # Initial values
        lastModelo = (curr_time // interval) % 2
        currentlyFirst = True
        change_occurred = True

    curr_modelo = (curr_time // interval) % 2
    if curr_modelo != lastModelo:
        currentlyFirst = not currentlyFirst
        change_occurred = True
        lastModelo = curr_modelo

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
