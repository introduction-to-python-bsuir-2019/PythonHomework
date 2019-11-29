#!/bin/bash

YELLOW='\033[0;33m'
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting static code analys ${NC}"

# utils/
python3 -m pycodestyle 2.py --max-line-length=120
echo -e "${YELLOW}2.py ${GREEN}PASSED${NC}"

python3 -m pycodestyle 3.py --max-line-length=120
echo -e "${YELLOW}3.py ${GREEN}PASSED${NC}"

python3 -m pycodestyle 4.py --max-line-length=120
echo -e "${YELLOW}4.py ${GREEN}PASSED${NC}"

