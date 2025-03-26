import os
import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename

# URL da página com os anexos
url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

# Diretório onde os arquivos PDF serão salvos
download_folder = "downloads"
os.makedirs(download_folder, exist_ok=True)

# Função para realizar o download dos PDFs
def download_pdf(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Arquivo {filename} baixado com sucesso!")
    else:
        print(f"Falha ao baixar {filename}")

# Função para coletar todos os links para os PDFs
def get_pdf_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontra todos os links de arquivos PDF
    pdf_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        # Verifica se o nome do arquivo corresponde aos nomes exatos desejados
        if 'Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf' in href or 'Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf' in href:
            pdf_links.append(href)

    return pdf_links

# Coleta os links dos PDFs
pdf_links = get_pdf_links(url)

# Baixar todos os PDFs encontrados
for link in pdf_links:
    # Formata o nome do arquivo para salvar localmente
    filename = os.path.join(download_folder, link.split('/')[-1])
    download_pdf(link, filename)

# Solicita ao usuário onde salvar o arquivo compactado
Tk().withdraw()  # Esconde a janela principal do Tkinter
zip_filename = asksaveasfilename(defaultextension=".zip", filetypes=[("Arquivos ZIP", "*.zip")], title="Escolha o local para salvar o arquivo compactado")

if zip_filename:
    # Compactar os arquivos PDF em um único arquivo ZIP no local escolhido pelo usuário
    with ZipFile(zip_filename, 'w') as zipf:
        for root, _, files in os.walk(download_folder):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.basename(file_path))
                print(f"Arquivo {file} adicionado ao ZIP")

    print(f"Todos os arquivos foram compactados em {zip_filename}")
else:
    print("Operação cancelada. Nenhum arquivo foi compactado.")
