from setuptools import setup, find_packages

setup(
   name='meu_investimento_alura_djflucena',
   version='0.1.1',
   packages=find_packages(),
   install_requires=[],
   author='David J F de Lucena',
   author_email='djflucena@sefaz.al.gov.br',
   description='Uma biblioteca para cálculos de investimentos.',
   url='https://github.com/djflucena/meu_investimento',
   classifiers=[
       'Programming Language :: Python :: 3',
       'License :: OSI Approved :: MIT License',
       'Operating System :: OS Independent',
   ],
   python_requires='>=3.6',
)