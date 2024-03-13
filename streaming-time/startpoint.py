from __future__ import print_function, division, absolute_import

from hkube_python_wrapper import Algorunner

from sender import SenderThread
import time

global numberOfMsg
numberOfMsg = 0
sum = 0
active = True
sumFromStart = 0
process_time = 0.0001

def start(args, hkube_api):
    i = 0
    sent = 0
    rate = 100
    active = True
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
            print ("Got process time " + str(process_time))
        if len(args['input']) > 0 and isinstance(args['input'][0], dict) and args['input'][0].get("flows") is not None:
            print("has flows")
            for flow in args['input'][0]['flows']:
                print("about to start flow with " + str(flow))
                sender = SenderThread(hkube_api=hkube_api, flow=flow["name"], program=flow["program"])
                sender.start()
        else:
            print("no flows" + str(args["input"][0]))
            if type(args['input'][0]) is dict and 'rate' in args['input'][0]:
                rate = args['input'][0]['rate']
            if type(args['input'][0]) is dict and 'size' in args['input'][0]:
                size = args['input'][0]['size']
            sender = SenderThread(hkube_api=hkube_api, flow=None,
                                  program=[{"rate": rate, "size": size, "time": 120}])
            sender.start()

    myimage = bytearray(size)

    while True:
        i = i + 1
        if i % 80 == 0:
            global numberOfMsg
            if numberOfMsg > 0:
                print("Avg from prev node " + str(sum / numberOfMsg))
                print("Avg from start node " + str(sumFromStart / numberOfMsg))
        time.sleep(0.25)


def stop(a):
    print("at stop")


def main():
    print("starting algorithm runner")
    print(str(Algorunner))

    Algorunner.Debug('ws://cd.hkube.io/hkube/debug/return-range', start=start)
    # Algorunner.Run(start=start, init=init)


if __name__ == "__main__":
    main()
