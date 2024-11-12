## Hello my targets! - HiTarget

HiTarget API is writen in Python (Pypy) and FastAPI. It works as backend for HiTarget ToDo list.

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
