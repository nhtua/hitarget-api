## Hello my targets! - HiTarget

HiTarget API is writen in Python (Pypy) and FastAPI. It works as backend for HiTarget ToDo list. `hitarget` was designed with 3 main components: 

- [hitarget-api](https://github.com/nhtua/hitarget-api): the backend api is written in Python 3.6 using FastAPI, which processes all logic of this TODO list app
- [hitarget-ui](https://github.com/nhtua/hitarget-ui): the frontent UI is written in Javascript using VueJs 3.x
- [hitarget-it](https://github.com/nhtua/hitarget-it): the configuration and deployment management scripts using Ansible Playbook


### Prequisite

- MongoDB `mongodb-org-4.4`
- Python `pypy3.6-7.3.1` (other Python version >= 3.6 may be compatible)

### Configuration
All configuration can be found at [hitarget/core/config.py](https://github.com/nhtua/hitarget-api/blob/master/hitarget/core/config.py).
You can easily custom these values by set environment variables

### Run the API server

```
python -m ensurepip
python -m pip install -U pip wheel
pip install poetry
poetry install

/start.sh --workers 10
```
