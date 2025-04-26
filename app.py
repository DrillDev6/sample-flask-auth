from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import re
import bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] ="your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI']= "mysql+pymysql://root:admin123@127.0.0.1:3306/flask-crud"

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
#view
login_manager.login_view = 'login'
#Session<- conexão ativa

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/login', methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    if  not email.endswith(('@gmail.com', '@outlook.com', 'hotmail.com')):
        return jsonify({"message": "O email deve conter '@gmail.com', '@outlook.com' ou 'hotmail.com'"}), 400

    if username and email and password:#verificando se a condicional foi cumprida na basededados
        user = User.query.filter_by(username=username).first()
        user = User.query.filter_by(email=email).first() 

        if user and email and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
            login_user(user)
            print (current_user.is_authenticated)
            return jsonify ({"message": "Autenticação realizada com sucesso"})
                                                                            
    return jsonify({"message": "Dados inseridos invalidos!"}), 400
        

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso"})


@app.route('/user', methods=['Post'])
def create_user():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not email.endswith(('@gmail.com', '@outlook.com', 'hotmail.com')):
        return jsonify({"message": "O email deve conter '@gmail.com', '@outlook.com' ou 'hotmail.com'"}), 400          

    if username and email and password:
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        user = User(username=username, email=email, password=hashed_password, role='user')
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuario cadastrado com sucesso!"})
    
    return jsonify({"message": "Dados inseridos inválidos"}), 400

@app.route('/user/<int:id_user>', methods=['GET'])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)

    if user:
        return {"username": user.username, "email": user.email }
    
    return jsonify({"message": "Usuario não encontrado"}), 404


@app.route('/user/<int:id_user>', methods=['PUT'])
@login_required
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user)

    if id_user != current_user.id and current_user.role == 'user':
        return jsonify({"message": "A ação não é permitida"}), 403
    
    if user and data.get("password"):
        user.password = data.get("password")
        db.session.commit()

        return jsonify({"message": f"Senha do usuario: {id_user}, atualizada com sucesso"})
    
    return jsonify({"message": "Usuario não encontrado!"}), 404

@app.route('/user/<int:id_user>', methods=['DELETE'])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)

    if current_user.role != 'admin':
        return jsonify ({"message": "Operação não permitida"}), 403
    
    if id_user == current_user.id:

        return jsonify({"message": "Você não pode deletar o usuario que está em uso!"}), 403

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Usuário {id_user} deletado com sucesso"})
    

    return jsonify({"message": "Usuario não encontrado!"}), 404

@app.route("/hello", methods=['GET'])
def hello():
    return "hello"

if __name__ == '__main__':
    app.run(debug=True)