# tests_setup is shell script tool aim to setup tests lab


# color palette
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color


# create labdb container from postgres:12.0-alpine image
labdb_init() {
    # creating labdb
    echo ""
    echo -e "${GREEN}Creating${NC} labdb..."
    docker run --rm -d \
        --name labdb \
        -p 6551:5432 \
        -h 0.0.0.0 \
        --env-file ./.env-tests \
        postgres:12.0-alpine
    echo ""
}


# stop labdb container
labdb_stop() {
    # stopping labdb
    echo ""
    echo -e "${RED}Stopping${NC} labdb..."
    docker stop labdb
    echo ""
}


# start tests_runner.sh
tests_runner() {
    # starting tests_runner.sh
    echo ""
    echo -e "${GREEN}Starting${NC} tests_runner.sh ..."
    if [[ ${BASH_ARGV[$1]} == "1" ]]; then
        ./tests_runner.sh 1
    elif [[ ${BASH_ARGV[$1]} == "2" ]]; then 
        ./tests_runner.sh 2
    else
        ./tests_runner.sh 9999
    fi
    echo ""
}


labdb_init
sleep 5
tests_runner
sleep 2
labdb_stop
