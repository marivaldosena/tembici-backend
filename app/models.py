from datetime import datetime
from app import db


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
    # TODO: Implementar data de atualização para o mesmo que a data da criação.
    # TODO: Criar uuid, depois de todas as outras implementações.
    # TODO: Evitar duplicação de e-mails no model.
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(70), nullable=False)
    senha = db.Column(db.String(120), nullable=False)
    telefones = db.relationship('Telefone', backref='usuario', lazy=False)

    data_criacao = db.Column(db.DateTime, default=datetime.now)
    data_atualizacao = db.Column(db.DateTime, onupdate=datetime.now)
    ultimo_login = db.Column(db.DateTime)
    token = db.Column(db.String(120), nullable=True)

    def __str__(self):
        return '<Usuário: {} - {}>'.format(self.nome, self.email)

    def __repr__(self):
        return '<Usuário: {} - {}>'.format(self.nome, self.email)


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

    id = db.Column(db.int, primary_key=True)
    numero = db.Column(db.String(16), nullable=False)
    ddd = db.Column(db.String(2), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    def __str__(self):
        return '<Telefone: ({}) {}>'.format(self.numero, self.ddd)

    def __repr__(self):
        return '<Telefone: ({}) {}>'.format(self.numero, self.ddd)
