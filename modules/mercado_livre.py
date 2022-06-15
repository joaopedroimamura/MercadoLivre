from locale import currency, setlocale, LC_ALL
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class MercadoLivre:
    def __init__(self, search_text, driver, page):
        self.url_home = 'https://www.mercadolivre.com.br/'
        self.search_text = search_text
        self.driver = driver
        self.page = page
        self.control_print = True
        self.valid_page = True

        if self.page == 1:
            self.open_site()
            self.search_product()
            self.store_page()

        if self.valid_page:
            self.scroll()
            self.parents = self.products_list()

    def open_site(self) -> None:
        print('\nAbrindo navegador...')
        self.driver.maximize_window()
        self.driver.get(self.url_home)

    def search_product(self) -> None:
        print('Pesquisando produto...\n')
        text_input = self.driver.find_element(By.NAME, 'as_word')
        text_input.send_keys(self.search_text, Keys.ENTER)

    def store_page(self) -> None:
        if 'store' in self.driver.current_url:
            self.valid_page = False

    def scroll(self):
        print(f'Rolando página {self.page}...')
        y = 1000

        for _ in range(20):
            self.driver.execute_script(f"window.scrollTo(0, {y})")
            y += 1000
            sleep(.2)

    def products_list(self) -> list:
        print(f'Obtendo lista de produtos (página {self.page})...')
        return self.driver.find_elements(By.CLASS_NAME, 'ui-search-result__wrapper')

    def products_name(self) -> list:
        if self.control_print:
            print(f'Obtendo nome dos produtos (página {self.page})...')
        names = self.driver.find_elements(By.CLASS_NAME, 'ui-search-item__title')
        return [name.text for name in names]

    def products_price(self) -> list:
        print(f'Obtendo preço dos produtos (página {self.page})...')
        prices = []
        price_divs = self.driver.find_elements(By.CLASS_NAME, 'ui-search-price.ui-search-price--size-medium')

        setlocale(LC_ALL, 'pt_BR')

        for price_div in price_divs:
            price = price_div.find_element(By.XPATH, './/div//span//span').text

            if price:
                price = price.split(' ')

                if len(price) == 5:
                    price = float(f'{price[0]}.{price[3]}')
                else:
                    price = float(f'{price[0]}')

                format_price = currency(price, grouping=True)
                prices.append(format_price)

        self.control_print = False
        difference = abs(len(self.products_name()) - len(prices))

        # remove preço de produtos em anúncio
        for _ in range(difference):
            prices.pop(0)

        return prices

    def products_price_installment(self) -> list:
        print(f'Obtendo parcelas dos produtos (página {self.page})...')
        prices = []
        texts1 = []
        texts2 = []
        installments = []

        # region preco da parcela
        for parent in self.parents:
            try:
                xpath = './/div[@class="ui-search-price ui-search-price--size-x-tiny ui-search-color--BLACK"]' \
                        '//span[@class="price-tag-text-sr-only"]'
                price = parent.find_element(By.XPATH, xpath).text

                setlocale(LC_ALL, 'pt_BR')

                if price:
                    price = price.split(' ')

                    if len(price) == 5:
                        price = float(f'{price[0]}.{price[3]}')
                    else:
                        price = float(f'{price[0]}')

                    format_price = currency(price, grouping=True)
                    prices.append(format_price)

            except:
                try:
                    xpath = './/div[@class="ui-search-price ui-search-price--size-x-tiny ' \
                            'ui-search-color--LIGHT_GREEN"]//span[@class="price-tag-text-sr-only"]'
                    price = parent.find_element(By.XPATH, xpath).text

                    setlocale(LC_ALL, 'pt_BR')

                    if price:
                        price = price.split(' ')

                        if len(price) == 5:
                            price = float(f'{price[0]}.{price[3]}')
                        else:
                            price = float(f'{price[0]}')

                        format_price = currency(price, grouping=True)
                        prices.append(format_price)

                except:
                    prices.append(None)
        # endregion

        # region numero de parcelas
        for i in range(1, len(self.parents) + 1):
            try:
                xpath = f'/html/body/main/div/div[1]/section/ol/li[{i}]' \
                        f'/div/div/div[2]/div[2]/div[1]/div[1]/span/text()[1]'
                script = f"return document.evaluate('{xpath}', document, null, XPathResult." \
                         f"FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.textContent;"
                text = self.driver.execute_script(script)
                texts1.append(text)
            except:
                try:
                    xpath = f'/html/body/main/div/div[1]/section/ol/li[{i}]' \
                            f'/div/div/div[2]/div[3]/div[1]/div[1]/span/text()[1]'
                    script = f"return document.evaluate('{xpath}', document, null, XPathResult." \
                             f"FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.textContent;"
                    text = self.driver.execute_script(script)
                    texts1.append(text)
                except:
                    texts1.append(None)

        if texts1.count(None) == len(texts1):
            for i in range(1, 19):
                for j in range(1, 4):
                    try:
                        xpath = f'/html/body/main/div/div[1]/section/ol[{i}]/li[{j}]' \
                                f'/div/div/a/div[1]/div[1]/span/text()'
                        script = f"return document.evaluate('{xpath}', document, null, XPathResult." \
                                 f"FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.textContent;"
                        text = self.driver.execute_script(script)
                        texts2.append(text)
                    except:
                        try:
                            xpath = f'/html/body/main/div/div[1]/section/ol[{i}]/li[{j}]' \
                                    f'/div/div/a/div/div[2]/span/text()'
                            script = f"return document.evaluate('{xpath}', document, null, XPathResult." \
                                     f"FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.textContent;"
                            text = self.driver.execute_script(script)
                            texts2.append(text)
                        except:
                            try:
                                xpath = f'/html/body/main/div/div[1]/section/ol[{i}]/li[{j}]' \
                                        f'/div/div/a/div/div[3]/span/text()'
                                script = f"return document.evaluate('{xpath}', document, null, XPathResult." \
                                         f"FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.textContent;"
                                text = self.driver.execute_script(script)
                                texts2.append(text)
                            except:
                                texts2.append(None)
        # endregion

        for cont in range(len(prices)):
            if texts2:
                if texts2[cont] is None:
                    installments.append(None)
                else:
                    installments.append(f'{texts2[cont]}de {prices[cont]}')
            else:
                if texts1[cont] is None:
                    installments.append(None)
                else:
                    installments.append(f'{texts1[cont]}de {prices[cont]}')

        return installments

    def products_image(self) -> list:
        print(f'Obtendo imagens dos produtos (página {self.page})...')
        images = []

        for parent in self.parents:
            image = parent.find_element(By.XPATH, './/div[@data-index="0"]//img')
            images.append(image.get_attribute('src'))

        return images

    def products_link(self) -> list:
        print(f'Obtendo link dos produtos (página {self.page})...')
        links = []

        # region os links podem ter duas classes diferentes
        link_div = self.driver.find_elements(By.CLASS_NAME, 'ui-search-item__group__element.ui-search-link')

        if not link_div:
            link_div = self.driver.find_elements(By.CLASS_NAME, 'ui-search-result__content.ui-search-link')
        # endregion

        for link in link_div:
            links.append(link.get_attribute('href'))

        return links

    def products_shipping(self) -> list:
        print(f'Obtendo frete dos produtos (página {self.page})...')
        shippings = []

        for parent in self.parents:
            xpath = './/p[@class="ui-search-item__shipping ui-search-item__shipping--free"]'

            try:
                shipping = parent.find_element(By.XPATH, xpath).text
            except:
                shipping = None

            if shipping:
                shippings.append(True)
            else:
                shippings.append(None)

        return shippings

    def products_store(self) -> list:
        print(f'Obtendo loja dos produtos (página {self.page})...')
        stores = []

        for parent in self.parents:
            xpath_name = './/p[@class="ui-search-official-store-label ' \
                         'ui-search-item__group__element ui-search-color--GRAY"]'
            xpath_link = './/a[@class="ui-search-official-store-item__link ui-search-link"]'

            try:
                store_name = parent.find_element(By.XPATH, xpath_name).text
            except:
                store_name = None

            try:
                store_link = parent.find_element(By.XPATH, xpath_link).get_attribute('href')
            except:
                store_link = None

            if store_name and (store_name.startswith('Vendido') or store_name.startswith('vendido')):
                store_name = ' '.join(store_name.split(' ')[2::])
            elif store_name and (store_name.startswith('Por') or store_name.startswith('por')):
                store_name = ' '.join(store_name.split(' ')[1::])

            if store_name and store_link:
                stores.append(f'{store_name} ({store_link})')
            elif store_name:
                stores.append(store_name)
            else:
                stores.append(None)

        return stores

    def next_page(self) -> None:
        if self.page < 5:
            print('\nTrocando de página...\n')

        class_name = 'andes-pagination__button.andes-pagination__button--next'
        next_page_div = self.driver.find_element(By.CLASS_NAME, class_name)
        next_page = next_page_div.find_element(By.XPATH, './/a//span')
        next_page.click()

    def quit_driver(self):
        print('\nEncerrando conexão...')
        self.driver.quit()
