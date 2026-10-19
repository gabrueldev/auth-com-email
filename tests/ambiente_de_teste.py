import os

os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["SECRET_KEY"] = "chave-de-teste"
os.environ["MAIL_USERNAME"] = "teste@example.com"
os.environ["MAIL_PASSWORD"] = "senha"
os.environ["MAIL_FROM"] = "teste@example.com"
