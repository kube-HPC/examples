import time
import random

numberOfMsg = 0
sum = 0
active = True
sumFromStart = 0


def start(args, hkube_api):
    min_process_time = 0.0001
    max_process_time = 1
    if args['input']:
        if type(args['input'][0]) is dict and 'min_process_time' in args['input'][0]:
            min_process_time = args['input'][0]['min_process_time']
        if type(args['input'][0]) is dict and 'max_process_time' in args['input'][0]:
            max_process_time = args['input'][0]['max_process_time']
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
    time.sleep(random.uniform(min_process_time, max_process_time))
    return msg



if __name__ == '__main__':
    start(args={'streamInput': {'message': "hi"}}, hkube_api="None")