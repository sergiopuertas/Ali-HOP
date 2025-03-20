#!/bin/bash

# Configura las variables
GITHUB_TOKEN=${{ secrets.PAT_TOKEN }}
OWNER="sergiopuertas"   # Tu usuario de GitHub
REPO="Ali-HOP"          # Tu repositorio
WORKFLOW="daily-commit.yml"  # Nombre del archivo del workflow
BRANCH="main"           # Cambia si tu rama principal no es 'main'

# Llamada a la API de GitHub para ejecutar el workflow
curl -X POST -H "Accept: application/vnd.github+json" \
     -H "Authorization: token $GITHUB_TOKEN" \
     "https://api.github.com/repos/$OWNER/$REPO/actions/workflows/$WORKFLOW/dispatches" \
     -d "{\"ref\":\"$BRANCH\"}"
