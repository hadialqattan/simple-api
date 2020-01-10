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

    # set export command
    CMDs=()
    # set tests commands
    if [[ ${BASH_ARGV[$1]} == "b" ]]; then 
        echo ""
        echo -e "${GREEN}Starting${NC} both unit & integraion tests..."
        echo ""
        declare -a CMDs=("echo 'Unit tests:';", "cd unit;", "pytest -vv;", "cd ..;", "echo '';", "echo 'Integration tests:';", "cd integration;", "nosetests --verbosity=2 test_integration.py;")
    elif [[ ${BASH_ARGV[$1]} == "u" ]]; then
        echo ""
        echo -e "${GREEN}Starting${NC} unit tests..."
        echo ""
        declare -a CMDs=("cd unit;", "pytest -vv;")
    elif [[ ${BASH_ARGV[$1]} == "i" ]]; then 
        echo ""
        echo -e "${GREEN}Starting${NC} integration tests..."
        echo ""
        declare -a CMDs=("cd integration;", "nosetests --verbosity=2 test_integration.py;")
    fi
    # extract array elements without commas
    nCMDs="${CMDs[@]%,}"
    # run the test inside docker
    docker run \
            --name testslab \
            --link labdb \
            --network simple-project-1_default \
            --env-file ./.env-tests \
            --rm -v ${PWD}:/lab -w /lab simpleapi \
            /bin/bash -c "${nCMDs[@]}"
    echo ""
    echo -e "${GREEN}Goodbye!${NC}"
    echo ""
}


if [[ $1 == "b" ]] || [[ $1 == "u" ]] || [[ $1 == "i" ]]; then 
    labdb_init
    tests_runner
    labdb_stop
else 
    echo ""
    echo -e "  ---------------------"
    echo -e "  | ${RED}Id${NC} |     ${GREEN}Type${NC}     |"
    echo -e "  |-------------------|"
    echo -e "  | ${RED}b${NC}  |     ${GREEN}Both${NC}     |"
    echo -e "  | ${RED}u${NC}  |     ${GREEN}Unit${NC}     |"
    echo -e "  | ${RED}i${NC}  |  ${GREEN}Integration${NC} |"
    echo -e "  ---------------------"
    echo ""
fi 
