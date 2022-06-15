# Depois ver regras de import
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep


class MercadoLivre:
    # otimizado
    def __init__(self, url_home, search_text, driver, page):
        self.url_home = url_home
        self.search_text = search_text
        self.driver = driver
        self.page = page

        if self.page == 1:
            self.open_site()
            self.search_product()

        self.scroll()
        self.parents = self.products_list()

    # otimizado
    def open_site(self) -> None:
        self.driver.maximize_window()
        self.driver.get(self.url_home)

    # otimizado
    def search_product(self) -> None:
        text_input = self.driver.find_element(By.NAME, 'as_word')
        text_input.send_keys(self.search_text, Keys.ENTER)

    # otimizado
    def scroll(self):
        y = 1000

        for _ in range(20):
            self.driver.execute_script(f"window.scrollTo(0, {y})")
            y += 1000
            sleep(.6)

    # otimizado
    def products_list(self) -> list:
        return self.driver.find_elements(By.CLASS_NAME, 'ui-search-result__wrapper')

    # otimizado
    def products_name(self) -> list:
        names = self.driver.find_elements(By.CLASS_NAME, 'ui-search-item__title')
        return [name.text for name in names]

    # otimizado
    def products_price(self) -> list:
        prices = []
        price_div = self.driver.find_elements(By.CLASS_NAME, 'ui-search-price.ui-search-price--size-medium')

        for price_element in price_div:
            price = price_element.find_element(By.XPATH, './/div//span//span').text

            if price:
                price = price.split(' ')

                if len(price) == 5:
                    price = f'R${price[0]}.{price[3]}'
                else:
                    price = f'R${price[0]}.00'

                prices.append(price)

        # remove preço de produtos em anúncio
        difference = abs(len(self.products_name()) - len(prices))

        for _ in range(difference):
            prices.pop(0)

        return prices

    # otimizar
    def products_price_installment(self) -> list:
        prices = []
        texts1 = []
        texts2 = []
        installments = []

        installment_div = self.driver.find_elements(By.CLASS_NAME, 'ui-search-result__content-wrapper')

        for installment in installment_div:
            try:
                xpath = './/div//span//div[2]//div//span//span'
                price = installment.find_element(By.XPATH, xpath).text
                price = price.split(' ')

                if len(price) == 5:
                    price = f'R${price[0]}.{price[3]}'
                else:
                    price = f'R${price[0]}.00'
            except:
                try:
                    xpath = './/div[2]//div[1]//div[1]//span//div[2]//div[2]//div//span//span'
                    price = installment.find_element(By.XPATH, xpath).text
                    price = price.split(' ')

                    if len(price) == 5:
                        price = f'R${price[0]}.{price[3]}'
                    else:
                        price = f'R${price[0]}.00'
                except:
                    price = None

            prices.append(price)

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

        for cont in range(len(prices)):
            if texts2:
                installments.append(f'{texts2[cont]}de {prices[cont]}')
            else:
                installments.append(f'{texts1[cont]}de {prices[cont]}')

        return installments

    # otimizar
    def products_image(self) -> list:
        images = []
        image_div = self.driver.find_elements(By.CLASS_NAME, 'ui-search-result-image__element')

        for image in image_div:
            images.append(image.get_attribute('src'))

        return images

    # otimizado
    def products_link(self) -> list:
        links = []

        # region os links podem ter duas classes diferentes
        link_div = self.driver.find_elements(By.CLASS_NAME, 'ui-search-item__group__element.ui-search-link')

        if not link_div:
            link_div = self.driver.find_elements(By.CLASS_NAME, 'ui-search-result__content.ui-search-link')
        # endregion

        for link in link_div:
            links.append(link.get_attribute('href'))

        return links

    # otimizar
    def products_shipping(self) -> list:
        shippings = []

        for parent in self.parents:
            try:
                free_shipping = parent.find_element(By.XPATH, './/div//div[2]//div[2]//div[1]//div[2]//div//p').text

                if 'gratis' in free_shipping or 'grátis' in free_shipping:
                    free_shipping = 'Frete grátis'
                else:
                    free_shipping = None
            except:
                try:
                    free_shipping = parent.find_element(By.XPATH, './/div//a//div//div[2]//div//p').text

                    if 'gratis' in free_shipping or 'grátis' in free_shipping:
                        free_shipping = 'Frete grátis'
                    else:
                        free_shipping = None
                except:
                    try:
                        free_shipping = parent.find_element(By.XPATH, './/div//a/div//div[3]//div//p').text

                        if 'gratis' in free_shipping or 'grátis' in free_shipping:
                            free_shipping = 'Frete grátis'
                        else:
                            free_shipping = None
                    except:
                        try:
                            xpath = './/div//div[2]//div[3]//div[1]//div[2]//div//p'
                            free_shipping = parent.find_element(By.XPATH, xpath)

                            if 'gratis' in free_shipping or 'grátis' in free_shipping:
                                free_shipping = 'Frete grátis'
                            else:
                                free_shipping = None
                        except:
                            free_shipping = None

            shippings.append(free_shipping)

        return shippings

    # otimizar
    def products_store(self) -> list:
        stores = []

        for parent in self.parents:
            try:
                store_name = parent.find_element(By.XPATH, './/div//div[2]//div[1]//a[2]//p').text
                store_name = ' '.join(store_name.split(' ')[2::])

                store_link = parent.find_element(By.XPATH, './/div//div[2]//div[1]//a[2]')
                store_link = store_link.get_attribute('href')

                store = f'{store_name} ({store_link})'
            except:
                try:
                    store = parent.find_element(By.XPATH, './/div//a//div//div[3]//p').text
                    store = ' '.join(store.split(' ')[1::])

                    if 'gratis' in store or 'grátis' in store:
                        store = None
                except:
                    try:
                        store_name = parent.find_element(By.XPATH, './/div//div[2]//div[2]//a[2]//p').text
                        store_name = ' '.join(store_name.split(' ')[2::])

                        store_link = parent.find_element(By.XPATH, './/div//div[2]//div[2]//a[2]')
                        store_link = store_link.get_attribute('href')

                        store = f'{store_name} ({store_link})'
                    except:
                        try:
                            store = parent.find_element(By.XPATH, './/div//a//div//div[4]//p').text
                            store = ' '.join(store.split(' ')[1::])

                            if 'gratis' in store or 'grátis' in store:
                                store = None
                        except:
                            try:
                                store = parent.find_element(By.XPATH, './/div//a//div[1]//div[2]//p').text
                                store = ' '.join(store.split(' ')[1::])

                                if 'gratis' in store or 'grátis' in store:
                                    store = None
                            except:
                                store = None

            stores.append(store)

        return stores

    # otimizar
    def next_page(self) -> None:
        url_div = self.driver.find_elements(By.CLASS_NAME, 'andes-pagination__arrow-title')

        for url in url_div:
            if url.text == 'Seguinte':
                url.click()
                break
