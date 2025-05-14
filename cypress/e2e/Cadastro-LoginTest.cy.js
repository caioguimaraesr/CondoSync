describe('Teste de Cadastro e Login', () => {
  const user = {
    username: 'admin',
    password: '123'
  };

  const cadastrar = {
    first_name: 'carlos',
    last_name: 'roberto',
    username: 'carlosdasilva',
    email: 'carlosdasilva@gmail.com',
    password: '123'
  }

  it('Logar com o usuário', () => {
    cy.visit('/');
    cy.get('form > [type="text"]').type(user.username)
    cy.get('form > [type="password"]').type(user.password)
    cy.get('.sign-in > form > button').click()
  });

  it('Cadastrar um novo usuário', () => {
    cy.visit('/');
    cy.get('#register').click()
    cy.get('[name="first_name"]').type(cadastrar.first_name)
    cy.get('[name="last_name"]').type(cadastrar.last_name)
    cy.get(':nth-child(5) > [type="text"]').type(cadastrar.username)
    cy.get('[type="email"]').type(cadastrar.email)
    cy.get(':nth-child(6) > [name="password"]').type(cadastrar.password)
    cy.get('[name="confirm_password"]').type(cadastrar.password)
    cy.get('select[name="apartamento"]').select('Apartamento 104');
    cy.get('#usuario').check()
    cy.get('.sign-up > form > button').click()
  })
});
