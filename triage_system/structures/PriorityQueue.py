class PriorityQueue:
    
    # COLAS 
    
    def __init__(self):
        self.queueNodes = [] 

    def enqueue(self, patient):
        self.queueNodes.append(patient)

    def dequeue(self):
        if not self.isQueueEmpty():
            return self.queueNodes.pop(0) 
        return None

    def isQueueEmpty(self):
        return len(self.queueNodes) == 0