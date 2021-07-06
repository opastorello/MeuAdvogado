#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyfiglet import Figlet
from clint.textui import colored
from pyfiglet import Figlet
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from threading import Thread
from bs4 import BeautifulSoup
from os import system
import time
import requests
import os
import re

class MeuAdvogado:
	def __init__(self):
		firefox_options = Options()
		firefox_options.add_argument('--headless')
		firefox_options.add_argument("--no-sandbox")
		firefox_options.add_argument("--mute-audio")
		firefox_options.add_argument("--log-level=3")
		firefox_options.add_argument("--ignore-certificate-errors")
		firefox_options.add_argument('--disable-gpu')
		firefox_options.add_argument('--disable-extensions')
		firefox_options.add_argument('--disable-default-apps')
		firefox_options.add_argument("--disable-dev-shm-usage")
		profile = webdriver.FirefoxProfile() 
		profile.executable_path = r'./geckodriver.exe'
		self.browser = webdriver.Firefox(profile, options=firefox_options, service_log_path="C:\\Windows\\Temp\\geckodriver.log")
		self.browser.get("https://www.meuadvogado.com.br/advogado/sp/")
		self.coletarPerfis()
		self.coletarDados()

	def coletarPerfis(self):
		total_resultados = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, r"/html/body/section/div/div/div[1]/div[3]/div/p[2]/strong[1]"))).text
		total_paginas = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, r"/html/body/section/div/div/div[1]/div[3]/div/p[2]/strong[3]"))).text
		pagina = 0

		print(colored.yellow("Encontrados {} resultados, vamos coletar dados de {} páginas uma a uma.\n".format(total_resultados, total_paginas)))

		while pagina < int(total_paginas):
			pagina += 1
			url = "https://www.meuadvogado.com.br/advogado/results.php?letter=&screen=" + str(pagina) + "&category_id=0&location_3=26&location_4=0&location_5=0"

			self.browser.get(url)

			perfils = self.browser.find_elements_by_class_name('advogado')

			print(colored.yellow("\nColetando perfils de advogados da Pagina número {}.\n".format(pagina)))

			for perfil in perfils:
				link_perfil = perfil.find_element_by_class_name('image').get_attribute('href')
				print(colored.green("[+] " + link_perfil))
				open("perfils.txt", "a+").write(link_perfil + "\n")

	def coletarDados(self):
		if os.path.isfile("perfils.txt"):
			with open("perfils.txt", "r", encoding="utf8") as perfils:
				print(colored.yellow("\nColetando dados dos advogados.\n"))
				for perfil in perfils:
					try:
						url = requests.get(perfil)
						soup = BeautifulSoup(url.text, 'html.parser')

						nome_advogado = soup.find(class_='main-name').text.strip()
						telefone_advogado = soup.find(class_='phoneBlock').text.strip()
						telefone_manipulado = re.sub(r'[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ.:,/]', '', telefone_advogado).replace('\n', '')

						print(colored.green("[+] Nome do Advogado: {}".format(nome_advogado)))
						print(colored.green("[+] Telefone do Advogado: {}\n".format(telefone_manipulado)))

						open("Dados.txt", "a+").write(nome_advogado + "," + telefone_manipulado + "\n")
					except:
						pass

system("title "+ f"Meu Advogado Web scraping")
Graph = Figlet(font="slant")
GraphRender = Graph.renderText("Meu Advogado")
system("cls")
print("%s" % (colored.yellow(GraphRender)))

try:
	MeuAdvogado()
except (KeyboardInterrupt):
	pass