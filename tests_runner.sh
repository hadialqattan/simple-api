RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo ""
echo -e "Tests ${GREEN}runner${NC}:"
if [ -f .env ]; then
    export $(cat .env | sed 's/#.*//g' | xargs)
fi
# export DB_URL=postgresql://api_owner:api112233@localhost/apidb
echo ""

docker run --rm -d \
        --name the_db \
        -p 5432:5432 \
        --env-file ./.env \
         postgres:12.0-alpine 

run_test() {

    while true; do

        echo ""
        echo -e "  ---------------------"
        echo -e "  | ${RED}Id${NC} |     ${GREEN}Type${NC}     |"
        echo -e "  |-------------------|"
        echo -e "  | ${RED}1${NC}  |     ${GREEN}Unit${NC}     |"
        echo -e "  | ${RED}2${NC}  |  ${GREEN}Integration${NC} |"
        echo -e "  ---------------------"
        echo ""

        echo -ne "Enter test ${RED}id${NC}: "
        read ans
        echo ""

        if [[ $ans == "1" ]]; then
            echo "Run unit tests..."
            echo ""
            cd unit
            pytest -vv
            cd ..
            if repeat; then
                continue
            else
                break
            fi
        elif [[ $ans == "2" ]]; then
            echo "Run integration tests..."
            echo ""
            # cd integration
            docker run --rm --env-file ./.env simpleapi && nosetests --verbosity=2 integration/test_integration.py
            # cd ..
            if repeat; then
                continue
            else
                break
            fi
        else
            echo -e "${RED}Invalid${NC} test ${RED}id${NC}!"
            echo ""
        fi

    done
}

repeat() {
    echo ""
    echo -ne "${GREEN}Run${NC} another test? (${GREEN}y${NC}/${RED}n${NC}) "
    read reans
    echo ""
    if [[ $reans == "y" ]] || [[ $reans == "Y" ]]; then
        echo -e "${GREEN}Cleaning${NC} the DB..."
        python integration/db_cleaner.py
        echo ""
        return 0
    else
        echo -e "${GREEN}Goodbye!${NC}"
        echo ""
        return 1
    fi
}

run_test
