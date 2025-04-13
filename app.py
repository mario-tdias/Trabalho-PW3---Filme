from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dados em memória (substitui o banco de dados)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)  # Evita reinicialização

reviews = [
    {
        "filme": "O Poderoso Chefão",
        "autor": "Carlos",
        "nota": 5,
        "comentario": "Clássico absoluto do cinema!",
        "imagem": "https://media.themoviedb.org/t/p/w300_and_h450_bestv2/uP46DujkD3nwcisOjz9a0Xw0Knj.jpg"  # URL da imagem
    },
    {
        "filme": "Matrix",
        "autor": "Ana",
        "nota": 4,
        "comentario": "Revolucionou os efeitos visuais.",
        "imagem": "https://media.themoviedb.org/t/p/w300_and_h450_bestv2/wHZfVKwhf4Vl3cODkIzfIUzKCeu.jpg"  # URL da imagem
    }
]

# ... (o resto do código permanece igual)

# Rota principal (mostra todos os reviews)
@app.route('/')
def index():
    return render_template('index.html', reviews=reviews)

# Rota para adicionar novo review
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        novo_review = {
            "filme": request.form['filme'],
            "autor": request.form['autor'],
            "nota": int(request.form['nota']),
            "comentario": request.form['comentario']
        }
        reviews.append(novo_review)
        return redirect(url_for('index'))
    return render_template('adicionar.html')

if __name__ == '__main__':
    app.run(debug=True)