# Baozi Store API - UNINTER

Trabalho de Desenvolvimento Web Back-End  
Centro Universitário Internacional UNINTER  
**Aluno:** Murilo Bauermann Cremm Domingues Ferreira  
**RU:** 4425054  
**Professora:** Luciane Kanashiro, Me.

---

## 📌 Descrição do Projeto
A **Baozi Store API** é uma API REST desenvolvida em Java com Spring Boot para gerenciamento e controle básico de clientes, produtos e pedidos de uma loja especializada na venda de pãezinhos chineses (*baozi*).

A aplicação segue a arquitetura em camadas MVC do Spring:
- **`model`**: Definição das entidades JPA (`Cliente`, `Produto`, `Pedido`).
- **`repository`**: Interfaces de acesso a dados com Spring Data JPA (`JpaRepository`).
- **`controller`**: Controladores REST com endpoints para operações CRUD completas retornando respostas em formato JSON.

---

## 🛠️ Tecnologias Utilizadas
- **Java 17** (ou superior)
- **Spring Boot 3.2.5**
  - Spring Web
  - Spring Data JPA
- **H2 Database** (Banco relacional em memória com console web integrado) / Suporte a **MySQL**
- **Maven** para gerenciamento de dependências
- **Postman** para testes de endpoints

---

## 🚀 Como Executar a Aplicação

### Pré-requisitos
- JDK 17 instalado e configurado no PATH
- Maven instalado (ou executando via IDE como IntelliJ IDEA, Eclipse ou VS Code)

### Execução via Linha de Comando (Maven)
No diretório raiz do projeto:
```bash
mvn spring-boot:run
```

A aplicação estará disponível em: `http://localhost:8080`

### Console do Banco H2
Para visualizar as tabelas e dados gravados no banco relacional H2, acesse pelo navegador:
- **URL:** [http://localhost:8080/h2-console](http://localhost:8080/h2-console)
- **JDBC URL:** `jdbc:h2:mem:baozidb`
- **User Name:** `sa`
- **Password:** *(deixe em branco)*

---

## 📡 Endpoints da API

### 1. Clientes (`/clientes`)
- `POST /clientes` - Cadastrar novo cliente
- `GET /clientes` - Listar todos os clientes
- `GET /clientes/{id}` - Buscar cliente por ID
- `PUT /clientes/{id}` - Atualizar cliente por ID
- `DELETE /clientes/{id}` - Remover cliente por ID

### 2. Produtos (`/produtos`)
- `POST /produtos` - Cadastrar novo produto
- `GET /produtos` - Listar todos os produtos
- `GET /produtos/{id}` - Buscar produto por ID
- `PUT /produtos/{id}` - Atualizar produto por ID
- `DELETE /produtos/{id}` - Remover produto por ID

### 3. Pedidos (`/pedidos`)
- `POST /pedidos` - Registrar novo pedido
- `GET /pedidos` - Listar todos os pedidos
- `GET /pedidos/{id}` - Buscar pedido por ID
- `PUT /pedidos/{id}` - Atualizar pedido por ID
- `DELETE /pedidos/{id}` - Remover pedido por ID

---

## 🧪 Testes no Postman
O arquivo `BaoziStore_Postman_Collection.json` está disponível na raiz do repositório. Para utilizá-lo:
1. Abra o Postman.
2. Clique no botão **Import**.
3. Selecione o arquivo `BaoziStore_Postman_Collection.json`.
4. Todas as requisições (POST, GET geral, GET por ID e DELETE) já estarão prontas com os dados da atividade prática.

