import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from selenium.webdriver.chrome.options import Options
from .models import Apartamento, Encomenda, Aviso, Sugestoes, Veiculo, Ocorrencia, Boleto
from django.core.files.uploadedfile import SimpleUploadedFile
import pytest
import os
import time
import tempfile

@pytest.mark.django_db
class TestRetiradaEncomendas(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='adminteste',
            email='admin@example.com',
            password='Admin@teste2025',
        )

        self.apartamento = Apartamento.objects.create(
            numero='101',
            morador=self.user,
        )

        self.driver.get(self.live_server_url + '/')
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
        driver.get(self.live_server_url + '/condosync/home/')
        time.sleep(2)

        retirada_encomendas_link = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'retirada-encomendas-link'))
        )
        retirada_encomendas_link.click()

        time.sleep(2)
        assert '/condosync/encomendas' in driver.current_url

    def test_adicionar_encomenda(self):
        driver = self.driver
        driver.get(self.live_server_url + '/condosync/home/')
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
        apartamento_select.find_element(By.XPATH, '//option[not(@disabled)][1]').click()

        peso_field = driver.find_element(By.NAME, 'peso_kg')
        peso_field.send_keys('5')

        origem_field = driver.find_element(By.NAME, 'origem')
        origem_field.send_keys('Amazon')
        time.sleep(1)

        submit_button = driver.find_element(By.XPATH, '//button[text()="Salvar Encomenda"]')
        submit_button.click()

        time.sleep(3)
        assert '/condosync/encomendas' in driver.current_url

    def test_editar_encomenda(self):
        encomenda = Encomenda.objects.create(
            apartamento=self.apartamento,
            peso_kg=2.0,
            origem="Shopee",
        )

        driver = self.driver
        driver.get(self.live_server_url + '/condosync/home/')
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

        submit_button = driver.find_element(By.XPATH, '//button[text()="Salvar Alterações"]')
        submit_button.click()

        assert '/condosync/encomendas' in driver.current_url 
    
    def test_excluir_encomenda(self):
        encomenda = Encomenda.objects.create(
            apartamento=self.apartamento,
            peso_kg=3.5,
            origem="Magazine Luiza",
        )

        driver = self.driver
        driver.get(self.live_server_url + '/condosync/home/')
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

        assert '/condosync/encomendas' in driver.current_url
    
    def tearDown(self):
        self.user.delete()
        self.apartamento.delete()

@pytest.mark.django_db
class TestAvisos(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='adminteste',
            email='admin@example.com',
            password='Admin@teste2025',
        )

        self.driver.get(self.live_server_url + '/')
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
        driver.get(self.live_server_url + '/condosync/home/')

        avisos_link = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'menu-avisos'))
        )
        avisos_link.click()

        time.sleep(2)
        assert '/condosync/avisos' in driver.current_url

    def test_adicionar_aviso(self):
        driver = self.driver
        driver.get(self.live_server_url + '/condosync/home/')

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

        submit_button = driver.find_element(By.XPATH, '//button[text()="Salvar Aviso"]')
        submit_button.click()

        assert '/condosync/avisos' in driver.current_url

    def test_editar_aviso(self):
        Aviso.objects.create(
            titulo='Aviso Temporário',
            conteudo='Conteúdo de teste para exclusão.',
        )

        driver = self.driver
        driver.get(self.live_server_url + '/condosync/home/')
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
        conteudo.send_keys('Lorem ipsum dolor sit amet consectetur adipisicing elit. Nulla vitae, minus ex sint, quisquam veniam nemo vel distinctio sunt at sapiente placeat harum!...')

        time.sleep(2)
        submit_button = driver.find_element(By.XPATH, '//button[text()="Salvar Alterações"]')
        submit_button.click()

        time.sleep(3)
        assert '/condosync/avisos' in driver.current_url

    def test_excluir_avisos(self):
        Aviso.objects.create(
            titulo='Aviso Temporário',
            conteudo='Conteúdo de teste para exclusão.',
        )
        driver = self.driver
        driver.get(self.live_server_url + '/condosync/home/')

        avisos_link = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'menu-avisos'))
        )
        avisos_link.click()

        excluir_avisos_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.text a .bx.bx-x'))
        )
        excluir_avisos_link.click()

        submit_button = driver.find_element(By.XPATH, '//button[text()="Sim, excluir"]')
        submit_button.click()

        time.sleep(3)
        assert '/condosync/avisos' in driver.current_url
        
