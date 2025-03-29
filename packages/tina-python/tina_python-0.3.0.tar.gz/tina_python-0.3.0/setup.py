from setuptools import setup, find_packages

setup(
name='tina-python',
version='0.3.0',
packages=find_packages(),
install_requires=[
    'httpx',
    'diskcache',
    'faiss-cpu',
    'Jinja2',
    'lxml',
    'MarkupSafe',
    'numpy',
    'packaging',
    'PyPDF2',
    'python-docx',
   'setuptools',
    'typing_extensions',
    'wheel'
],

description='tina is in your computer!',
long_description=open('README.md',encoding="utf-8").read(),
long_description_content_type="text/markdown",
url='https://gitee.com/wang-churi/tina',
author='王出日',
author_email='wangchuri@163.com',
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: Apache Software License',
'Operating System :: OS Independent',
],
python_requires='>=3.10',
)
