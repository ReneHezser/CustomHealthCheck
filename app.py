import time
import random

READ_INTERVAL = 10 #seconds

def writeStatus(status):
    f = open("/app/system-status.txt", "w")
    f.write(status)
    f.close()

def run():
    # set healthy state (0 means healthy)
    print("Starting and writing health check to 'system-status.txt'")
    writeStatus("0")

    next_call = time.time()

    while True:
        next_call = next_call + READ_INTERVAL

        # generating random number and check for one to simulate an error
        if random.randrange(1, 10) == 5:
            print("Simulating failure")
            # set healthy state (1 means unhealthy)
            writeStatus("1")

        print("sleeping...")
        # sleep until the next read cycle by calculating the time between the next desired call and now
        time.sleep(next_call - time.time())

run()  