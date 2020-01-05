GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo ""
echo -e "${GREEN}Cloning${NC} the repo..."
echo ""
git clone https://github.com/mojtaba42/simple-project-1.git

echo "cd simple-project-1"
cd simple-project-1

echo -e "${GREEN}Run${NC} tests runner..."
echo ""
echo ""
./tests_runner.sh
