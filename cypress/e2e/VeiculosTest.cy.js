Cypress.Commands.add('createApartamentos', () => {
  cy.exec('python create_apartamento.py', { failOnNonZeroExit: false });
});

Cypress.Commands.add('deleteAllApartamentos', () => {
  cy.exec('python delete_apartamento.py', { failOnNonZeroExit: false });
});

Cypress.Commands.add('deleteAllUsers', () => {
  cy.exec('python delete_users.py', { failOnNonZeroExit: false });
});

Cypress.Commands.add('login', (username, password) => {
    cy.visit('/');
    cy.get('form > [type="text"]').type(username)
    cy.get('form > [type="password"]').type(password);
    cy.get('.sign-in > form > button').click();
});

Cypress.Commands.add('createUser', (first_name, last_name, username, email, password, confirm_password  ) => {
    cy.visit('/');
    cy.get('#register').click();
    cy.get('[name="first_name"]').type(first_name);
    cy.get('[name="last_name"]').type(last_name);
    cy.get(':nth-child(5) > [type="text"]').type(username);
    cy.get('[type="email"]').type(email);
    cy.get(':nth-child(6) > [name="password"]').type(password);
    cy.get('[name="confirm_password"]').type(confirm_password);
    cy.get('select').select('Apartamento 101');
    cy.get('#usuario').check();
    cy.get('.sign-up > form > button').click();
});

Cypress.Commands.add('createSuperUser', (first_name, last_name, username, email, password, confirm_password  ) => {
    cy.visit('/');
    cy.get('#register').click();
    cy.get('[name="first_name"]').type(first_name);
    cy.get('[name="last_name"]').type(last_name);
    cy.get(':nth-child(5) > [type="text"]').type(username);
    cy.get('[type="email"]').type(email);
    cy.get(':nth-child(6) > [name="password"]').type(password);
    cy.get('[name="confirm_password"]').type(confirm_password);
    cy.get('select').select('Apartamento 101');
    cy.get('#admin').check();
    cy.get('#admin_password').type('senha');
    cy.get('.sign-up > form > button').click();
});

describe('Aba de Veiculos', () => {
    beforeEach(() => {
        cy.deleteAllApartamentos();
        cy.createApartamentos();
    });

    it('Adicionar veículo', () => {
        cy.visit('/');
        cy.get('#register').click();
        cy.createUser('Test', 'User','testuser', 'testuser@example.com', 'password123', 'password123');
        cy.login('testuser', 'password123');

        cy.get('#cadastramento-veiculos-link > h1').click();
        cy.get('[href="/condosync/veiculos/adicionar_veiculos/"]').click();
        cy.get('#tipo_veiculo').select('Carro');
        cy.get('#marca').type('Fiat');
        cy.get('#modelo').type('Argo');
        cy.get('#placa').type('BHZ6S26');
        cy.get('#cor').type('Branco');
        cy.get('#ano').type('2025');
        cy.get('.btn-adicionar').click();
    });
    
    it('Editar veiculos', () => {
        cy.visit('/');
        cy.get('#register').click();
        cy.createUser('Test', 'User','testuser', 'testuser@example.com', 'password123', 'password123');
        cy.login('testuser', 'password123');

        cy.get('#cadastramento-veiculos-link > h1').click();
        cy.get('[href="/condosync/veiculos/adicionar_veiculos/"]').click();
        cy.get('#tipo_veiculo').select('Carro');
        cy.get('#marca').type('Fiat');
        cy.get('#modelo').type('Argo');
        cy.get('#placa').type('BHZ6S26');
        cy.get('#cor').type('Branco');
        cy.get('#ano').type('2025');
        cy.get('.btn-adicionar').click();

        cy.get('[href="/condosync/veiculos/gerenciar_veiculos/"]').click();
        cy.get('.editar-veiculo > .bx').click();
        cy.get('#tipo_veiculo').select('Carro');
        cy.get('#marca').clear().type('Honda');
        cy.get('#modelo').clear().type('Pop 100');
        cy.get('#placa').clear().type('BFQ6S82');
        cy.get('#cor').clear().type('Preto');
        cy.get('#ano').clear().type('2023');
        cy.get('.btn-adicionar').click();
    });

    it('Excluir veiculos', () => {
        cy.visit('/');
        cy.get('#register').click();
        cy.createUser('Test', 'User','testuser', 'testuser@example.com', 'password123', 'password123');
        cy.login('testuser', 'password123');

        cy.get('#cadastramento-veiculos-link > h1').click();
        cy.get('[href="/condosync/veiculos/adicionar_veiculos/"]').click();
        cy.get('#tipo_veiculo').select('Carro');
        cy.get('#marca').type('Fiat');
        cy.get('#modelo').type('Argo');
        cy.get('#placa').type('BHZ6S26');
        cy.get('#cor').type('Branco');
        cy.get('#ano').type('2025');
        cy.get('.btn-adicionar').click();

        cy.get('[href="/condosync/veiculos/gerenciar_veiculos/"]').click()
        cy.get('.deletar-veiculo > .bx').click()
        cy.get('.btn-confirm').click();
    });

    it('Pesquisar veiculos', () => {
        cy.visit('/');
        cy.get('#register').click();
        cy.createUser('Test', 'User','testuser', 'testuser@example.com', 'password123', 'password123');
        cy.login('testuser', 'password123');

        cy.get('#cadastramento-veiculos-link > h1').click();
        cy.get('[href="/condosync/veiculos/adicionar_veiculos/"]').click();
        cy.get('#tipo_veiculo').select('Carro');
        cy.get('#marca').type('Fiat');
        cy.get('#modelo').type('Argo');
        cy.get('#placa').type('BHZ6S26');
        cy.get('#cor').type('Branco');
        cy.get('#ano').type('2025');
        cy.get('.btn-adicionar').click();

        cy.get('#menu-logout > h3').click();
        
        cy.visit('/');
        cy.get('#register').click();
        cy.visit('/');
        cy.get('#register').click();
        cy.get('[name="first_name"]').type('fist_name');
        cy.get('[name="last_name"]').type('last_name');
        cy.get(':nth-child(5) > [type="text"]').type('username');
        cy.get('[type="email"]').type('email@email.com');
        cy.get(':nth-child(6) > [name="password"]').type('password');
        cy.get('[name="confirm_password"]').type('password');
        cy.get('select').select('Apartamento 102');
        cy.get('#admin').check();
        cy.get('#admin_password').type('senha');
        cy.get('.sign-up > form > button').click();
        cy.login('username', 'password');

        cy.get('#cadastramento-veiculos-link > h1').click();
        cy.get('.form-pesquisa > form > input').type('Nissan');
        cy.get('form > button').click();
        cy.get('.form-pesquisa > form > input').clear().type('Argo');
        cy.get('form > button').click();
    });

    afterEach(() => {
      cy.deleteAllApartamentos();
      cy.deleteAllUsers();
    });
});