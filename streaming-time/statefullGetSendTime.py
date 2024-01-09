import time

global numberOfMsg
numberOfMsg = 0
sum = 0
active = True
sumFromStart = 0
childs =[]

def start(args, hkube_api):
    print("~~~~~~~~~starts~~~~~~~~~~~~updated")
    process_time = 0.0001
    if args['input']:
        if type(args['input'][0]) is dict and 'process_time' in args['input'][0]:
            process_time = args['input'][0]['process_time']
    print("process time: " + str(process_time))


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
        global childs
        time.sleep(float(process_time))
        if origin == 'stateless':
            time.sleep(0.01)
        if (childs):
            hkube_api.sendMessage(msg)
    hkube_api.registerInputListener(onMessage=handleMessage)
    hkube_api.startMessageListening()
    active = True
    i = 0
    while (active):
        time.sleep(1)
        i = i + 1
        if i % 20 == 0:
            global  numberOfMsg
            if numberOfMsg > 0:
                print("Avg from prev node " + str(sum / numberOfMsg))
                print("Avg from start node " + str(sumFromStart / numberOfMsg))
def init(options):
    global childs
    childs = options['childs']