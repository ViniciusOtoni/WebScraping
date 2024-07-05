from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_star_rating(class_string):

    """ Extrai o número de estrelas da string da classe. """

    for word in class_string.split():
        if word.lower() in ['one', 'two', 'three', 'four', 'five']:
            return word
        
    return "No rating"

def webScraping(url):

    """ Extrai os valores do livro de acordo com a sua categoria. 
        Valores Extraidos:
        --Título
        --Categoria
        --Preço
        --Estoque
        --Avaliação
        
        """

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(url) # entrando ná pagina com a URL passada

        # esperando carregar os dados da página
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.nav-list > li > ul > li > a')))

        # pegando todas as URL das categorias
        category_links = driver.find_elements(By.CSS_SELECTOR, 'ul.nav-list > li > ul > li > a')
        category_urls = [link.get_attribute("href") for link in category_links] #href das categorias
        category_names = [link.text.strip() for link in category_links]  # nome das categorias

        # utilizando a função zip para combinar os valores e pegando os valores de forma unitária (nome da categoria, href da categoria)
        for category_url, category_name in zip(category_urls, category_names):
            driver.get(category_url) # entrando na página da categoria utilizando o href

            # esperando dados da página de categoria carregar
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h3 > a')))
            
            # pegando links dos livros para inspecionar de forma unitária
            book_links = driver.find_elements(By.CSS_SELECTOR, 'h3 > a')

            
            for book_link in book_links:
                book_url = book_link.get_attribute("href")

                # inspecionar livro de forma unitária
                driver.get(book_url)

                # esperando dados do livro carregar
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="col-sm-6 product_main"]')))

                # coletando valores (titulo, preço, estoque e avaliação)
                title = driver.find_element(By.XPATH, '//div[@class="col-sm-6 product_main"]/h1').text.strip()
                price = driver.find_element(By.XPATH, '//p[@class="price_color"]').text.strip()
                stock = driver.find_element(By.XPATH, '//p[@class="instock availability"]').text.strip()

                # pegando o valor contido na classe star-rating, (subclass) e chamando a função para realizar a extração do valor
                star_rating_element = driver.find_element(By.XPATH, '//p[contains(@class, "star-rating")]')
                star_rating_class = star_rating_element.get_attribute("class")
                star_rating = get_star_rating(star_rating_class)

                
                print(f"Categoria: {category_name}")
                print(f"Título: {title}")
                print(f"Preço: {price}")
                print(f"Estoque: {stock}")
                print(f"Classificação: {star_rating}")
                print("-" * 40)

                # voltar para a página da categoria
                driver.back()

                # esperando dados da página de categoria carregar
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h3 > a')))

    finally:
        # fechar o browser.
        driver.quit()



webScraping("http://books.toscrape.com/")
