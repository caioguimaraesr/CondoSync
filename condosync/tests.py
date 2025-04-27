import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

class RetiradaEncomendasTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

        self.driver.get('http://127.0.0.1:8000/')
        login_div = self.driver.find_element(By.CLASS_NAME, 'sign-in')
        username_field = login_div.find_element(By.NAME, 'username')
        password_field = login_div.find_element(By.NAME, 'password')
        username_field.send_keys('adminteste')
        password_field.send_keys('teste123')
        login_button = login_div.find_element(By.TAG_NAME, 'button')
        login_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'retirada-encomendas-link'))
        )

    def test_abrir_retirada_encomendas(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/condosync/home/')
        time.sleep(2)

        retirada_encomendas_link = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'retirada-encomendas-link'))
        )
        retirada_encomendas_link.click()

        time.sleep(2)
        self.assertIn('/condosync/encomendas', driver.current_url)
    
    def test_adicionar_encomenda(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/condosync/home/')
        time.sleep(2)

        retirada_encomendas_link = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'retirada-encomendas-link'))
        )
        retirada_encomendas_link.click()

        adicionar_encomenda_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'btn-adicionar-aviso'))
        )
        adicionar_encomenda_button.click()

        apartamento_select = driver.find_element(By.NAME, 'apartamento')
        apartamento_select.click()
        apartamento_select.find_element(By.XPATH, '//option[not(@disabled)][3]').click()

        peso_field = driver.find_element(By.NAME, 'peso_kg')
        peso_field.send_keys('5')

        origem_field = driver.find_element(By.NAME, 'origem')
        origem_field.send_keys('Amazon')
        time.sleep(1)

        submit_button = driver.find_element(By.XPATH, '//button[text()="Salvar Encomenda"]')
        submit_button.click()

        time.sleep(3)
        self.assertIn('/condosync/encomendas', driver.current_url)

    def test_editar_encomenda(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/condosync/home/')
        time.sleep(2)

        retirada_encomendas_link = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'retirada-encomendas-link'))
        )
        retirada_encomendas_link.click()

        editar_encomenda_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.icons a .bx.bx-pencil'))
        )
        editar_encomenda_link.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'peso_kg'))
        )

        peso_field = driver.find_element(By.NAME, 'peso_kg')
        peso_field.clear()
        peso_field.send_keys('10.5') 

        origem_field = driver.find_element(By.NAME, 'origem')
        origem_field.clear()
        origem_field.send_keys('Mercado Livre')

        time.sleep(2)
        submit_button = driver.find_element(By.XPATH, '//button[text()="Salvar Alterações"]')
        submit_button.click()

        time.sleep(3)
        self.assertIn('/condosync/encomendas', driver.current_url) 
    
    def test_editar_encomenda_voltar(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/condosync/home/')
        time.sleep(2)

        retirada_encomendas_link = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'retirada-encomendas-link'))
        )
        retirada_encomendas_link.click()

        editar_encomenda_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.icons a .bx.bx-pencil'))
        )
        editar_encomenda_link.click()

        time.sleep(2)
        submit_button = driver.find_element(By.XPATH, '//a[text()="← Voltar para a lista de encomendas"]')
        submit_button.click()

        time.sleep(2)
        self.assertIn('/condosync/encomendas', driver.current_url) 
    
    def test_excluir_encomenda(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/condosync/home/')
        time.sleep(2)

        retirada_encomendas_link = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'retirada-encomendas-link'))
        )
        retirada_encomendas_link.click()

        editar_encomenda_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.icons a .bx.bx-x'))
        )
        editar_encomenda_link.click()

        time.sleep(2)
        submit_button = driver.find_element(By.XPATH, '//button[text()="Sim, excluir"]')
        submit_button.click()

        time.sleep(3)
        self.assertIn('/condosync/encomendas', driver.current_url) 
    
    def test_excluir_encomenda_cancelar(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/condosync/home/')
        time.sleep(2)

        retirada_encomendas_link = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'retirada-encomendas-link'))
        )
        retirada_encomendas_link.click()

        editar_encomenda_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.icons a .bx.bx-x'))
        )
        editar_encomenda_link.click()

        time.sleep(2)
        submit_button = driver.find_element(By.XPATH, '//a[text()="Cancelar"]')
        submit_button.click()

        time.sleep(3)
        self.assertIn('/condosync/encomendas', driver.current_url) 

    def tearDown(self):
        self.driver.quit()

class AvisosTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

        self.driver.get('http://127.0.0.1:8000/')
        login_div = self.driver.find_element(By.CLASS_NAME, 'sign-in')
        username_field = login_div.find_element(By.NAME, 'username')
        password_field = login_div.find_element(By.NAME, 'password')
        username_field.send_keys('adminteste')
        password_field.send_keys('teste123')
        login_button = login_div.find_element(By.TAG_NAME, 'button')
        login_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'menu-avisos'))
        )

    def test_abrir_retirada_encomendas(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/condosync/home/')
        time.sleep(2)

        avisos_link = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'menu-avisos'))
        )
        avisos_link.click()

        time.sleep(2)
        self.assertIn('/condosync/avisos', driver.current_url)

    def test_adicionar_aviso(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/condosync/home/')
        time.sleep(2)

        avisos_link = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'menu-avisos'))
        )
        avisos_link.click()

        adicionar_encomenda_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'btn-adicionar-aviso'))
        )
        adicionar_encomenda_button.click()

        titulo = driver.find_element(By.NAME, 'titulo')
        titulo.send_keys('Reunião XX/XX')
        
        conteudo = driver.find_element(By.NAME, 'conteudo')
        conteudo.send_keys('Lorem, ipsum dolor sit amet consectetur adipisicing elit. Sint itaque excepturi voluptatibus eligendi, laboriosam voluptatem accusantium dignissimos beatae repellat illum! Delectus omnis ducimus quod. Rerum beatae reprehenderit animi quisquam. Est, itaque.')
        time.sleep(1)

        submit_button = driver.find_element(By.XPATH, '//button[text()="Salvar Aviso"]')
        submit_button.click()

        time.sleep(3)
        self.assertIn('/condosync/avisos', driver.current_url)

    def test_editar_aviso(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/condosync/home/')
        time.sleep(2)

        avisos_link = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'menu-avisos'))
        )
        avisos_link.click()

        editar_avisos_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.text a .bx.bx-pencil'))
        )
        editar_avisos_link.click()

        titulo = driver.find_element(By.NAME, 'titulo')
        titulo.clear()
        titulo.send_keys('Excesso de Sujeiras')
        
        conteudo = driver.find_element(By.NAME, 'conteudo')
        conteudo.clear()
        conteudo.send_keys('Lorem ipsum dolor sit amet consectetur adipisicing elit. Nulla vitae, minus ex sint, quisquam veniam nemo vel distinctio sunt at sapiente placeat harum! Pariatur minus atque dolore expedita, ad voluptatibus quisquam nisi maiores officia quos quam aliquam nesciunt, totam, sit assumenda eius. Voluptates cumque saepe similique incidunt ipsum sunt rem molestias eum.')
        time.sleep(1)

        time.sleep(2)
        submit_button = driver.find_element(By.XPATH, '//button[text()="Salvar Alterações"]')
        submit_button.click()

        time.sleep(3)
        self.assertIn('/condosync/avisos', driver.current_url) 
    
    def test_editar_aviso_voltar(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/condosync/home/')
        time.sleep(2)

        avisos_link = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'menu-avisos'))
        )
        avisos_link.click()

        editar_avisos_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.text a .bx.bx-pencil'))
        )
        editar_avisos_link.click()

        time.sleep(2)
        submit_button = driver.find_element(By.XPATH, '//a[text()="← Voltar para a lista de avisos"]')
        submit_button.click()

        time.sleep(3)
        self.assertIn('/condosync/avisos', driver.current_url) 

    def test_excluir_avisos(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/condosync/home/')
        time.sleep(2)

        avisos_link = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'menu-avisos'))
        )
        avisos_link.click()

        excluir_avisos_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.text a .bx.bx-x'))
        )
        excluir_avisos_link.click()

        time.sleep(2)
        submit_button = driver.find_element(By.XPATH, '//button[text()="Sim, excluir"]')
        submit_button.click()

        time.sleep(3)
        self.assertIn('/condosync/avisos', driver.current_url)
    
    def test_excluir_avisos_cancelar(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/condosync/home/')
        time.sleep(2)

        avisos_link = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'menu-avisos'))
        )
        avisos_link.click()

        excluir_avisos_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.text a .bx.bx-x'))
        )
        excluir_avisos_link.click()

        time.sleep(2)
        submit_button = driver.find_element(By.XPATH, '//a[text()="Cancelar"]')
        submit_button.click()

        time.sleep(3)
        self.assertIn('/condosync/avisos', driver.current_url)

if __name__ == "__main__":
    unittest.main()
