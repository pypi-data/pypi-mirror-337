Referencias:
Daniel Amorin
https://medium.com/@dev.daniel.amorim/como-criar-biblioteca-python-pypi-343219656838

python -m venv env
env\Scripts\activate
pip install setuptools
python setup.py sdist
pip install twine
pip install twine build
pip install setuptools wheel twine
python -m build
python setup.py sdist bdist_wheel
twine upload dist/*


#Função de retorno 
Funcação de retorno de valores passados para o parametro
minhafuncao(XXX) #insira os valores a serem retornados no print