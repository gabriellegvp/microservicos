# Microserviços com FastAPI e RabbitMQ

Uma arquitetura de microserviços dividida em serviços independentes para gerenciamento de usuários, produtos e pedidos, utilizando **FastAPI** para a construção das APIs e **RabbitMQ** para comunicação assíncrona entre os serviços.

---

## Tecnologias Utilizadas

- **FastAPI**: Framework moderno e rápido (baseado em Python) para construção de APIs RESTful.
- **RabbitMQ**: Sistema de mensageria para comunicação assíncrona entre os microserviços.
- **Docker**: Para conteinerização dos serviços e dependências.
- **Docker Compose**: Para orquestração dos contêineres.
- **Pydantic**: Para validação de dados e serialização.
- **Uvicorn**: Servidor ASGI para rodar a aplicação FastAPI.
- **Python 3.9**: Linguagem de programação utilizada para desenvolver os microserviços.

---

## Arquitetura do Sistema

O sistema é composto por três microserviços principais:

1. **Usuários** (`users_service`):
   - Gerencia a criação e listagem de usuários.

2. **Produtos** (`products_service`):
   - Gerencia o inventário de produtos.

3. **Pedidos** (`orders_service`):
   - Processa pedidos e se comunica com os serviços de usuários e produtos via RabbitMQ.

A comunicação entre os serviços é feita através do **RabbitMQ**, garantindo que os pedidos sejam processados de forma assíncrona e confiável.

---

## Como Configurar

### Pré-requisitos

- Docker e Docker Compose instalados.
- Git (para clonar o repositório).