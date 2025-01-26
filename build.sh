#!/usr/bin/env bash

if [ -f .env ]; then
    source .env
else
    echo "Файл .env не найден!"
    exit 1
fi

curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
make install && psql -a -d $DATABASE_URL -f database.sql