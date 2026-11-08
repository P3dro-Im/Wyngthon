#!/usr/bin/env bash
# Builds both documentation sites: Persian at site/ and English at site/en/.
set -e
cd "$(dirname "$0")"
mkdocs build -f mkdocs.yml
mkdocs build -f mkdocs-en.yml
