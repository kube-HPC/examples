from __future__ import print_function, division, absolute_import

import time

def start(args, hkubeapi):
    i = 0
    sent = 0
    rate = 100
    active = True
    process_time = 0.0001
    size = 7000

    if args['input']:
        if type(args['input'][0]) is dict and 'process_time' in args['input'][0]:
            process_time = args['input'][0]['process_time']
        if type(args['input'][0]) is dict and 'rate' in args['input'][0]:
            rate = args['input'][0]['rate']
        if type(args['input'][0]) is dict and 'size' in args['input'][0]:
            size = args['input'][0]['size']


    print("rate is: " + str(rate))
    print("process time: " + str(process_time))
    while active:
        for _ in range(0, rate):
            if active:
                msg = {"image": bytearray(size),
                       "node": 1,
                       "id": str(sent),
                       "time1": time.time()
                       }
                sent += 1
                hkubeapi.sendMessage(msg)
                time.sleep(float(process_time))
        i = i + 1
        time.sleep(1)



def stop(a):
    print("at stop")

