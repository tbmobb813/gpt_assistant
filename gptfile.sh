#!/bin/bash

# Load API key
source ~/.openai_key

# Setup
LOG_DIR=-/gpt_logs
mkdir -p "$LOG_DIR"

# Colors
BLUE="\033[1;34m"
GREEN="\033[1;32m"
YELLOW="\033[1;33m"
RED="\033[1;31m"
RESET="\033[0m"

# Choose GPT model
echo -e "${BLUE}\nChoose GPT model to use:${RESET}"
echo -e "${YELLOW}1) GPT-3.5 (faster, cheaper)"
echo -e "2) GPT-4 (slower, smarter)${RESET}"
read -p "Option: " model_option
model_option=$(echo "$model_option" | tr -d '[:space:]')  # Strip spaces/newlines
echo "DEBUG: You entered '$model_option'"

if [ "$model_option" = "2" ]; then
    model_choice="gpt-4"
elif [ "$model_option" = "1" ]; then
    model_choice="gpt-3.5-turbo"
else
    echo -e "${RED}❌ Invalid model option.${RESET}"
    exit 1
fi


# Prompt selection
echo -e "${BLUE}\nChoose what you want GPT to do:${RESET}"
echo -e "${YELLOW}1) Summarize"
echo "2) Explain"
echo -e "3) Rewrite for clarity${RESET}"
read -p "Option: " mode

# File mode
echo -e "${BLUE}\nSingle file or batch folder mode?${RESET}"
echo -e "${YELLOW}1) Single file"
echo -e "2) Batch process folder${RESET}"
read -p "Option: " batch_mode

# File Input
if [ "$batch_mode" = "1" ]; then
  read -p "$(echo -e ${YELLOW}Path to file:${RESET}) " filepath
  if [ ! -f "$filepath" ]; then
    echo -e "${RED}❌ File not found!${RESET}"
    exit 1
  fi
  file_list=("$filepath")
else
  read -p "$(echo -e ${YELLOW}Path to folder:${RESET}) " folderpath
  if [ ! -d "$folderpath" ]; then
    echo -e "${RED}❌ Folder not found!${RESET}"
    exit 1
  fi
  file_list=()
  for f in "$folderpath"/*.{txt,md,py}; do
    [ -e "$f" ] && file_list+=("$f")
  done
  if [ ${#file_list[@]} -eq 0 ]; then
    echo -e "${RED}❌ No .txt, .md, or .py files found in folder.${RESET}"
    exit 1
  fi
fi

# Load file content
for filepath in "${file_list[@]}"; do
  echo -e "\n${BLUE}📄 Processing: $filepath${RESET}"
  filecontent=$(cat "$filepath")


  # Choose initial system prompt
  case $mode in
    1) user_prompt="Summarize this file:\n\n$filecontent" ;;
    2) user_prompt="Explain the following code or text to a beginner:\n\n$filecontent" ;;
    3) user_prompt="Rewrite this to be more clear and professional:\n\n$filecontent" ;;
    *) echo -e "${RED}❌ Invalid option.${RESET}"; exit 1 ;;
  esac

  # Initialize conversation history
  history='[
    {"role": "user", "content": "'"${user_prompt//$'\n'/\\n}"'"}
  ]'

  while true; do
    echo -e "\n${BLUE}⏳ Asking GPT...${RESET}"
  
  # Send request
  response=$(curl https://api.openai.com/v1/chat/completions \
    -s \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -d '{
      "model": "$model_choice",
      "messages": $history,
      "temperature": 0.7
    }')

  reply=$(echo "$response" | jq -r '.choices[0].message.content')
  echo -e "\n${GREEN}🧠 GPT Says:${RESET}\n$reply"

  # Save response to log
  timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
  filename=$(basename "$filepath")
  logfile="$LOG_DIR/${filename}_$timestamp.txt"

  {
    echo "🗂️ File: $filename"
    echo "🔧 Task: $mode"
    echo "🕒 Time: $timestamp"
    echo ""
    echo "$reply"
  } > "$logfile"
  echo -e "${YELLOW}📝 Saved to: $logfile${RESET}"

  # Ask for follow-up
  read -p "$(echo -e ${YELLOW}\nAsk a follow-up or press ENTER to quit:${RESET} )" followup

  if [ -z "$followup" ]; then
    echo -e "${BLUE}👋 Exiting chat.${RESET}"
    break
  fi

  # Add follow-up to history
  history=$(echo "$history" | jq \
    --arg user "$followup" \
    --arg reply "$reply" \
    '. + [{"role":"assistant", "content":$reply}, {"role":"user", "content":$user}]')
done
done
