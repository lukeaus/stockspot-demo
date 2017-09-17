#!/bin/bash

# Setup everything from scratch
printf '\nHold tight while we get everything setup...\n'
source bin/env.sh

dcdev build
printf '\nCreating the database...\n'
./bin/init_db.sh

printf '\nFiring up the engines...\n'
dcdev up -d

printf '\nMigrating database...\n'
dcdev run --rm  django ./bin/django.sh migrate

printf '\nImporting Stockspot sample data...\n'
dcdev run --rm  django ./bin/django.sh import_sample_data

printf '\nCreate a superuser account:\n'
dcdev run --rm  django ./bin/django.sh createsuperuser

printf '\nRestarting so you can see the logs...\n'
dcdev stop && dcdev rm -f
dcdev up
