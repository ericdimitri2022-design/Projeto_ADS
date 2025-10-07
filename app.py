from flask import Flask, request, render_template, url_for
import os

app = Flask(__name__)

# Rota principal da página de espera
@app.route('/espera')
def pagina_espera():
    # Pega a URL de destino do parâmetro na URL (ex: ?destino=...)
    destino_url = request.args.get('destino')

    # Se não for fornecida uma URL de destino, retorna um erro
    if not destino_url:
        return "Erro: URL de destino não fornecida.", 400

    # Renderiza o arquivo espera.html e passa a URL de destino para dentro dele
    return render_template('espera.html', destino_url=destino_url)

# Rota para a página inicial
@app.route('/')
def index():
    # Renderiza a página principal a partir de um arquivo HTML
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
