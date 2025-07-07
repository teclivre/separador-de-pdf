# Separador de PDF - Aplicativo Desktop v2.3.1

> Um aplicativo de desktop nativo para Linux que automatiza a separação de páginas de arquivos PDF e as renomeia de forma inteligente com base no conteúdo.

## 🎯 Sobre o Projeto

Este projeto foi criado para resolver um problema específico: a tarefa manual e repetitiva de abrir um PDF com múltiplas folhas de pagamento (ou holerites), separar cada uma em um arquivo individual e renomeá-lo com o nome do funcionário e o mês de referência.

O aplicativo oferece uma interface gráfica nativa onde o usuário pode simplesmente selecionar um arquivo PDF. O backend processa o arquivo, lê as informações necessárias de cada página e, ao final, gera um único arquivo `.zip` com todos os PDFs separados e corretamente nomeados, pronto para ser salvo em qualquer pasta.

## ✨ Funcionalidades

* **Interface Gráfica Nativa:** Construído com Python e a biblioteca **PyQt6**, garantindo um aplicativo rápido, responsivo e que não depende de navegadores.
* **Processamento Inteligente de PDF:** Utiliza a biblioteca `pypdf` para ler e manipular os arquivos PDF.
* **Extração de Dados:** Expressões regulares (RegEx) customizadas para encontrar e extrair dados específicos (nome do funcionário, mês de referência) do texto de cada página.
* **Renomeação Automática:** Cria nomes de arquivo padronizados e limpos, como `NOME_DO_FUNCIONARIO_ANO-MES.pdf`.
* **Compactação em .zip:** Junta todos os arquivos gerados em um único pacote `.zip` para facilitar o armazenamento e a distribuição.
* **Diálogo para Salvar Nativo:** Utiliza o seletor de arquivos do sistema operacional para que o usuário escolha onde deseja salvar o arquivo `.zip` final.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Interface Gráfica:** PyQt6
* **Manipulação de PDF:** pypdf
* **Outras bibliotecas:** unidecode

## 🚀 Como Usar

### Pré-requisitos

Antes de começar, garanta que você tem os seguintes softwares instalados em um sistema Linux baseado em Debian/Ubuntu (como Pop!_OS):
* **Python 3.10** ou superior.

### Instalação

1.  **Clone ou baixe este repositório:**
    ```bash
    # Se você usar git
    git clone [https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git)
    cd SEU_REPOSITORIO/
    ```

2.  **Dê permissão de execução ao instalador:**
    ```bash
    chmod +x install.sh
    ```

3.  **Execute o script de instalação:**
    ```bash
    ./install.sh
    ```
    O script irá verificar as dependências do sistema e do Python, e instalar o que for necessário. Ao final, um atalho para o "Separador de PDF" será adicionado ao seu menu de programas.

4.  **Execute o programa:**
    * Procure por "Separador de PDF" no seu menu de aplicativos e clique para abrir.
    * Ou, se preferir, execute diretamente pelo terminal com o comando: `python3 main.py`

---
Desenvolvido com a ajuda da IA Gemini.
