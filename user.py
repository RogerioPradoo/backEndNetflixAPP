from operator import or_
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from flask import Flask, Response, request, jsonify
from dataclasses import dataclass
from sqlalchemy.orm import declarative_base,  sessionmaker
import json
import bcrypt
import random

from flask_login import LoginManager, login_user, UserMixin
import jwt
from datetime import datetime


app = Flask(__name__)

login_manager = LoginManager()
Base = declarative_base()

login_manager.init_app(app)
app.config['SECRET_KEY'] = 'secret'


@login_manager.user_loader
def get_user(user_id):
    logado = Usuario.query.filter_by(id=user_id).first()
    return logado


@dataclass
class Usuario(Base, UserMixin):

    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(20), nullable=False)
    password = Column(String(200), nullable=False)
    telefone = Column(String(20), nullable=False)

    def __init__(self, nome, email, password, telefone):
        self.nome = nome
        self.email = email
        self.password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())
        self.telefone = telefone

    def __repre__(self):
        return f"({self.nome} {self.email} {self.password} {self.telefone})"

    def to_json(self):
        return {"id": self.id, "nome": self.nome, "email": self.email, "password": self.password, "telefone": self.telefone}


class Filme(Base):
    __tablename__ = "filme"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    autores = Column(String(100), nullable=False)
    categoria = Column(String(50), nullable=False)
    descricao = Column(String(500), nullable=False)
    avaliacao = Column(Integer, nullable=False)
    duracao = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)
    img = Column(String(300))
    trailer = Column(String(300))

    def __init__(self, nome, autores, categoria, descricao, avaliacao, duracao, ano, img, trailer):
        self.nome = nome
        self.autores = autores
        self.categoria = categoria
        self.descricao = descricao
        self.avaliacao = avaliacao
        self.duracao = duracao
        self.ano = ano
        self.img = img
        self.trailer = trailer

    def __repre__(self):
        return f"({self.nome} {self.autores} {self.categoria} {self.descricao} {self.avaliacao} {self.duracao} {self.ano} {self.img} {self.trailer})"

    def to_json(self):
        return {"id": self.id, "nome": self.nome, "autores": self.autores, "categoria": self.categoria, "descricao": self.descricao, "avaliacao": self.avaliacao, "duracao": self.duracao, "ano": self.ano, "img": self.img, "trailer": self.trailer}


class Serie(Base):
    __tablename__ = "serie"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    autores = Column(String(100), nullable=False)
    categoria = Column(String(50), nullable=False)
    descricao = Column(String(500), nullable=False)
    avaliacao = Column(Integer, nullable=False)
    duracao = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)
    img = Column(String(300))
    trailer = Column(String(300))
    tipo = Column(String(10))

    def __init__(self, nome, autores, categoria, descricao, avaliacao, duracao, ano, img, trailer, tipo):
        self.nome = nome
        self.autores = autores
        self.categoria = categoria
        self.descricao = descricao
        self.avaliacao = avaliacao
        self.duracao = duracao
        self.ano = ano
        self.img = img
        self.trailer = trailer
        self.tipo = tipo

    def __repre__(self):
        return f"({self.nome} {self.autores}  {self.categoria} {self.descricao} {self.avaliacao} {self.duracao} {self.ano} {self.img} {self.trailer}  {self.tipo})"

    def to_json(self):
        return {"id": self.id, "nome": self.nome, "autores": self.autores, "categoria": self.categoria, "descricao": self.descricao, "avaliacao": self.avaliacao, "duracao": self.duracao, "ano": self.ano, "img": self.img, "trailer": self.trailer,  "tipo": self.tipo}


class Temporada(Base):
    __tablename__ = "temporada"
    id = Column(Integer, primary_key=True, autoincrement=True)
    idSerie = Column(Integer, ForeignKey(Serie.id), nullable=False)
    tempo = Column(Integer, nullable=False)

    def __init__(self, idSerie, tempo):
        self.idSerie = idSerie
        self.tempo = tempo

    def __repre__(self):
        return f"({self.idSerie} {self.tempo})"

    def to_json(self):
        return {"id": self.id, "idSerie": self.idSerie}


