from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista em memória (substitui o banco de dados)
filmes = [
    {"id": 1, "titulo": "O Poderoso Chefão", "ano": 1972, "genero": "Drama"},
    {"id": 2, "titulo": "Matrix", "ano": 1999, "genero": "Ficção Científica"},
]

# Rota principal (exibe a lista de filmes)
@app.route('/')
def index():
    return render_template('index.html', filmes=filmes)

# Rota para cadastrar novo filme
@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        novo_filme = {
            "id": len(filmes) + 1,
            "titulo": request.form['titulo'],
            "ano": int(request.form['ano']),
            "genero": request.form['genero']
        }
        filmes.append(novo_filme)
        return redirect(url_for('index'))
    return render_template('cadastro.html')

if __name__ == '__main__':
    app.run(debug=True)