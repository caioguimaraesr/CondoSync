Cypress.Commands.add('createApartamentos', () => {
  cy.exec('python create_apartamento.py', { failOnNonZeroExit: false });
});

Cypress.Commands.add('deleteAllApartamentos', () => {
  cy.exec('python delete_apartamento.py', { failOnNonZeroExit: false });
});

Cypress.Commands.add('deleteAllUsers', () => {
  cy.exec('python delete_users.py', { failOnNonZeroExit: false });
});

Cypress.Commands.add('deleteAllSugestoes', () => {
  cy.exec('python delete_sugestoes.py', { failOnNonZeroExit: false });
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
        cy.deleteAllSugestoes();

        cy.visit('/');
        cy.get('#register').click();
        cy.createUser('Test', 'User','testuser', 'testuser@example.com', 'password123', 'password123');
        cy.login('testuser', 'password123');
    });

    it('Adicionar sugestão', () => {
        cy.get('#sugestoes-melhoria-link > h1').click();
        cy.get('.btn-adicionar-aviso').click();
        cy.get('#titulo').type('Título sugestão teste');
        cy.get('#descricao').type('Descrição sugestão teste');
        cy.get('.btn-submit').click();
    });

    it('Deletar sugestão', () => {
        cy.get('#sugestoes-melhoria-link > h1').click();
        cy.get('.btn-adicionar-aviso').click();
        cy.get('#titulo').type('Título sugestão teste');
        cy.get('#descricao').type('Descrição sugestão teste');
        cy.get('.btn-submit').click();

        cy.get('.text .bx.bx-pencil').click();
        cy.get('#titulo').clear().type('Alterando Título sugestão teste');
        cy.get('#descricao').clear().type('Alterando Descrição sugestão teste');
        cy.get('.btn-submit').click()    
    });
    
    it('Excluir sugestão', () => {
        cy.get('#sugestoes-melhoria-link > h1').click();
        cy.get('.btn-adicionar-aviso').click();
        cy.get('#titulo').type('Título sugestão teste');
        cy.get('#descricao').type('Descrição sugestão teste');
        cy.get('.btn-submit').click();

        cy.get('.text .bx.bx-x').click();
        cy.get('.btn-confirm').click()    
    });

    afterEach(() => {
      cy.deleteAllApartamentos();
      cy.deleteAllUsers();
      cy.deleteAllSugestoes();
    });
});