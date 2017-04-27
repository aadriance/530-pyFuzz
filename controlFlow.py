#controlFlow.py defines the ControlFlow class
import json

class ControlFlow:
    def __init__(self):
        #the sequence of control flow objects
        self.flowTrace = []
        #how we refer to this thing.  Maybe a function name, or conditional statement
        #for the first turn in this is certainly just going to be a function name
        self.descriptor = ''
        #a dictionary of string:value where string is the parameter, and value is it's value.
        #for a function its relevent variables, for a conditional its what it is checking
        #we won't really need to use this for the first turn in
        self.parameters = dict()
    #encodes self and returns a json string
    def encode(self):
        return json.dumps(self, default = jdefault)
    #Takes as a parameters an object returned by json.loads
    #ANY NEW CLASS VARAIBLES NEED TO BE ADDED HERE
    def load(self, jObj):
        self.descriptor = jObj["descriptor"]
        self.parameters = jObj["parameters"]
        #get flow trace array, add elements one by one
        flowFromJ = jObj["flowTrace"]
        for flow in flowFromJ:
            newFlow = ControlFlow()
            newFlow.load(flow)
            self.flowTrace.append(newFlow)
    #takes a json string and loads the object
    def decode(self, jStr):
        self.load(json.loads(jStr))
    
#Tells json library how to handle out object
def jdefault(o):
    return o.__dict__

#Function to test the json encoding/decoding
def test():
    top = ControlFlow()
    top.descriptor = 'top'
    bottom = ControlFlow()
    bottom.descriptor = 'bottom'
    top.flowTrace.append(bottom)
    print(top.encode())
    fromJson = ControlFlow()
    fromJson.decode(top.encode())
    print(fromJson.encode())