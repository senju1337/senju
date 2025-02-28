#!/bin/sh

curl http://ollama:11434/api/pull -d '{"model": "llama3.2:1b"}'

cd /app
poetry run sh -c 'flask --app senju/main run --host=0.0.0.0'
