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
        password_field.send_keys('Admin@teste2025')
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
        password_field.send_keys('Admin@teste2025')
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
        
class SugestaoMelhoriasTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

        self.driver.get('http://127.0.0.1:8000/')
        login_div = self.driver.find_element(By.CLASS_NAME, 'sign-in')
        username_field = login_div.find_element(By.NAME, 'username')
        password_field = login_div.find_element(By.NAME, 'password')
        username_field.send_keys('adminteste')
        password_field.send_keys('Admin@teste2025')
        login_button = login_div.find_element(By.TAG_NAME, 'button')
        login_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'menu-avisos'))
        )

    def test_abrir_sugestoes_melhoria(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/condosync/home/')
        time.sleep(2)

        sugestoes_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'sugestoes-melhoria-link'))
        )
        sugestoes_link.click()

        time.sleep(3)
        self.assertIn('/condosync/sugestoes', driver.current_url)

    def test_criar_sugestao(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/condosync/sugestoes/create/')

        titulo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'titulo'))
        )
        descricao = driver.find_element(By.NAME, 'descricao')

        titulo.send_keys('Sugestão Selenium')
        descricao.send_keys('Teste automatizado de sugestão.')

        submit = driver.find_element(By.XPATH, "//button[@type='submit']")
        submit.click()

        WebDriverWait(driver, 10).until(
            EC.url_contains('/condosync/sugestoes')
        )
        self.assertIn('Sugestão Selenium', driver.page_source)
    
    def test_editar_sugestao(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/condosync/sugestoes/')

        editar_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/sugestoes/edit/')]"))
        )
        editar_link.click()

        titulo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'titulo'))
        )
        titulo.clear()
        titulo.send_keys('Sugestão Editada Selenium')

        salvar_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        salvar_btn.click()

        WebDriverWait(driver, 10).until(
            EC.url_contains('/condosync/sugestoes')
        )
        self.assertIn('Sugestão Editada Selenium', driver.page_source)

    def test_deletar_sugestao(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/condosync/sugestoes/')

        deletar_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/sugestoes/delete/')]"))
        )                 
        deletar_link.click()

        confirmar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sim, excluir')]"))
        )
        confirmar_btn.click()

        WebDriverWait(driver, 10).until(
            EC.url_contains('/condosync/sugestoes')
        )
        self.assertNotIn('Sugestão Editada Selenium', driver.page_source)

class CadastramentoVeiculosTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

        self.driver.get('http://127.0.0.1:8000/')
    
    def test_clicar_cadastramento_veiculos(self):
        login_div = self.driver.find_element(By.CLASS_NAME, 'sign-in')
        username_field = login_div.find_element(By.NAME, 'username')
        password_field = login_div.find_element(By.NAME, 'password')
        username_field.send_keys('adminteste')
        password_field.send_keys('Admin@teste2025')
        login_button = login_div.find_element(By.TAG_NAME, 'button')
        login_button.click()

        driver = self.driver
        driver.get('http://127.0.0.1:8000/condosync/home/')

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cadastramento-veiculos-link"))
        )

        botao_veiculos = driver.find_element(By.ID, "cadastramento-veiculos-link")
        botao_veiculos.click()

        WebDriverWait(driver, 10).until(
            EC.url_contains('/veiculos')
        )

        self.assertIn('/veiculos', driver.current_url)

    def test_adicionar_veiculo(self):
        login_div = self.driver.find_element(By.CLASS_NAME, 'sign-in')
        username_field = login_div.find_element(By.NAME, 'username')
        password_field = login_div.find_element(By.NAME, 'password')
        username_field.send_keys('userteste') 
        password_field.send_keys('User@teste2025') 
        login_button = login_div.find_element(By.TAG_NAME, 'button')
        login_button.click()

        driver = self.driver
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cadastramento-veiculos-link"))
        )

        driver.get('http://127.0.0.1:8000/condosync/veiculos/adicionar_veiculos/')

        tipo_input = driver.find_element(By.NAME, 'tipo_veiculo')
        tipo_input.send_keys('Carro')

        marca_input = driver.find_element(By.NAME, 'marca')
        marca_input.send_keys('Ford') 

        modelo_input = driver.find_element(By.NAME, 'modelo')
        modelo_input.send_keys('Fiesta') 

        placa_input = driver.find_element(By.NAME, 'placa')
        placa_input.send_keys('ABC-1234')

        cor_input = driver.find_element(By.NAME, 'cor')
        cor_input.send_keys('Azul')

        ano_input = driver.find_element(By.NAME, 'ano')
        ano_input.send_keys('2020')

        submit_button = driver.find_element(By.TAG_NAME, 'button')
        submit_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//td[text()="Fiesta"]'))
        )

    def test_gerenciar_e_editar_veiculo(self):
        login_div = self.driver.find_element(By.CLASS_NAME, 'sign-in')
        username_field = login_div.find_element(By.NAME, 'username')
        password_field = login_div.find_element(By.NAME, 'password')
        username_field.send_keys('userteste')  
        password_field.send_keys('User@teste2025')  
        login_button = login_div.find_element(By.TAG_NAME, 'button')
        login_button.click()

        driver = self.driver
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cadastramento-veiculos-link"))
        )

        driver.get('http://127.0.0.1:8000/condosync/veiculos/gerenciar_veiculos/')

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//span[text()="Fiesta - ABC-1234"]'))
        )

        editar_button = driver.find_element(By.CSS_SELECTOR, '.veiculos-elements a.editar-veiculo i.bx.bxs-pencil')
        editar_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h1'))
        )

        self.assertIn('Editar Veículo', driver.page_source)

        cor_input = driver.find_element(By.NAME, 'cor')
        cor_input.clear()
        cor_input.send_keys('Preto') 

        ano_input = driver.find_element(By.NAME, 'ano')
        ano_input.clear()
        ano_input.send_keys('2022')

        submit_button = driver.find_element(By.TAG_NAME, 'button')
        submit_button.click()

        self.assertIn('condosync/veiculos/', driver.current_url)
    
    def test_gerenciar_e_excluir_veiculo(self):
        login_div = self.driver.find_element(By.CLASS_NAME, 'sign-in')
        username_field = login_div.find_element(By.NAME, 'username')
        password_field = login_div.find_element(By.NAME, 'password')
        username_field.send_keys('userteste')  
        password_field.send_keys('User@teste2025')  
        login_button = login_div.find_element(By.TAG_NAME, 'button')
        login_button.click()

        driver = self.driver
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cadastramento-veiculos-link"))
        )

        driver.get('http://127.0.0.1:8000/condosync/veiculos/gerenciar_veiculos/')

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//span[text()="Fiesta - ABC-1234"]'))
        )

        excluir_button = driver.find_element(By.CSS_SELECTOR, '.veiculos-elements a.deletar-veiculo i.bx.bx-x')
        excluir_button.click()

        confirmar_exclusao_button = driver.find_element(By.CSS_SELECTOR, '.confirm-box .btn-confirm')
        confirmar_exclusao_button.click()

        self.assertIn('condosync/veiculos/', driver.current_url)

class OcorrenciaTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

        self.driver.get('http://127.0.0.1:8000/')

        login_div = self.driver.find_element(By.CLASS_NAME, 'sign-in')
        username_field = login_div.find_element(By.NAME, 'username')
        password_field = login_div.find_element(By.NAME, 'password')
        username_field.send_keys('userteste')
        password_field.send_keys('User@teste2025')
        login_button = login_div.find_element(By.TAG_NAME, 'button')
        login_button.click()

    def test_clicar_ocorrencias(self):
        driver = self.driver
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "menu-ocorrencias"))
        )

        ocorrencias_link = driver.find_element(By.ID, 'menu-ocorrencias')
        ocorrencias_link.click()

        self.assertIn('condosync/ocorrencias/', driver.current_url)

    def test_criar_ocorrencia(self):
        driver = self.driver
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "menu-ocorrencias"))
        )
        ocorrencias_link = driver.find_element(By.ID, 'menu-ocorrencias')
        ocorrencias_link.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[text()='OCORRÊNCIAS']"))
        )

        create_ocorrencia_link = driver.find_element(By.LINK_TEXT, 'Registrar Ocorrência') 
        create_ocorrencia_link.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[text()='CRIAR OCORRÊNCIAS']"))
        )

        titulo_input = driver.find_element(By.ID, 'titulo')
        descricao_input = driver.find_element(By.ID, 'desc')

        titulo_input.send_keys('Teste de Ocorrência')
        descricao_input.send_keys('Descrição de teste para a ocorrência.')

        submit_button = driver.find_element(By.XPATH, "//button[text()='Registrar Ocorrência']")
        submit_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[text()='OCORRÊNCIAS']"))
        )

        self.assertIn('condosync/ocorrencias', driver.current_url)
        self.assertIn('Teste de Ocorrência', driver.page_source)

if __name__ == "__main__":
    unittest.main()
