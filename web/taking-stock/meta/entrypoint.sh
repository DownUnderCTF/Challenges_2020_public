#!/bin/bash

gunicorn -k gevent -b 0.0.0.0:8000 app:app