import customtkinter as ctk
from tkinter import filedialog
import qrcode
from PIL import Image
import os


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class GeradorQRCode(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Criador de QR Code em Python")
        self.geometry("800x600")
        self.resizable(False, False)

        # Título
        self.label_titulo = ctk.CTkLabel(
            self, text="Gerador de QR Code", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.label_subtitulo = ctk.CTkLabel(
            self, text="Gerador de QR Code em Python", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.label_titulo.pack(pady=(25, 15))
        self.label_subtitulo.pack(pady=(25, 15))

        # Entrada do link
        self.label_link = ctk.CTkLabel(self, text="Insira o link ou texto:")
        self.label_link.pack()
        self.entry_link = ctk.CTkEntry(self, width=320, placeholder_text="Insira aqui")
        self.entry_link.pack(pady=5)

        # Botão Gerar
        self.btn_gerar = ctk.CTkButton(
            self, text="Gerar QR Code", 
            command=self.gerar_qr,
            font=ctk.CTkFont(weight="bold")
        )
        self.btn_gerar.pack(pady=15)

        # Frame para exibir o QR Code
        self.qr_frame = ctk.CTkFrame(self, width=250, height=250, fg_color="#333333")
        self.qr_frame.pack(pady=10)
        self.qr_frame.pack_propagate(False) # Mantém o tamanho do frame fixo

        self.label_img = ctk.CTkLabel(self.qr_frame, text="O QR Code aparecerá aqui")
        self.label_img.pack(expand=True)

        # Botão Salvar
        self.btn_salvar = ctk.CTkButton(
            self, text="Salvar Imagem", 
            command=self.salvar_qr,
            fg_color="transparent", border_width=2,
            state="disabled" # Desabilitado até que um QR seja gerado
        )
        self.btn_salvar.pack(pady=15)

        self.label_feedback = ctk.CTkLabel(self, text="", text_color="#2ecc71")
        self.label_feedback.pack()

        self.img_qrcode = None # Variável para armazenar a imagem

    def gerar_qr(self):
        try:
            texto = self.entry_link.get().strip()
            
            if not texto:
                self.label_feedback.configure(text="Erro: Insira um link ou texto!", text_color="#e74c3c")
                return

            # Geração do QR Code
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(texto)
            qr.make(fit=True)

            # Criando a imagem com PIL
            img = qr.make_image(fill_color="black", back_color="white")
            self.img_qrcode = img # Salva para o método de salvar depois

            # Convertendo para formato compatível com CTk
            ctk_img = ctk.CTkImage(light_image=img.get_image(), 
                                   dark_image=img.get_image(), 
                                   size=(230, 230))

            self.label_img.configure(image=ctk_img, text="")
            self.btn_salvar.configure(state="normal")
            self.label_feedback.configure(text="QR Code gerado!", text_color="#2ecc71")

        except Exception as e:
            print(f"Erro: {e}")
            self.label_feedback.configure(text="Erro ao gerar QR Code.", text_color="#e74c3c")

    def salvar_qr(self):
        if self.img_qrcode:
            try:
                # Abre a janela de diálogo para salvar arquivo
                caminho_arquivo = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[("Arquivos PNG", "*.png"), ("Todos os arquivos", "*.*")],
                    title="Escolha onde salvar seu QR Code",
                    initialfile="qrcode_gerado.png"
                )

                # Se o usuário não cancelar a janela (clicar em 'Salvar')
                if caminho_arquivo:
                    self.img_qrcode.save(caminho_arquivo)
                    self.label_feedback.configure(
                        text="QR Code salvo com sucesso!", 
                        text_color="#2ecc71"
                    )
                else:
                    # Caso o usuário feche a janela sem salvar
                    self.label_feedback.configure(
                        text="Operação cancelada.", 
                        text_color="#f39c12"
                    )

            except Exception as e:
                print(f"Erro ao salvar: {e}")
                self.label_feedback.configure(
                    text="Erro ao salvar o arquivo.", 
                    text_color="#e74c3c"
                )

if __name__ == "__main__":
    app = GeradorQRCode()
    app.mainloop()