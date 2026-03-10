from flask import Flask, render_template, url_for, flash, request, redirect
from sqlalchemy.exc import SQLAlchemyError

from database import db_session, Usuario, Funcionario
from sqlalchemy import select, and_, func
from flask_login import LoginManager, login_manager, login_user, logout_user, current_user, login_required



app = Flask(__name__)
app.config['SECRET_KEY'] = 'corinthans'


login_manager = LoginManager(app)
login_manager.login_view = 'login'

@app.route('/')
def home():
    return render_template("home.html")

@login_manager.user_loader

def load_user(user_id):
    user = select(Usuario).where(Usuario.id == int(user_id))
    resultado = db_session.execute(user).scalar_one_or_none()
    return resultado

@app.route('/calculos')
def calculos():
    return render_template("calculos.html")

@app.route('/operacoes')
def operacoes():
    return render_template("operacoes.html")

@app.route('/somar', methods=['GET', 'POST'])
def somar():
    if request.method == 'POST':
        if request.form['form-n1'] and request.form['form-n2']:
            n1 = int(request.form['form-n1'])
            n2 = int(request.form['form-n2'])
            soma = n1 + n2
            flash("Soma realizada", "success")
            return render_template("operacoes.html", n1=n1, n2=n2, soma=soma)
        else:
            flash("Preencha o campo", "alert-danger")
    return render_template("operacoes.html")

@app.route('/subtrair', methods=['GET', 'POST'])
def subtrair():
    if request.method == 'POST':
        if request.form['form-n1'] and request.form['form-n2']:
            n1 = int(request.form['form-n1'])
            n2 = int(request.form['form-n2'])
            sub = n1 - n2
            return render_template("operacoes.html", n1=n1, n2=n2, sub=sub)

    return render_template("operacoes.html")

@app.route('/multiplicar', methods=['GET', 'POST'])
def multiplicar():
    if request.method == 'POST':
        if request.form['form-n1'] and request.form['form-n2']:
            n1 = int(request.form['form-n1'])
            n2 = int(request.form['form-n2'])
            mul = n1 * n2
            return render_template("operacoes.html", n1=n1, n2=n2, mul=mul)

    return render_template("operacoes.html")

@app.route('/dividir', methods=['GET', 'POST'])
def dividir():
    if request.method == 'POST':
        if request.form['form-n1'] and request.form['form-n2']:
            n1 = int(request.form['form-n1'])
            n2 = int(request.form['form-n2'])
            div = n1 / n2
            return render_template("operacoes.html", n1=n1, n2=n2, div=div)

    return render_template("operacoes.html")

@app.route('/geometria')
def geometria():
    return render_template("geometria.html")

@app.route('/funcionarios', methods=['GET', 'POST'])
@login_required
def funcionarios():
    funcio = select(Funcionario)
    funcio_exe = db_session.execute(funcio).scalars().all()
    return render_template("funcionarios.html", funcio_exe=funcio_exe)





@app.route('/cadastro_funcionarios', methods=['GET', 'POST'])
def cadastrar_funcionarios():
    if request.method == 'POST':
        nome = request.form.get('form-nome')
        data_nasc = request.form.get('form-data-nasc')
        cpf = request.form.get('form-cpf')
        email = request.form.get('form-email')
        cargo = request.form.get('form-cargo')
        salario = request.form.get('form-salario')

        print(nome, data_nasc, cpf, email, salario)

        if not nome or not cpf or not email or not cargo or not salario:
            flash(f'Preencher todos os campos!', 'danger')
            return render_template("funcionarios.html")
        try:
            novo_funcionario = Funcionario(nome=nome, data_nasc=data_nasc, cpf=cpf, email=email, cargo=cargo, salario=float(salario))
            db_session.add(novo_funcionario)
            db_session.commit()
            flash(f'Funcionário {nome} criado com sucesso!', 'success')
            return redirect(url_for('funcionarios'))
        except SQLAlchemyError as e:
            flash(f'Erro ao cadastrar funcionario', 'danger')
            print(f'Erro: {e}')
            return redirect(url_for('funcionarios'))
        except Exception as e:
            flash(f'Erro ao cadastrar funcionario: {e}', 'danger')
            print(f'Erro: {e}')
            return redirect(url_for('funcionarios'))
    return render_template('funcionarios.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('form-email')
        senha = request.form.get('form-senha')
        if not email or not senha:
            flash('Email ou senha vazios!', 'alert-danger')
            return render_template("login.html")

        if email and senha:
            verificar_email = select(Usuario).where(Usuario.email == email)
            resultado = db_session.execute(verificar_email).scalar_one_or_none()
            if resultado:
                if resultado.check_password(senha):
                    login_user(resultado)
                    flash(f'Login com sucesso!', 'success')
                    return redirect(url_for('home'))
                else:
                    flash('Senha incorreta!', 'danger')
                    return render_template("login.html")
            else:
                flash(f'Usuário não encontrado!', 'danger')
                return render_template("login.html")
    else:
        return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout com sucesso!', 'success')
    return redirect(url_for('home'))


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        nome = request.form.get('form-nome')
        email = request.form.get('form-email')
        senha = request.form.get('form-senha')
        if not nome or not email or not senha:
            flash(f'Nome ou senha vazio!', 'danger')
            return render_template("cadastro.html")
        verificar_email = select(Usuario).where(Usuario.email == email)
        resultado = db_session.execute(verificar_email).scalar_one_or_none()
        if resultado:
            flash(f'Email {email} já está cadastrado!', 'danger')
            return render_template('cadastro.html')
        try:
            novo_usuario = Usuario(nome=nome, email=email)
            novo_usuario.set_password(senha)
            db_session.add(novo_usuario)
            db_session.commit()
            flash(f'Usuario {nome} cadastrado com sucesso!', 'success')
            return redirect(url_for('login'))
        except SQLAlchemyError as e:
            flash(f'Erro na base de dados ao cadastrar usuario', 'danger')
            print(f'Erro: {e}')
            return redirect(url_for('cadastro_usuario'))
        except Exception as e:
            flash(f'Erro ao cadastrar usuario: {e}', 'danger')
            print(f'Erro: {e}')
            return redirect(url_for('cadastro_usuario'))
    return render_template('cadastro.html')


@app.route('/animais')
def animais():
    return render_template('animais.html')

#TODO Final do código

if __name__ == '__main__':
    app.run(debug=True)