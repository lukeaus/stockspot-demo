#!/bin/bash
source bin/env.sh


# fix so using dctest
dcdev build

if ! [[ $* == *--skipbuild* ]]; then
    ./bin/build_frontend.sh
else
    echo "skipping frontend build..."
fi


# fix so using dctest
dcdev run --rm  django ./bin/test.sh "$@"