@pytest.mark.django_db
class TestSugestaoMelhorias(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='adminteste',
            email='admin@example.com',
            password='Admin@teste2025',
        )

        self.apartamento = Apartamento.objects.create(
            numero='101',
            morador=self.user,
        )

        self.driver.get(self.live_server_url + '/')
        login_div = self.driver.find_element(By.CLASS_NAME, 'sign-in')
        username_field = login_div.find_element(By.NAME, 'username')
        password_field = login_div.find_element(By.NAME, 'password')
        username_field.send_keys('adminteste')
        password_field.send_keys('Admin@teste2025')
        login_button = login_div.find_element(By.TAG_NAME, 'button')
        login_button.click()

    def test_abrir_sugestoes_melhoria(self):
        driver = self.driver
        driver.get(self.live_server_url + '/condosync/home/')
        time.sleep(2)

        sugestoes_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'sugestoes-melhoria-link'))
        )
        sugestoes_link.click()

        time.sleep(3)
        assert '/condosync/sugestoes' in driver.current_url

    def test_criar_sugestao(self):
        driver = self.driver
        driver.get(self.live_server_url + '/condosync/sugestoes/create/')

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

        assert 'Sugestão Selenium' in driver.page_source
    
    def test_editar_sugestao(self):
        Sugestoes.objects.create(
            titulo='Sugestão Inicial',
            descricao='Descrição original',
            usuario=self.user 
        )
        driver = self.driver
        driver.get(self.live_server_url + '/condosync/sugestoes/')

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
        assert 'Sugestão Editada Selenium' in driver.page_source

    def test_deletar_sugestao(self):
        Sugestoes.objects.create(
            titulo='Sugestão Inicial',
            descricao='Descrição original',
            usuario=self.user 
        )
        driver = self.driver
        driver.get(self.live_server_url + '/condosync/sugestoes/')

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

        assert 'Sugestão Editada Selenium' not in driver.page_source

class TestCadastramentoVeiculos(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='adminteste',
            email='admin@example.com',
            password='Admin@teste2025',
        )

        self.user_normal = User.objects.create_user(
            username='userteste',
            email='userteste@gmail.com',
            password='User@teste2025',
        )

        self.apartamento = Apartamento.objects.create(
            numero='101',
            morador=self.user,
        )

        self.driver.get(self.live_server_url + '/')
        login_div = self.driver.find_element(By.CLASS_NAME, 'sign-in')
        username_field = login_div.find_element(By.NAME, 'username')
        password_field = login_div.find_element(By.NAME, 'password')
        username_field.send_keys('userteste')
        password_field.send_keys('User@teste2025')
        login_button = login_div.find_element(By.TAG_NAME, 'button')
        login_button.click()

    def test_clicar_cadastramento_veiculos(self):
        driver = self.driver
        driver.get(self.live_server_url + '/condosync/home/')

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cadastramento-veiculos-link"))
        )

        botao_veiculos = driver.find_element(By.ID, "cadastramento-veiculos-link")
        botao_veiculos.click()

        WebDriverWait(driver, 10).until(
            EC.url_contains('/veiculos')
        )

        assert '/veiculos' in driver.current_url

    def test_adicionar_veiculo(self):
        driver = self.driver
        driver.get(self.live_server_url + '/condosync/veiculos/adicionar_veiculos/')

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
        Veiculo.objects.create(
            tipo_veiculo='Carro',
            placa='ABC1234',
            marca='Ford',
            modelo='Fiesta',
            cor='Azul',
            ano='2020',
            usuario=self.user_normal
        )

        driver = self.driver

        driver.get(self.live_server_url + '/condosync/veiculos/gerenciar_veiculos/')

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//span[text()="Fiesta - ABC1234"]'))
        )

        editar_button = driver.find_element(By.CSS_SELECTOR, '.veiculos-elements a.editar-veiculo')
        editar_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h1'))
        )

        cor_input = driver.find_element(By.NAME, 'cor')
        cor_input.clear()
        cor_input.send_keys('Preto') 

        ano_input = driver.find_element(By.NAME, 'ano')
        ano_input.clear()
        ano_input.send_keys('2022')

        submit_button = driver.find_element(By.TAG_NAME, 'button')
        submit_button.click()

        WebDriverWait(driver, 10).until(
            EC.url_contains('/condosync/veiculos/')
        )

        assert 'condosync/veiculos/' in driver.current_url
    
    def test_gerenciar_e_excluir_veiculo(self):
        Veiculo.objects.create(
            tipo_veiculo='Carro',
            placa='ABC1234',
            marca='Ford',
            modelo='Fiesta',
            cor='Azul',
            ano='2020',
            usuario=self.user_normal
        )

        driver = self.driver

        driver.get(self.live_server_url + '/condosync/veiculos/gerenciar_veiculos/')

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//span[text()="Fiesta - ABC1234"]'))
        )

        excluir_button = driver.find_element(By.CSS_SELECTOR, '.veiculos-elements a.deletar-veiculo')
        excluir_button.click()

        confirmar_exclusao_button = driver.find_element(By.CSS_SELECTOR, '.confirm-box .btn-confirm')
        confirmar_exclusao_button.click()

        WebDriverWait(driver, 10).until(
            EC.url_contains('/condosync/veiculos/')
        )

        assert 'condosync/veiculos/' in driver.current_url

