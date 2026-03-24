class PatientHistory:


    def __init__(self):
        self.stackRecords = []

    def pushToHistory(self, patient):
        self.stackRecords.append(patient) 

    def popFromHistory(self):
        if len(self.stackRecords) > 0:
            return self.stackRecords.pop() 
        return None