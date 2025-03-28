addit aigc core
==============================

## Installation

```bash
pip install aiddit_agic_core
```

## pypi打包
```bash
pip freeze -> requirements.txt  
```

```bash
rm -rf dist/* build/ *.egg-info
```

```bash
python setup.py sdist bdist_wheel 
```

```bash
twine upload dist/*
```

````
pypi-AgEIcHlwaS5vcmcCJDY5NTI5OTFjLTBhOGQtNDViZS1hYjhhLTY2ZjcyNjlmYjc3OQACKlszLCJlM2UwZDYwZi1iMWI2LTQ4NzUtYmEzYS0yNjZmM2Q2NWMzNTYiXQAABiDNqD2GEDGWB1w50Sf-zD7c_3oBkFAl2m4vQ9rM9Cen2w
````