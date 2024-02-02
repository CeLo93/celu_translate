import tkinter as tk
import requests
import pyttsx3
import threading


def translate_text():
    text = entry.get("1.0", tk.END).strip()
    if text:
        max_chars_per_request = 500  # Define o máximo de caracteres por solicitação
        parts = [text[i:i+max_chars_per_request]
                 for i in range(0, len(text), max_chars_per_request)]
        translations = []
        for part in parts:
            translation = translate_with_mymemory(part, 'en', 'pt')
            translations.append(translation)
        output_text = ' '.join(translations)
        output.delete("1.0", tk.END)
        output.insert(tk.END, output_text)


def read_text():
    text = entry.get("1.0", tk.END).strip()
    if text:
        global reading_thread
        reading_thread = threading.Thread(
            target=read_text_thread, args=(text,))
        reading_thread.start()


def read_text_thread(text):
    engine = pyttsx3.init()
    # Configura a velocidade da fala (valores típicos estão entre 100 e 200)
    engine.setProperty('rate', 130)
    # Lista todas as vozes disponíveis e suas propriedades
    voices = engine.getProperty('voices')
    # Seleciona uma voz em inglês (altere o índice conforme necessário)
    # Exemplo: voices[0] para voz masculina, voices[1] para voz feminina
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()


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

label = tk.Label(root, text="Digite o texto em inglês:")
label.pack()

entry = tk.Text(root, wrap="word", height=10, width=50)
entry.pack()

translate_button = tk.Button(root, text="Traduzir", command=translate_text)
translate_button.pack()

read_button = tk.Button(root, text="Ler texto em inglês", command=read_text)
read_button.pack()

output = tk.Text(root, wrap="word", height=10, width=50)
output.pack()

entry.config(bd=2, relief="groove", bg="lightgray")
output.config(bd=2, relief="groove", bg="lightgray")

# Adiciona um evento para fechar a janela


def on_closing():
    global reading_thread
    if reading_thread and reading_thread.is_alive():
        # Para a leitura se estiver em andamento
        pyttsx3.init().stop()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)

# Variável para armazenar o thread de leitura
reading_thread = None

root.mainloop()