@pytest.mark.django_db
class TestOcorrencias(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        self.user = User.objects.create_user(
            username='userteste',
            email='user@example.com',
            password='User@teste2025',
        )

        self.user_admin = User.objects.create_superuser(
            username='adminteste',
            email='admin@example.com',
            password='Admin@teste2025',
        )

        self.apartamento = Apartamento.objects.create(
            numero='202',
            morador=self.user,
        )

    def test_clicar_ocorrencias(self):
        self.driver.get(self.live_server_url + '/')
        login_div = self.driver.find_element(By.CLASS_NAME, 'sign-in')
        username_field = login_div.find_element(By.NAME, 'username')
        password_field = login_div.find_element(By.NAME, 'password')
        username_field.send_keys('userteste')
        password_field.send_keys('User@teste2025')
        login_button = login_div.find_element(By.TAG_NAME, 'button')
        login_button.click()

        driver = self.driver

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "menu-ocorrencias"))
        )

        ocorrencias_link = driver.find_element(By.ID, 'menu-ocorrencias')
        ocorrencias_link.click()

        assert 'condosync/ocorrencias/' in driver.current_url

    def test_criar_ocorrencia(self):
        self.driver.get(self.live_server_url + '/')
        login_div = self.driver.find_element(By.CLASS_NAME, 'sign-in')
        username_field = login_div.find_element(By.NAME, 'username')
        password_field = login_div.find_element(By.NAME, 'password')
        username_field.send_keys('userteste')
        password_field.send_keys('User@teste2025')
        login_button = login_div.find_element(By.TAG_NAME, 'button')
        login_button.click()

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

        assert 'condosync/ocorrencias' in driver.current_url
        assert 'Teste de Ocorrência' in driver.page_source

    def test_editar_ocorrencia(self):
        Ocorrencia.objects.create(
            titulo='Ocorrência Inicial',
            desc='Descrição inicial.',
            usuario=self.user,
            status='pendente'
        )

        self.driver.get(self.live_server_url + '/')
        login_div = self.driver.find_element(By.CLASS_NAME, 'sign-in')
        username_field = login_div.find_element(By.NAME, 'username')
        password_field = login_div.find_element(By.NAME, 'password')
        username_field.send_keys('userteste')
        password_field.send_keys('User@teste2025')
        login_button = login_div.find_element(By.TAG_NAME, 'button')
        login_button.click()
        driver = self.driver

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "menu-ocorrencias"))
        )
        driver.find_element(By.ID, 'menu-ocorrencias').click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[text()='OCORRÊNCIAS']"))
        )

        edit_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".box-main-ocorrencias .box-main-avisos .text h2 a i.bx.bx-pencil"))
        )

        edit_button = edit_icon.find_element(By.XPATH, "./..")
        edit_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Editar Ocorrência')]"))
        )

        titulo_input = driver.find_element(By.ID, 'titulo')
        descricao_input = driver.find_element(By.ID, 'desc')

        titulo_input.clear()
        titulo_input.send_keys('Ocorrência Editada')
        descricao_input.clear()
        descricao_input.send_keys('Descrição atualizada para teste.')

        submit_button = driver.find_element(By.XPATH, "//button[text()='Salvar Alterações']")
        submit_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[text()='OCORRÊNCIAS']"))
        )

        page_source = driver.page_source
        assert 'Ocorrência Editada' in page_source
        assert 'Descrição atualizada para teste.' in page_source

    def test_excluir_ocorrencia(self):
        Ocorrencia.objects.create(
            titulo='Ocorrência Inicial',
            desc='Descrição inicial.',
            usuario=self.user,
            status='pendente'
        )

        self.driver.get(self.live_server_url + '/')
        login_div = self.driver.find_element(By.CLASS_NAME, 'sign-in')
        username_field = login_div.find_element(By.NAME, 'username')
        password_field = login_div.find_element(By.NAME, 'password')
        username_field.send_keys('userteste')
        password_field.send_keys('User@teste2025')
        login_button = login_div.find_element(By.TAG_NAME, 'button')
        login_button.click()

        driver = self.driver

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "menu-ocorrencias"))
        )
        driver.find_element(By.ID, 'menu-ocorrencias').click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[text()='OCORRÊNCIAS']"))
        )

        delete_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".box-main-ocorrencias .box-main-avisos .text h2 a i.bx.bx-x"))
        )
        delete_button = delete_icon.find_element(By.XPATH, "./..")
        delete_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "confirm-box"))
        )
        confirm_button = driver.find_element(By.XPATH, "//button[text()='Sim, excluir']")
        confirm_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[text()='OCORRÊNCIAS']"))
        )

        page_source = driver.page_source
        assert 'Título da Ocorrência' not in page_source

    def test_editar_status_ocorrencia(self):
        Ocorrencia.objects.create(
            titulo='Ocorrência Inicial',
            desc='Descrição inicial.',
            usuario=self.user_admin,
            status='pendente'
        )

        self.driver.get(self.live_server_url + '/')
        login_div = self.driver.find_element(By.CLASS_NAME, 'sign-in')
        username_field = login_div.find_element(By.NAME, 'username')
        password_field = login_div.find_element(By.NAME, 'password')
        username_field.send_keys('adminteste')
        password_field.send_keys('Admin@teste2025')
        login_button = login_div.find_element(By.TAG_NAME, 'button')
        login_button.click()

        driver = self.driver

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "menu-ocorrencias"))
        )
        driver.find_element(By.ID, 'menu-ocorrencias').click()

        status_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'status'))
        )
        status_select.click()

        status_select.find_element(By.XPATH, "//option[@value='resolvido']").click()

        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'btn-salvar-status'))
        )
        save_button.click()

        status_select_after = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'status'))
        )
        selected_option = status_select_after.find_element(By.XPATH, ".//option[@selected]")

        assert selected_option.get_attribute("value") == "resolvido"

