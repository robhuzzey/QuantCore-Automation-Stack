#!/bin/bash
ASSET=$1
if [ -z "$ASSET" ]; then
    echo "Usage: ./add.sh SYMBOL"
    exit 1
fi
mkdir -p $ASSET
cp XAUUSD/active_strategy.json $ASSET/
cp XAUUSD/trader.py $ASSET/
cp XAUUSD/optimizer.py $ASSET/
echo "Added asset $ASSET"
