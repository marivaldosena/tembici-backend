from datetime import datetime, timedelta
from app import db, bcrypt, app
from flask_sqlalchemy import event
from flask_jwt_extended import create_access_token


class Usuario(db.Model):
    """Armazena os detalhes do usuário cadastrado.
    
    Os campos principais são: Nome, E-mail, Senha e Telefone.
    
    Além dessas informações, o modelo inclui metadados:
    Data de Criação, Data de Atualização, Último Login e Token.

    :param nome: Nome do usuário
    :type nome: str
    :param email: E-mail do usuário
    :type email: str
    :param senha: Senha do usuário a passar por hash
    :type senha: str
    :param telefones: Telefones do usuário em forma de lista.
    :type telefones: list

    """
    # TODO: implementar uma forma de atualizar o token.
    # TODO: Criar uuid, depois de todas as outras implementações.
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(70), nullable=False, unique=True)
    senha = db.Column(db.String(120), nullable=False)
    telefones = db.relationship('Telefone', backref='usuario', lazy=False)

    data_criacao = db.Column(db.DateTime, default=datetime.now)
    data_atualizacao = db.Column(db.DateTime, onupdate=datetime.now)
    ultimo_login = db.Column(db.DateTime)
    token = db.Column(db.String(120), nullable=True)
    expires_at = db.Column(db.DateTime)

    def __str__(self):
        return '<Usuário: {} - {}>'.format(self.nome, self.email)

    def __repr__(self):
        return '<Usuário: {} - {}>'.format(self.nome, self.email)

    def to_json(self):
        resultado = {
            'id': self.id,
            'data_criacao': self.data_criacao,
            'data_atualizacao': self.data_atualizacao,
            'ultimo_login': self.ultimo_login,
            'token': self.token
        }

        return resultado

    def verificar_token(self, token):
        """ Verifica se o Token informado é válido.

        Retorna True se o token for igual ao do usuário e for dentro do prazo de expiração.
        Se não, retorna False.

        :param token: Token informado pelo usuário
        :type token: str
        :return: bool
        """

        if 'Bearer {}'.format(self.token) != token:
            return False

        data_inicial = datetime.now()

        if data_inicial > self.expires_at:
            return False

        return True

    def _


class Telefone(db.Model):
    """Armazena os telefones dos usuários.
    
    Os principais campos são Número e DDD.

    :param numero: Número do telefone
    :type numero: str
    :param ddd: DDD do telefone
    :type ddd: str
    :param usuario_id: Identificador do usuário
    :type usuario_id: int

    """
    __tablename__ = 'telefones'

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(16), nullable=False)
    ddd = db.Column(db.String(2), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    def __str__(self):
        return '<Telefone: ({}) {}>'.format(self.numero, self.ddd)

    def __repr__(self):
        return '<Telefone: ({}) {}>'.format(self.numero, self.ddd)


@event.listens_for(Usuario, 'before_insert')
def on_before_insert_usuario(mapper, connection, target):
    target.senha = bcrypt.generate_password_hash(target.senha).decode('utf-8')

    if not target.data_atualizacao:
        target.data_atualizacao = datetime.now()

    if not target.ultimo_login:
        target.ultimo_login = datetime.now()

    if not target.token:
        target.token = create_access_token(target.email)

    if not target.expires_at:
        target.expires_at = datetime.now() + app.config.get('JWT_ACCESS_TOKEN_EXPIRES', 30)
