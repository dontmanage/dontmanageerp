#!/bin/bash

set -e

cd ~ || exit

sudo apt update && sudo apt install redis-server libcups2-dev

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
    mysql --host 127.0.0.1 --port 3306 -u root -e "SET GLOBAL character_set_server = 'utf8mb4'"
    mysql --host 127.0.0.1 --port 3306 -u root -e "SET GLOBAL collation_server = 'utf8mb4_unicode_ci'"

    mysql --host 127.0.0.1 --port 3306 -u root -e "CREATE USER 'test_dontmanage'@'localhost' IDENTIFIED BY 'test_dontmanage'"
    mysql --host 127.0.0.1 --port 3306 -u root -e "CREATE DATABASE test_dontmanage"
    mysql --host 127.0.0.1 --port 3306 -u root -e "GRANT ALL PRIVILEGES ON \`test_dontmanage\`.* TO 'test_dontmanage'@'localhost'"

    mysql --host 127.0.0.1 --port 3306 -u root -e "UPDATE mysql.user SET Password=PASSWORD('travis') WHERE User='root'"
    mysql --host 127.0.0.1 --port 3306 -u root -e "FLUSH PRIVILEGES"
fi

if [ "$DB" == "postgres" ];then
    echo "travis" | psql -h 127.0.0.1 -p 5432 -c "CREATE DATABASE test_dontmanage" -U postgres;
    echo "travis" | psql -h 127.0.0.1 -p 5432 -c "CREATE USER test_dontmanage WITH PASSWORD 'test_dontmanage'" -U postgres;
fi


install_whktml() {
    wget -O /tmp/wkhtmltox.tar.xz https://github.com/dontmanage/wkhtmltopdf/raw/master/wkhtmltox-0.12.3_linux-generic-amd64.tar.xz
    tar -xf /tmp/wkhtmltox.tar.xz -C /tmp
    sudo mv /tmp/wkhtmltox/bin/wkhtmltopdf /usr/local/bin/wkhtmltopdf
    sudo chmod o+x /usr/local/bin/wkhtmltopdf
}
install_whktml &

cd ~/dontmanage-bench || exit

sed -i 's/watch:/# watch:/g' Procfile
sed -i 's/schedule:/# schedule:/g' Procfile
sed -i 's/socketio:/# socketio:/g' Procfile
sed -i 's/redis_socketio:/# redis_socketio:/g' Procfile

bench get-app payments --branch ${githubbranch%"-hotfix"}
bench get-app dontmanageerp "${GITHUB_WORKSPACE}"

if [ "$TYPE" == "server" ]; then bench setup requirements --dev; fi

bench start &> bench_run_logs.txt &
CI=Yes bench build --app dontmanage &
bench --site test_site reinstall --yes
