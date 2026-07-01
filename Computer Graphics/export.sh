#!/bin/bash

# Script para exportar o trabalho para envio no Moodle.
# Comprime o diretório fornecido, excluindo arquivos/diretórios listados em .gitignore.

if [ "$#" -ne 2 ]; then
    echo "Uso: $0 <diretorio_a_zipar> <nome_do_zip>"
    exit 1
fi

DIR_TO_COMPRESS="$1"
OUTPUT_ZIP_NAME="$2"

OUTPUT_ZIP_NAME="${OUTPUT_ZIP_NAME%.zip}.zip"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

TEMP_DIR=$(mktemp -d)

echo "Copiando diretório para localização temporária..."
cp -r "$DIR_TO_COMPRESS" "$TEMP_DIR/"

DIR_BASENAME=$(basename "$DIR_TO_COMPRESS")

if [ -f "$SCRIPT_DIR/.gitignore" ]; then
    echo ".gitignore encontrado. Processando remoções..."
    pushd "$TEMP_DIR/$DIR_BASENAME" > /dev/null
    
    while IFS= read -r pattern || [ -n "$pattern" ]; do
        if [[ -z "$pattern" || "$pattern" =~ ^\s*# ]]; then
            continue
        fi

        pattern="${pattern#./}"
        pattern="${pattern%/}"
        echo "Removendo arquivos/diretórios com o padrão $pattern..."
        find . -name "$pattern" -exec rm -rf {} + 2>/dev/null || true
    done < "$SCRIPT_DIR/.gitignore"
    
    popd > /dev/null
else
    echo "Nenhum arquivo .gitignore encontrado no diretório do script. Pulando exclusões."
fi

echo "Comprimindo diretório..."
(cd "$TEMP_DIR" && zip -rq "$OUTPUT_ZIP_NAME" "$DIR_BASENAME")

mv "$TEMP_DIR/$OUTPUT_ZIP_NAME" .

rm -rf "$TEMP_DIR"

echo "Compressão terminada. Arquivo resultante: $OUTPUT_ZIP_NAME"