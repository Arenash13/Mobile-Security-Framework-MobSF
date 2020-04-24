#!/bin/bash
# Dev Server
. venv/bin/activate && python manage.py runserver
# Prod Server
# . venv/bin/activate && daphne -b 0.0.0.0 -p 8000 MobSF.asgi:application 
 # --workers=1 