Destaques da pasta
Projeto Integrador I foca em baixar arquivos XML de notas fiscais com um plano de ação que inicia em Fev 2026 e um código-fonte de automação.

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
import os
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from tkcalendar import DateEntry


class NFSeDownloaderGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("NFSe XML Downloader")
        self.root.geometry("525x635+0+0")
        self.root.resizable(False, False)

        self.driver = None
        self.downloading = False
        self.pasta_destino = tk.StringVar()

        # NOVO: tipo de nota (Emitidas ou Recebidas)
        self.tipo_nota = tk.StringVar(value="Emitidas")

        self.criar_interface()

    # =====================================================
    # INTERFACE
    # =====================================================
    def criar_interface(self):

        self.main_frame = ttk.Frame(self.root, padding=15)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            self.main_frame,
            text="Pasta de destino e Período das Notas:",
            font=("Arial", 11, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 10)
        )

        pasta_frame = ttk.Frame(self.main_frame)
        pasta_frame.grid(row=1, column=0, columnspan=2, sticky="w")

        ttk.Button(
            pasta_frame,
            text="Selecionar pasta",
            command=self.selecionar_pasta
        ).pack(side=tk.LEFT)

        ttk.Entry(
            pasta_frame,
            textvariable=self.pasta_destino,
            width=65,
            state="readonly"
        ).pack(side=tk.LEFT, padx=8)

        datas_frame = ttk.Frame(self.main_frame)
        datas_frame.grid(row=2, column=0, columnspan=2, pady=15, sticky="w")

        ttk.Label(datas_frame, text="Data inicial:").pack(side=tk.LEFT)
        self.data_inicio = DateEntry(
            datas_frame,
            date_pattern="dd/mm/yyyy",
            locale="pt_BR",
            firstweekday="sunday",
            width=12
        )
        self.data_inicio.pack(side=tk.LEFT, padx=10)

        ttk.Label(datas_frame, text="Data final:").pack(side=tk.LEFT)
        self.data_fim = DateEntry(
            datas_frame,
            date_pattern="dd/mm/yyyy",
            locale="pt_BR",
            firstweekday="sunday",
            width=12
        )
        self.data_fim.pack(side=tk.LEFT, padx=10)

        # NOVO: seleção do tipo de nota
        tipo_frame = ttk.Frame(self.main_frame)
        tipo_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="w")

        ttk.Label(tipo_frame, text="Tipo de notas:").pack(side=tk.LEFT)

        ttk.Radiobutton(
            tipo_frame,
            text="Emitidas",
            variable=self.tipo_nota,
            value="Emitidas"
        ).pack(side=tk.LEFT, padx=10)

        ttk.Radiobutton(
            tipo_frame,
            text="Recebidas",
            variable=self.tipo_nota,
            value="Recebidas"
        ).pack(side=tk.LEFT)

        ttk.Button(
            self.main_frame,
            text="Abrir navegador / Login",
            command=self.abrir_navegador
        ).grid(row=4, column=0, pady=10, sticky="w")

        self.btn_iniciar_download = ttk.Button(
            self.main_frame,
            text="Iniciar download",
            command=self.iniciar_download,
            state="disabled"
        )
        self.btn_iniciar_download.grid(row=4, column=1, pady=10, sticky="w")

        ttk.Label(
            self.main_frame,
            text="Status:",
            font=("Arial", 11, "bold")
        ).grid(row=6, column=0, sticky="w")

        self.log_text = tk.Text(
            self.main_frame,
            height=25,
            width=70,
            font = ("Arial", 9)
        )
        self.log_text.grid(row=7, column=0, columnspan=2, pady=5, sticky="w")

        self.log(
            "INSTRUÇÕES:\n"
            "1 - Selecione a pasta onde os arquivos XML serão salvos.\n"
            "2 - Informe o período das notas a serem baixadas.\n"
            "3 - Escolha se deseja baixar notas EMITIDAS ou RECEBIDAS.\n"
            "4 - Clique em ABRIR NAVEGADOR / LOGIN, faça o login.\n"
            "5 - Retorne ao programa e clique em INICIAR DOWNLOAD.\n"
            "6 - Aguarde até a conclusão do processo.\n"
            + "-" * 60
        )

    # =====================================================
    # UTILITÁRIOS
    # =====================================================
    def log(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.root.update()

    def selecionar_pasta(self):
        pasta = filedialog.askdirectory()
        if pasta:
            self.pasta_destino.set(pasta)
            self.log(f"Pasta selecionada: {pasta}")

    # =====================================================
    # NAVEGADOR
    # =====================================================
    def abrir_navegador(self):
        if not self.pasta_destino.get():
            messagebox.showwarning("Atenção", "Selecione a pasta de destino.")
            return

        options = webdriver.ChromeOptions()

        # 🔹 NOVO MODO APP (sem barra de endereço)
        options.add_argument(
            "--app=https://www.nfse.gov.br/EmissorNacional/Login"
        )

        # 🔹 Define tamanho do Chrome
        options.add_argument("--window-size=1280,930")

        # 🔹 Posiciona o navegador ao lado da janela do programa
        options.add_argument("--window-position=470,0")

        self.driver = webdriver.Chrome(options=options)

        self.btn_iniciar_download.config(state="normal")

        self.log("Navegador aberto em modo integrado.")
        self.log("Faça o login manualmente e NÃO feche o navegador.")
        self.log("Botão 'Iniciar Download' liberado.")


    # =====================================================
    # CONTROLE DE DOWNLOAD
    # =====================================================
    def iniciar_download(self):
        if self.downloading:
            return

        if not self.driver:
            messagebox.showwarning("Atenção", "Abra o navegador primeiro.")
            return

        self.downloading = True

        data_inicio = self.data_inicio.get()
        data_fim = self.data_fim.get()

        threading.Thread(
            target=self.processar_download,
            args=(data_inicio, data_fim),
            daemon=True
        ).start()

    # =====================================================
    # DOWNLOAD + PAGINAÇÃO
    # =====================================================
    def processar_download(self, data_inicio, data_fim):
        try:
            pasta = self.pasta_destino.get()
            pagina = 1
            total = 0
            total_registros_site = None

            # Conta XML já existentes na pasta
            arquivos_existentes = [
                f for f in os.listdir(pasta)
                if f.lower().endswith(".xml")
            ]

            total_antes = len(arquivos_existentes)
            self.log(f"Arquivos XML já existentes na pasta: {total_antes}")

            tipo = self.tipo_nota.get()

            if tipo == "Emitidas":
                base_url = "https://www.nfse.gov.br/EmissorNacional/Notas/Emitidas"
            else:
                base_url = "https://www.nfse.gov.br/EmissorNacional/Notas/Recebidas"

            self.log(f"Iniciando download de notas {tipo} de {data_inicio} até {data_fim}")

            while True:

                if tipo == "Recebidas":
                    url = (
                        f"{base_url}"
                        f"?pg={pagina}"
                        f"&executar=1"
                        f"&busca="
                        f"&datainicio={data_inicio}"
                        f"&datafim={data_fim}"
                    )
                else:
                    url = (
                        f"{base_url}"
                        f"?pg={pagina}"
                        f"&busca="
                        f"&datainicio={data_inicio}"
                        f"&datafim={data_fim}"
                    )

                self.log(f"Acessando página {pagina}")
                self.driver.get(url)
                time.sleep(3)

                if pagina == 1:
                    try:
                        elemento_total = self.driver.find_element(
                            By.CSS_SELECTOR,
                            "div.descricao"
                        ).text

                        import re
                        match = re.search(r"Total de\s+(\d+)", elemento_total)

                        if match:
                            total_registros_site = int(match.group(1))
                            self.log(f"Total de notas informado pelo site: {total_registros_site}")
                        else:
                            total_registros_site = None
                            self.log("Não foi possível extrair o total de notas.")

                    except Exception as e:
                        total_registros_site = None
                        self.log("Elemento de total de notas não encontrado.")

                linhas = self.driver.find_elements(By.CSS_SELECTOR, "tbody tr")

                if not linhas:
                    break

                encontrou_xml = False

                for linha in linhas:
                    links = linha.find_elements(
                        By.XPATH,
                        ".//a[contains(@href,'/Notas/Download/NFSe/')]"
                    )

                    if not links:
                        continue

                    encontrou_xml = True
                    link_xml = links[0].get_attribute("href")
                    chave = link_xml.split("/")[-1]
                    arquivo = os.path.join(pasta, f"{chave}.xml")

                    if os.path.exists(arquivo):
                        continue

                    cookies = {c["name"]: c["value"] for c in self.driver.get_cookies()}
                    r = requests.get(link_xml, cookies=cookies)

                    if r.status_code == 200:
                        with open(arquivo, "wb") as f:
                            f.write(r.content)
                        total += 1
                        self.log(f"Baixado: {chave}.xml")

                if not encontrou_xml:
                    break

                pagina += 1  # vai para próxima página

            messagebox.showinfo(
                "Concluído",
                f"Download finalizado.\nTotal de arquivos baixados: {total}"
            )

            # ===========================
            # Validação real considerando XML já existentes
            # ===========================

            total_final = total_antes + total

            if total_registros_site is not None:

                if total_final == total_registros_site:
                    self.log("=" * 50)
                    self.log("✔ TODAS AS NOTAS FORAM BAIXADAS CORRETAMENTE.")

                else:
                    self.log("=" * 50)
                    self.log("⚠ FALTOU NOTAS A SEREM BAIXADAS, CONFIRA!")
                    self.log(f"Total esperado no site: {total_registros_site}")
                    self.log(f"Total existente na pasta: {total_final}")

            else:
                self.log("=" * 50)
                self.log("Não foi possível validar o total de registros.")

            self.log("=" * 50)
            self.log(f"TOTAL DE ARQUIVOS BAIXADOS: {total}")
            self.log("=" * 50)

        except Exception as e:
            messagebox.showerror("Erro", str(e))

        finally:
            self.downloading = False
            self.log("Processo encerrado.")

if __name__ == "__main__":
    root = tk.Tk()
    app = NFSeDownloaderGUI(root)
    root.mainloop()

