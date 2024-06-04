# Chat app
import microbit
import threading

# Find the channel you and your recipient is on
def find_channels(sender, recipient):
    microbit.radio.config(channel=1, group=1, queue=10, length=251)
    users = {}

    while True:
        request = f"GET_GROUP:{recipient}"
        microbit.radio.send(request)
        response = microbit.radio.receive()
        if response != "None":
            user = response.split(":")[0]
            channel = response.split(":")[1]
            if channel == "Not Found" or user in channels:
                continue
            if user == recipient or user == sender:
                users[user] = int(channel)
                if len(channels.keys()) == 2:
                    break
        microbit.sleep(1000)

    return channels

microbit.radio.on()

# TODO: sender and recipient name validation with regex
#sender = input("Who are you (first.last)?")
#recipient = input("Who do you want to talk to (first.last)?")

# Connect on the larger of the two group ids
# channels = find_channels(sender, recipient)
channels = {
    "abigail.adegbiji": 0,
    "katerina.broten": 13
}
num = max(channels.values())
microbit.radio.config(channel=num, group=num)

lock = threading.Lock()

def send():
    global lock
    while True:
        message = input(">")
        lock.acquire()
        microbit.radio.send(message)
        lock.release()

def receive():
    global lock
    while True:
        lock.acquire()
        message = microbit.radio.receive()
        lock.release()
        if message != "None":
            print("Received:", message)

# Dispatch threads
threads = [
    threading.Thread(target=send, args=()),
    threading.Thread(target=receive, args=())
]
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()