@pytest.mark.django_db
class TestBoletos(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='adminteste',
            email='admin@example.com',
            password='Admin@teste2025',
        )

        self.user_normal = User.objects.create_user(
            username='userteste',
            email='user@gmail.com',
            password='User@teste2025',
        )

        self.apartamento = Apartamento.objects.create(
            numero='Sindico',
            morador=self.user,
        )

        self.apartamento_normal = Apartamento.objects.create(
            numero='102',
            morador=self.user_normal,
        )
        
    def test_cadastrar_boleto(self):
        self.driver.get(self.live_server_url + '/')
        login_div = self.driver.find_element(By.CLASS_NAME, 'sign-in')
        login_div.find_element(By.NAME, 'username').send_keys('adminteste')
        login_div.find_element(By.NAME, 'password').send_keys('Admin@teste2025')
        login_div.find_element(By.TAG_NAME, 'button').click()

        driver = self.driver

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'menu-boletos'))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'form'))
        )

        apartamento_select = driver.find_element(By.NAME, 'apartamento')
        apartamento_select.click()
        apartamento_select.find_element(By.XPATH, '//option[not(@disabled)]').click()

        mes_select = driver.find_element(By.NAME, 'mes_referencia')
        mes_select.click()
        mes_select.find_element(By.XPATH, '//option[@value="Abril"]').click()

        upload_input = driver.find_element(By.NAME, 'arquivo')
        caminho_relativo = 'condosync/static/condosync/documentos/REGIMENTO INTERNO CONDOSYNC-2.pdf'
        caminho_absoluto = os.path.abspath(caminho_relativo)
        upload_input.send_keys(caminho_absoluto)

        driver.find_element(By.CSS_SELECTOR, 'form button[type="submit"]').click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'message-success'))
        )

    def test_download_boleto(self):
        caminho_relativo = 'condosync/static/condosync/documentos/REGIMENTO INTERNO CONDOSYNC-2.pdf'
        caminho_absoluto = os.path.abspath(caminho_relativo)

        with open(caminho_absoluto, 'rb') as f:
            arquivo_simulado = SimpleUploadedFile(
                name='REGIMENTO INTERNO CONDOSYNC-2.pdf',
                content=f.read(),
                content_type='application/pdf'
            )

        Boleto.objects.create(
            apartamentos=self.apartamento_normal,
            mes_referencia="Abril",
            arquivo=arquivo_simulado
        )

        self.driver.get(self.live_server_url + '/')
        login_div = self.driver.find_element(By.CLASS_NAME, 'sign-in')
        login_div.find_element(By.NAME, 'username').send_keys('userteste')
        login_div.find_element(By.NAME, 'password').send_keys('User@teste2025')
        login_div.find_element(By.TAG_NAME, 'button').click()

        driver = self.driver

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'menu-boletos'))
        ).click()

        download_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'btn-download'))
        )
        download_button.click()

        time.sleep(5)

        assert 'boletos' in self.driver.current_url.lower()
    
