from flask import Flask, render_template
from controllers import routes
from models.database import db
import os

# criando a instancia do Flask na variável app
app = Flask(__name__, template_folder='views')  # representa o nome do arquivo

routes.init_app(app)

dir = os.path.abspath(os.path.dirname(__file__))
#configuração banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir, 'models/database.db')

# iniciando o servidor
if __name__ == '__main__':
    db.init_app(app)
    #Verifica no inicio da aplicação se o BD existe
    with app.test_request_context():
        db.create_all()
    app.run(host='0.0.0.0', port=4000, debug=True)
