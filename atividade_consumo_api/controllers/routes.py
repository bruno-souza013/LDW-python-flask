import urllib.request
from flask import render_template, request, redirect, url_for
#essa bibilioteca serve para ler determinada URL
import urllib
#Converte dados para o formato JSON
import json
import random


jogadores = []
gamelist = [{'titulo': 'CS-GO',
        'ano': 2012,
        'categoria': 'FPS Online'}]


def init_app(app):
    @app.route('/')
    # view function - função de visualização
    def home():
        return render_template('index.html')

    @app.route('/community', methods=['GET', 'POST'])
    def community():
        game = gamelist[0]

        if request.method == 'POST':
            if request.form.get('jogador'):
                jogadores.append(request.form.get('jogador'))
                return redirect(url_for('games'))

        return render_template('games.html',
                               game=game,
                               jogadores=jogadores)

    @app.route('/cadmusic', methods=['GET', 'POST'])
    def cadmusic():
        if request.method == 'POST':
            form_data = request.form.to_dict()
            gamelist.append(form_data)
            return (redirect(url_for('cadgames'))) 
        return render_template('cadgames.html', 
                               gamelist=gamelist)
    
    @app.route('/apimusic', methods=['GET', 'POST'])
    def apimusic():
        search_results = []  

        if request.method == 'POST':  
            search_query = request.form.get('search')  
            url = f'https://api.deezer.com/search?q={urllib.parse.quote(search_query)}'
            res = urllib.request.urlopen(url)
            data = res.read()
            search_results = json.loads(data)['data']  
        
        else:  
            try:
                # 1️⃣ Lista de IDs dos gêneros desejados
                genre_ids = [472, 116, 152, 85, 144]

                # 2️⃣ Escolhe um gênero aleatório
                random_genre_id = random.choice(genre_ids)

                # 3️⃣ Busca artistas desse gênero
                artist_url = f'https://api.deezer.com/genre/{random_genre_id}/artists'
                res = urllib.request.urlopen(artist_url)
                data = res.read()
                artists = json.loads(data)['data']

                if artists:
                    # 4️⃣ Escolhe até 5 artistas aleatórios para criar um mix
                    random_artists = random.sample(artists, min(5, len(artists)))

                    # 5️⃣ Puxa músicas populares de cada artista e cria um mix
                    for artist in random_artists:
                        artist_id = artist['id']
                        music_url = f'https://api.deezer.com/artist/{artist_id}/top?limit=5'
                        res = urllib.request.urlopen(music_url)
                        data = res.read()
                        artist_tracks = json.loads(data)['data']

                        # Adiciona as músicas ao mix
                        search_results.extend(artist_tracks)

                    # 6️⃣ Embaralha as músicas para criar um verdadeiro mix
                    random.shuffle(search_results)

            except Exception as e:
                print("Erro ao buscar músicas:", e)
                search_results = []  # Se der erro, mantém vazio
            
        return render_template('apimusic.html', search_results=search_results)
        