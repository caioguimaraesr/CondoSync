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

describe('Aba de Visitantes', () => {
    beforeEach(() => {
        cy.deleteAllApartamentos();
        cy.createApartamentos();

        cy.visit('/');
        cy.get('#register').click();
        cy.createSuperUser('Test', 'User','testuser', 'testuser@example.com', 'password123', 'password123', 'senha');
        cy.login('testuser', 'password123');
    });

    it('Cadastrar Visitante', () => {
        cy.get('#menu-visitantes > h3').click();
        cy.get('[href="/condosync/visitantes/create_visitantes/"]').click();
        cy.get('#id_nome').type('Visitante Teste');
        cy.get('#id_cpf').type('19243276492');
        cy.get('#id_apartamento option').eq(1).then(option => {
            cy.get('#id_apartamento').select(option.val());
        });
        cy.get('.btn-salvar').click();
    });

    it('Editar Visitante', () => {
        cy.get('#menu-visitantes > h3').click();
        cy.get('[href="/condosync/visitantes/create_visitantes/"]').click();
        cy.get('#id_nome').type('Visitante Teste');
        cy.get('#id_cpf').type('19243276492');
        cy.get('#id_apartamento option').eq(1).then(option => {
            cy.get('#id_apartamento').select(option.val());
        });
        cy.get('.btn-salvar').click();

        cy.get('[href="/condosync/visitantes/gerenciar_visitantes/"]').click();
        cy.get('.editar-veiculo').click();
        cy.get('#id_nome').clear().type('Atualizando Visitante');
        cy.get('#id_cpf').clear().type('48120384192')
        cy.get('.btn.btn-salvar').click()
    });

    it('Deletar Visitante', () => {
        cy.get('#menu-visitantes > h3').click();
        cy.get('[href="/condosync/visitantes/create_visitantes/"]').click();
        cy.get('#id_nome').type('Visitante Teste');
        cy.get('#id_cpf').type('19243276492');
        cy.get('#id_apartamento option').eq(1).then(option => {
            cy.get('#id_apartamento').select(option.val());
        });
        cy.get('.btn-salvar').click();

        cy.get('[href="/condosync/visitantes/gerenciar_visitantes/"]').click();
        cy.get('.deletar-veiculo > .bx').click();
        cy.get('.btn-confirm').click();
    });

    afterEach(() => {
      cy.deleteAllApartamentos();
      cy.deleteAllUsers();
    });
});