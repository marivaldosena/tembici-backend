from flask import Blueprint, request, jsonify


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

        e_existente = Usuario.query.filter_by(email=json['email']).first()

        if e_existente:
            return jsonify({'mensagem': 'E-mail já existente.'}), 403

        usuario = Usuario(nome=json['nome'],
                          email=json['email'],
                          senha=json['senha'])

        for item in json['telefones']:
            telefone = Telefone(ddd=item['ddd'], numero=item['numero'])
            usuario.telefones.append(telefone)

        db.session.add(usuario)
        db.session.commit()

        return jsonify(usuario.to_json()), 201
    else:
        return jsonify({'mensagem': 'JSON inválido ou vazio.'}), 422


@usuarios_bp.route('/<usuario_id>')
def buscar_usuario(usuario_id):
    # TODO: Implementar funcionalidade
    usuario = Usuario.query.get_or_404(usuario_id)
    return jsonify(usuario.to_json()), 200


@usuarios_bp.route('/signin')
def signin():
    # TODO: Implementar funcionalidade
    return 'signin'
