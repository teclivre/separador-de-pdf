#!/bin/bash
set -e

echo "--- Iniciando a instalação do Separador de PDF v2.3.0 (PyQt6) ---"

# --- 1. VERIFICAÇÃO DE DEPENDÊNCIAS DE SISTEMA ---
# Adicionado libxcb-cursor0 à lista
SYSTEM_DEPS=( "python3-pyqt6" "qt6-base-dev" "libxcb-cursor0" )
missing_deps=()
for dep in "${SYSTEM_DEPS[@]}"; do
    if ! dpkg -s "$dep" &> /dev/null; then
        missing_deps+=("$dep")
    fi
done

if [ ${#missing_deps[@]} -gt 0 ]; then
    echo "AVISO: As seguintes dependências de sistema estão faltando:"
    for dep in "${missing_deps[@]}"; do echo "  - $dep"; done
    read -p "Deseja que o script tente instalá-las agora? (s/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        sudo apt-get update
        sudo apt-get install -y "${missing_deps[@]}"
    else
        echo "Instalação cancelada."
        exit 1
    fi
fi

# --- 2. INSTALAÇÃO DE DEPENDÊNCIAS PYTHON ---
PYTHON_DEPS=( "PyQt6" "pypdf" "unidecode" )
echo "[PASSO 1 de 2] Instalando pacotes Python..."
pip install --user --upgrade pip > /dev/null
pip install --user "${PYTHON_DEPS[@]}" > /dev/null
echo "Pacotes Python instalados com sucesso."

# --- 3. CRIAÇÃO DO ATALHO ---
cd "$(dirname "$0")"
APP_DIR=$(pwd)
echo "[PASSO 2 de 2] Criando e instalando o atalho..."
cat > "$APP_DIR/separador-pdf.desktop" << EOL
[Desktop Entry]
Version=2.3.0
Name=Separador de PDF
Comment=Separa páginas de um PDF e as renomeia
Exec=python3 $APP_DIR/main.py
Icon=$APP_DIR/separador-pdf.png
Terminal=false
Type=Application
Categories=Office;Utility;
EOL
APP_LAUNCHER_DIR="$HOME/.local/share/applications"
mkdir -p "$APP_LAUNCHER_DIR"
rm -f "$APP_LAUNCHER_DIR/separador-pdf.desktop"
cp "$APP_DIR/separador-pdf.desktop" "$APP_LAUNCHER_DIR/"
update-desktop-database "$APP_LAUNCHER_DIR"

echo ""
echo "--- INSTALAÇÃO CONCLUÍDA COM SUCESSO! ---"
echo "O atalho para a nova versão PyQt6 foi criado no seu menu de aplicativos."
