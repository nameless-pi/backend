## API RESTful

### Requisitos
- `pip install -r requirements.txt` (para instalar as dependências)
- banco MySQL
- alterar as configurações do banco em `config.py`
- após configurar o banco, executar as migrações da base de dados: `python migrate.py db init`, `python migrate.py db migrate` e `python migrate.py db upgrade` 


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