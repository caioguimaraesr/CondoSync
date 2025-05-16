Cypress.Commands.add('createApartamentos', () => {
  cy.exec('python create_apartamento.py', { failOnNonZeroExit: false });
});

Cypress.Commands.add('deleteAllApartamentos', () => {
  cy.exec('python delete_apartamento.py', { failOnNonZeroExit: false });
});

Cypress.Commands.add('deleteAllUsers', () => {
  cy.exec('python delete_users.py', { failOnNonZeroExit: false });
});

Cypress.Commands.add('deleteAllVoceSabia', () => {
  cy.exec('python delete_vocesabia.py', { failOnNonZeroExit: false });
});

Cypress.Commands.add('createVoceSabia', () => {
  cy.exec('python create_vocesavia.py', { failOnNonZeroExit: false });
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

describe('Reservar área comum', () => {
    beforeEach(() => {
        cy.deleteAllUsers();
        cy.deleteAllApartamentos();
        cy.createApartamentos();
        cy.deleteAllVoceSabia();
        cy.createVoceSabia();

        cy.visit('/');
        cy.get('#register').click();
        cy.createSuperUser('Test', 'User','testuser', 'testuser@example.com', 'password123', 'password123', 'senha');
        cy.login('testuser', 'password123');
    });

    it('Editar curiosidades', () => {
        cy.get('h1 > a > .bx').click();
        cy.get('#titulo_1').type('Alterando o titulo 1 para teste');
        cy.get('#conteudo_1').type('Alterando o conteudo 1 para teste');
        cy.get('#titulo_2').type('Alterando o titulo 2 para teste');
        cy.get('#conteudo_2').type('Alterando o conteudo 2 para teste');
        cy.get('.form-group button').click()
    });

    afterEach(() => {
      cy.deleteAllApartamentos();
      cy.deleteAllUsers();
      cy.deleteAllVoceSabia();
    });
});