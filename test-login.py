import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestAuthentication(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configurar el ChromeDriver con webdriver-manager
        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service)
        cls.driver.implicitly_wait(10)  # Espera implícita
        cls.driver.maximize_window()

    def login(self, email, password):
        """Función auxiliar para realizar el login"""
        self.driver.get("http://localhost:5173/iniciar_sesion") 

        # Introducir el correo electrónico
        email_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_field.send_keys(email)

        # Introducir la contraseña
        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys(password)

        # Hacer clic en el botón de iniciar sesión
        login_button = self.driver.find_element(By.ID, "submit")
        login_button.click()

    def logout(self):
        """Función auxiliar para realizar el logout"""
        # Hacer clic en el dropdown del nombre del usuario para expandir el menú
        user_dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "nav-dropdown"))
        )
        user_dropdown.click()

        # Esperar hasta que la opción "Cerrar sesión" (NavDropdown.Item) esté visible y hacer clic
        logout_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "cerrar_sesion")) 
        )
        logout_button.click()

        # Verificar que se vuelve a la página de inicio de sesión
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "submit"))
        )

    def test_valid_login_and_logout(self):
        """Prueba de inicio de sesión válido y cierre de sesión (Happy Path)"""
        self.login("mamichofer16@gmail.com", "1234")

        # Verificar que se redirige a la página principal después de iniciar sesión
        WebDriverWait(self.driver, 10).until(EC.url_contains("/principal"))
        self.assertIn("/principal", self.driver.current_url)

        # Cerrar sesión
        self.logout()

        # Verificar que se ha cerrado la sesión y se vuelve a la página de inicio de sesión
        WebDriverWait(self.driver, 10).until(EC.url_contains("/iniciar_sesion"))
        self.assertIn("/iniciar_sesion", self.driver.current_url)


    def test_invalid_login(self):
        """Prueba de inicio de sesión con credenciales inválidas"""
        self.login("usuario_invalido@example.com", "contraseña_invalida")

        # Verificar que sigue en la página de inicio de sesión
        WebDriverWait(self.driver, 10).until(EC.url_contains("/iniciar_sesion"))
        self.assertIn("/iniciar_sesion", self.driver.current_url)


    def test_multiple_users(self):
        """Pruebas con múltiples usuarios"""
        users = [
            {"email": "usuario1@example.com", "password": "1234"},  
            {"email": "usuario_invalido@example.com", "password": "1234"},  
            {"email": "usuario3@example.com", "password": "1234"}   
        ]

        for user in users:
            self.login(user["email"], user["password"])

            if user["email"] == "usuario_invalido@example.com":
                # Verificar que sigue en la página de inicio de sesión para usuarios inválidos
                WebDriverWait(self.driver, 10).until(EC.url_contains("/iniciar_sesion"))
                self.assertIn("/iniciar_sesion", self.driver.current_url)
            else:
                # Verificar que se redirige a la página principal para usuarios válidos
                WebDriverWait(self.driver, 10).until(EC.url_contains("/principal"))
                self.assertIn("/principal", self.driver.current_url)

                # Cerrar sesión
                self.logout()

                # Verificar que vuelve a la página de inicio de sesión
                WebDriverWait(self.driver, 10).until(EC.url_contains("/iniciar_sesion"))
                self.assertIn("/iniciar_sesion", self.driver.current_url)


    @classmethod
    def tearDownClass(cls):
        """Cerrar el navegador al final de todas las pruebas"""
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
