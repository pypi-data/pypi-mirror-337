from abc import ABC, abstractmethod
from typing import List

from jobs.enums.flow_enum import TaskErrorHandling



class JobInterface(ABC):
    def __init__(self, data=None, parameters=None, errors=None):
        from jobs.flow.flow_builder import TaskFlowBuilder
        self.task_flow_builder: TaskFlowBuilder = TaskFlowBuilder() 
        self.data = data
        self.errors = errors
        self.parameters = parameters
        self.task_flow_builder.data = self.data
        self.task_flow_builder.parameters = self.parameters
        self.task_flow_builder.errors = self.errors
         

    @abstractmethod
    def handle(self):
        return self.data
    

    def configureTasks(self,task_error_action : TaskErrorHandling = TaskErrorHandling.BREAK):
          self.task_flow_builder.task_error_handling = task_error_action
