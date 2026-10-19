
USER = {"email": "joao@example.com", "name": "João", "password": "senhaforte123"}

def cadastrar(client, emails):
    response = client.post("/user/cadaster/", json=USER)
    assert response.status_code == 202
    return emails[USER["email"]]

def cadastrar_e_verificar(client, emails):
    codigo = cadastrar(client, emails)
    response = client.post("/user/verify/", json={"email": USER["email"], "codigo": codigo})
    assert response.status_code == 201

def test_cadastro_completo_e_login(client, emails):
    cadastrar_e_verificar(client, emails)

    response = client.post("/user/login/", json={"email": USER["email"], "password": USER["password"]})
    assert response.status_code == 200
    token = response.json()["access_token"]

    response = client.get("/user/me/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "email": USER["email"], "name": USER["name"]}

def test_login_antes_de_verificar(client, emails):
    cadastrar(client, emails)
    response = client.post("/user/login/", json={"email": USER["email"], "password": USER["password"]})
    assert response.status_code == 401

def test_senha_errada(client, emails):
    cadastrar_e_verificar(client, emails)
    response = client.post("/user/login/", json={"email": USER["email"], "password": "errada123"})
    assert response.status_code == 401

def test_email_ja_cadastrado(client, emails):
    cadastrar_e_verificar(client, emails)
    response = client.post("/user/cadaster/", json=USER)
    assert response.status_code == 409

def test_codigo_invalido(client, emails):
    codigo = cadastrar(client, emails)
    errado = "000000" if codigo != "000000" else "111111"
    response = client.post("/user/verify/", json={"email": USER["email"], "codigo": errado})
    assert response.status_code == 400

def test_limite_de_tentativas(client, emails):
    codigo = cadastrar(client, emails)
    errado = "000000" if codigo != "000000" else "111111"
    for _ in range(5):
        client.post("/user/verify/", json={"email": USER["email"], "codigo": errado})

    # Mesmo o código certo é recusado depois de 5 erros
    response = client.post("/user/verify/", json={"email": USER["email"], "codigo": codigo})
    assert response.status_code == 429

def test_codigo_expirado(client, emails, monkeypatch):
    codigo = cadastrar(client, emails)
    monkeypatch.setattr("app.routers.auth.verify.time.time", lambda: 10**12)
    response = client.post("/user/verify/", json={"email": USER["email"], "codigo": codigo})
    assert response.status_code == 400

def test_reenviar_codigo(client, emails):
    antigo = cadastrar(client, emails)
    response = client.post("/user/cadaster/reenviar", json={"email": USER["email"]})
    assert response.status_code == 202

    novo = emails[USER["email"]]
    if novo != antigo:
        response = client.post("/user/verify/", json={"email": USER["email"], "codigo": antigo})
        assert response.status_code == 400

    response = client.post("/user/verify/", json={"email": USER["email"], "codigo": novo})
    assert response.status_code == 201

def test_me_sem_token(client):
    response = client.get("/user/me/")
    assert response.status_code in (401, 403)

def test_me_token_invalido(client):
    response = client.get("/user/me/", headers={"Authorization": "Bearer abc.def.ghi"})
    assert response.status_code == 401
