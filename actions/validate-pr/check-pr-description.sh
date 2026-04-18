#!/usr/bin/env bash
set -euo pipefail

if [ -z "$(echo "$PR_BODY" | tr -d '[:space:]')" ]; then
  echo "::error::A descrição do PR não pode estar vazia. Descreva as mudanças realizadas."
  exit 1
fi
echo "Descrição preenchida."
