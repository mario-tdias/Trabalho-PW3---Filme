from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_super_segura'

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Banco de dados simulado
reviews = [
    {
        "id": 1,
        "filme": "O Poderoso Chefão", 
        "autor": "Carlos", 
        "nota": 5, 
        "comentario": "Uma obra-prima absoluta do cinema. A atuação de Marlon Brando é lendária.",
        "imagem": "https://image.tmdb.org/t/p/w500/oJagOzBu9Rdd9BrciseCm3U3MCU.jpg",
        "data": "2023-10-15",
        "categorias": ["Drama", "Crime"],
        "likes": 42
    },
    {
        "id": 2,
        "filme": "Matrix", 
        "autor": "Ana", 
        "nota": 5, 
        "comentario": "Revolucionou a ficção científica com seus efeitos visuais inovadores.",
        "imagem": "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
        "data": "2023-09-22",
        "categorias": ["Ficção Científica", "Ação"],
        "likes": 38
    },
    {
        "id": 3,
        "filme": "Titanic",
        "autor": "Bruna",
        "nota": 5,
        "comentario": "Romance épico com efeitos especiais incríveis. Uma história inesquecível.",
        "imagem": "https://image.tmdb.org/t/p/w500/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg",
        "data": "2023-08-10",
        "categorias": ["Drama", "Romance"],
        "likes": 51
    },
    {
        "id": 4,
        "filme": "Interestelar",
        "autor": "Lucas",
        "nota": 5,
        "comentario": "Um espetáculo visual e emocional. Nolan entrega um sci-fi marcante.",
        "imagem": "https://image.tmdb.org/t/p/w500/rAiYTfKGqDCRIIqo664sY9XZIvQ.jpg",
        "data": "2023-11-01",
        "categorias": ["Ficção Científica", "Drama"],
        "likes": 47
    },
    {
        "id": 5,
        "filme": "Clube da Luta",
        "autor": "João",
        "nota": 5,
        "comentario": "Um clássico cult que te faz refletir sobre a sociedade moderna.",
        "imagem": "https://image.tmdb.org/t/p/w500/bptfVGEQuv6vDTIMVCHjJ9Dz8PX.jpg",
        "data": "2023-12-05",
        "categorias": ["Drama", "Suspense"],
        "likes": 40
    },
    {
        "id": 6,
        "filme": "Forrest Gump",
        "autor": "Marina",
        "nota": 5,
        "comentario": "Inspirador e emocionante. Tom Hanks está brilhante.",
        "imagem": "https://image.tmdb.org/t/p/w500/saHP97rTPS5eLmrLQEcANmKrsFl.jpg",
        "data": "2023-07-19",
        "categorias": ["Drama", "Romance"],
        "likes": 46
    },
    {
        "id": 7,
        "filme": "Os Vingadores",
        "autor": "Rafael",
        "nota": 4,
        "comentario": "Explosivo e divertido. Um marco dos filmes de super-heróis.",
        "imagem": "https://image.tmdb.org/t/p/w500/RYMX2wcKCBAr24UyPD7xwmjaTn.jpg",
        "data": "2023-06-30",
        "categorias": ["Ação", "Ficção Científica"],
        "likes": 34
    },
    {
        "id": 8,
        "filme": "Pulp Fiction",
        "autor": "Gabriel",
        "nota": 5,
        "comentario": "Tarantino em sua melhor forma. Diálogos afiados e cenas marcantes.",
        "imagem": "https://image.tmdb.org/t/p/w500/dRZpdpKLgN9nk57zggJCs1TjJb4.jpg",
        "data": "2023-10-05",
        "categorias": ["Crime", "Drama"],
        "likes": 44
    },
    {
        "id": 9,
        "filme": "O Senhor dos Anéis: O Retorno do Rei",
        "autor": "Renata",
        "nota": 5,
        "comentario": "Épico em todos os sentidos. Um final digno para a trilogia.",
        "imagem": "https://image.tmdb.org/t/p/w500/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg",
        "data": "2023-09-18",
        "categorias": ["Fantasia", "Aventura"],
        "likes": 50
    },
    {
        "id": 10,
        "filme": "O Cavaleiro das Trevas",
        "autor": "Eduardo",
        "nota": 5,
        "comentario": "Heath Ledger como Coringa é simplesmente inesquecível.",
        "imagem": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
        "data": "2023-10-20",
        "categorias": ["Ação", "Crime", "Drama"],
        "likes": 49
    },
    {
        "id": 11,
        "filme": "A Origem",
        "autor": "Fernanda",
        "nota": 5,
        "comentario": "Mind-blowing! Um dos roteiros mais criativos do cinema moderno.",
        "imagem": "https://image.tmdb.org/t/p/w500/edv5CZvWj09upOsy2Y6IwDhK8bt.jpg",
        "data": "2023-08-28",
        "categorias": ["Ação", "Ficção Científica"],
        "likes": 45
    },
    {
        "id": 12,
        "filme": "Gladiador",
        "autor": "Vinícius",
        "nota": 5,
        "comentario": "Russell Crowe está fantástico. Um clássico do cinema histórico.",
        "imagem": "https://image.tmdb.org/t/p/w500/ty8TGRuvJLPUmAR1H1nRIsgwvim.jpg",
        "data": "2023-11-10",
        "categorias": ["Ação", "Drama", "Histórico"],
        "likes": 41
    }
]


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_next_id():
    return max(review['id'] for review in reviews) + 1 if reviews else 1