class VoceSabiaTest(StaticLiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

        self.user = User.objects.create_superuser(
            username='adminteste',
            email='admin@example.com',
            password='Admin@teste2025',
        )

        self.user_normal = User.objects.create_user(
            username='userteste',
            email='user@gmail.com',
            password='User@teste2025',
        )

        self.apartamento = Apartamento.objects.create(
            numero='Sindico',
            morador=self.user,
        )

        self.apartamento_normal = Apartamento.objects.create(
            numero='102',
            morador=self.user_normal,
        )

        self.driver.get('http://127.0.0.1:8000/')
        login_div = self.driver.find_element(By.CLASS_NAME, 'sign-in')
        username_field = login_div.find_element(By.NAME, 'username')
        password_field = login_div.find_element(By.NAME, 'password')
        username_field.send_keys('adminteste')
        password_field.send_keys('Admin@teste2025')
        login_button = login_div.find_element(By.TAG_NAME, 'button')
        login_button.click()

    def test_editar_vocesabia(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.box-main a'))
        ).click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'titulo_1'))
        )

        self.driver.find_element(By.ID, 'titulo_1').clear()
        self.driver.find_element(By.ID, 'titulo_1').send_keys('Novo Título 1 de Teste')

        self.driver.find_element(By.ID, 'conteudo_1').clear()
        self.driver.find_element(By.ID, 'conteudo_1').send_keys('Novo Conteúdo 1 para o teste automatizado.')

        self.driver.find_element(By.ID, 'titulo_2').clear()
        self.driver.find_element(By.ID, 'titulo_2').send_keys('Novo Título 2 de Teste')

        self.driver.find_element(By.ID, 'conteudo_2').clear()
        self.driver.find_element(By.ID, 'conteudo_2').send_keys('Novo Conteúdo 2 para o teste automatizado.')

        self.driver.find_element(By.CSS_SELECTOR, 'form button[type="submit"]').click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'box-main'))
        )

        box_main = self.driver.find_element(By.CLASS_NAME, 'box-main')
        textos = box_main.find_elements(By.CLASS_NAME, 'text')

        assert 'Novo Título 1 de Teste' in textos[0].text
        assert 'Novo Conteúdo 1 para o teste automatizado.' in textos[0].text
        assert 'Novo Título 2 de Teste' in textos[1].text
        assert 'Novo Conteúdo 2 para o teste automatizado.' in textos[1].text

        print("✅ Teste de edição do 'Você sabia...?' executado com sucesso!")

    def tearDown(self):
        self.driver.quit()

