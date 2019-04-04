from flask import Blueprint, request, jsonify

usuarios_bp = Blueprint('usuarios', __name__)

from app.models import Usuario, db


@usuarios_bp.route('/', methods=['POST'])
def criar_usuario():
    nome = request.json['nome']
    email = request.json['email']
    senha = request.json['senha']
    telefones = request.json['telefones']

    usuario = Usuario(nome=nome,
                      email=email,
                      senha=senha)

    db.session.add(usuario)
    db.session.commit()

    return jsonify(usuario.nome), 201


@usuarios_bp.route('/<usuario_id>')
def buscar_usuario(usuario_id):
    return 'buscar_usuario'


@usuarios_bp.route('/signin')
def signin():
    return 'signin'
