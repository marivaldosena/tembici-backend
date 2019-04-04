from datetime import datetime
from app import db


class Usuario(db.Model):
    """
    Armazena os detalhes do usuário cadastrado.

    Os campos principais são: Nome, E-mail, Senha e Telefone.

    Além dessas informações, o modelo inclui metadados:
    Data de Criação, Data de Atualização, Último Login e Token.
    """
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
    """
    Armazena os telefones dos usuários.

    Os principais campos são Número e DDD.
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
