from flask import Flask, render_template, request, redirect, url_for
import instaloader
import os

app = Flask(__name__)
loader = instaloader.Instaloader()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        if username:
            try:
                # Cria um diretório para armazenar as postagens
                os.makedirs(f'static/{username}', exist_ok=True)
                
                # Baixa as postagens do usuário
                loader.download_profile(username, profile_pic_only=False)
                
                # Mova as postagens para o diretório estático
                os.rename(username, f'static/{username}')
                
                return redirect(url_for('profile', username=username))
            except Exception as e:
                return f'Erro ao baixar o perfil: {e}'
    return render_template('index.html')

@app.route('/profile/<username>')
def profile(username):
    # Lista de postagens para exibir
    files = os.listdir(f'static/{username}')
    return render_template('profile.html', username=username, files=files)

if __name__ == '__main__':
    app.run(debug=True)

