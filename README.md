# REST API wit python and FastAPI web Framework

## Setup Locally (Windows)

### 1) Install Python >= 3.6 version

### 2) Create virtual Environment
```shell
py -m pip install --user virtualenv
```
```shell
py -m venv env
```
```shell
.\env\Scripts\activate
```
##### Leaving the virtual environment
```shell
deactivate
```
### 3) Generate Dependencies file

```shell
pip freeze > requirements.txt
```
### 4) Install Dependencies

```shell
pipenv install -r requirements.txt
```

### 5) Run the code

```shell
python main.py
```