@pytest.mark.django_db
class TestCadastro(StaticLiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

        self.apartamento = Apartamento.objects.create(
            numero='101',
            morador=None,
        )

    def tearDown(self):
        self.driver.quit()

    def test_cadastro_user(self):
        self.driver.get(self.live_server_url + '/') 
        time.sleep(1)

        self.driver.find_element(By.ID, 'register').click()
        time.sleep(1)

        self.driver.find_element(By.NAME, 'first_name').send_keys('user')
        self.driver.find_element(By.NAME, 'last_name').send_keys('teste')
        self.driver.find_element(By.NAME, 'username').send_keys('userteste')
        self.driver.find_element(By.NAME, 'email').send_keys('userteste@gmail.com')
        self.driver.find_element(By.NAME, 'password').send_keys('User@teste2025')
        self.driver.find_element(By.NAME, 'confirm_password').send_keys('User@teste2025')

        self.driver.find_element(By.NAME, 'apartamento').click()
        self.driver.find_element(By.XPATH, '//option[not(@disabled)]').click()

        self.driver.find_element(By.NAME, 'usuario').click()

        self.driver.find_element(By.TAG_NAME, 'button').click()
        time.sleep(1)

        assert '/' in self.driver.current_url

    def test_cadastro_admin(self):
        self.driver.get(self.live_server_url + '/') 
        time.sleep(1)

        self.driver.find_element(By.ID, 'register').click()
        time.sleep(1)

        self.driver.find_element(By.NAME, 'first_name').send_keys('admin')
        self.driver.find_element(By.NAME, 'last_name').send_keys('teste')
        self.driver.find_element(By.NAME, 'username').send_keys('adminteste')
        self.driver.find_element(By.NAME, 'email').send_keys('adminteste@gmail.com')
        self.driver.find_element(By.NAME, 'password').send_keys('Admin@teste2025')
        self.driver.find_element(By.NAME, 'confirm_password').send_keys('Admin@teste2025')

        self.driver.find_element(By.NAME, 'apartamento').click()
        self.driver.find_element(By.XPATH, '//option[not(@disabled)]').click()

        self.driver.find_element(By.NAME, 'admin').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'admin_password').send_keys('senha')

        self.driver.find_element(By.TAG_NAME, 'button').click()
        time.sleep(1)

        assert '/' in self.driver.current_url

class TestLogin(StaticLiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

        self.admin = User.objects.create_superuser(
            username="adminteste",
            email="adminteste@gmail.com",
            password="Admin@teste2025"
        )

        self.user = User.objects.create_user(
            username="userteste",
            email="userteste@gmail.com",
            password="User@teste2025"
        )

        Apartamento.objects.create(numero="101", morador=self.admin)
        Apartamento.objects.create(numero="102", morador=self.user)

    def tearDown(self):
        self.driver.quit()

    def test_login_user(self):
        self.driver.get(self.live_server_url + '/')

        time.sleep(1)

        login_div = self.driver.find_element(By.CLASS_NAME, 'sign-in')
        username_field = login_div.find_element(By.NAME, 'username')
        password_field = login_div.find_element(By.NAME, 'password')

        username_field.send_keys('userteste') 
        password_field.send_keys('User@teste2025')

        login_button = login_div.find_element(By.TAG_NAME, 'button')
        login_button.click()

        time.sleep(1)
        print("URL atual (usuário):", self.driver.current_url)

        assert 'condosync/home/' in self.driver.current_url

    def test_login_admin(self):
        self.driver.get(self.live_server_url + '/')

        time.sleep(1)

        login_div = self.driver.find_element(By.CLASS_NAME, 'sign-in')
        username_field = login_div.find_element(By.NAME, 'username')
        password_field = login_div.find_element(By.NAME, 'password')

        username_field.send_keys('adminteste') 
        password_field.send_keys('Admin@teste2025')

        login_button = login_div.find_element(By.TAG_NAME, 'button')
        login_button.click()

        time.sleep(1)
        print("URL atual (admin):", self.driver.current_url)

        assert 'condosync/home/' in self.driver.current_url