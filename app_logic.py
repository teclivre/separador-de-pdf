import os
import re
from datetime import datetime
from pypdf import PdfReader, PdfWriter
import traceback
from unidecode import unidecode
import zipfile
import time

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

def processar_e_zipar_pdf(caminho_pdf_entrada, caminho_zip_saida, update_status_callback):
    """
    Função principal que faz todo o trabalho: lê, separa, nomeia e compacta o PDF.
    Ela agora aceita uma função 'callback' para enviar atualizações de status para a interface.
    """
    try:
        update_status_callback(f"Lendo o arquivo: {os.path.basename(caminho_pdf_entrada)}...")
        leitor_pdf = PdfReader(caminho_pdf_entrada)
        
        temp_dir = os.path.join(os.path.dirname(caminho_zip_saida), "temp_paginas_pdf")
        os.makedirs(temp_dir, exist_ok=True)
        
        arquivos_gerados = []
        paginas_processadas = 0
        total_paginas = len(leitor_pdf.pages)
        
        for i, page in enumerate(leitor_pdf.pages):
            update_status_callback(f"Processando página {i + 1}/{total_paginas}...")
            nome = encontrar_nome(page.extract_text() or "")
            mes_ref = encontrar_mes(page.extract_text() or "")

            if nome and mes_ref:
                paginas_processadas += 1
                nome_sanitizado = sanitizar_nome_arquivo(nome)
                novo_nome_arquivo = f"{nome_sanitizado}_{mes_ref}.pdf"
                caminho_saida_pagina = os.path.join(temp_dir, novo_nome_arquivo)
                
                escritor_pdf = PdfWriter()
                escritor_pdf.add_page(page)
                with open(caminho_saida_pagina, "wb") as f_out:
                    escritor_pdf.write(f_out)
                
                arquivos_gerados.append(caminho_saida_pagina)

        if not arquivos_gerados:
            update_status_callback("Erro: Nenhuma página com dados reconhecíveis foi encontrada.", "red")
            os.rmdir(temp_dir)
            return

        update_status_callback(f"Compactando {len(arquivos_gerados)} arquivos...")
        with zipfile.ZipFile(caminho_zip_saida, 'w') as zipf:
            for arquivo in arquivos_gerados:
                zipf.write(arquivo, os.path.basename(arquivo))
        
        update_status_callback("Limpando arquivos temporários...")
        for arquivo in arquivos_gerados:
            os.remove(arquivo)
        os.rmdir(temp_dir)
        
        update_status_callback(f"Sucesso! Arquivo '{os.path.basename(caminho_zip_saida)}' criado.", "green")

    except Exception as e:
        error_info = traceback.format_exc()
        print(error_info)
        update_status_callback(f"Ocorreu um erro: {e}", "red")
