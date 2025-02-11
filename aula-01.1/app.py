from flask import Flask, render_template
#criando a instancia do Flask na variável app
app = Flask(__name__, template_folder='views') #representa o nome do arquivo

#Criando a primeira rota da aplicação
@app.route('/')
#view function - função de visualização
def home():
    return render_template('index.html')

@app.route('/games')
def games():
    return render_template('games.html')
#iniciando o servidor
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)