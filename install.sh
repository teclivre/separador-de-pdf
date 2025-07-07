#!/bin/bash
set -e

# --- Script de Instalação Final (usando Eel) ---

echo "--- Iniciando a instalação do Separador de PDF com Eel ---"

# --- 1. VERIFICAÇÃO DE DEPENDÊNCIAS ---
# Eel precisa do Chrome/Chromium para funcionar
if ! command -v google-chrome-stable &> /dev/null && ! command -v chromium-browser &> /dev/null && ! command -v chromium &> /dev/null; then
    echo "ERRO: Google Chrome ou Chromium não foi encontrado."
    echo "Por favor, instale um deles para continuar (ex: sudo apt install chromium-browser)"
    exit 1
else
    echo "Navegador compatível (Chrome/Chromium) encontrado."
fi

# Dependências de Python (PIP)
PYTHON_DEPS=(
    "eel"
    "Flask"
    "pypdf"
    "python-dateutil"
    "unidecode"
    "Flask-Cors"
)

# --- 2. CONFIGURAÇÃO DO PROJETO E DEPENDÊNCIAS PYTHON ---
cd "$(dirname "$0")"
APP_DIR=$(pwd)
PYTHON_EXEC=$(which python3)

echo ""
echo "[PASSO 1 de 3] Criando script de inicialização 'launch.sh'..."
cat > "$APP_DIR/launch.sh" << EOL
#!/bin/bash
cd "\$(dirname "\$0")"
python3 gui.py
EOL
chmod +x "$APP_DIR/launch.sh"

echo ""
echo "[PASSO 2 de 3] Instalando pacotes Python para o usuário..."
pip install --user --upgrade pip > /dev/null
pip install --user "${PYTHON_DEPS[@]}" > /dev/null
echo "Pacotes Python instalados com sucesso."

# --- 3. CRIAÇÃO E INSTALAÇÃO DO ATALHO ---
echo ""
echo "[PASSO 3 de 3] Criando e instalando o atalho no menu de aplicativos..."
cat > "$APP_DIR/separador-pdf.desktop" << EOL
[Desktop Entry]
Version=1.0
Name=Separador de PDF
Comment=Separa páginas de um PDF e as renomeia
Exec="$APP_DIR/launch.sh"
Icon="$APP_DIR/separador-pdf.png"
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
echo "----------------------------------------------------"
echo "--- INSTALAÇÃO CONCLUÍDA COM SUCESSO! ---"
echo "----------------------------------------------------"
echo "O 'Separador de PDF' está pronto para ser usado no seu menu de aplicativos."
