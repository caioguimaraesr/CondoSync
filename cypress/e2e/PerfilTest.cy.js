Cypress.Commands.add('createApartamentos', () => {
  cy.exec('python create_apartamento.py', { failOnNonZeroExit: false });
});

Cypress.Commands.add('deleteAllApartamentos', () => {
  cy.exec('python delete_apartamento.py', { failOnNonZeroExit: false });
});

Cypress.Commands.add('createAreasComuns', () => {
  cy.exec('python create_area.py', { failOnNonZeroExit: false });
});

Cypress.Commands.add('deleteAllAreasComuns', () => {
  cy.exec('python delete_area.py', { failOnNonZeroExit: false });
});

Cypress.Commands.add('deleteAllUsers', () => {
  cy.exec('python delete_users.py', { failOnNonZeroExit: false });
});

Cypress.Commands.add('deleteAllHorarios', () => {
  cy.exec('python delete_horario.py', { failOnNonZeroExit: false });
});

Cypress.Commands.add('createHorarios', () => {
  cy.exec('python create_horario.py', { failOnNonZeroExit: false });
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

describe('Aba de perfil', () => {
    beforeEach(() => {
        cy.deleteAllApartamentos();
        cy.createApartamentos();

        cy.visit('/');
        cy.get('#register').click();
        cy.createUser('Test', 'User','testuser', 'testuser@example.com', 'password123', 'password123');
        cy.login('testuser', 'password123');
    });

    it('Configurando o perfil', () => {
        cy.get('.profile-photo > img').click();
        cy.get('h1 > .bx').click();
        cy.get('#id_telefone').type('81998253482');
        cy.get('#id_instagram').type('cesarschool');
        cy.get('#id_bio').type('Olá, nos somos os integrantes do condosync e estamos desenvolvendo esse site para a cadeira de FDS. ')
        cy.get(':nth-child(1) > label > input').check();
        cy.get(':nth-child(2) > label > input').check();
        cy.get('.salvar').click();
        cy.get('.cancelar').click();
        cy.reload(true);
    });

    afterEach(() => {
      cy.deleteAllApartamentos();
      cy.deleteAllUsers();
    });
});