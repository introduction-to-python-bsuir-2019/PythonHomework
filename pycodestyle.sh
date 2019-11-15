#!/bin/bash

YELLOW='\033[0;33m'
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting static code analys ${NC}"

# utils/
python3 -m pycodestyle utils/ --max-line-length=120
echo -e "${YELLOW}utils/ ${GREEN}PASSED${NC}"

# rss.py
python3 -m pycodestyle rss.py --max-line-length=120
echo -e "${YELLOW}rss.py/ ${GREEN}PASSED${NC}"

# bots/
python3 -m pycodestyle bots/ --max-line-length=120
echo -e "${YELLOW}bots/ ${GREEN}PASSED${NC}"