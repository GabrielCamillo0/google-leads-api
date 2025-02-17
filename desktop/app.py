import tkinter as tk
import requests

def buscar_leads():
    api_key = entry_key.get()
    site = entry_site.get()
    keyword = entry_keyword.get()

    response = requests.post("http://localhost:8000/search-leads", json={"api_key": api_key, "site": site, "keyword": keyword})
    leads = response.json()

    text_result.delete("1.0", tk.END)
    for lead in leads:
        text_result.insert(tk.END, f"{lead['title']}\n{lead['link']}\n\n")

app = tk.Tk()
app.title("Google Leads Scraper - Desktop")

tk.Label(app, text="API Key:").pack()
entry_key = tk.Entry(app)
entry_key.pack()

tk.Label(app, text="Site:").pack()
entry_site = tk.Entry(app)
entry_site.pack()

tk.Label(app, text="Palavra-chave:").pack()
entry_keyword = tk.Entry(app)
entry_keyword.pack()

btn_buscar = tk.Button(app, text="Buscar Leads", command=buscar_leads)
btn_buscar.pack()

text_result = tk.Text(app)
text_result.pack()

app.mainloop()
