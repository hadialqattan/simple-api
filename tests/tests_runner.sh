# tests_setup is shell script tool aim to setup tests lab


# color palette
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color


# create .evn-tests file
create_env_tests() {
    cat >.env-tests <<EOL
POSTGRES_USER=lab
POSTGRES_PASSWORD=lab000111
POSTGRES_DB=labdb
DB_HOST=172.18.0.1
APP_HOST=localhost
APP_PORT=5057
EOL
}


# create labdb container from postgres:12.0-alpine image
labdb_init() {
    # creating labdb
    echo -e "\n${GREEN}Creating${NC} labdb...\n"
    docker run --rm -d \
        --name labdb \
        -p 5432 \
        -h 0.0.0.0 \
        --env-file ./.env-tests \
        postgres:12.0-alpine
    
    # append DB_PORT to .env-tests
    port=$(docker port labdb)
    port=${port:20:25}
    echo -e "DB_PORT=$port" >> .env-tests
    
    # waiting for labdb port
    echo -e "\n${GREEN}Waiting${NC} labdb...\n"
    sleep 3
    i=0
    while ! nc -z localhost $port; do
        i+=1
        echo $i
        sleep 1
    done
}


run_tests() {
    # set export command
    CMDs=()
    # set tests commands
    if [[ ${BASH_ARGV[$1]} == "u" ]]; then
        echo -e "\n${GREEN}Starting${NC} unit tests...\n"
        declare -a CMDs=("pytest -vv unit/users.py unit/configs.py;")
    elif [[ ${BASH_ARGV[$1]} == "i" ]]; then 
        echo -e "\n${GREEN}Starting${NC} integration tests...\n"
        declare -a CMDs=("pytest -vv integration/users.py integration/configs.py;")
    fi
    # extract array elements without commas
    nCMDs="${CMDs[@]%,}"
    # run the tests inside docker
    docker run \
        --name testslab \
        --link labdb \
        --env-file ./.env-tests \
        --rm -v ${PWD}:/lab -w /lab simpleapi \
        /bin/bash -c "${nCMDs[@]}"
    # print goodbye statement
    echo -e "\n${GREEN}Goodbye!${NC}\n"
}


# stop labdb container
labdb_stop() {
    # stopping labdb
    echo -e "\n${RED}Stopping${NC} labdb...\n"
    docker stop labdb
}


if [[ $1 == "u" ]] || [[ $1 == "i" ]]; then 
    (
        set -Ee
        function _finally {
            labdb_stop
            # delete .env-tests
            rm -fr .env-tests
        }
        
        # finally
        trap _finally EXIT
        
        # try
        create_env_tests
        labdb_init
        run_tests
    )
else 
    echo ""
    echo -e "  ---------------------"
    echo -e "  | ${RED}Id${NC} |     ${GREEN}Type${NC}     |"
    echo -e "  |-------------------|"
    echo -e "  | ${RED}u${NC}  |     ${GREEN}Unit${NC}     |"
    echo -e "  | ${RED}i${NC}  |  ${GREEN}Integration${NC} |"
    echo -e "  ---------------------"
    echo ""
fi