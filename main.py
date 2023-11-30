import random
import re
import requests
import os
import sys

from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
from colorama import Fore, init

if sys.platform.lower() == 'linux':
    os.system('clear')

if sys.platform.lower() == 'windows':
    os.system('cls')

while True:
    try:
        init()
        qtd_itens = input(
            f'{Fore.CYAN}Quantos sites deseja que o script analíse? >> ')
        qtd_itens = sys.maxsize if len(qtd_itens) < 1 else qtd_itens
        print(f"{Fore.YELLOW}Quantide de sites pedidos: {qtd_itens}")
        print(f"{Fore.YELLOW}script iniciado!")
        
        if os.path.exists('./links_encontrados.txt'):
            os.remove('./links_encontrados.txt')

        if os.path.exists('./emails_encontrados.txt'):
            os.remove('./emails_encontrados.txt')

        filtro = '("consultoria de" AND TI OR Desenvolvimento OR Programação OR Trabalhe Conosco) ' \
            'OR ("estamos contratando" AND TI OR Desenvolvedor OR Programador OR Trabalhe Conosco) ' \
            'OR ("enviar currículo" AND "Desenvolvedor" OR Programador OR Trabalhe Conosco) ' \
            'OR ("enviar curriculum" AND "Desenvolvedor" OR Trabalhe Conosco)'

        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.64',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.64',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        ]

        with DDGS() as ddgs:
            results = [r for r in ddgs.text(
                filtro, safesearch="on", region="pt-br", max_results=int(qtd_itens), backend="lite")]
            filtro = re.findall(
                'https?://(?:www\.)?[a-zA-Z0-9][a-zA-Z0-9-]*\.(?:com|com\.br)(?:\/[^\s]*)?|http://(?:www\.)?[a-zA-Z0-9][a-zA-Z0-9-]*\.(?:com|com\.br)(?:\/[^\s]*)?', str(results))
            print(f"{Fore.BLUE}Total de sites para encontrados: {len(filtro)}")

            for link in set(filtro):
                try:
                    user_agent_dic = {'User-Agent': random.choice(user_agents)}
                    print(f"{Fore.GREEN}Analisando site: {link}")
                    requisicao_site = requests.get(
                        url=link, allow_redirects=True, timeout=5, headers=user_agent_dic)
                    bs_filtro = BeautifulSoup(
                        requisicao_site.text, 'html.parser')
                    for link_no_site in bs_filtro.find_all('a', href=True):
                        link_encontrado = link_no_site['href']
                        if (re.match('https?://(?:www\.)?[a-zA-Z0-9][a-zA-Z0-9-]*\.(?:com|com\.br)(?:\/[^\s]*)?|http://(?:www\.)?[a-zA-Z0-9][a-zA-Z0-9-]*\.(?:com|com\.br)(?:\/[^\s]*)?', link_encontrado)):
                            with open('links_encontrados.txt', 'a+') as fwrite:
                                fwrite.write(link_encontrado + '\n')

                    for email_no_site in bs_filtro.find_all(re.compile('[a-zA-Z0-9.-]*@[a-zA-Z0-9.-]*\.[a-zA-Z0-9.-]*')):
                        email_encontrado = email_no_site.get_text()
                        with open('emails_encontrados.txt', 'a+') as fwrite:
                            fwrite.write(email_encontrado + '\n')

                    for telefone_no_site in bs_filtro.find_all(re.compile(r'\b(?:\+55|55)?\s?(?:\([1-9]{2}\)|[1-9]{2})\s?9?[6-9]\d{3}[-.\s]?\d{4}\b')):
                        telefone_encontrado = telefone_no_site.get_text()
                        with open('telefones_encontrados.txt', 'a+') as fwrite:
                            fwrite.write(telefone_encontrado + '\n')

                except requests.exceptions.RequestException as e:
                    print(f"{Fore.RED}Erro ao acessar site: {link}")
    except Exception as e:
        print("Erro:", e)
