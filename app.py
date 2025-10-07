# app.py (VERSÃO COM SUPORTE AO sw.js)

# A importação de 'send_from_directory' é a novidade aqui
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

# --- NOVA REGRA PARA O ARQUIVO sw.js ---
# Este código ensina o servidor a encontrar o arquivo sw.js na pasta principal
@app.route('/sw.js')
def serve_sw():
    return send_from_directory(app.root_path, 'sw.js')
# -----------------------------------------

@app.route('/')
def home():
    destino_final = request.args.get('destino')

    if not destino_final:
        return render_template('verificacao.html')

    return redirect(url_for('pagina_espera', destino=destino_final))


@app.route('/espera')
def pagina_espera():
    destino_url = request.args.get('destino')
    
    if not destino_url:
        return redirect(url_for('home'))

    return render_template('espera.html', destino_url=destino_url)

if __name__ == '__main__':
    app.run(debug=True)
