import os
from flask import Flask, request, send_from_directory, render_template_string
from datetime import datetime

app = Flask(__name__)

# Definir o diretório da pasta de uploads (dentro da pasta do usuário)
UPLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "UPLOAD_FOLDER")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Cria o diretório de upload se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Página HTML simples para upload, entrada de texto e lista de arquivos
HTML_TEMPLATE = '''
<!doctype html>
<title>Gerenciador de Arquivos</title>
<h1>Upload de um arquivo</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=Upload>
</form>

<h1>Enviar Texto</h1>
<form method=post>
  <textarea name="texto" rows="10" cols="30" placeholder="Digite seu texto aqui..."></textarea><br>
  <input type=submit value="Enviar Texto">
</form>

<h1>Arquivos disponíveis para download</h1>
<ul>
    {% for file in files %}
        <li><a href="{{ url_for('download_file', filename=file) }}">{{ file }}</a></li>
    {% endfor %}
</ul>
'''

# Página inicial com upload, envio de texto e lista de arquivos
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Verifica se o arquivo está na requisição
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return 'Nenhum arquivo selecionado'
            # Salva o arquivo
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return 'Arquivo enviado com sucesso!'

        # Verifica se o texto está na requisição
        if 'texto' in request.form:
            texto = request.form['texto']
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'conteudo_{timestamp}.txt'
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            with open(filepath, 'w') as file:
                file.write(texto)
            return f'Arquivo {filename} criado com sucesso!'

    # Lista os arquivos no diretório de upload
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template_string(HTML_TEMPLATE, files=files)

# Rota para download dos arquivos
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
