#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias con pip
pip install -r render_requirements.txt

# Crear directorios necesarios
mkdir -p /tmp/report_uploads