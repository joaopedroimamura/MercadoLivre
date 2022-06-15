import os
from modules.mercado_livre import MercadoLivre
from selenium.webdriver.chrome import service
from selenium import webdriver
from time import sleep
import json

# nao esquecer de explicar casos que nao retornam nada, ex: playstation

# 1. Valor (check)
# 2. Valor parcelado (check)
# 3. Nome do produto (check)
# 4. Foto (check)
# 5. Frete gratis (check)
# 6. Nome da loja (check)
# 7. Link do produto (check)
# 8. Codigo do produto


# pelucia, pincel

url = os.environ.get('URL')
search_text = input('Digite o termo de busca: ')
driver_path = os.environ.get('DRIVER_PATH')
serv = service.Service(driver_path)
driver = webdriver.Chrome(service=serv)

ml = MercadoLivre(url_home=url, search_text=search_text, driver=driver, page=1)

sleep(1)

nm = ml.products_name()
pr = ml.products_price()
li = ml.products_link()
sh = ml.products_shipping()
st = ml.products_store()
im = ml.products_image()
pr_in = ml.products_price_installment()


print(nm)
print(pr)
print(li)
print(sh)
print(st)
print(im)
print(pr_in)

# ml.next_page()

print(len(nm))
print(len(pr))
print(len(li))
print(len(sh))
print(len(st))
print(len(im))
print(len(pr_in))

#
# products = []

# for i in range(len(nm)):
#     product = {'valor': pr[i],
#                'valor_parcelado': pr_in[i],
#                'nome_do_produto': nm[i],
#                'foto': im[i],
#                'frete_gratis': False if sh[i] is None else True,
#                'nome_da_loja': st[i],
#                'link_do_produto': li[i]
#                }
#
#     products.append(product)
#
# for p in products:
#     print(p)


url = 'https://www.mercadolivre.com.br/'
products = []

# for page in range(1, 6):
#     mercado_livre = MercadoLivre(url_home=url, search_text=search_text, driver=driver, page=page)
#
#     sleep(.5)
#
#     nm = mercado_livre.products_name()
#     pr = mercado_livre.products_price()
#     li = mercado_livre.products_link()
#     sh = mercado_livre.products_shipping()
#     st = mercado_livre.products_store()
#     im = mercado_livre.products_image()
#     pr_in = mercado_livre.products_price_installment()
#
#     for i in range(len(nm)):
#         product = {'valor': pr[i],
#                    'valor_parcelado': pr_in[i],
#                    'nome_do_produto': nm[i],
#                    'foto': im[i],
#                    'frete_gratis': None if sh[i] is None else True,
#                    'nome_da_loja': st[i],
#                    'link_do_produto': li[i]
#                    }
#
#         products.append(product)
#
#     mercado_livre.next_page()
#
# file_name = '-'.join(search_text.split(' '))
#
# with open(f'.\\outputs\\{file_name}.json', mode='w', encoding='utf-8') as file:
#     json.dump(products, file, indent=4, ensure_ascii=False)

