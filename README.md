# Despysas-Flask
**Autores:** Mateus Costa Ribeiro, Clara Padilha, Marco Antonio Nitsche

## Introdução
Este projeto foi desenvolvido durante o ano, para a matéria de Projeto Integrador, ministrada pelo Professor Mestre Odair Moreira de Souza, no Instituto Federal do Paraná, Campu Cascavel.
Ele se trata de um site para controle de despesas e ganhos, no qual o usuário pode cadastrar essas informações e serão gerados gráficos e tabelas para que ele posso verificar essas informações. 
Além disso, há uma seção "Investimentos", onde por meio da consulta da API [Brapi](https://brapi.dev/), obtem-se informações da bolsa de valores e estima-se um possível lucro em alguma ação selecionada.

## Tecnologias
Para o desenvolvimento deste site, utilizou-se o framework Flask, da linguagem Python, para a implementação geral. Para armazenar os dados utiliza-se um banco SQLite, mantido junto da própria aplicação.

## Como Utilizar
Para baixar, instalar e executar a aplicação, siga a seguinte passo a passo:
- ```python
  git clone https://github.com/M-C-Ribeiro/Despysas-Flask
- ```python
  cd Despysas-Flask
- ```python
  pip install -r requirements.txt
- ```python
  flask --app despysas run --debug
