from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dados iniciais (8 filmes com reviews e imagens reais)
reviews = [
    {
        "filme": "O Poderoso Chefão", 
        "autor": "Carlos", 
        "nota": 5, 
        "comentario": "Obra-prima do cinema! Marlon Brando é incrível.",
        "imagem": "https://image.tmdb.org/t/p/w500/oJagOzBu9Rdd9BrciseCm3U3MCU.jpg"
    },
    {
        "filme": "Matrix", 
        "autor": "Ana", 
        "nota": 5, 
        "comentario": "Revolucionou a ficção científica e os efeitos visuais.",
        "imagem": "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg"
    },
    {
        "filme": "Parasita", 
        "autor": "Li", 
        "nota": 5, 
        "comentario": "Genial! Crítica social afiada e direção impecável.",
        "imagem": "https://image.tmdb.org/t/p/w500/igw938inb6Fy0YVcwIyxQ7Lu5FO.jpg"
    },
    {
        "filme": "Clube da Luta", 
        "autor": "Rafael", 
        "nota": 4, 
        "comentario": "Plot twist icônico. Brad Pitt rouba a cena!",
        "imagem": "https://image.tmdb.org/t/p/w500/hZkgoQYus5vegHoetLkCJzb17zJ.jpg"
    },
    {
        "filme": "Interestelar", 
        "autor": "Maria", 
        "nota": 5, 
        "comentario": "Emocionante e visualmente deslumbrante. Hans Zimmer arrasa!",
        "imagem": "https://image.tmdb.org/t/p/w500/mZSDJHHxZ8LiQX8KJle6EBoXugo.jpg"
    },
    {
        "filme": "Coringa", 
        "autor": "Pedro", 
        "nota": 4, 
        "comentario": "Joaquin Phoenix entregou uma atuação histórica.",
        "imagem": "https://image.tmdb.org/t/p/w500/xLxgVxFWvb9hhUyCDDXxRPPnFck.jpg"
    },
    {
        "filme": "Toy Story", 
        "autor": "Lucas", 
        "nota": 4, 
        "comentario": "Clássico da Pixar que marcou gerações.",
        "imagem": "https://image.tmdb.org/t/p/w500/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg"
    },
    {
        "filme": "Pulp Fiction", 
        "autor": "Julia", 
        "nota": 5, 
        "comentario": "Tarantino no seu melhor. Diálogos inesquecíveis!",
        "imagem": "https://image.tmdb.org/t/p/w500/fIE3lAGcZDV1G6XM5KmuWnNsPp1.jpg"
    }
]

# Rota principal (todos os reviews)
@app.route('/')
def index():
    return render_template('index.html', reviews=reviews)

# Rota para adicionar review (mantida igual)
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        novo_review = {
            "filme": request.form['filme'],
            "autor": request.form['autor'],
            "nota": int(request.form['nota']),
            "comentario": request.form['comentario'],
            "imagem": request.form['imagem']
        }
        reviews.append(novo_review)
        return redirect(url_for('index'))
    return render_template('adicionar.html')

# Rota para ranking (nova!)
@app.route('/ranking')
def ranking():
    # Ordena reviews por nota (decrescente)
    reviews_ordenados = sorted(reviews, key=lambda x: x['nota'], reverse=True)
    return render_template('ranking.html', reviews=reviews_ordenados)

# app.py
@app.route('/buscar')
def buscar():
    termo = request.args.get('q', '').strip().lower()
    
    if not termo:
        return redirect(url_for('index'))
    
    resultados = [
        review for review in reviews 
        if termo in review['filme'].lower() or 
           termo in review['comentario'].lower() or
           termo in review['autor'].lower()
    ]
    
    return render_template('busca.html', resultados=resultados, termo=termo)

@app.route('/filme/<nome_filme>')
def detalhes_filme(nome_filme):
    # Encontra o filme pelo nome exato (case-sensitive)
    filme = next((f for f in reviews if f['filme'] == nome_filme), None)
    
    if filme:
        return render_template('detalhes_filme.html', filme=filme)
    else:
        return "Filme não encontrado", 404

if __name__ == '__main__':
    app.run(debug=True)