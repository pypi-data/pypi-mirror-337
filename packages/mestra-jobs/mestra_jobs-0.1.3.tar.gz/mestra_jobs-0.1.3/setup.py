from setuptools import setup, find_packages

setup(
    name="mestra-jobs",
    version="0.1.3",
    packages=find_packages(),
    author='Mestra',
    keywords='mestra_job',
    author_email='mestraac@gmail.com',
    description='Lib responsavel por gerenciar task e jobs para executar determinadas tarefas',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/mestra1/jobs_lib',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
