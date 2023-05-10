# Author: Jomar Malpica
# Course: CS 361
# Date: 2023-05-08

import json
import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to Credit Card Validator…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
print("Connected!\n")

#  Do 10 requests, waiting each time for a response
data_dict = {}

with open("ccinfo.json", "r") as in_file:
    data_dict = json.load(in_file)

for cc in data_dict["Creditcards"]:
    print("Sending request…")
    socket.send_json(cc)

    #  Get the reply.
    message = socket.recv()
    print(f"Validation Processed:", message.decode())
