import time
from threading import Thread


class SenderThread(Thread):
    def __init__(self, hkube_api, flow=None, program=[{"rate": 100, "time": 120, "size": 80}]):
        Thread.__init__(self)
        self.program = program
        self.flow = flow
        self.hkube_api = hkube_api

    def run(self):
        sent = 0
        print("Demonstrating ein-")
        while True:
            for scenario in self.program:
                print("Demonstrating ein")
                print("rate is: " + str(scenario["rate"]))
                myimage = bytearray(scenario["size"])
                i = 0
                while i < scenario["time"]:
                    for _ in range(0, int(scenario["rate"])):
                        msg = {"image": myimage,
                               "node": 1,
                               "id": str(sent),
                               "time1": time.time()
                               }
                        sent += 1
                        if self.flow is not None:
                            self.hkube_api.sendMessage(msg, self.flow)
                        else:
                            self.hkube_api.sendMessage(msg)
                    i = i + 1
                    time.sleep(1)
