import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from ttkthemes import ThemedTk
from concurrent.futures import ThreadPoolExecutor
from rembg import remove
from PIL import Image
import logging

logging.basicConfig(filename='process.log', level=logging.INFO)

def log_processing(image_name, status):
    logging.info(f"{image_name}: {status}")

def remove_background(input_path, output_path):
    try:
        img = Image.open(input_path)
        output = remove(img)
        
        if not output_path.lower().endswith(".png"):
            output_path += ".png"

        output.save(output_path, "PNG")
        log_processing(input_path, "Sucesso")
        return True
    except Exception as e:
        log_processing(input_path, f"Erro: {e}")
        return str(e)

def process_folder(input_folder, output_folder):
    with ThreadPoolExecutor() as executor:
        futures = []
        for filename in os.listdir(input_folder):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_no_bg.png")
            futures.append(executor.submit(remove_background, input_path, output_path))

        for future in futures:
            future.result() 

def show_image(image_path):
    img = Image.open(image_path)
    img.show()

def process_images(input_path, output_path):
    if os.path.isdir(input_path):
        process_folder(input_path, output_path)
        messagebox.showinfo("Sucesso", "Processamento concluído!")
    else:
        result = remove_background(input_path, output_path)
        if result is True:
            show_image(output_path)
            messagebox.showinfo("Sucesso", "Fundo removido com sucesso!")
        else:
            messagebox.showerror("Erro", f"Erro ao processar: {result}")

def select_input():
    path = filedialog.askopenfilename(title="Selecione uma imagem")
    input_path.set(path)

def select_output():
    path = filedialog.asksaveasfilename(defaultextension=".png", title="Salvar imagem como")
    output_path.set(path)

def process_button_click():
    if input_path.get() and output_path.get():
        process_images(input_path.get(), output_path.get())
    else:
        messagebox.showwarning("Atenção", "Por favor, selecione os caminhos de entrada e saída.")

root = ThemedTk(theme="arc")
root.title("Remoção de Fundo de Imagens")
root.geometry("400x300")

input_path = tk.StringVar()
output_path = tk.StringVar()

frame = ttk.Frame(root, padding="20")
frame.pack(expand=True, fill="both")

ttk.Label(frame, text="Caminho da Imagem de Entrada:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
input_entry = ttk.Entry(frame, textvariable=input_path, width=40)
input_entry.grid(row=1, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Selecionar Imagem", command=select_input).grid(row=1, column=2, padx=10)

ttk.Label(frame, text="Caminho da Imagem de Saída:", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
output_entry = ttk.Entry(frame, textvariable=output_path, width=40)
output_entry.grid(row=3, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Selecionar Saída", command=select_output).grid(row=3, column=2, padx=10)

process_button = ttk.Button(frame, text="Processar Imagem", command=process_button_click)
process_button.grid(row=4, column=0, columnspan=3, pady=20)
process_button.config(width=25)

root.mainloop()
