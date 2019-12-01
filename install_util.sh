#!/bin/bash
GREEN='\033[0;32m'
YELLOW='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Installing requirements: ${NC}"
pyhton3 -m pip install -r requirements.txt
echo -e "${GREEN}Installing rss_reader: ${NC}"
python3 -m pip install .

echo -e "${GREEN}Launching rss_reader:  ${YELLOW}python3 -m rss_reader -h${NC}"
echo -e "${RED}"
python3 -m rss_reader -h
echo -e "${NC}"


#echo -e "${GREEN}Launching docker-compose build: ${NC}"
#docker-compose up --build
#
#echo -e "${GREEN}Docker-compose builing is finished. Server should be started. ${NC}"
#
echo -e "${GREEN}Launching server: ${NC}"
python3 -m server
echo -e "${GREEN}Server should be started. ${NC}"