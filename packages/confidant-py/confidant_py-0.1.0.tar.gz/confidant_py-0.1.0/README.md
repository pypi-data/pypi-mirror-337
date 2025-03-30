# Confidant-Py

Multi platform scalable environment variables manager

## Installation

```sh
pip install confidant-py
```

## Usage

```python
from confidant_py.loader import ConfidantLoader

loader = ConfidantLoader()
envs = loader.get_envs()
print(envs)
```


## **4. Publish to PyPI**
1. Install necessary tools:
```sh
pip install setuptools wheel twine
```

2. Build the package

```sh
python setup.py sdist bdist_wheel
```

3. Upload to PyPI:

```sh
twine upload dist/*
```