class Episodio(Base):
    __tablename__ = "episodio"
    id = Column(Integer, primary_key=True, autoincrement=True)
    idEpisodio = Column(Integer, nullable=False)
    idTemporada = Column(Integer, ForeignKey(Temporada.id))
    titulo = Column(String(50), nullable=False)
    descri = Column(String(500), nullable=False)
    dura = Column(Integer, nullable=False)

    def __init__(self, idEpisodio, idTemporada, titulo, descri, dura):
        self.idEpisodio = idEpisodio
        self.idTemporada = idTemporada
        self.titulo = titulo
        self.descri = descri
        self.dura = dura

    def __repre__(self):
        return f"({self.idEpisodio} {self.idTemporada} {self.titulo} {self.descri} {self.dura})"

    def to_json(self):
        return {"id": self.id, "idEpisodio": self.idEpisodio,  "idTemporada": self.idTemporada, "titulo": self.titulo, "descri": self.descri, "dura": self.dura}


class Contas(Base):

    __tablename__ = "contas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    idUsuario = Column(Integer, ForeignKey(Usuario.id))
    nome = Column(String(50), nullable=False)
    password = Column(String(200), nullable=True)

    def __init__(self, idUsuario, nome,  password):
        self.idUsuario = idUsuario
        self.nome = nome
        self.password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())

    def __repre__(self):
        return f"( {self.idUsuario} {self.nome} {self.password} )"

    def to_json(self):
        return {"id": self.id, "idUsuario": self.idUsuario, "nome": self.nome, "password": self.password}


class Lista(Base):
    __tablename__ = "lista"
    id = Column(Integer, primary_key=True, autoincrement=True)
    idUsuario = Column(Integer,  ForeignKey(Contas.id))
    idFilme = Column(Integer, nullable=True)
    idSerie = Column(Integer, nullable=True)

    def __init__(self, idUsuario, idFilme, idSerie):
        self.idUsuario = idUsuario
        self.idFilme = idFilme
        self.idSerie = idSerie

    def __repre__(self):
        return f"({self.idUsuario} {self.idFilme} {self.idSerie})"

    def to_json(self):
        return {"id": self.id, "idUsuario": self.idUsuario, "idFilme": self.idFilme, "idSerie": self.idSerie}


engine = create_engine("mysql://root:@127.0.0.1/algo", echo=True)

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


@app.route("/buscar/<id>", methods=["GET"])
def seleciona_clientes(id):

    try:
        contas = session.query(Contas).filter(Contas.idUsuario == id)
        conta = [usuario.to_json() for usuario in contas]

        return gera_response(201, conta.to_json())
    except Exception as e:
        print('erro', e)
        return gera_response(400, "usuario", {}, "Erro ao cadastrarr")


