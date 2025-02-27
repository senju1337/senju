#!/bin/sh

curl http://ollama:11434/api/pull -d '{"model": "llama3.2:1b"}'

flask --app senju/main run --debug --host=0.0.0.0

