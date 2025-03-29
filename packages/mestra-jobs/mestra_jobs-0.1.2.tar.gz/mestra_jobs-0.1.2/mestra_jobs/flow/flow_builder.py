

from typing import List, Optional

from jobs.enums.flow_enum import ExitStatus, TaskErrorHandling
from jobs.interfaces.job_interface import JobInterface
from jobs.interfaces.task_interface import TaskInterface
from jobs.interfaces.task_validator_interface import TaskValidatorInterface

class JobFlowBuilder():
    
    def __init__(self,data={}) -> None:
        self.data = data
        self.errors = []
        self.jobs : List[JobInterface] = []  
        self.parameters : Optional[dict] = {}
        self.currenty_job : Optional[JobInterface] = None
       
    def add(self, job : JobInterface):
        job.task_flow_builder.data = job.data = self.data
        job.task_flow_builder.parameters = job.parameters = self.parameters
        job.task_flow_builder.errors = job.errors = self.errors
        self.jobs.append(job)
        return job
        
    def run(self):
        for job in self.jobs:
            job.handle()
        
        return self



class TaskFlowBuilder():
    def __init__(self) -> None:
        self.tasks : List[TaskInterface] = []  
        self.currenty_task: Optional[TaskInterface] = None
        self.parameters : Optional[dict] = None
        self.task_error_handling = TaskErrorHandling.BREAK
        self.data = None
        self.errors = []
        
    def add(self, task : TaskInterface):
        task.parameters = self.parameters
        task.data = self.data
        task.errors = self.errors
        self.tasks.append(task)
        
    def run(self):
        for task in self.tasks:
            self.currenty_task = task


            before_response = task.before_step()
            if(not self.is_a_valid_Task(before_response)):
                if self.should_break_tasks_flow():
                    break 
                else:
                    continue

            execute_response = task.execute()
            if(not self.is_a_valid_Task(execute_response)):
                if self.should_break_tasks_flow():
                    break 
                else:
                    continue

            after_response = task.after_step()
            if(not self.is_a_valid_Task(after_response)):
                if self.should_break_tasks_flow():
                    break 
                else:
                    continue

    
    def is_a_valid_Task(self, task_retrun : ExitStatus):
        return  task_retrun != ExitStatus.PROCESS_FAILURE
      
        
    def should_break_tasks_flow(self):
       return self.task_error_handling == TaskErrorHandling.BREAK  or issubclass(self.currenty_task.__class__, TaskValidatorInterface)