@app.route('/home', methods=["GET"])
def seleciona_Homes():

    try:
        filmes = session.query(Filme).all()
        salvarFilmes = [film.to_json() for film in filmes]

        series = session.query(Serie).all()
        salvarSeries = [serie.to_json() for serie in series]

        todos = salvarFilmes + salvarSeries
        random.shuffle(todos)

        n = 5
        final = [todos[i * n:(i + 1) * n]
                 for i in range((len(todos) + n - 1) // n)]

        filmes = final

        return json.dumps(filmes)
    except Exception as e:
        print('erro', e)
        return gera_response(404, "", {[]}, "Nenhum item encontrado.")


@app.route("/buscarserie", methods=["GET"])
def todasSerie():

    try:
        series = session.query(Serie).all()
        salvarSeries = [serie.to_json() for serie in series]

        todos = salvarSeries
        random.shuffle(todos)

        n = 5
        final = [todos[i * n:(i + 1) * n]
                 for i in range((len(todos) + n - 1) // n)]

        filmes = final

        return json.dumps(filmes)
    except Exception as e:
        print('erro', e)
        return gera_response(404, "", {[]}, "Nenhuma serie localizada. ")


@app.route("/buscarfilme", methods=["GET"])
def seleciona_Filmes():
    try:
        series = session.query(Filme).all()
        salvar = [serie.to_json() for serie in series]

        n = 5
        todos = salvar
        random.shuffle(todos)
        final = [salvar[i * n:(i + 1) * n]
                 for i in range((len(todos) + n - 1) // n)]

        return json.dumps(final)
    except Exception as e:
        print('erro', e)
        return gera_response(404, "usuario", {[]}, "Nenhum filme localizado.")


@app.route("/adicionar",  methods=["POST"])
def adiciona():

    try:
        nome = request.json['nome']
        email = request.json['email']
        password = request.json['password']
        telefone = request.json['telefone']

        user = Usuario(nome, email, password, telefone)
        session.add(user)
        session.commit()
        return gera_response(201, "Usuario", user.to_json(), "criado com sucesso")
    except Exception as e:
        print('erro', e)
        return gera_response(400, "usuario", {}, "Erro ao cadastrarr")


@app.route("/adicionarContas",  methods=["POST"])
def adiciona_conta():

    usuari = session.query(Contas).all()

    if len(usuari) >= 5:
        return gera_response(400, "usuario", {}, "Numero de contas atingido.")

    try:
        id = request.json['id']
        nome = request.json['nome']
        password = request.json['password']

        idEncontrado = session.query(
            Usuario).filter(Usuario.id == id)

        for algo in idEncontrado:
            idEncontrado = algo.id
        idUsuario = idEncontrado

        user = Contas(idUsuario, nome, password)
        session.add(user)
        session.commit()
        return gera_response(201, "Usuario", {}, "Conta criada com sucesso")
    except Exception as e:
        print('erro', e)
        return gera_response(404, "usuario", {}, "Id não encontrado")


@app.route("/adicionarFilme", methods=["POST"])
def adiciona_filme():

    try:
        nome = request.json['nome']
        autores = request.json['autores']
        categoria = request.json['categoria']
        descricao = request.json['descricao']
        avaliacao = request.json['avaliacao']
        duracao = request.json['duracao']
        ano = request.json['ano']
        img = request.json['img']

        filmes = Filme(nome, autores, categoria, descricao,
                       avaliacao, duracao, ano, img)
        session.add(filmes)
        session.commit()
        return gera_response(201, "Filme", filmes.to_json(), "Filme adicionado com sucesso")
    except Exception as e:
        print('erro', e)
        return gera_response(400, "usuario", {}, "Erro ao cadastrar filme")


@app.route("/adicionarSerie", methods=["POST"])
def adiciona_Serie():

    try:
        nome = request.json['nome']
        autores = request.json['autores']
        categoria = request.json['categoria']
        descricao = request.json['descricao']
        avaliacao = request.json['avaliacao']
        duracao = request.json['duracao']
        ano = request.json['ano']
        temporada = request.json['temporada']
        episodio = request.json['episodio']
        img = request.json['img']
        trailer = request.json['trailer']

        series = Serie(nome, autores, categoria, descricao,
                       avaliacao, duracao, ano, temporada, episodio, img, trailer)

        session.add(series)
        session.commit()
        return gera_response(201, "Serie", {}, "Serie adicionada com sucesso")
    except Exception as e:
        print('erro', e)
        return gera_response(400, "usuario", {}, "Erro ao cadastrar serie")


@app.route("/atualizar/<id>", methods=["PATCH"])
def mudar_conta(id):

    try:
        usuario = session.query(Usuario).filter(Usuario.id == id)
        usuario.nome = request.json['nome']
        usuario.email = request.json['email']
        usuario.password = request.json['password']
        usuario.telefone = request.json['telefone']

        user = Usuario(usuario.nome, usuario.email,
                       usuario.password, usuario.telefone)

        session.add(user)
        session.commit()
        return gera_response(201, "Usuario", user.to_json(), "Usuario alterado com sucesso")
    except Exception as e:
        print('erro', e)
        return gera_response(400, "usuario", {}, "Erro ao atualizar o usuario")


@app.route("/excluir/<id>", methods=["DELETE"])
def excluir(id):
    try:
        usuari = session.query(Usuario).filter(Usuario.id == id)
        for algo in usuari:
            session.delete(algo)
            session.commit()

        return gera_response(201, "Usuario", algo.to_json(), "Excluido com sucesso")
    except Exception as e:
        print('erro', e)
        return gera_response(400, "usuario", {}, "Erro ao excluir o usuario")


@app.route("/excluirConta/<id>", methods=["DELETE"])
def excluir_conta(id):
    try:
        lista = session.query(Lista).filter(Lista.idUsuario == id)
        for excluirFilmes in lista:
            session.delete(excluirFilmes)
            session.commit()

        usuario = session.query(Contas).filter(Contas.id == id)
        for dados in usuario:
            session.delete(dados)
            session.commit()

        return gera_response(201, "Usuario", {}, "Conta excluida com sucesso")
    except Exception as e:
        print('erro', e)
        return gera_response(400, "usuario", {}, "Erro ao excluir a conta")


@app.route("/login", methods=["GET", "POST"])
def login_conta():

    exp_tempo = datetime.now()
    exp_tempoExpirado = int(exp_tempo.timestamp())
    load = {
        "payload": str(exp_tempo),
        "exp": exp_tempoExpirado
    }

    token = jwt.encode(load, "sagar", algorithm="HS256")

    try:
        email = request.json['email']
        password = request.json['password']

        usuarioEmail = session.query(Usuario).filter_by(email=email).first()

        usuarioLogado = session.query(Usuario).filter(Usuario.email == email)
        teste = [usuario.to_json() for usuario in usuarioLogado]
        categorias = {"usuario": teste[0], "token": token}

        if not email:
            return "Erro no email", 400

        if not password:
            return "Erro na senha", 400

        if not usuarioEmail:
            return "User não encontrado.", 404

        if bcrypt.checkpw(password.encode('utf-8'), usuarioEmail.password.encode('utf-8')):
            login_user(usuarioEmail)

            return json.dumps(categorias)

        else:
            return "Erro de senha", 404

    except Exception as e:
        print('erro', e)
        return gera_response(400, "usuario", {}, "Erro ao fazer login")


@app.get("/buscaar/<id>")
def selecionaUmCliente(id):

    try:
        lista = session.query(Lista).filter(Lista.idUsuario == id)

        guardarDadosEncontrados = [filmes.to_json() for filmes in lista]
        idFilmes = []
        idSeries = []
        acheiFilme = []
        filmesGuardados = []
        seriesGuardadas = []

        for pegarId in guardarDadosEncontrados:
            acheiFilme = pegarId['idFilme']
            idFilmes.append(acheiFilme)
            filmesGuardados = session.query(Filme).filter(
                Filme.id.in_(idFilmes)).all()

        for pegarId in guardarDadosEncontrados:
            acheiSerie = pegarId['idSerie']
            idSeries.append(acheiSerie)

            seriesGuardadas = session.query(Serie).filter(
                Serie.id.in_(idSeries)).all()

        film = [listagem.to_json() for listagem in filmesGuardados]
        seri = [pessoa.to_json() for pessoa in seriesGuardadas]

        filmesEseries = film + seri
        return json.dumps(filmesEseries)
    except Exception as e:
        print('erro', e)
        return gera_response(400, "usuario", {[]}, "Nenhum item encontrado.")


@app.route("/adicionarLista", methods=["POST"])
def salvarLista():
    nome = request.json['nome']
    idUsuario = request.json["id"]

    guardarFilme = ''
    guardarSerie = ''
    filmes = ''
    series = ''

    escolhido = session.query(Filme).filter(Filme.nome == nome)
    for pegarId in escolhido:
        achei = pegarId.id
        guardarFilme = achei

    escolhido = session.query(Serie).filter(Serie.nome == nome)
    for pegarId in escolhido:
        achei = pegarId.id
        guardarSerie = achei

    procurarGeral = session.query(Lista).filter(Lista.idUsuario == idUsuario)
    resultado = [result.to_json() for result in procurarGeral]
    for detalhes in resultado:
        filmes = detalhes['idFilme']
        series = detalhes['idSerie']
        if filmes == guardarFilme:
            guardarFilme = None
        if series == guardarSerie:
            guardarSerie = None

    if guardarFilme == '':
        guardarFilme = None

    if guardarSerie == '':
        guardarSerie = None

    try:
        idFilme = guardarFilme
        idSerie = guardarSerie
        if idFilme == None and idSerie == None:
            return gera_response(400, "usuario", {}, "Já esta adicionada.")
        adicionados = Lista(idUsuario, idFilme, idSerie)
        session.add(adicionados)
        session.commit()
        return gera_response(201, "Usuario", adicionados.to_json(), "criado com sucesso")
    except Exception as e:
        print('erro', e)
        return gera_response(400, "usuario", {}, "Erro ao cadastrarr")


@app.route("/lista/<id>", methods=["GET"])
def selecionarLista(id):
    idFilmes = []
    filmes = ''
    series = ''

    try:
        lista = session.query(Lista).filter(Lista.idUsuario == id)
        resultado = [result.to_json() for result in lista]

        for detalhes in resultado:
            filmes = detalhes['idFilme']
            if filmes != None:
                idFilmes.append(filmes)

            series = detalhes['idSerie']
            if series != None:
                idFilmes.append(series)

        return json.dumps(idFilmes)

    except Exception as e:
        print('erro', e)
        return gera_response(400, "usuario", {[]}, "Nenhum item encontrado.")


@app.route("/excluirFilmeLista/<id>", methods=["DELETE"])
def excluir_filmeLista(id):
    try:
        idFilme = session.query(Lista).filter(Lista.idFilme == id)
        idSerie = session.query(Lista).filter(Lista.idSerie == id)

        for pegouFilme in idFilme:
            session.delete(pegouFilme)
            session.commit()

        for pegouSerie in idSerie:
            session.delete(pegouSerie)
            session.commit()

        return gera_response(201, "Filme", {}, "Excluido com sucesso")
    except Exception as e:
        print('erro', e)
        return gera_response(400, "usuario", {[]}, "Erro ao excluir.")


@app.route("/recuperar", methods=["GET", "PATCH"])
def recuperar():

    try:
        email = request.json['email']
        senha = request.json['senha']
        confirmacaoSenha = request.json['confirmacaoSenha']

        usuarioEmail = session.query(Usuario).filter_by(email=email).first()

        if not usuarioEmail:
            return "User não encontrado.", 404

        if senha == confirmacaoSenha:
            senhaCripto = bcrypt.hashpw(
                confirmacaoSenha.encode('utf-8'), bcrypt.gensalt())
            usuarioEmail.password = senhaCripto
        else:
            return "Senha não compatível", 404

        return gera_response(201, "", {}, "Senha alterada com sucesso !")

    except Exception as e:
        print('erro', e)
        return gera_response(404, "", {}, "Erro ao atualiza a senha.")


@app.route("/configuracao", methods=["PATCH"])
def configurar():

    try:
        id = request.json['id']

        usuario = session.query(
            Contas).filter(Contas.id == id).first()

        body = request.get_json()

        if ('nome' in body):
            usuario.nome = body['nome']

        if ('senha' in body):
            pegarSenha = body['senha']

            senhaCripto = bcrypt.hashpw(
                pegarSenha.encode('utf-8'), bcrypt.gensalt())

            usuario.password = senhaCripto

        session.add(usuario)
        session.commit()
        return gera_response(200, "Usuario", usuario.to_json(), "Alterado com sucesso")

    except Exception as e:
        print('erro', e)
        return gera_response(400, "usuario", {}, "Erro do servidor")


@app.get("/seriesETempo/<id>")
def selSerieETEMP(id):

    try:
        temporadas = session.query(Temporada).filter(
            Temporada.idSerie == id).all()
        guardarDadosEncontrados = [filmes.to_json() for filmes in temporadas]

        idFilmes = []
        acheiFilme = []
        filmesGuardados = []

        for pegarId in guardarDadosEncontrados:
            acheiFilme = pegarId['id']
            idFilmes.append(acheiFilme)

        filmesGuardados = session.query(Episodio).filter(
            Episodio.idTemporada.in_(idFilmes)).all()

        film = [listagem.to_json() for listagem in filmesGuardados]

        return json.dumps(film)
    except Exception as e:
        print('erro', e)
        return gera_response(400, "usuario", {}, "Nenhum item encontrado. ")


def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if (mensagem):
        body["mensagem"] = mensagem
    return Response(json.dumps(body), status, mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
