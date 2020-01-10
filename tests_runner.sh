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


# start tests
tests_runner() {
    # waiting labdb init
    echo ""
    echo -e "${GREEN}Waiting${NC} labdb..."
    echo ""
    for i in {1..3}; do
        echo -e "${GREEN}${i}${NC}"
        sleep 1
    done

    # starting tests
    echo ""
    echo -e "${GREEN}Starting${NC} tests..."
    # set export command
    CD=""
    CMD=""
    # set tests commands
    if [[ ${BASH_ARGV[$1]} == "1" ]]; then 
        CD="cd unit;"
        CMD="pytest -vv;"
    elif [[ ${BASH_ARGV[$1]} == "2" ]]; then 
        CD="cd integration;"
        CMD="nosetests --verbosity=2 test_integration.py;"
    fi
    
    # run the test inside docker
    docker run -it \
            --name testslab \
            --link labdb \
            --network simple-project-1_default \
            --env-file ./.env-tests \
            --rm -v ${PWD}:/lab -w /lab simpleapi \
            /bin/bash -c "$CD $CMD"
    echo ""
}

if [[ $1 == "1" ]] || [[ $1 == "2" ]]; then 
    labdb_init
    tests_runner
    labdb_stop
else 
    echo ""
    echo -e "  ---------------------"
    echo -e "  | ${RED}Id${NC} |     ${GREEN}Type${NC}     |"
    echo -e "  |-------------------|"
    echo -e "  | ${RED}1${NC}  |     ${GREEN}Unit${NC}     |"
    echo -e "  | ${RED}2${NC}  |  ${GREEN}Integration${NC} |"
    echo -e "  ---------------------"
    echo ""
fi 
