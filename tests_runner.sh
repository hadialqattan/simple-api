RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

export $(cat .env-tests)

if [[ $1 == "1" ]]; then
    cd unit
    pytest -vv
elif [[ $1 == "2" ]]; then 
    cd integration
    nosetests --verbosity=2 test_integration.py
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
