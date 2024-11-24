#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'
BOLD='\033[1m'

# Fancy banner
echo -e "${PURPLE}╔════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║${NC}     ${BOLD}Environment Setup Wizard${NC}           ${PURPLE}║${NC}"
echo -e "${PURPLE}╚════════════════════════════════════════╝${NC}"
echo

# Check if .env file exists, create if not
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    touch .env
fi

# Function to check and prompt for empty values
check_env_value() {
    local key=$1
    local prompt=$2
    local value=$(grep "^${key}=" .env | cut -d'=' -f2)
    
    if [ -z "$value" ]; then
        echo -e "\n${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${BOLD}${BLUE}$prompt${NC}"
        echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        read -p "$(echo -e ${GREEN}Enter value for $key: ${NC})" new_value
        if [ -n "$new_value" ]; then
            if grep -q "^${key}=" .env; then
                sed -i "s|^${key}=.*|${key}=${new_value}|" .env
            else
                echo "${key}=${new_value}" >> .env
            fi
            echo -e "${GREEN}✓ Successfully set $key${NC}"
        fi
    fi
}

# Install requirements
echo -e "\n${YELLOW}Installing requirements...${NC}"
pip3 install -r requirements.txt

echo -e "\n${BLUE}${BOLD}Checking environment variables...${NC}"

# MongoDB setup
echo -e "\n${PURPLE}📦 MongoDB Configuration${NC}"
check_env_value "MONGO_CONNECTION_URL" "Please enter your MongoDB connection URL"
check_env_value "DB_NAME" "Please enter a name for the DB. (Can be anything)"

# Telegram setup
echo -e "\n${PURPLE}💬 Telegram Configuration${NC}"
check_env_value "TELEGRAM_API_KEY" "Follow these steps to get your Telegram API key:
${YELLOW}1.${NC} Open Telegram and search for '${BOLD}BotFather${NC}'
${YELLOW}2.${NC} Send ${BOLD}/newbot${NC} command
${YELLOW}3.${NC} Choose a name for your bot
${YELLOW}4.${NC} Select a username ending with 'bot'
${YELLOW}5.${NC} Copy the provided HTTP API token"

# Gmail setup
echo -e "\n${PURPLE}📧 Gmail Configuration${NC}"
check_env_value "GMAIL_ACCOUNT" "Enter your Gmail account"
check_env_value "GMAIL_PASS" "Enter your Gmail password or app-specific password"

# Discord setup
echo -e "\n${PURPLE}🎮 Discord Configuration${NC}"
check_env_value "BOT_TOKEN" "Enter your Discord bot token"
check_env_value "GUILD_ID" "Enter your Discord guild ID"

# Completion message
echo -e "\n${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║${NC}     ${BOLD}Environment Setup Complete! ✨${NC}        ${GREEN}║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"