# Credit Card Validator Microservice

### Communication Contract: This contract states how to REQUEST and RECEIVE data from the Credit Card Validator Microservice.
---
#### To **REQUEST** data from the microservice:

- First, establish a connection to the microservice's socket by creating a ZMQ REQ socket and connecting it to the microservice's endpoint: socket = zmq.Context().socket(zmq.REQ) followed by socket.connect("tcp://<microservice-ip>:5555"). Replace <microservice-ip> with the IP address of the machine where the microservice is running. (In this case 'localhost')
- Next, prepare the credit card information to be validated by creating a dictionary with the required fields (ccissuer, ccnumber, and expdate) and convert it to a JSON string.
- Finally, send the request to the microservice by calling the send method on the socket, passing the cc_info_json string as the argument: socket.send(cc_info_json)
 
 ##### Example Call:
 'import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

cc_info = {"ccissuer": "Visa", "ccnumber": "1234 5678 9012 3456", "expdate": "07/25"}
cc_info_json = json.dumps(cc_info)
socket.send(cc_info_json)

result = socket.recv()
result_dict = json.loads(result)
result_str = result_dict['result']
print(result_str)'

---  
 #### To **RECEIVE** data from the microservice:

- After sending the request, wait for the microservice's response by calling the recv method on the socket: result = socket.recv()
- The response received from the microservice is a string in JSON format, which can be parsed to a Python dictionary using json.loads: result_dict = json.loads(result)
- The result dictionary will contain a single key, which is the validation result as a string: result_str = result_dict['result']
---
 
