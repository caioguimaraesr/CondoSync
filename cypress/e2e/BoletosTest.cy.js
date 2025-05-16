Cypress.Commands.add('createApartamentos', () => {
  cy.exec('python create_apartamento.py', { failOnNonZeroExit: false });
});

Cypress.Commands.add('deleteAllApartamentos', () => {
  cy.exec('python delete_apartamento.py', { failOnNonZeroExit: false });
});

Cypress.Commands.add('deleteAllUsers', () => {
  cy.exec('python delete_users.py', { failOnNonZeroExit: false });
});

Cypress.Commands.add('deleteAllBoletos', () => {
  cy.exec('python delete_boletos.py', { failOnNonZeroExit: false });
});

Cypress.Commands.add('createBoletos', () => {
  cy.exec('python create_boleto.py', { failOnNonZeroExit: false });
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

Cypress.Commands.add('createSuperUser', (first_name, last_name, username, email, password, confirm_password, senha_admin) => {
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
    cy.get('#admin_password').type(senha_admin);
    cy.get('.sign-up > form > button').click();
});

describe('Aba de boeltos', () => {
    beforeEach(() => {
        cy.deleteAllApartamentos();
        cy.deleteAllUsers();
        cy.deleteAllBoletos();
        cy.createApartamentos();
        cy.createBoletos();
    });
    
    it('Baixar Boleto', () => {
        cy.visit('/');
        cy.get('#register').click();
        cy.createUser('Test', 'User','testuser', 'testuser@example.com', 'password123', 'password123');
        cy.login('testuser', 'password123');

        cy.get('#menu-boletos > h3').click();
        cy.get('.btn-download').click();
    });

    afterEach(() => {
      cy.deleteAllApartamentos();
      cy.deleteAllBoletos();
      cy.deleteAllUsers();
    });
});