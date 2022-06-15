from json import dump
from os import environ

from selenium import webdriver
from selenium.webdriver.chrome import service
from time import sleep
from time import time

from modules.mercado_livre import MercadoLivre


def solution():
    products = []
    success = True
    search_text = input('Digite o termo de busca: ')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--window-size=1920,1080")

    driver_path = environ.get('DRIVER_PATH')
    serv = service.Service(driver_path)
    driver = webdriver.Chrome(service=serv, options=chrome_options)

    for page in range(1, 6):
        mercado_livre = MercadoLivre(search_text=search_text, driver=driver, page=page)

        if not mercado_livre.valid_page:
            print('Essa é uma página de loja! O programa será encerrado sem nenhum output!')
            success = False
            break

        sleep(.3)

        names = mercado_livre.products_name(1)
        prices = mercado_livre.products_price()
        links = mercado_livre.products_link()
        shippings = mercado_livre.products_shipping()
        stores = mercado_livre.products_store()
        images = mercado_livre.products_image()
        installments = mercado_livre.products_price_installment()

        for i in range(len(names)):
            product = {'valor': prices[i],
                       'valor_parcelado': installments[i],
                       'nome_do_produto': names[i],
                       'foto': images[i],
                       'frete_gratis': None if shippings[i] is None else True,
                       'nome_da_loja': stores[i],
                       'link_do_produto': links[i],
                       'codigo_produto': None
                       }
            products.append(product)

        mercado_livre.next_page()

    mercado_livre.quit_driver()

    if success:
        file_name = '-'.join(search_text.split(' '))

        with open(f'.\\outputs\\{file_name}.json', mode='w', encoding='utf-8') as file:
            dump(products, file, indent=4, ensure_ascii=False)

        print('\nO programa foi encerrado com sucesso! Veja seu arquivo .json na pasta de outputs!')


if __name__ == '__main__':
    start = time()
    solution()
    execution_time = time() - start

    print(f'Tempo de execução foi de{execution_time: .2f} segundos.')