@app.route('/')
def index():
    theme = request.args.get('theme', session.get('theme', 'light'))
    session['theme'] = theme
    return render_template('index.html', 
                         reviews=reviews[:4], 
                         all_reviews=reviews,
                         theme=theme)

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        novo_review = {
            "id": get_next_id(),
            "filme": request.form['filme'],
            "autor": request.form['autor'],
            "nota": int(request.form['nota']),
            "comentario": request.form['comentario'],
            "data": datetime.now().strftime("%Y-%m-%d"),
            "categorias": [cat.strip() for cat in request.form['categorias'].split(',')],
            "imagem": "",
            "likes": 0
        }
        
        if 'imagem' in request.files:
            file = request.files['imagem']
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{novo_review['id']}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                novo_review['imagem'] = url_for('static', filename=f'uploads/{filename}')
        
        if not novo_review['imagem']:
            novo_review['imagem'] = request.form.get('imagem_url', url_for('static', filename='images/default-movie.jpg'))
        
        reviews.append(novo_review)
        flash('Review adicionado com sucesso!', 'success')
        return redirect(url_for('detalhes_filme', filme_id=novo_review['id']))
    
    return render_template('adicionar.html', theme=session.get('theme', 'light'))

@app.route('/filme/<int:filme_id>')
def detalhes_filme(filme_id):
    filme = next((f for f in reviews if f['id'] == filme_id), None)
    if filme:
        return render_template('detalhes.html', 
                             filme=filme,
                             theme=session.get('theme', 'light'))
    flash('Filme não encontrado!', 'danger')
    return redirect(url_for('index'))

@app.route('/like/<int:filme_id>')
def like(filme_id):
    filme = next((f for f in reviews if f['id'] == filme_id), None)
    if filme:
        filme['likes'] += 1
        flash('Você curtiu este review!', 'success')
    return redirect(url_for('detalhes_filme', filme_id=filme_id))

@app.route('/ranking')
def ranking():
    reviews_ordenados = sorted(reviews, key=lambda x: (-x['nota'], -x['likes']))
    return render_template('ranking.html', 
                         reviews=reviews_ordenados,
                         theme=session.get('theme', 'light'))

@app.route('/buscar')
def buscar():
    termo = request.args.get('q', '').strip().lower()
    if not termo:
        return redirect(url_for('index'))
    
    resultados = [
        review for review in reviews 
        if (termo in review['filme'].lower() or 
            termo in review['comentario'].lower() or
            termo in review['autor'].lower() or
            any(termo in cat.lower() for cat in review['categorias']))
    ]
    
    return render_template('busca.html', 
                         resultados=resultados, 
                         termo=termo,
                         theme=session.get('theme', 'light'))

@app.route('/tema/<tema>')
def alterar_tema(tema):
    if tema in ['light', 'dark']:
        session['theme'] = tema
    return redirect(request.referrer or url_for('index'))

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)