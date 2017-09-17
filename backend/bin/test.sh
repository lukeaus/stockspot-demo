#!/bin/bash
./bin/install.sh
python3 manage.py test --noinput -p 8082 "$@"
