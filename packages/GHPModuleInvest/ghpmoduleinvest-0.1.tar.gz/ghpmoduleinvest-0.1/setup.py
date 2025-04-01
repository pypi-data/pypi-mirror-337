from setuptools import setup, find_packages

setup(
   name='GHPModuleInvest',
   version='0.1',
   packages=find_packages(),
   install_requires=[],
   author='Gabriel Henrique Pascon',
   author_email='gh.pascon@gmail.com',
   description='Uma biblioteca para cálculos de investimentos.',
   url='https://github.com/ghpascon/meu_investimento_ghp',
   classifiers=[
       'Programming Language :: Python :: 3',
       'License :: OSI Approved :: MIT License',
       'Operating System :: OS Independent',
   ],
   python_requires='>=3.6',
)