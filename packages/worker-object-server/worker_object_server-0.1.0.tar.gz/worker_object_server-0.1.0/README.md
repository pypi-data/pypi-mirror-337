# worker-object-server

## Package consumption

```bash
pip install -i https://test.pypi.org/simple/ worker-object-server
```

## Package distribution

```bash
python3 -m pip install --upgrade build
python3 -m build
python3 -m pip install --upgrade twine
python3 -m twine upload --repository testpypi dist/*
```

## Example usage

```python
from worker_object_server.object_server import ObjectServer
import asyncio

async def main():
    obj = ObjectServer()
    await obj.start()
    # ws://localhost:8765 open to connections

    obj["key"] = "value"
    assert obj["key"] == "value"

    await asyncio.sleep(1000)  # await connections

    await obj.stop()

asyncio.run(main())
```

## Development

```bash
pyenv local 3.8.20
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

Tests:
```bash
pytest tests/standalone.py
```

Manual testing:
```bash
$ python -m asyncio
...
>>> from tests.interactive import obj, end
```