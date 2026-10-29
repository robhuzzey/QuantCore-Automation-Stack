#!/bin/bash
ASSET=$1
if [ -z "$ASSET" ]; then
    echo "Usage: ./remove.sh SYMBOL"
    exit 1
fi
pkill -f "$ASSET/trader.py"
rm -rf $ASSET
echo "Removed asset $ASSET"
