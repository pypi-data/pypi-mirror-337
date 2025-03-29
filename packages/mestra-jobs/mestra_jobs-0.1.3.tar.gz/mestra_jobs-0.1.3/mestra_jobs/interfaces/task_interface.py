from abc import ABC, abstractmethod

from mestra_jobs.enums.flow_enum import ExitStatus



class TaskInterface(ABC):

    def __init__(self) -> None:
        self.data = None
        self.parameters = None
        self.errors = []

    @abstractmethod
    def before_step(self):
        return ExitStatus.FINISHED

    @abstractmethod
    def execute(self):
        return ExitStatus.FINISHED

    @abstractmethod
    def after_step(self):
        return ExitStatus.SUCCESSFULLY_PROCESSED
       
        
        