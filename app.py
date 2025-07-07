import os
import re
import atexit
import time
from datetime import datetime
from flask import Flask, request, jsonify # A importação de 'cors' foi removida desta linha
from flask_cors import CORS             # <-- 1. ESTA É A IMPORTAÇÃO CORRETA
from pypdf import PdfReader, PdfWriter
import traceback
from unidecode import unidecode
import zipfile

# --- Funções ---

def limpar_pastas():
    """Esta função é executada quando o programa fecha para limpar tudo."""
    print("Executando limpeza ao sair...")
    for pasta in [UPLOADS_FOLDER, PAGINAS_FOLDER, ZIPS_FOLDER]:
        try:
            if os.path.exists(pasta):
                for filename in os.listdir(pasta):
                    file_path = os.path.join(pasta, filename)
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                    except Exception as e:
                        print(f"Erro ao apagar o arquivo {filename}: {e}")
        except Exception as e:
            print(f"Erro durante o processo de limpeza da pasta {pasta}: {e}")

def sanitizar_nome_arquivo(nome: str) -> str:
    nome_sem_acento = unidecode(nome)
    nome_limpo = re.sub(r'[\\/*?:"<>|]', "", nome_sem_acento)
    nome_final = re.sub(r'\s+', ' ', nome_limpo)
    return nome_final.strip()

def encontrar_nome(texto_da_pagina: str) -> str | None:
    padrao = re.compile(r"(.*\S.*)\s*\n\s*Nome do Funcionário", re.IGNORECASE)
    match = padrao.search(texto_da_pagina)
    if match:
        nome_bruto = match.group(1).strip()
        nome_limpo = re.sub(r'^[0-9\s]+', '', nome_bruto).strip()
        return nome_limpo.upper()
    return None

def encontrar_mes(texto_da_pagina: str) -> str | None:
    padrao = re.compile(r"Folha Mensal.*(\d{2}/\d{4})", re.IGNORECASE)
    match = padrao.search(texto_da_pagina)
    if match:
        data_str = match.group(1)
        try:
            data_obj = datetime.strptime(data_str, '%m/%Y')
            return data_obj.strftime('%Y-%m')
        except ValueError:
            return None
    return None

# --- Configuração do Flask ---
app = Flask(__name__, static_folder='static')
CORS(app) # <-- 2. USO CORRETO
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOADS_FOLDER = os.path.join(BASE_DIR, 'uploads')
PAGINAS_FOLDER = os.path.join(BASE_DIR, 'static', 'paginas_separadas')
ZIPS_FOLDER = os.path.join(BASE_DIR, 'static', 'zips')
os.makedirs(UPLOADS_FOLDER, exist_ok=True)
os.makedirs(PAGINAS_FOLDER, exist_ok=True)
os.makedirs(ZIPS_FOLDER, exist_ok=True)
atexit.register(limpar_pastas)

# --- Rotas da Aplicação ---
@app.route('/')
def index_redirect():
    return "Servidor Flask está rodando."

@app.route('/separar', methods=['POST'])
def separar_pdf():
    if 'pdf_file' not in request.files:
        return jsonify({'success': False, 'message': 'Nenhum arquivo enviado.'}), 400
    file = request.files['pdf_file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'Nenhum arquivo selecionado.'}), 400

    if file and file.filename.endswith('.pdf'):
        try:
            filepath = os.path.join(UPLOADS_FOLDER, file.filename)
            file.save(filepath)
            leitor_pdf = PdfReader(filepath)
            
            arquivos_gerados = []
            
            for i, page in enumerate(leitor_pdf.pages):
                nome = encontrar_nome(page.extract_text() or "")
                mes_ref = encontrar_mes(page.extract_text() or "")

                if nome and mes_ref:
                    nome_sanitizado = sanitizar_nome_arquivo(nome)
                    novo_nome_arquivo = f"{nome_sanitizado}_{mes_ref}.pdf"
                    caminho_saida = os.path.join(PAGINAS_FOLDER, novo_nome_arquivo)
                    
                    escritor_pdf = PdfWriter()
                    escritor_pdf.add_page(page)
                    with open(caminho_saida, "wb") as f_out:
                        escritor_pdf.write(f_out)
                    
                    arquivos_gerados.append(caminho_saida)

            if not arquivos_gerados:
                return jsonify({'success': False, 'message': 'Nenhuma página com dados reconhecíveis foi encontrada para processar.'})

            nome_base_zip, _ = os.path.splitext(file.filename)
            nome_zip = f"{nome_base_zip}_{int(time.time())}.zip"
            caminho_zip = os.path.join(ZIPS_FOLDER, nome_zip)

            with zipfile.ZipFile(caminho_zip, 'w') as zipf:
                for arquivo in arquivos_gerados:
                    zipf.write(arquivo, os.path.basename(arquivo))
            
            for arquivo in arquivos_gerados:
                os.remove(arquivo)

            return jsonify({
                'success': True,
                'message': f'{len(arquivos_gerados)} arquivos foram compactados.',
                'download_url': f'/static/zips/{nome_zip}'
            })

        except Exception as e:
            print(traceback.format_exc())
            return jsonify({'success': False, 'message': f'Ocorreu um erro inesperado: {str(e)}'}), 500
    else:
        return jsonify({'success': False, 'message': 'Arquivo inválido. Envie um PDF.'}), 400
