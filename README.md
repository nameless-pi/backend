## API RESTful


### Requisitos
- `pip3 install -r requirements.txt` (para instalar as dependências)
- banco MySQL
- alterar as configurações do banco em `config.py`
- após configurar o banco, executar as migrações da base de dados: `python3 migrate.py db init`, `python3 migrate.py db migrate` e `python3 migrate.py db upgrade` 


## Para executar
- `python3 run.py` (usem o Postman para testar os métodos)

### O que falta fazer?
- CRUD admin
- Melhorar o método PUT de quase todos os recursos, principalmente query parameters


### O que está funcionando?
- **CR**U**D** usuário
- **CR**U**D** salas
- **CR**U**D** horarios
- Ao deletar um usuário, ele é removido de acesso
- Ao deletar uma sala, ela é removida de acesso

Talvez eu tenha esquecido de algo xD
