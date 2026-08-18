#!/bin/bash
set -e

echo "Starting Xvfb virtual display..."
Xvfb :99 -screen 0 1024x768x24 > /tmp/xvfb.log 2>&1 &
XVFB_PID=$!
echo "Xvfb PID: $XVFB_PID"

# Czekaj na start X serwera
sleep 3

echo "Running GUI tests..."
cd /app
python developers/docker_Teste/gui_test_automation.py

echo "Killing Xvfb..."
kill $XVFB_PID 2>/dev/null || true

echo "GUI tests completed. Screenshots saved to /app/gui_test_logs/"
