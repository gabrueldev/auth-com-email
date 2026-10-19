# Auth com Email

### Cadastro com confirmação por email, do jeito que os sites grandes fazem

API em **FastAPI** de cadastro e login onde a conta só é criada depois que o usuário confirma o email. No cadastro, a API manda um código de 6 dígitos para o email informado; com o código certo, o usuário é criado e já pode logar e receber seu **JWT**.

## Como funciona

```
POST /user/cadaster/          → recebe nome, email e senha e envia o código por email
POST /user/cadaster/reenviar  → gera e envia um código novo
POST /user/verify/            → confere o código e cria a conta
POST /user/login/             → devolve o access_token (JWT)
GET  /user/me/                → rota protegida, devolve os dados do usuário logado
```

Até confirmar o código, o cadastro fica numa tabela separada (`pending_users`). Só depois da confirmação ele vai para `users`, então nenhum email falso vira conta.

## Segurança

+ Senhas com hash **Argon2**
+ Códigos gerados com `secrets` (aleatoriedade criptográfica) e salvos como hash, nunca em texto puro
+ Código expira em **5 minutos** e trava depois de **5 tentativas erradas**, contra força bruta
+ Email duplicado é recusado (`409`)
+ Erro de login genérico, para não revelar quais emails estão cadastrados
+ O envio de email não é uma rota pública: só o próprio cadastro dispara

## Tecnologias

+ Python 3.12+
+ FastAPI
+ SQLAlchemy + PostgreSQL
+ FastAPI-Mail (SMTP)
+ JWT com python-jose
+ Passlib + Argon2
+ Docker Compose
+ Pytest | Testes Automatizados

## Rodando o projeto

Suba o banco:

    docker compose up -d

Crie o `.env` a partir do exemplo e preencha com seus dados:

    cp .env.example .env

> Para usar o Gmail, gere uma **senha de app** em myaccount.google.com/apppasswords. A senha normal da conta não funciona.

Instale as dependências e rode:

    pip install -r requirements.txt
    uvicorn app.main:app --reload

A documentação interativa fica em **http://localhost:8000/docs**. Para testar a rota `/user/me/`, faça login, copie o `access_token` e cole no botão **Authorize**.

## Testes

    pytest

Os testes usam SQLite e simulam o envio de email, então não precisam de Postgres nem de SMTP. Eles cobrem o fluxo completo de cadastro, verificação e login, além de código inválido, expirado, limite de tentativas, reenvio, email duplicado e token inválido.
