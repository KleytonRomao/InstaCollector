from flask import Flask, render_template, request, redirect, url_for, send_file
import instaloader
import os
import zipfile

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
                
                # Apagar o que não seja foto
                for item in os.listdir(f'static/{username}'):
                    file_path = os.path.join(f'static/{username}', item)
                    
                    if os.path.isfile(file_path) and not item.lower().endswith('.jpg'):
                        os.remove(file_path)

                return redirect(url_for('profile', username=username))
            except Exception as e:
                return f'Erro ao baixar o perfil: {e}'
    return render_template('index.html')


@app.route('/profile/<username>')
def profile(username):
    # Lista de postagens para exibir
    files = os.listdir(f'static/{username}')
    
    # Cria o arquivo ZIP
    zip_filename = f'static/{username}.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in files:
            file_path = os.path.join(f'static/{username}', file)
            if os.path.isfile(file_path):
                zipf.write(file_path, arcname=file)
    
    return render_template('profile.html', username=username, files=files, zip_filename=zip_filename)


@app.route('/download/<username>')
def download(username):
    zip_filename = f'static/{username}.zip'
    if os.path.exists(zip_filename):
        return send_file(zip_filename, as_attachment=True)
    else:
        return 'Arquivo ZIP não encontrado', 404

if __name__ == '__main__':
    app.run(debug=True)

