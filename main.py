import tkinter as tk
import requests

def translate_text():
    text = entry.get("1.0", tk.END).strip()
    if text:
        translation = translate_with_mymemory(text, 'en', 'pt')
        output.delete("1.0", tk.END)
        output.insert(tk.END, translation)

def translate_with_mymemory(text, source_lang, target_lang):
    url = 'https://api.mymemory.translated.net/get'
    params = {
        'q': text,
        'langpair': f'{source_lang}|{target_lang}'
    }
    response = requests.get(url, params=params)
    data = response.json()
    if 'responseStatus' in data and data['responseStatus'] == 200:
        return data['responseData']['translatedText']
    else:
        return "Erro na tradução"

root = tk.Tk()
root.title("Tradutor de Inglês para Português")

window_width = 600
window_height = 400
root.geometry(f"{window_width}x{window_height}")
root.configure(borderwidth=2, relief="groove")

def on_resize(event):
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    entry.config(width=window_width//12, height=window_height//30)
    output.config(width=window_width//12, height=window_height//30)

root.bind("<Configure>", on_resize)

label = tk.Label(root, text="Digite o texto em inglês:")
label.pack()

entry = tk.Text(root, wrap="word", height=10, width=50)
entry.pack()

button = tk.Button(root, text="Traduzir", command=translate_text)
button.pack()

output = tk.Text(root, wrap="word", height=10, width=50)
output.pack()

entry.config(bd=2, relief="groove", bg="lightgray")
output.config(bd=2, relief="groove", bg="lightgray")

root.mainloop()  
