from setuptools import setup, find_packages

setup(
   name='hnr_investimento',
   version='0.1',
   packages=find_packages(),
   install_requires=[],
   author='Henrique F Tambalo',
   author_email='henrique.comp@gmail.com',
   description='Uma biblioteca para cálculos de investimentos.',
   url='https://github.com/henriquecomp/investpy',
   classifiers=[
       'Programming Language :: Python :: 3',
       'License :: OSI Approved :: MIT License',
       'Operating System :: OS Independent',
   ],
   python_requires='>=3.6',
)