#!/bin/bash

# Define the Python executable (use python3 if python is not aliased to python3)
PYTHON_EXEC="python3"

# Run the first Python script (script.py)
echo "Running script.py..."
$PYTHON_EXEC script.py

# Check if script.py ran successfully
if [ $? -ne 0 ]; then
    echo "script.py failed. Exiting."
    exit 1
fi

# Run the second Python script (analysis.py)
echo "Running analysis.py..."
$PYTHON_EXEC analysis.py

# Check if analysis.py ran successfully
if [ $? -ne 0 ]; then
    echo "analysis.py failed. Exiting."
    exit 1
fi

echo "Both scripts ran successfully."

