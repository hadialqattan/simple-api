RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo ""
echo -e "Tests ${GREEN}runner${NC}:"
echo ""
echo -ne "Do you ${GREEN}allow${NC} tests runner to ${RED}clean${NC} the DB? (${GREEN}y${NC}/${RED}n${NC}) "
read allow #GOTO line 74


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
            pytest test -vv
            if repeat; then 
                continue
            else 
                break
            fi
        elif [[ $ans == "2" ]]; then 
            echo "Run integration tests..."
            echo ""
            nosetests --verbosity=2 tests/test_integration.py
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
    echo -e "${GREEN}Cleaning${NC} the database..."
    python test/db_cleaner.py
    echo ""
    echo -ne "${GREEN}Run${NC} another test? (${GREEN}y${NC}/${RED}n${NC}) "
    read reans
    echo ""
    if [[ $reans == "y" ]] || [[ $reans == "Y" ]]; then 
        return 0
    else
        echo -e "${GREEN}Goodbye!${NC}"
        echo ""
        return 1
    fi
}


if [[ $allow == "Y" ]] || [[ $allow == "y" ]]; then
    echo "" 
    echo -e "${GREEN}Cleaning${NC} the database..."
    echo ""
    run_test
else 
    echo ""
    echo -e "If you want to run tests without losing data, you can take a backup or change the DB."
    echo ""
fi 
