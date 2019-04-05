from flask import Blueprint, request, jsonify
from app import bcrypt

usuarios_bp = Blueprint('usuarios', __name__)

from app.models import Usuario, db, Telefone


@usuarios_bp.route('/', methods=['POST'])
def criar_usuario():
    """
    Criar um usuário com os seguintes dados fornecidos no formato JSON:

    - nome: str Nome do usuário
    - email: str E-mail para login
    - senha: str Senha para login
    - telefones: list Lista com telefones do usuário

    O resultado retornado é um JSON com o seguintes valores:

    - id: str Identificador do usuário
    - data_criacao: date Data de criação do usuário
    - data_atualizacao: date Data de atualização dos dados do usuário
    - ultimo_login: date Data do último login
    - token: str Token JWT para requisições futuras de acesso

    """
    if request.data:
        json = request.get_json()

        e_existente = Usuario.query.filter_by(email=json.get('email', None)).first()

        if e_existente:
            return jsonify({'mensagem': 'E-mail já existente.'}), 400

        usuario = Usuario(nome=json.get('nome', None),
                          email=json.get('email', None),
                          senha=json.get('senha', None))

        if json.get('telefones', None):
            for item in json.get('telefones', None):
                telefone = Telefone(ddd=item.get('ddd', None), numero=item.get('numero', None))
                usuario.telefones.append(telefone)

        db.session.add(usuario)
        db.session.commit()

        return jsonify(usuario.to_json()), 201
    else:
        return jsonify({'mensagem': 'JSON inválido ou vazio.'}), 422


@usuarios_bp.route('/<usuario_id>')
def buscar_usuario(usuario_id):
    # Verifica se há o cabeçalho com o token
    if not request.headers.get('Authentication', None):
        return jsonify({'mensagem': 'Não autorizado'}), 401

    usuario = Usuario.query.get_or_404(usuario_id)

    if 'Bearer {}'.format(usuario.token) != request.headers.get('Authentication', None):
        return jsonify({'mensagem': 'Não autorizado'}), 401

    # Verifica se o token é o mesmo do usuário
    if not usuario.verificar_token(request.headers.get('Authentication', None)):
        return jsonify({'mensagem': 'Sessão inválida'}), 401


    return jsonify(usuario.to_json()), 200


@usuarios_bp.route('/signin')
def signin():
    if request.data:
        json = request.get_json()

        usuario = Usuario.query.filter_by(email=json.get('email', None)).first()

        # E-mail inexistente
        if not usuario:
            return jsonify({'mensagem': 'Usuário e/ou senha inválidos'}), 401

        # Senha
        if not json.get('senha', None) or \
                not usuario.verificar_senha(json.get('senha', None)):
            return jsonify({'mensagem': 'Usuário e/ou senha inválidos'})

        return jsonify(usuario.to_json())
    else:
        return jsonify({'mensagem': 'JSON inválido ou vazio.'}), 422
