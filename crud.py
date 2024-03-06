from pathlib import Path

from sqlalchemy import create_engine, String, Boolean, Integer , select, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, Relationship

from werkzeug.security import generate_password_hash, check_password_hash

pasta_atual = Path(__file__).parent
PATH_TO_BD = pasta_atual / 'bd_usuarios.sqlite'

class Base(DeclarativeBase):
    pass

class UsuarioFerias(Base):
    __tablename__ = 'usuarios_ferias'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(30))
    senha: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(30))
    acesso_gestor: Mapped[bool] = mapped_column(Boolean(), default=False)
    inicio_empresa: Mapped[str] = mapped_column(String(30))
    eventos_ferias: Mapped[list["EventosFerias"]] = Relationship(lazy='subquery', back_populates="parent")

    def __repr__(self):
        return f"Usuario({self.id=}, {self.nome=})"
    
    def define_senha(self, senha):
        self.senha = generate_password_hash(senha)

    def verifica_senha(self, senha):
        return check_password_hash(self.senha, senha)
    
class EventosFerias(Base):
    __tablename__ = 'eventos_ferias'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey('usuarios_ferias.id'))
    parent: Mapped[UsuarioFerias] = Relationship(lazy='subquery')
    inicio_ferias: Mapped[str] = mapped_column(String(30))
    fim_ferias: Mapped[str] = mapped_column(String(30))
    total_dias: Mapped[int] = mapped_column(Integer())

    def __repr__(self):
        return f"EventosFerias({self.id=}, {self.id_usuario=}, {self.data_inicio=}, {self.data_fim=}, {self.aprovado=})"

    def verifica_senha(self, senha):
        return check_password_hash(self.senha, senha)
    
     
    
engine = create_engine(f'sqlite:///{PATH_TO_BD}')
Base.metadata.create_all(bind=engine)


# CRUD ======================
def cria_usuarios(
        nome,
        senha,
        email,
        **kwargs
):
    with Session(bind=engine) as session:
        usuario = UsuarioFerias(
            nome=nome,
            email=email,
            **kwargs
        )
        usuario.define_senha(senha)
        session.add(usuario)
        session.commit()

def le_todos_usuarios():
    with Session(bind=engine) as session:
        comando_sql = select(UsuarioFerias)
        usuarios = session.execute(comando_sql).fetchall()
        usuarios = [user[0] for user in usuarios]
        return usuarios

def le_usuario_por_id(id):
    with Session(bind=engine) as session:
        comando_sql = select(UsuarioFerias).filter_by(id=id)
        usuarios = session.execute(comando_sql).fetchall()
        return usuarios[0][0]

def modifica_usuario_old(
        id, 
        nome=None,
        senha=None,
        email=None,
        acesso_gestor=None
        ):
    with Session(bind=engine) as session:
        comando_sql = select(UsuarioFerias).filter_by(id=id)
        usuarios = session.execute(comando_sql).fetchall()
        for usuario in usuarios:
            if nome:
                usuario[0].nome = nome
            if senha:
                usuario[0].senha = senha
            if email:
                usuario[0].email = email
            if not acesso_gestor is None:
                usuario[0].acesso_gestor = acesso_gestor
        session.commit()

def modifica_usuario(
        id, 
        **kwargs
        ):
    with Session(bind=engine) as session:
        comando_sql = select(UsuarioFerias).filter_by(id=id)
        usuarios = session.execute(comando_sql).fetchall()
        for usuario in usuarios:
            for key, value in kwargs.items():
                if key == 'senha':
                    usuario[0].define_senha(value)
                else:
                    setattr(usuario[0], key, value)
        session.commit()

def deleta_usuario(id):
    with Session(bind=engine) as session:
        comando_sql = select(UsuarioFerias).filter_by(id=id)
        usuarios = session.execute(comando_sql).fetchall()
        for usuario in usuarios:
            session.delete(usuario[0])
        session.commit()


if __name__ == '__main__':
    
    pass
    
    #     cria_usurios(
    #     'Clara Cavalcante',
    #     senha='thia',
    #     email="clara.bonancea@hotmail.com",
    #     inicio_empresa='2020-01-01',
    #     acesso_gestor=False,
    # )
    
    
    # cria_usurios(
    #     'Thiarly Cavalcante',
    #     senha='thia',
    #     email="thiarly.cavalcante@live.com",
    #     inicio_empresa='2021-01-01',
    #     acesso_gestor=True,
    # )
    
    
    # cria_usurios(
    #     'Luca Cavalcante',
    #     senha='thia',
    #     email="luca.bonancea@hotmail.com",
    #     inicio_empresa='2023-01-01',
    #     acesso_gestor=True,
    # )