# Telegram Translation Bot

## Overview

A Telegram bot that translates messages between languages using Google Translate. Users can send any message and receive a translation in their chosen target language.

## Stack

- **Language**: Python 3.11
- **Bot framework**: python-telegram-bot v22.7
- **Translation**: deep-translator v1.11.4 (Google Translate)
- **Package manager**: uv (pyproject.toml)

## Structure

```
bot.py          # Main bot logic - all handlers and translation code
requirements.txt  # Python dependencies
pyproject.toml    # uv project config
```

## Features

- Automatic source language detection
- 40+ target languages selectable via inline keyboard
- `/start` - Welcome message
- `/language` - Choose translation target language
- `/see` - Admin command to view all users (requires ADMIN_ID secret)

## Required Secrets

- `TELEGRAM_BOT_TOKEN` - Bot token from Telegram @BotFather (required)
- `ADMIN_ID` - Telegram user ID for admin access to `/see` command (optional)

## Running

The bot runs in polling mode via the "Telegram Bot" workflow which executes `python3 bot.py`.
