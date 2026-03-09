from flask_login import UserMixin
from sqlalchemy import create_engine, String, Integer, func, Column, DateTime, Float
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from werkzeug.security import generate_password_hash, check_password_hash
engine = create_engine('mysql+pymysql://root:senaisp@localhost:3306/empresa_db')


db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class Usuario(Base, UserMixin):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    senha = Column(String(255), nullable=False)
    email = Column(String, nullable=False, unique=True)
    criado_em = Column(DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return f'<Usuario {self.nome}>'

    def set_password(self, password):
        self.senha = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha, password)

    def save(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except SQLAlchemyError:
            db_session.rollback()
            raise

class Funcionario(Base, UserMixin):
    __tablename__ = 'funcionarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    data_nasc = Column(String, nullable=False)
    cargo = Column(String, nullable=False)
    salario = Column(Float, nullable=False)

    def __repr__(self):
        return f'<Funcionario {self.nome}>'

    def set_password(self, password):
        self.senha = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.senha, password)
    def save(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except SQLAlchemyError:
            db_session.rollback()
            raise


def create_tables():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    create_tables()
    print('Tables created')
