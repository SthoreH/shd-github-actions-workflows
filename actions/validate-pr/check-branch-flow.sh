#!/usr/bin/env bash
set -euo pipefail

echo "Verificando regra de esteira: $HEAD_REF → $BASE_REF"

if [[ "$BASE_REF" == "main" ]]; then
  if [[ "$HEAD_REF" != "dev" ]]; then
    echo "::error::PRs para 'main' só são permitidos a partir de 'dev'. Branch de origem: '$HEAD_REF'."
    exit 1
  fi
elif [[ "$BASE_REF" == "dev" ]]; then
  if [[ "$HEAD_REF" != feature/* ]]; then
    echo "::error::PRs para 'dev' só são permitidos a partir de branches 'feature/*'. Branch de origem: '$HEAD_REF'."
    exit 1
  fi
else
  echo "::warning::Branch de destino '$BASE_REF' não é monitorada pelas regras de esteira."
fi

echo "Regra de esteira válida: $HEAD_REF → $BASE_REF"
