# API - GTI Tech Store 

> **Link da API em Produção (Swagger):** [👉 CLIQUE AQUI PARA TESTAR A API](https://gti-tech-api.onrender.com/docs)

API REST desenvolvida como solução para o desafio técnico do Processo Seletivo 2026.1 da **GTI Engenharia Jr**. 

O sistema simula o back-end de um e-commerce (GTI Tech Store), permitindo o gerenciamento completo de pedidos, acompanhamento de status e a geração de um relatório financeiro inteligente com recortes temporais (mensal e anual).

---

## Funcionalidades Principais

Atendendo aos requisitos do escopo principal, a API possui:

* **CRUD Completo de Pedidos:** Criação, Listagem, Busca por ID, Atualização de Status e Exclusão Permanente.
* **Dashboard Financeiro (Apresentação da Empresa):** Rota que calcula dinamicamente o faturamento real (somente pedidos concluídos), quantidade de pedidos pendentes/finalizados e categorização por ticket (Alto, Médio e Baixo), filtrados por Mês e Ano.
* **Tratamento de Dados:** Proteção contra erros de digitação de status utilizando o método `.capitalize()` e suporte a múltiplas grafias ("Concluido" ou "Concluído").
* **Feed de Atualizações:** Rota estática listando as últimas notícias e melhorias do sistema.

---

## Etapas Bônus Implementadas

Além do escopo básico, os seguintes diferenciais foram adicionados ao projeto:

*  **Deploy na Nuvem:** Hospedagem no Render com banco de dados SQLite dedicado.
*  **Documentação Interativa:** Interface Swagger UI gerada nativamente, permitindo testar rotas diretamente pelo navegador.
*  **Paginação:** Implementação de `skip` e `limit` na rota de listagem, protegendo o servidor contra sobrecarga de dados.
*  **Testes Automatizados:** Suíte de testes validando as regras de negócio de criação de pedidos e regras de paginação utilizando **Pytest**.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Framework Web:** FastAPI (alta performance e documentação automática)
* **Banco de Dados:** SQLite (leve e ideal para o deploy sem custos)
* **ORM:** SQLAlchemy (abstração de consultas e segurança contra SQL Injection)
* **Validação de Dados:** Pydantic
* **Testes:** Pytest & HTTPX

---

## 💻 Como rodar o projeto localmente

Se desejar clonar o projeto para testar na sua máquina, siga os passos abaixo:

**1. Clone o repositório:**

```bash
git clone [https://github.com/natanbszx/Desafio-Backend-APIrest-GTIjr.git](https://github.com/natanbszx/Desafio-Backend-APIrest-GTIjr.git)
cd Desafio-Backend-APIrest-GTIjr
```

2. Crie e ative o ambiente virtual:

```bash
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

3. Instale as Dependências:
   
```bash
pip install -r requirements.txt
```

4. Inicie o Servidor Local:
```bash
uvicorn main:app --reload
```

5. Acesse a documentação local:
Abra o navegador em: http://127.0.0.1:8000/docs

Desenvolvido com dedicação por Natanael Batalha para o processo seletivo da GTI Engenharia Jr.

