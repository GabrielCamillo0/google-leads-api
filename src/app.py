import requests
import os
import pandas as pd
from dotenv import load_dotenv
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import logging

# Carregar variáveis de ambiente
load_dotenv(override=True)

API_KEY = os.getenv("API_KEY")
CX_ID = os.getenv("CX_ID")

# Configuração de logging
logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)
logging.info("Iniciando o aplicativo...")

def buscar_leads(site, keyword):
    """Faz uma busca no Google usando a Custom Search API para capturar nome, e-mail, telefone e link."""
    QUERY = f"site:{site} \"{keyword}\" (\"@gmail.com\" OR \"@hotmail.com\" OR \"@yahoo.com\" OR \"@outlook.com\" OR \"@icloud.com\" OR \"@aol.com\" OR \"@live.com\" OR \"@protonmail.com\" OR \"@zoho.com\") (\"(11)\" OR \"+55\")"
    url = f"https://www.googleapis.com/customsearch/v1?q={QUERY}&key={API_KEY}&cx={CX_ID}"
    params = {
        "q": QUERY,
        "key": API_KEY,
        "cx": CX_ID,
        "num": 10
    }
    
    leads = []
    start = 1  # Paginação inicial
    max_results = 100  # Definir um limite para evitar bloqueios da API
    
    try:
        while len(leads) < max_results:
            params["start"] = start
            logging.debug(f"Enviando requisição para o Google com os parâmetros: {params}")
            response = requests.get(url, params=params)
            logging.debug(f"Status da resposta: {response.status_code}")
            
            if response.status_code == 200:
                resultados = response.json()
                logging.debug(f"Resposta completa: {resultados}")
                items = resultados.get("items", [])
                
                if not items:
                    break  # Sai do loop se não houver mais resultados
                
                for item in items:
                    title = item.get("title", "Desconhecido")
                    link = item.get("link", "Sem link")
                    snippet = item.get("snippet", "Sem descrição")
                    
                    email = "N/A"
                    telefone = "N/A"
                    
                    # Extração simples de e-mail e telefone
                    for word in snippet.split():
                        if "@" in word and "." in word:
                            email = word.strip(',').strip('.')
                        if word.startswith("+") or word.startswith("()"):
                            telefone = word.strip(',').strip('.')
                    
                    leads.append({"Nome": title, "Email": email, "Telefone": telefone, "Link": link})
                
                start += 10  # Avança para a próxima página de resultados
            else:
                logging.error(f"Erro na requisição: {response.status_code} - {response.text}")
                break
    except Exception as e:
        logging.critical(f"Erro crítico ao buscar leads: {e}", exc_info=True)
    
    return leads

def exibir_resultados(resultados):
    """Exibe os resultados na interface gráfica sem cortar os dados."""
    tree.delete(*tree.get_children())  # Limpa resultados antigos
    for item in resultados:
        tree.insert("", "end", values=(item["Nome"], item["Email"], item["Telefone"], item["Link"]))
    logging.info(f"Exibindo {len(resultados)} resultados.")

def salvar_em_planilha(resultados):
    """Salva os resultados em um arquivo Excel."""
    if not resultados:
        messagebox.showwarning("Aviso", "Nenhum resultado para salvar.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
    if not file_path:
        return

    df = pd.DataFrame(resultados)
    df.to_excel(file_path, index=False)
    messagebox.showinfo("Sucesso", "Resultados salvos com sucesso!")

def iniciar_busca():
    """Inicia a busca a partir da entrada do usuário."""
    site = entrada_site.get().strip()
    keyword = entrada_keyword.get().strip()
    if not site or not keyword:
        messagebox.showwarning("Aviso", "Por favor, insira um site e uma palavra-chave.")
        logging.warning("Tentativa de busca sem site ou palavra-chave inseridos.")
        return

    logging.info(f"Iniciando busca para: site={site}, keyword={keyword}")
    resultados = buscar_leads(site, keyword)
    if resultados:
        exibir_resultados(resultados)
    else:
        messagebox.showinfo("Info", "Nenhum resultado encontrado ou erro na busca.")
        logging.warning(f"Busca sem resultados: site={site}, keyword={keyword}")

# Interface Gráfica
app = tk.Tk()
app.title("Google Leads Scraper")

# Entrada de site
tk.Label(app, text="Site para buscar:").pack(pady=5)
entrada_site = tk.Entry(app, width=50)
entrada_site.insert(0, "instagram.com")  # Padrão definido
entrada_site.pack(pady=5)

# Entrada de palavra-chave
tk.Label(app, text="Palavra-chave:").pack(pady=5)
entrada_keyword = tk.Entry(app, width=50)
entrada_keyword.insert(0, "roupas")  # Padrão definido
entrada_keyword.pack(pady=5)

# Botão de busca
btn_buscar = tk.Button(app, text="Buscar Leads", command=iniciar_busca)
btn_buscar.pack(pady=10)

# Tabela de resultados
colunas = ("Nome", "Email", "Telefone", "Link")
tree = ttk.Treeview(app, columns=colunas, show="headings")
for coluna in colunas:
    tree.heading(coluna, text=coluna)
    tree.column(coluna, width=300)  # Ajustado para evitar corte

tree.pack(expand=True, fill="both", pady=10)

# Botão para salvar resultados
btn_salvar = tk.Button(app, text="Salvar em Excel", command=lambda: salvar_em_planilha(buscar_leads(entrada_site.get(), entrada_keyword.get())))
btn_salvar.pack(pady=10)

app.mainloop()





    