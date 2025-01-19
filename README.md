# Microserviços com FastAPI e RabbitMQ

Uma arquitetura de microserviços dividida em serviços independentes para gerenciamento de usuários, produtos e pedidos, utilizando RabbitMQ para comunicação.

## Serviços
- *Usuários*: Gerenciamento de usuários.
- *Produtos*: Gerenciamento de inventário.
- *Pedidos*: Processamento de pedidos.

## Como Configurar
1. Clone o repositório:  
   git clone <url-do-repositorio>
2. Configure o Docker:  
   docker-compose up
3. Acesse os microserviços nos seguintes endpoints:  
   - Usuários: http://localhost:8001
   - Produtos: http://localhost:8002
   - Pedidos: http://localhost:8003

## Exemplos
- Criar um usuário:  
  POST /users
- Criar um pedido:  
  POST /orders
