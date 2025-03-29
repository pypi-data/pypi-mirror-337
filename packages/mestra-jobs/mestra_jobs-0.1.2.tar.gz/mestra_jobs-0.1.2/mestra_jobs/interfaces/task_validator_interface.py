
from jobs.interfaces.task_interface import TaskInterface


class TaskValidatorInterface(TaskInterface):
 
    def __init__(self) -> None:
        super().__init__()

    def before_step(self):
        super().before_step()

    def execute(self):
        super().execute()

    def after_step(self):
        super().after_step()