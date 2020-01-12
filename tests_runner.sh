# tests_setup is shell script tool aim to setup tests lab


# color palette
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color


# create labdb container from postgres:12.0-alpine image
labdb_init() {
    # creating .evn-tests file
    cat >.env-tests <<EOL
POSTGRES_USER=lab
POSTGRES_PASSWORD=lab000111
POSTGRES_DB=labdb
DB_HOST=172.18.0.1
APP_HOST=172.18.0.1
APP_PORT=5057
EOL

    # creating labdb
    echo -e "\n${GREEN}Creating${NC} labdb...\n"
    docker run --rm -d \
        --name labdb \
        -p 5432 \
        -h 0.0.0.0 \
        --env-file ./.env-tests \
        postgres:12.0-alpine
}


# stop labdb container
labdb_stop() {
    # stopping labdb
    echo -e "\n${RED}Stopping${NC} labdb...\n"
    docker stop labdb

    # delete .env-tests
    rm -fr .env-tests
}


# start tests
tests_runner() {
    # append DB_PORT to .env-tests
    port=$(docker port labdb)
    echo -e "DB_PORT=${port:20:25}" >> .env-tests

    # waiting labdb init
    echo -e "\n${GREEN}Waiting${NC} labdb...\n"
    for i in {1..3}; do
        echo -e "${GREEN}${i}${NC}"
        sleep 1
    done

    # set export command
    CMDs=()
    # set tests commands
    if [[ ${BASH_ARGV[$1]} == "b" ]]; then 
        echo -e "\n${GREEN}Starting${NC} both unit & integraion tests...\n"
        declare -a CMDs=("echo 'Unit tests:';", "cd unit;", "pytest -vv;", "cd ..;", "echo '';", "echo 'Integration tests:';", "cd integration;", "nosetests --verbosity=2 test_integration.py;")
    elif [[ ${BASH_ARGV[$1]} == "u" ]]; then
        echo -e "\n${GREEN}Starting${NC} unit tests...\n"
        declare -a CMDs=("cd unit;", "pytest -vv;")
    elif [[ ${BASH_ARGV[$1]} == "i" ]]; then 
        echo -e "\n${GREEN}Starting${NC} integration tests...\n"
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
    echo -e "\n${GREEN}Goodbye!${NC}\n"
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