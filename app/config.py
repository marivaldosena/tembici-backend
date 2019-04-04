import os
from datetime import timedelta

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
      Configuração padrão básica.
    """

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY =  os.environ.get('JWT_SECRET_KEY') or '331168d77efc93d6dcef1e13761890d5b764bccc74c730c3a7d743e7b6a01499'
    JWT_ERROR_MESSAGE_KEY = 'mensagem'
    JWT_HEADER_NAME = 'Authentication'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES') or 30)
    )


class DevConfig(Config):
    """
      Configuração para o ambiente de desenvolvimento.

      A propriedade de DEBUG está definida como verdadeira para
      possibilitar que a aplicação utiliza as alterações mais
      recentes sem a necessidade de reiniciá-la.

      O banco de dados utilizado pela propriedade SQLALCHEMY_DATABASE_URI
      para o ambiente de desenvolvimento é o SQLite.
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(BASEDIR, 'db.sqlite')


class TestingConfig(Config):
    """
      Configuração para o ambiente de teste.

      A propriedade TESTING está definida como verdadeira para
      que os testes unitários levem-na em conta.

      O banco de dados utilizado pela propriedade SQLALCHEMY_DATABASE_URI
      é o SQLite.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(BASEDIR, 'testing.db')


class ProdConfig(Config):
    """
      Configuração para o ambiente de produção.

      Neste caso as propriedades de DEBUG e TESTING estão desabilitadas
      para que a aplicação utilize os recursos de caching em conjunto com
      o servidor.

      O banco de dados utilizado pela propriedade SQLALCHEMY_DATABASE_URI
      é o PostgreSQL porque possui recursos mais avançados que o SQLite.

      Outra opção é utilizar o MySQL. Neste caso, a propriedade SQLALCHEMY_DATABASE_URI
      deve ser definida como mysql://username:password@hostname/database
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'postgresql://username:password@hostname/database'

    # Descomente o trecho abaixo e comente o de cima para utilizar o MySQL.
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #                          'mysql://username:password@hostname/database'


def get_config(config):
    if config == 'dev':
        return DevConfig
    elif config == 'test':
        return TestingConfig
    elif config == 'prod':
        return ProdConfig
    else:
        return DevConfig