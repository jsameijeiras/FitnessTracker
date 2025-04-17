
#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r render_requirements.txt

# Create required directories
mkdir -p instance
