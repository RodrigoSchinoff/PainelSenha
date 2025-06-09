import socket
import threading
import tkinter as tk
from PIL import Image, ImageTk
import os
import winsound  # Nativo no Windows

class TelaServidor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Painel de Senhas")
        self.root.geometry("1920x1080")
        self.root.configure(bg="white")
        self.root.state('zoomed')
        # self.root.overrideredirect(True)  # Descomente se quiser sem bordas

        self.ultima_senha = ""

        # Caminho base
        self.caminho_base = os.path.dirname(os.path.abspath(__file__))

        # Carregar logo
        logo_path = os.path.join(self.caminho_base, "logo_prefeitura.png")
        logo_img = Image.open(logo_path).resize((300, 300))
        self.logo_prefeitura_img = ImageTk.PhotoImage(logo_img)

        # Frame topo usando grid
        topo_frame = tk.Frame(self.root, bg="white")
        topo_frame.pack(side="top", pady=10, fill="x")

        # Configurar grid com 3 colunas
        topo_frame.columnconfigure(0, weight=3)  # esquerda (logo + secretaria)
        topo_frame.columnconfigure(1, weight=1)  # centro vazio
        topo_frame.columnconfigure(2, weight=3)  # direita (texto)

        # Esquerda: logo + secretaria
        esquerda = tk.Frame(topo_frame, bg="white")
        esquerda.grid(row=0, column=0, sticky="nsew", padx=20)

        tk.Label(esquerda, image=self.logo_prefeitura_img, bg="white").pack()

        tk.Label(
            esquerda,
            text="Secretaria Municipal de Fazenda",
            font=("Arial", 26, "bold"),
            fg="black",
            bg="white",
            wraplength=600,
            justify="center"
        ).pack(pady=10)

        # Centro vazio (apenas para separar)
        centro = tk.Frame(topo_frame, bg="white")
        centro.grid(row=0, column=1, sticky="nsew")

        # Direita: título ajustado
        direita = tk.Frame(topo_frame, bg="white")
        direita.grid(row=0, column=2, sticky="nsew", padx=20)

        tk.Label(direita,
                 text="Central de Atendimento ao Contribuinte",
                 font=("Arial", 30, "bold"),
                 fg="black", bg="white",
                 wraplength=700,
                 justify='center').pack(pady=50, fill="both", expand=True)

        # Senha atual
        self.label = tk.Label(self.root, text="Aguardando senha...",
                              font=("Arial", 48, "bold"), fg="black", bg="white")
        self.label.pack(pady=40)

        # Última senha
        self.ultima_label = tk.Label(self.root, text="",
                                     font=("Arial", 24), fg="gray", bg="white")
        self.ultima_label.pack()

        self.contadores = {"SF": 0, "P/SF": 0, "FP": 0, "SD": 0, "VS": 0}
        self.clientes = []

        threading.Thread(target=self.iniciar_servidor, daemon=True).start()
        self.root.mainloop()

    def iniciar_servidor(self):
        host = '0.0.0.0'
        porta = 12345
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind((host, porta))
        servidor.listen()

        print("Servidor ouvindo... Aceitando múltiplos painéis.")
        while True:
            conn, addr = servidor.accept()
            print(f"Conectado por {addr}")
            self.clientes.append(conn)
            threading.Thread(target=self.tratar_cliente, args=(conn,), daemon=True).start()

    def tratar_cliente(self, conn):
        while True:
            try:
                dados = conn.recv(1024).decode()
                if not dados:
                    break
                tipo, guiche = dados.split("|")
                senha = self.gerar_proxima_senha(tipo.strip())
                mensagem = f"{guiche.strip()} - Senha: {senha}"
                print(f"Chamando: {mensagem}")

                # Atualizar tela
                if self.label.cget("text") != "Aguardando senha...":
                    self.ultima_senha = self.label.cget("text").split(":")[-1].strip()

                self.label.config(text=mensagem)
                self.ultima_label.config(text=f"Última senha: {self.ultima_senha}" if self.ultima_senha else "")

                # Reproduzir som
                caminho_audio = os.path.join(self.caminho_base, "aeromoca.wav")
                if os.path.exists(caminho_audio):
                    winsound.PlaySound(caminho_audio, winsound.SND_FILENAME)

            except Exception as e:
                print(f"Erro: {e}")
                break
        conn.close()

    def gerar_proxima_senha(self, tipo):
        if tipo in self.contadores:
            self.contadores[tipo] += 1
            return f"{tipo}{self.contadores[tipo]:03d}"
        return "Tipo inválido"

if __name__ == "__main__":
    TelaServidor()
