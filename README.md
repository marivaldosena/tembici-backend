# Tembici Backend

Essa API foi criada utilizando Python 3.7 com Flask.

Os principais endpoints são:


Criar usuário:
POST https://msena-tembici-backend.herokuapp.com/api/users/

```json
{
	"nome": "Nome",
	"email": "email",
	"senha": "senha"
	"telefones": [
		{"numero": "12341234", "ddd": "11"}
	]
}
```

Logar usuário
GET https://msena-tembici-backend.herokuapp.com/api/users/signin

```json
{
	"email": "email",
	"senha": "senha"
}
``


Buscar Usuário
GET https://msena-tembici-backend.herokuapp.com/api/users/:id


```json
  Authentication: Bearer token12345
```




