#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt

python SkillOrbit/manage.py collectstatic --noinput
python SkillOrbit/manage.py migrate
