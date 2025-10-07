# app.py (VERSÃO CORRIGIDA E FUNCIONAL)

from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

# Rota para servir o arquivo sw.js da pasta principal
@app.route('/sw.js')
def serve_sw():
    return send_from_directory(app.root_path, 'sw.js')

# Rota principal '/'
@app.route('/')
def home():
    # Esta página agora vai renderizar o seu 'index.html' como uma página de testes.
    # Se alguém tentar acessar diretamente com um '?destino=', será redirecionado.
    destino_final = request.args.get('destino')
    if destino_final:
        return redirect(url_for('pagina_espera', destino=destino_final))
    
    # Se não houver 'destino', mostra a página inicial de testes.
    return render_template('index.html')


# Rota '/espera' que mostra a contagem regressiva
@app.route('/espera')
def pagina_espera():
    destino_url = request.args.get('destino')
    
    if not destino_url:
        return redirect(url_for('home'))

    return render_template('espera.html', destino_url=destino_url)

if __name__ == '__main__':
    # Em produção, o Render.com usa o Gunicorn, então esta parte é para testes locais.
    app.run(debug=True)
