#!/bin/sh
exec uvicorn extension:app --host 0.0.0.0 --port ${PORT:-8080} --workers 1
