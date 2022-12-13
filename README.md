## Bysykkel API

Explore this API on https://bysykkel.apps.larsenserver.com/docs


## Set up local development

with docker-compose:
```
docker-compose build
docker-compose up
```

with Python:
```
inititalize venv
pip install -r reqiurements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8080 --reload
```
