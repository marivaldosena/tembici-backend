from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
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

        for item in json.get('telefones', None):
            telefone = Telefone(ddd=item.get('ddd', None), numero=item.get('numero', None))
            usuario.telefones.append(telefone)

        usuario.token = create_access_token(usuario.email)
        print(usuario.token)

        db.session.add(usuario)
        db.session.commit()

        return jsonify(usuario.to_json()), 201
    else:
        return jsonify({'mensagem': 'JSON inválido ou vazio.'}), 422


@usuarios_bp.route('/<usuario_id>')
@jwt_required
def buscar_usuario(usuario_id):
    # TODO: Implementar funcionalidade
    # TODO: Caso o token não exista, retornar erro com status apropriado com a mensagem "Não autorizado".
    # TODO: Caso o token exista, buscar o usuário pelo user_id passado no path e comparar se o token no modelo é igual ao token passado no header.
    # TODO: Caso não seja o mesmo token, retornar erro com status apropriado e mensagem "Não autorizado"
    # TODO: Caso não seja a MENOS que 30 minutos atrás, retornar erro com status apropriado com mensagem "Sessão inválida".
    # TODO: Mudar a mensagem quando não há o cabeçalho Authentication para "Não autorizado"
    # TODO: Mudar a mensagem de token expirado para "Sessão inválida"
    usuario = Usuario.query.get_or_404(usuario_id)
    return jsonify(usuario.to_json()), 200


@usuarios_bp.route('/signin')
def signin():
    if request.data:
        json = request.get_json()

        usuario = Usuario.query.filter_by(email=json.get('email', None)).first()

        # E-mail inexistente
        if not usuario:
            return jsonify({'mensagem': 'Usuário e/ou senha inválidos'}), 401

        if not json.get('senha', None) or \
                not bcrypt.check_password_hash(usuario.senha, json.get('senha', None)):
            return jsonify({'mensagem': 'Usuário e/ou senha inválidos'})

        return jsonify(usuario.to_json())
    else:
        return jsonify({'mensagem': 'JSON inválido ou vazio.'}), 422
