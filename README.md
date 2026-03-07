# Log Dashboard

Simple Flask + Bootstrap dashboard for XML logs.

## Install (local)

```bash
pip install -e .
```

## Run

```bash
dashboard run
```

Open http://localhost:5000

## Log format

```xml
<log>
  <entry>
    <timestamp>2026-03-07T08:12:05Z</timestamp>
    <level>INFO</level>
    <source>scheduler</source>
    <message>Job queue started</message>
  </entry>
</log>
```

You can load a different file by appending `?log=other.xml` or `?log=/abs/path/log.xml`.

## Publish to PyPI (when ready)

```bash
python -m build
python -m twine upload dist/*
```
