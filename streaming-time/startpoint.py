from __future__ import print_function, division, absolute_import

import time
global numberOfMsg
numberOfMsg = 0
sum = 0
active = True
sumFromStart = 0
def start(args, hkube_api):
    i = 0
    sent = 0
    rate = 100
    active = True
    process_time = 0.0001
    size = 7000

    print("~~~~~~~~~starts~~~~~~~~~~~~updated")
    def handleMessage(msg, origin):
        global numberOfMsg
        global sum
        global sumFromStart
        global numberOfMsg
        numberOfMsg += 1
        msg['node'] = msg['node'] + 1
        msg["time" + str(msg['node'])] = time.time()
        deltaFromPrev = msg["time" + str(msg['node'])] - msg["time" + str(msg['node'] - 1)]
        fromStart = msg["time" + str(msg['node'])] - msg["time1"]
        sumFromStart += fromStart
        sum += deltaFromPrev
        time.sleep(float(process_time))

    hkube_api.registerInputListener(onMessage=handleMessage)
    hkube_api.startMessageListening()

    flows = None
    if args['input']:
        if type(args['input'][0]) is dict and 'process_time' in args['input'][0]:
            process_time = args['input'][0]['process_time']
        if type(args['input'][0]) is dict and 'rate' in args['input'][0]:
            rate = args['input'][0]['rate']
        if type(args['input'][0]) is dict and 'size' in args['input'][0]:
            size = args['input'][0]['size']
        if type(args['input'][0]) is dict and 'flows' in args['input'][0]:
            flows = args['input'][0]['flows']


    print("Demonstrating ein 0.25")
    print("rate is: " + str(rate))
    print("process time: " + str(process_time))
    myimage = bytearray(size)
    while True:
        for _ in range(0, rate/4):
            if active:
                msg = {"image": myimage,
                       "node": 1,
                       "id": str(sent),
                       "time1": time.time()
                       }
                sent += 1
                if (flows is not None):
                    for flow in flows:
                        hkube_api.sendMessage(msg,flow)
                else:
                    hkube_api.sendMessage(msg)
        i = i + 1
        if i % 20 == 0:
            global numberOfMsg
            if numberOfMsg > 0:
                print("Avg from prev node " + str(sum / numberOfMsg))
                print("Avg from start node " + str(sumFromStart / numberOfMsg))
        time.sleep(0.25)
    time.sleep(600)



def stop(a):
    print("at stop")

