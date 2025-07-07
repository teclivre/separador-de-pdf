# Separador de PDF - Aplicativo Desktop v1.0.0

> Um aplicativo de desktop para automatizar a separação de páginas de arquivos PDF e renomeá-las de forma inteligente com base no conteúdo extraído.

![Screenshot do Aplicativo](https://i.imgur.com/gK1dY3i.png)

## 🎯 Sobre o Projeto

Este projeto foi criado para resolver um problema específico: a tarefa manual e repetitiva de abrir um PDF com múltiplas folhas de pagamento (ou holerites), separar cada uma em um arquivo individual e renomeá-lo com o nome do funcionário e o mês de referência.

O aplicativo oferece uma interface gráfica moderna e intuitiva onde o usuário pode simplesmente selecionar um arquivo PDF. O backend processa o arquivo, lê as informações necessárias de cada página e, ao final, gera um único arquivo `.zip` com todos os PDFs separados e corretamente nomeados, pronto para ser salvo em qualquer pasta.

## ✨ Funcionalidades

* **Interface Gráfica Moderna:** Construído com tecnologias web (HTML, CSS, JS) e empacotado como um aplicativo nativo com a biblioteca Eel.
* **Processamento Inteligente de PDF:** Utiliza a biblioteca `pypdf` para ler e manipular os arquivos PDF.
* **Extração de Dados:** Expressões regulares (RegEx) customizadas para encontrar e extrair dados específicos (nome do funcionário, mês de referência) do texto de cada página.
* **Renomeação Automática:** Cria nomes de arquivo padronizados e limpos, como `NOME_DO_FUNCIONARIO_ANO-MES.pdf`.
* **Compactação em .zip:** Junta todos os arquivos gerados em um único pacote `.zip` para facilitar o armazenamento e a distribuição.
* **Diálogo para Salvar:** Permite que o usuário escolha exatamente onde deseja salvar o arquivo `.zip` final.
* **Instalador Simplificado:** Um script `install.sh` para ambientes Linux (testado em Pop!_OS/Ubuntu) que configura o aplicativo e cria um atalho no menu de programas.

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python
* **Servidor Web:** Flask
* **Manipulação de PDF:** pypdf
* **GUI Wrapper:** Eel
* **Frontend:** HTML5, CSS3, JavaScript

## 🚀 Como Usar

### Pré-requisitos

Antes de começar, garanta que você tem os seguintes softwares instalados:
* **Python 3.10** ou superior.
* **Google Chrome** ou **Chromium Browser**.
* Um sistema operacional baseado em Debian/Ubuntu (como o Pop!\_OS).

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
    O script irá verificar as dependências do sistema e do Python, e instalar o que for necessário. Ao final, um atalho para o "Separador de PDF" será adicionado ao seu menu de aplicativos.

4.  **Execute o programa:**
    * Procure por "Separador de PDF" no seu menu de aplicativos e clique para abrir.
    * Ou, se preferir, execute diretamente pelo terminal com o script de inicialização: `./launch.sh`

## 📜 Licença

Distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais informações.

---
