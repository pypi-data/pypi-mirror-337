### Referencias #######
Daniel Amorim em 30/03/2025
https://medium.com/@dev.daniel.amorim/como-criar-biblioteca-python-pypi-343219656838

###Instalações###
#python -m venv env
#env\Scripts\activate
#pip install setuptools
#pip install setuptools
#python setup.py sdist
#pip install twine
pip install twine build
python -m build
twine upload dist/*
twine upload -u __token__ -p SEU_TOKEN_AQUI dist/*

# Para upload no repositório teste do Pypi
py -m pip install --index-url https://test.pypi.org/simple/ your-package
# Para upload no repositório definitivo no Pypi
py -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ your-package

# Calculadora

**Calculadora** como próprio nome ja diz, é uma calculadora
capaz de somar, subtrair, multiplicar e dividir 2 valores em Python.

# Funções

* `calculadora.metodo(a, b)` - Recebe valor a e b e aplica aos métodos:
  - Somar
  - subtrair
  - dividir
  - multiplicar

* `help()` - Retorna um print de help da biblioteca.