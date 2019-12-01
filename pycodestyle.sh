#!/bin/bash

YELLOW='\033[0;33m'
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting static code analys ${NC}"

# utils/
python3 -m pycodestyle rss_reader/ --max-line-length=120
echo -e "${YELLOW}rss_reader/ ${GREEN}PASSED${NC}"

# rss.py
python3 -m pycodestyle server/ --max-line-length=120
echo -e "${YELLOW}server/ ${GREEN}PASSED${NC}"
