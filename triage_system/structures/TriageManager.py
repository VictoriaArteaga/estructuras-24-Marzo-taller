import streamlit as st
from PatientHistory import PatientHistory
from PriorityQueue import PriorityQueue


class TriageManager:
    def __init__(self):

        self.priorityCategories = ["High", "Medium", "Low"]

        if 'triageState' not in st.session_state:
            st.session_state.triageState = {
                'criticalQueue': PriorityQueue(),
                'urgentQueue': PriorityQueue(),
                'standardQueue': PriorityQueue(),
                'archiveStack': PatientHistory(),
                'globalRegistry': []
            }
        
        self.currentData = st.session_state.triageState

    def registerPatient(self, patient):
        self.currentData['globalRegistry'].append(patient)
        
        if patient.priorityLevel == "High":
            self.currentData['criticalQueue'].enqueue(patient)
        elif patient.priorityLevel == "Medium":
            self.currentData['urgentQueue'].enqueue(patient)
        else:
            self.currentData['standardQueue'].enqueue(patient)

    def dispatchPatient(self):
        targetPatient = None
        
        if not self.currentData['criticalQueue'].isQueueEmpty():
            targetPatient = self.currentData['criticalQueue'].dequeue()
        elif not self.currentData['urgentQueue'].isQueueEmpty():
            targetPatient = self.currentData['urgentQueue'].dequeue()
        elif not self.currentData['standardQueue'].isQueueEmpty():
            targetPatient = self.currentData['standardQueue'].dequeue()
            
        if targetPatient:

            self.currentData['archiveStack'].pushToHistory(targetPatient)
            
        return targetPatient
    

    def getSystemState(self):

        return {
            "high": self.currentData['criticalQueue'].queueNodes,
            "medium": self.currentData['urgentQueue'].queueNodes,
            "low": self.currentData['standardQueue'].queueNodes,
            "history": self.currentData['archiveStack'].stackRecords,
            "allPatients": self.currentData['globalRegistry']
        }
    
    
    def UndoLastDispatch(self):

        patient = self.currentData['archiveStack'].popFromHistory()

        if not patient:
            return None

        if patient.priorityLevel == "High":
            self.currentData['criticalQueue'].queueNodes.insert(0, patient)

        elif patient.priorityLevel == "Medium":
            self.currentData['urgentQueue'].queueNodes.insert(0, patient)

        else:
            self.currentData['standardQueue'].queueNodes.insert(0, patient)

        return patient  
    
    
    def getCounts(self):
        return {
            "high": len(self.currentData['criticalQueue'].queueNodes),
            "medium": len(self.currentData['urgentQueue'].queueNodes),
            "low": len(self.currentData['standardQueue'].queueNodes),
            "history": len(self.currentData['archiveStack'].stackRecords),
            "total": len(self.currentData['globalRegistry'])

        }
    
    
