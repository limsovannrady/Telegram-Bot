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
bot.py              # Core bot logic - handlers, create_app() factory function
api/webhook.py      # Vercel serverless webhook handler (POST from Telegram)
api/ping.py         # Ping route for Uptimerobot health checks (HEAD/GET)
vercel.json         # Vercel deployment configuration
requirements.txt    # Python dependencies
pyproject.toml      # uv project config
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

## Running Modes

### Polling (Replit / local development)
The "Telegram Bot" workflow runs `python3 bot.py` which uses polling mode via `create_app().run_polling()`.

### Webhook (Vercel production)
Deploy to Vercel and set the webhook URL via Telegram API:
```
https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://<your-vercel-domain>/api/webhook
```
Vercel routes `POST /api/webhook` to `api/webhook.py` which processes each incoming update.

### Uptimerobot Ping
Add a monitor in Uptimerobot pointing to:
```
https://<your-vercel-domain>/api/ping
```
Supports both HEAD and GET requests. Returns `200 OK`.
