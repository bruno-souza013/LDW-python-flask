import urllib.request
from flask import render_template, request, redirect, url_for
#essa bibilioteca serve para ler determinada URL
import urllib
#Converte dados para o formato JSON
import json
import random
#importa model do banco
from models.database import db, Music

messages = []
musiclist = []

def init_app(app):
    @app.route('/', methods=['GET', 'POST'])
    def home():
        # atista específico 
        artist_url = "https://api.deezer.com/track/2761897271" 
        res = urllib.request.urlopen(artist_url)
        data = res.read()
        result = json.loads(data)
        try:
            #artistas variados
            genre_ids = [116, 152, 85, 144]  
            random_genre_id = random.choice(genre_ids)  
            artist_url = f'https://api.deezer.com/genre/{random_genre_id}/artists'
            res = urllib.request.urlopen(artist_url)
            data = res.read()
            artists = json.loads(data)['data']
            
            if artists:
                random_artists = random.sample(artists, min(18, len(artists)))  
            else:
                random_artists = []
        except Exception as e:
            print("Erro ao buscar artistas:", e)
            random_artists = []  
        try:
            #albuns
            album_ids = ["81763", "673968231", "293752", "119606", "62183462", "349710367", "78630952", "1318764","102819", "145196332"] 
            albums_info = []

            for album_id in album_ids:
                album_url = f"https://api.deezer.com/album/{album_id}"  
                res = urllib.request.urlopen(album_url)
                data = res.read()
                album_data = json.loads(data)

                if album_data:
                    albums_info.append(album_data)
            if albums_info:
                recent_music = random.sample(albums_info, min(3, len(albums_info)))  
            else:
                recent_music = []

        except Exception as e:
            print("Erro ao buscar lançamentos:", e)
            recent_music = []
        return render_template('index.html', result=result, artists=random_artists, recent_music=recent_music)




    @app.route('/community', methods=['GET', 'POST'])
    def community():
        if request.method == 'POST':
            if request.form.get('message'):
                messages.append(request.form.get('message'))
                return redirect(url_for('community'))
        return render_template('community.html',messages=messages)


    #CRUD com Sqlite
    @app.route('/cadmusic', methods=['GET', 'POST'])
    @app.route('/cadmusic/delete/<int:id>')
    def cadmusic(id=None):
        if id:
            music = Music.query.get(id)
            #Delete da musica
            db.session.delete(music)
            db.session.commit()
            return redirect(url_for('cadmusic'))
        
        if request.method =='POST':
            newmusic = Music(request.form['title'], request.form['artist'], request.form['category'], request.form['year'], request.form['album'])
            db.session.add(newmusic)
            db.session.commit()
            return redirect(url_for('cadmusic'))
        else:
            #Paginação
            page = request.args.get('page', 1, type=int)
            per_page = 5
            music_page = Music.query.paginate(page=page, per_page=per_page)
            return render_template('cadmusic.html', cad_music=music_page)  
    
    #Rota Edição
    @app.route('/editmusic/<int:id>', methods=['GET', 'POST'])
    def editmusic(id):
        music = Music.query.get(id)
        if request.method == 'POST':
            music.title = request.form['title']
            music.artist = request.form['artist']
            music.category = request.form['category']
            music.year = request.form['year']
            music.album = request.form['album']
            db.session.commit()
            return redirect(url_for('cadmusic'))
        return render_template('editmusic.html', music=music)
   
    @app.route('/apimusic', methods=['GET', 'POST'])
    def apimusic():
        search_results = []  
        #retorna pesquisa
        if request.method == 'POST':  
            search_query = request.form.get('search')  
            url = f'https://api.deezer.com/search?q={urllib.parse.quote(search_query)}'
            res = urllib.request.urlopen(url)
            data = res.read()
            search_results = json.loads(data)['data']  
        
        else:  
            try:
                #popula com artistas de generos variados
                genre_ids = [472, 116, 152, 85, 144]
                random_genre_id = random.choice(genre_ids)
                artist_url = f'https://api.deezer.com/genre/{random_genre_id}/artists'
                res = urllib.request.urlopen(artist_url)
                data = res.read()
                artists = json.loads(data)['data']
                if artists:    
                    random_artists = random.sample(artists, min(6, len(artists)))

                    for artist in random_artists:
                        artist_id = artist['id']
                        music_url = f'https://api.deezer.com/artist/{artist_id}/top?limit=5'
                        res = urllib.request.urlopen(music_url)
                        data = res.read()
                        artist_tracks = json.loads(data)['data']

                        search_results.extend(artist_tracks)
                    random.shuffle(search_results)

            except Exception as e:
                print("Erro ao buscar músicas:", e)
                search_results = []          
        return render_template('apimusic.html', search_results=search_results)
        