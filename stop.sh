#!/bin/bash

ps aux | grep gunicorn | awk '{print $2;}' | xargs kill -9 2>/dev/null
exit 0
