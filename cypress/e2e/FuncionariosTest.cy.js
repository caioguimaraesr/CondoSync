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

Cypress.Commands.add('deleteAllFuncionarios', () => {
  cy.exec('python delete_funcionario.py', { failOnNonZeroExit: false });
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

describe('Aba de funcionarios', () => {
    beforeEach(() => {
        cy.deleteAllFuncionarios();
        cy.deleteAllApartamentos();
        cy.createApartamentos();

        cy.visit('/');
        cy.get('#register').click();
        cy.createSuperUser('Test', 'User','testuser', 'testuser@example.com', 'password123', 'password123', 'senha');
        cy.login('testuser', 'password123');
    });

    it('Cadastrar Funcionario', () => {
        cy.get('#menu-funcionarios > h3').click()
        cy.get('.btn-adicionar-container > .btn').click();
        cy.get('#id_nome').type('Funcionario Teste')
        cy.get('#id_cargo').type('Cargo Teste')
        cy.get('.btn-salvar').click()
    });

    it('Editar Funcionario', () => {
        cy.get('#menu-funcionarios > h3').click()
        cy.get('.btn-adicionar-container > .btn').click();
        cy.get('#id_nome').type('Funcionario Teste')
        cy.get('#id_cargo').type('Cargo Teste')
        cy.get('.btn-salvar').click()

        cy.get(':nth-child(1) > .info-funcionario > .botoes-funcionario > .editar').click();
        cy.get('#id_nome').clear().type('Alterando Funcionario Teste')
        cy.get('#id_cargo').clear().type('Alterando Cargo Teste')
        cy.get('.btn-salvar').click();
    });

    it('Deletar Funcionario', () => {
        cy.get('#menu-funcionarios > h3').click()
        cy.get('.btn-adicionar-container > .btn').click();
        cy.get('#id_nome').type('Funcionario Teste')
        cy.get('#id_cargo').type('Cargo Teste')
        cy.get('.btn-salvar').click()

        cy.get(':nth-child(1) > .info-funcionario > .botoes-funcionario > .excluir').click();
        cy.get('.btn-confirm').click()
    });

    afterEach(() => {
      cy.deleteAllApartamentos();
      cy.deleteAllUsers();
      cy.deleteAllFuncionarios()
    });
});