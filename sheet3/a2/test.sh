#! /usr/bin/env bash

# Suppose a whitelisted and a non-whitelisted file:
touch whitelisted
touch non-whitelisted

# Generate whitelist:
echo "$(realpath whitelisted)" > whitelist.txt

# Set library preloading up:
export LD_PRELOAD="$PWD/sandbox.so"

# Run test routine on each file:
./test whitelisted
./test non-whitelisted

# Unset library preloading:
unset LD_PRELOAD

# Cleanup:
rm whitelist.txt whitelisted non-whitelisted