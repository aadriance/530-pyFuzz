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
    #prints the call tree from this object
    def printCallTree(self):
        self.printTreeLevel(0)
    #tree print helper
    def printTreeLevel(self, level):
        line = '|'
        for i in range(0,level):
            line += '-'
        line += self.descriptor
        print(line)
        for child in self.flowTrace:
            child.printTreeLevel(level+1)
    #print the call stats
    def printStats(self, funcList):
        stats = self.calcStats(funcList)
        print("Call count:")
        called = 0
        notCalled = 0
        for key, value in stats.items():
            print("|{} : {}".format(key, value))
            if value > 0:
                called += 1
            else:
                notCalled += 1
        print("{}% of functions called".format(100*called/(called + notCalled)))
    #calcs call stats
    def calcStats(self, funcList):
        stats = dict()
        for name in funcList:
            stats[name] = 0
        self.addMyStats(stats)
        return stats
    #adds your stats to the dict
    def addMyStats(self, stats):
        if self.descriptor in stats:
            stats[self.descriptor] += 1
        else:
            stats[self.descriptor] = 1
        for child in self.flowTrace:
            child.addMyStats(stats)


def calcStats(funcList, runList):
    stats = dict()
    for name in funcList:
        stats[name] = 0
    for run in runList:
        newStats = run.calcStats(funcList)
        for name in funcList:
            stats[name] += newStats[name]
    return stats

 #print the call stats
def printStats(stats):
    print("Call count:")
    called = 0
    notCalled = 0
    for key, value in stats.items():
        print("|{} : {}".format(key, value))
        if value > 0:
            called += 1
        else:
            notCalled += 1
    print("{}% of functions called".format(100*called/(called + notCalled)))

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