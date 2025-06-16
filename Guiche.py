import socket
import tkinter as tk
from tkinter import messagebox, ttk

class PainelControle:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Guichê")
        self.root.geometry("350x380")

        self.prefixos = {
            "SEMFAZ": "SF",
            "PROTOCOLO/SEMFAZ": "P/SF",
            "FISCAL DE PLANTÃO": "FP",
            "SEMDUH": "SD",
            "VIGILÂNCIA SANITÁRIA": "VS",
        }

        # Campo para o IP
        tk.Label(self.root, text="IP do Servidor:").pack(pady=5)
        self.ip_entry = tk.Entry(self.root)
        self.ip_entry.insert(0, "localhost")  # valor padrão
        self.ip_entry.pack(pady=5)

        # Botão para conectar
        self.conectar_btn = tk.Button(self.root, text="Conectar", command=self.conectar)
        self.conectar_btn.pack(pady=10)

        # Combobox de tipo
        tk.Label(self.root, text="Tipo de Atendimento:").pack(pady=5)
        self.tipo_combo = ttk.Combobox(self.root, values=list(self.prefixos.keys()), state="disabled")
        self.tipo_combo.pack(pady=5)

        # Combobox de guichê
        tk.Label(self.root, text="Guichê:").pack(pady=5)
        self.guiche_combo = ttk.Combobox(self.root, values=[
            "Guichê 1", "Guichê 2", "Guichê 3", "Guichê 4",
            "Guichê 5", "Guichê 6", "Guichê 7", "Guichê 8"
        ], state="disabled")
        self.guiche_combo.pack(pady=5)

        # Botão chamar senha
        self.botao = tk.Button(self.root, text="Chamar Próxima Senha", state="disabled", command=self.enviar_solicitacao)
        self.botao.pack(pady=20)

        # Status
        self.status = tk.Label(self.root, text="", fg="green")
        self.status.pack()

        self.root.mainloop()

    def conectar(self):
        host = self.ip_entry.get().strip()
        porta = 12345

        try:
            self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.cliente.connect((host, porta))
            self.status.config(text=f"Conectado a {host}", fg="green")

            # Ativar os controles
            self.tipo_combo.config(state="readonly")
            self.tipo_combo.current(0)
            self.guiche_combo.config(state="readonly")
            self.guiche_combo.current(0)
            self.botao.config(state="normal")
            self.conectar_btn.config(state="disabled")
            self.ip_entry.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível conectar: {e}")
            self.status.config(text="Falha na conexão", fg="red")

    def enviar_solicitacao(self):
        tipo_nome = self.tipo_combo.get()
        guiche = self.guiche_combo.get()
        tipo = self.prefixos.get(tipo_nome, "A")
        mensagem = f"{tipo}|{guiche}"

        try:
            self.cliente.send(mensagem.encode())
            self.status.config(text=f"Solicitado: {tipo} ({guiche})", fg="blue")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao enviar: {e}")
            self.status.config(text="Erro ao enviar", fg="red")

if __name__ == "__main__":
    PainelControle()
