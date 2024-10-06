import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class TestShopping(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configurar el ChromeDriver con webdriver-manager
        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service)
        cls.driver.implicitly_wait(10)  # Espera implícita
        cls.driver.maximize_window()

    def navigate_to_shop(self):
        """Función auxiliar para navegar a la tienda"""
        self.driver.get("https://demo.evershop.io/")
        shop_xpath = "/html/body/div/div/main/div[2]/div/div/div[2]/div/div/a"
        shop_url = "https://demo.evershop.io/women"
        # Click on the shop link
        self.driver.find_element(By.XPATH, shop_xpath).click()
        WebDriverWait(self.driver, 10).until(EC.url_contains(shop_url))
        self.assertIn(shop_url, self.driver.current_url)

    def filter_products_by_name(self, product_name):
        """Función auxiliar para buscar productos por nombre"""
        search_icon_xpath = "//a[@class='search-icon']"  # XPath para el ícono de búsqueda (lupa)
        search_input_xpath = "//input[@placeholder='Search']"
        # Encuentra el ícono de búsqueda y haz clic para mostrar el campo de búsqueda
        search_icon = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, search_icon_xpath))
        )
        search_icon.click()
        # Encuentra el campo de búsqueda, ingresa el nombre del producto
        search_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, search_input_xpath))
        )
        search_input.send_keys(product_name)
        # Enviar "Enter" para realizar la búsqueda
        search_input.send_keys(Keys.RETURN)
        # Esperar a que se cargue la página con los resultados y verificar que la URL contiene el término de búsqueda
        search_url = f"https://demo.evershop.io/search?keyword={product_name.replace(' ', '+')}"
        WebDriverWait(self.driver, 10).until(EC.url_contains(search_url))
        self.assertIn(search_url, self.driver.current_url)

    def filer_products_by_color(self):
        """Funcion auxiliar para filtrar productos por color"""
        color_xpath= "/html/body/div/div/main/div[3]/div[1]/div/div[4]/ul/li[1]/a"
        # Click on the color filter
        self.driver.find_element(By.XPATH, color_xpath).click()
        # Assert que la url cambió para filtrar
        filter_url = "https://demo.evershop.io/women?color%5Boperation%5D=in&color%5Bvalue%5D=27"
        WebDriverWait(self.driver, 10).until(EC.url_contains(filter_url))
        self.assertIn(filter_url, self.driver.current_url)

    def navigate_to_product(self, product_xpath, product_url ):
        # Click on the product image
        self.driver.find_element(By.XPATH, product_xpath).click()        
        # Assert que la url cambió para ir al producto
        WebDriverWait(self.driver, 10).until(EC.url_contains(product_url))
        self.assertIn(product_url, self.driver.current_url)


    def  add_to_cart(self, size_url, size_color_url ):
        """Función auxiliar para añadir un producto al carrito"""
        size_xpath = "/html/body/div/div/main/div[2]/div[2]/div/div[2]/div[2]/div[1]/ul/li[1]/a"
        color_xpath = "/html/body/div/div/main/div[2]/div[2]/div/div[2]/div[2]/div[2]/ul/li[1]/a"
        add_xpath = "/html/body/div/div/main/div[2]/div[2]/div/div[2]/form/div/div/div[2]/button"
    
        # Click on size and color options
        self.driver.find_element(By.XPATH, size_xpath).click()
        # Assert url is correct
        WebDriverWait(self.driver, 10).until(EC.url_contains(size_url))
        self.assertIn(size_url, self.driver.current_url)

        self.driver.find_element(By.XPATH, color_xpath).click()
        # Assert url is correct
        WebDriverWait(self.driver, 10).until(EC.url_contains(size_color_url))
        self.assertIn(size_color_url, self.driver.current_url)
        # Click on the add to cart button        
        # Wait until the add to cart button is clickable before clicking
        add_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, add_xpath))
        )
        add_button.click()

    def navigate_to_cart(self):
        confirmation_xpath = "/html/body/div/div/div[4]/div/div/div/div/div"
        # Wait until confirmation appears
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, confirmation_xpath))
        )
        cart_xpath = "/html/body/div/div/div[4]/div/div/div/div/div/a[1]"
        self.driver.find_element(By.XPATH, cart_xpath).click()
        cart_url = "https://demo.evershop.io/cart"
        WebDriverWait(self.driver, 10).until(EC.url_contains(cart_url))
        self.assertIn(cart_url, self.driver.current_url)


    def checkout(self):
        """Función auxiliar para realizar el checkout"""
        # Hacer clic en el botón de checkout usando XPath
        checkout_button_xpath = "/html/body/div/div/main/div[2]/div/div[2]/div/div[2]/div/div[2]/a"
        checkout_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, checkout_button_xpath))
        )
        checkout_button.click()
        checkout_url = "https://demo.evershop.io/checkout"
        WebDriverWait(self.driver, 10).until(EC.url_contains(checkout_url))
        self.assertIn(checkout_url, self.driver.current_url)

    def test_add_product_by_color_filter_to_cart(self):
        """Prueba de añadir un producto al carrito"""
        self.navigate_to_shop()
        self.filer_products_by_color()
        self.navigate_to_product("/html/body/div/div/main/div[3]/div[2]/div[2]/div/div[1]/div[1]/a", "https://demo.evershop.io/women/nike-revolution-5-186")
        self.add_to_cart("https://demo.evershop.io/women/nike-revolution-5-186?size=4" , "https://demo.evershop.io/women/nike-revolution-5-186?size=4&color=27")
        self.navigate_to_cart()
        # Verificar que el producto se ha añadido al carrito
        product_xpath = "/html/body/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/table/tbody/tr/td[1]/div/div[2]/a"
        product_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, product_xpath))
        )
        
        #Check if the text contains "Nike revolution 5"
        self.assertIn("Nike revolution 5", product_element.text, "El producto no se ha añadido al carrito.")
        self.checkout()

    def test_add_product_by_name_to_cart(self):
        """Prueba de añadir un producto al carrito usando la búsqueda por nombre"""
        self.navigate_to_shop()
        self.filter_products_by_name("Nike revolution 5")
        self.navigate_to_product("/html/body/div/div/main/div[3]/div[1]/div[2]/div/div[1]/div[1]/a", "https://demo.evershop.io/women/nike-revolution-5-186")
        self.add_to_cart("https://demo.evershop.io/women/nike-revolution-5-186?size=4", "https://demo.evershop.io/women/nike-revolution-5-186?size=4&color=27")
        self.navigate_to_cart()

        # Verificar que el producto se ha añadido al carrito
        product_xpath = "/html/body/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/table/tbody/tr/td[1]/div/div[2]/a"
        product_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, product_xpath))
        )

        # Check if the text contains "Nike revolution 5"
        self.assertIn("Nike revolution 5", product_element.text, "El producto no se ha añadido al carrito.")
        self.checkout()
        
    def test_add_product_by_name_to_cart_no_exist(self):
        """Prueba de añadir un producto al carrito usando la búsqueda por nombre"""
        self.navigate_to_shop()
        self.filter_products_by_name("Teni")
  
    def test_add_multiple_products_by_name_to_cart(self):
        """Prueba de añadir múltiples productos al carrito usando la búsqueda por nombre"""
        self.navigate_to_shop()
        # Lista de nombres de productos a buscar
        product_names = ["Nike revolution 5", "Nike court vision low"]
        products = ["nike-revolution-5-186", "nike-court-vision-low-165"]
        sizes = ["4", "25", "25"]
        colors = ["27", "18", "14"]
        count = 0
        
        for product_name in product_names:
            self.filter_products_by_name(product_name)  # Buscar el producto
            self.navigate_to_product("/html/body/div/div/main/div[3]/div[1]/div[2]/div/div[1]/div[1]/a", f"https://demo.evershop.io/women/{products[count]}")
            self.add_to_cart(f"https://demo.evershop.io/women/{products[count]}?size={sizes[count]}", f"https://demo.evershop.io/women/{products[count]}?size={sizes[count]}&color={colors[count]}")  # Añadir el producto al carrito
            self.driver.back()  # Volver a la página de resultados
            count = count + 1

        # Navegar al carrito
        self.navigate_to_cart()

        # Verificar que todos los productos están en el carrito
        for product_name in product_names:
            product_xpath = f"//a[contains(text(), '{product_name}')]"
            product_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, product_xpath))
            )
            self.assertIsNotNone(product_element, f"{product_name} no se encontró en el carrito.")

        self.checkout()
    @classmethod
    def tearDownClass(cls):
        """Cerrar el navegador al final de todas las pruebas"""
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
