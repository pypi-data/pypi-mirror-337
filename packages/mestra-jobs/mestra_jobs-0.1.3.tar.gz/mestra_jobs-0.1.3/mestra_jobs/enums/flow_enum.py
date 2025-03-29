from enum import Enum

class ExitStatus(Enum):
    SUCCESSFULLY_PROCESSED = 1 # USADO QUANDO UMA TASK/JOB É PROCESSADA SEM ERROS
    FINISHED = 2 # USADO QUANDO UMA DAS ETAPAS DE UMA TASK/JOB SÃO FINALIZADAS COM SUCESSO
    PROCESS_FAILURE = 3# USADO QUANDO OCORRE UM ERRO NO PROCESSAMENTO DE UMA TASK/JOB
    REPROCESS = 4 # USADO PARA REPROCESSAR UMA TASK/JOB INDEPENDENTE DE ERRO OU SUCESSO

class TaskErrorHandling(Enum):
    CONTINUE = 1 #Usado pra configurar as tasks de um job, em caso de erro vai parar a task atual e ir pra proxima
    BREAK = 2 #Usado pra configurar as tasks de um job, em caso de erro vai parar todas as tasks do job atual e ir pro proximo job se houver.
