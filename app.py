# app.py

from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)

# Rota principal da página de espera
@app.route('/espera')
def pagina_espera():
    # Pega a URL de destino do parâmetro na URL (ex: ?destino=...)
    destino_url = request.args.get('destino')

    # Se não for fornecida uma URL de destino, redireciona para uma página de erro ou principal
    if not destino_url:
        # Você pode criar uma página de erro ou redirecionar para seu site principal
        return "Erro: URL de destino não fornecida.", 400

    # Renderiza o arquivo espera.html e passa a URL de destino para dentro dele
    return render_template('espera.html', destino_url=destino_url)

# Rota de exemplo para a página inicial (opcional)
@app.route('/')
def index():
    # Exemplo de como você criaria os links para a página de espera
    return """
        <h1>Página Principal</h1>
        <p>Clique nos links abaixo para testar a página de espera:</p>
        <ul>
            <li><a href="/espera?destino=https://www.google.com.br">Ir para o Google (com espera de 10s)</a></li>
            <li><a href="/espera?destino=https://www.youtube.com">Ir para o YouTube (com espera de 10s)</a></li>
        </ul>
    """

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
