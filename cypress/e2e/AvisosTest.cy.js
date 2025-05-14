describe('Teste de Cadastro e Login', () => {
  const user = {
    username: 'admin',
    password: '123'
  };

  it('Criar um aviso', () => {
    cy.visit('/');
    cy.get('form > [type="text"]').type(user.username)
    cy.get('form > [type="password"]').type(user.password)
    cy.get('.sign-in > form > button').click()
    
    cy.get('#menu-avisos > h3').click()
    cy.get('.btn-adicionar-aviso').click()
    cy.get('#titulo').type('Titulo Teste')
    cy.get('#conteudo').type('Descrição do Conteúdo')
    cy.get('form > button').click()
  });

  it('Editar um aviso', () => {
    cy.visit('/');
    cy.get('form > [type="text"]').type(user.username)
    cy.get('form > [type="password"]').type(user.password)
    cy.get('.sign-in > form > button').click()

    cy.get('#menu-avisos > h3').click()    
    cy.get('[href="/condosync/avisos/edit/6"] > .bx').click()
    cy.get('#titulo').clear()
    cy.get('#titulo').type('Mudando o titulo Teste')
    cy.get('#conteudo').clear()
    cy.get('#conteudo').type('Mudando a desc do conteudo')
    cy.get('.form-edit-avisos > button').click()
  });

  it('Excluir um aviso', () => {
    cy.visit('/');
    cy.get('form > [type="text"]').type(user.username)
    cy.get('form > [type="password"]').type(user.password)
    cy.get('.sign-in > form > button').click()

    cy.get('#menu-avisos > h3').click()    
    cy.get('[href="/condosync/avisos/delete/6"] > .bx').click()
    cy.get('.btn-confirm').click()
});
});
