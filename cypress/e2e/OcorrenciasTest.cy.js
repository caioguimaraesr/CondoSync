Cypress.Commands.add('createApartamentos', () => {
  cy.exec('python create_apartamento.py', { failOnNonZeroExit: false });
});

Cypress.Commands.add('deleteAllApartamentos', () => {
  cy.exec('python delete_apartamento.py', { failOnNonZeroExit: false });
});

Cypress.Commands.add('deleteAllUsers', () => {
  cy.exec('python delete_users.py', { failOnNonZeroExit: false });
});

Cypress.Commands.add('deleteAllEncomendas', () => {
  cy.exec('python delete_encomendas.py', { failOnNonZeroExit: false });
});

Cypress.Commands.add('deleteAllOcorrencias', () => {
  cy.exec('python delete_ocorrencias.py', { failOnNonZeroExit: false });
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

describe('Ocorrencias', () => {
    beforeEach(() => {
        cy.deleteAllApartamentos();
        cy.createApartamentos();
        cy.deleteAllOcorrencias();

        cy.visit('/');
        cy.get('#register').click();
        cy.createUser('Test', 'User','testuser', 'testuser@example.com', 'password123', 'password123');
        cy.login('testuser', 'password123');
    });

    it('Adicionar uma ocorrencia', () => {
        cy.get('#menu-ocorrencias > h3').click();
        cy.get('.btn-adicionar-aviso').click();
        cy.get('#titulo').type('Titulo Ocorrencia Teste');
        cy.get('#desc').type('Descrição Ocorrência Teste');
        cy.get('form > button').click();
    });

    it('Editar uma ocorrencia', () => {
        cy.get('#menu-ocorrencias > h3').click();
        cy.get('.btn-adicionar-aviso').click();
        cy.get('#titulo').type('Titulo Ocorrencia Teste');
        cy.get('#desc').type('Descrição Ocorrência Teste');
        cy.get('form > button').click();

        cy.get('.text .bx.bx-pencil').click();
        cy.get('#titulo').clear().type('Alterando Titulo Ocorrencia Teste');
        cy.get('#desc').clear().type('Alterando Descrição Ocorrência Teste');
        cy.get('form > button').click();
    });

    it('Delete uma ocorrencia', () => {
        cy.get('#menu-ocorrencias > h3').click();
        cy.get('.btn-adicionar-aviso').click();
        cy.get('#titulo').type('Titulo Ocorrencia Teste');
        cy.get('#desc').type('Descrição Ocorrência Teste');
        cy.get('form > button').click();

        cy.get('.text .bx.bx-x').click();
        cy.get('.btn-confirm').click();
    });

    afterEach(() => {
      cy.deleteAllOcorrencias();
      cy.deleteAllApartamentos();
      cy.deleteAllUsers();
    });
});