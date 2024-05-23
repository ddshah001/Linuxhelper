# Linuxhelper

Linuxhelper is a Python script that can generate Linux shell scripts using OpenAI API.

## Setup

Install requirements

```bash
pip install -r requirements.txt
```

Create `config.ini` file with below content
```
[OpenAI]
key = <OpenAI API Key>
```

## Usage

```python
python3 linuxhelper.py
Please enter the task you want to automate with a shell script: 
```

Arguments
```python
optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show AI generated output and exported version of script
  -r, --run      Run shell script but use this option with caution
```
