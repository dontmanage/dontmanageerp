#!/bin/bash

set -e

cd ~ || exit

sudo apt update
sudo apt remove mysql-server mysql-client
sudo apt install libcups2-dev redis-server mariadb-client-10.6

pip install dontmanage-bench

githubbranch=${GITHUB_BASE_REF:-${GITHUB_REF##*/}}
dontmanageuser=${DONTMANAGE_USER:-"dontmanage"}
dontmanagebranch=${DONTMANAGE_BRANCH:-$githubbranch}

git clone "https://github.com/${dontmanageuser}/dontmanage" --branch "${dontmanagebranch}" --depth 1
bench init --skip-assets --dontmanage-path ~/dontmanage --python "$(which python)" dontmanage-bench

mkdir ~/dontmanage-bench/sites/test_site

if [ "$DB" == "mariadb" ];then
    cp -r "${GITHUB_WORKSPACE}/.github/helper/site_config_mariadb.json" ~/dontmanage-bench/sites/test_site/site_config.json
else
    cp -r "${GITHUB_WORKSPACE}/.github/helper/site_config_postgres.json" ~/dontmanage-bench/sites/test_site/site_config.json
fi


if [ "$DB" == "mariadb" ];then
    mariadb --host 127.0.0.1 --port 3306 -u root -proot -e "SET GLOBAL character_set_server = 'utf8mb4'"
    mariadb --host 127.0.0.1 --port 3306 -u root -proot -e "SET GLOBAL collation_server = 'utf8mb4_unicode_ci'"

    mariadb --host 127.0.0.1 --port 3306 -u root -proot -e "CREATE USER 'test_dontmanage'@'localhost' IDENTIFIED BY 'test_dontmanage'"
    mariadb --host 127.0.0.1 --port 3306 -u root -proot -e "CREATE DATABASE test_dontmanage"
    mariadb --host 127.0.0.1 --port 3306 -u root -proot -e "GRANT ALL PRIVILEGES ON \`test_dontmanage\`.* TO 'test_dontmanage'@'localhost'"

    mariadb --host 127.0.0.1 --port 3306 -u root -proot -e "FLUSH PRIVILEGES"
fi

if [ "$DB" == "postgres" ];then
    echo "travis" | psql -h 127.0.0.1 -p 5432 -c "CREATE DATABASE test_dontmanage" -U postgres;
    echo "travis" | psql -h 127.0.0.1 -p 5432 -c "CREATE USER test_dontmanage WITH PASSWORD 'test_dontmanage'" -U postgres;
fi


install_whktml() {
    if [ "$(lsb_release -rs)" = "22.04" ]; then
        wget -O /tmp/wkhtmltox.deb https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb
        sudo apt install /tmp/wkhtmltox.deb
    else
        echo "Please update this script to support wkhtmltopdf for $(lsb_release -ds)"
        exit 1
    fi
}
install_whktml &
wkpid=$!


cd ~/dontmanage-bench || exit

sed -i 's/watch:/# watch:/g' Procfile
sed -i 's/schedule:/# schedule:/g' Procfile
sed -i 's/socketio:/# socketio:/g' Procfile
sed -i 's/redis_socketio:/# redis_socketio:/g' Procfile

bench get-app payments --branch ${githubbranch%"-hotfix"}
bench get-app dontmanageerp "${GITHUB_WORKSPACE}"

if [ "$TYPE" == "server" ]; then bench setup requirements --dev; fi

wait $wkpid

bench start &>> ~/dontmanage-bench/bench_start.log &
CI=Yes bench build --app dontmanage &
bench --site test_site reinstall --yes
