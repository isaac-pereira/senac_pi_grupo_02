# SENAC 

## Curso: Análise e Desenvolvimento de Sistemas 

## Disciplina: Projeto Integrador

### Grupo:
<p>Isaac Elias Severino Pereira
<br>Luiz Miguel Andrade de Souza
<br>Miguel Angelo Santana de Almeida
<br>Narciso Dias de Almeida Neto
<br>Tiago Gomes da Silva</p>

### Descrição:
<p>Este aplicativo web foi desenvolvido com as tecnologias/linguagens (principais): HTML, CSS, JavaScript, Flask, SQLite3, Python 3.10, Git.</p>

### Como testar a aplicação:

<strong>Observações: </strong><em>Clone o repositório (ou baixe o .zip desta página e descompacte no seu computador). Caso não tenha o Python 3.8 ou superior no computador, será necessário instalá-lo antes de seguir os passos abaixo.</em>

1. Instale o `virtualenv` com o comando:
```
$ pip install virtualenv
```

2. Abra um terminal na pasta raíz do projeto e execute o comando:
```
$ virtualenv env
```

3.a. Então execute (no Windows):
```
$ .\env\Scripts\activate
```

3.b. Ou (no Linux):
```
$ source /env/bin/activate
```

4. Na sequência, instale as dependências listadas no arquivo `requirements.txt` através do comando:
```
$ (env) pip install -r requirements.txt
```

5. Inicie o servidor Web:
```
$ (env) python app.py
```

6. Abra um navegador e acesse:
```
http://localhost:5000
```

Observação: o servidor inicia por padrão na porta 5000. Para alterá-la, entre no arquivo `app.py` e faça a seguinte alteração:

```python
if __name__ == "__main__":
    app.run(debug=True, port=<numero_da_porta_desejada>)
```

### Funcionalidades:
<p>O aplicativo web apresenta as seguintes funcionalidades implementadas:</p>
<ul>
    <li>Cadastramento de usuário.</li><br>
    <li>Criação de senha com criptografia.</li><br>
    <li>Login/logout de usuário.</li><br>
    <li>Mensagens de erro/aviso, informando quando um e-mail e/ou CPF já existe na base de dados de cadastro (regra: não é permitido o registro de um mesmo e-mail/CPF mais de uma vez).</li><br>
    <li>Mensagens de erro/aviso, informando quando um usuário e/ou senha não confere com os registros do banco de dados.</li><br>
    <li>Páginas Html com navegação (roteamento), estilizadas com CSS e interação com JavaScript.</li><br>
</ul>
