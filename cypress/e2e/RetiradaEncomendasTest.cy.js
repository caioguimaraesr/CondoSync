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

describe('Retirada de Encomenda', () => {
    beforeEach(() => {
        cy.deleteAllApartamentos();
        cy.createApartamentos();
        cy.deleteAllEncomendas();

        cy.visit('/');
        cy.get('#register').click();
        cy.createSuperUser('Test', 'User','testuser', 'testuser@example.com', 'password123', 'password123', 'senha');
        cy.login('testuser', 'password123');
    });

    it('Adicionar uma encomenda', () => {
        cy.get('#retirada-encomendas-link > h1').click();
        cy.get('.btn-adicionar-aviso').click();
        cy.get('#apartamento').select('APTO101:')
        cy.get('#peso_kg').type('2.5');
        cy.get('#origem').type('Mercado Livre');
        cy.get('form > button').click();
    });

    it('Editar uma encomenda', () => {
        cy.get('#retirada-encomendas-link > h1').click();
        cy.get('.btn-adicionar-aviso').click();
        cy.get('#apartamento').select('APTO101:')
        cy.get('#peso_kg').type('2.5');
        cy.get('#origem').type('Mercado Livre');
        cy.get('form > button').click();

        cy.get('.text .bx.bx-pencil').click();
        cy.get('#apartamento').select('APTO102')
        cy.get('#peso_kg').clear().type('5.1');
        cy.get('#origem').clear().type('Amazon');
        cy.get('.form-edit-encomendas > button').click();
    });

    it('Delete uma encomenda', () => {
        cy.get('#retirada-encomendas-link > h1').click();
        cy.get('.btn-adicionar-aviso').click();
        cy.get('#apartamento').select('APTO101:');
        cy.get('#peso_kg').type('2.5');
        cy.get('#origem').type('Mercado Livre');
        cy.get('form > button').click();

        cy.get('.text .bx.bx-x').click();
        cy.get('.btn-confirm').click();
    });

    afterEach(() => {
      cy.deleteAllEncomendas();  
      cy.deleteAllApartamentos();
      cy.deleteAllUsers();
    });
});