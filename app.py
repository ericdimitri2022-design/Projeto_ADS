# app.py (VERSÃO COM CSP CORRIGIDO)

from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

@app.route('/sw.js')
def serve_sw():
    return send_from_directory(app.root_path, 'sw.js')

@app.route('/')
def home():
    destino_final = request.args.get('destino')
    if destino_final:
        return redirect(url_for('pagina_espera', destino=destino_final))
    return render_template('index.html')

@app.route('/espera')
def pagina_espera():
    destino_url = request.args.get('destino')
    if not destino_url:
        return redirect(url_for('home'))
    return render_template('espera.html', destino_url=destino_url)

@app.route('/bonus')
def pagina_bonus():
    destino = request.args.get('destino')
    if not destino:
        return redirect(url_for('home'))
    return render_template('bonus.html', destino=destino)

@app.after_request
def add_security_headers(response):
    csp_policy = {
        'default-src': ["'self'"],
        'script-src': [
            "'self'",
            "'unsafe-inline'",
            "'unsafe-eval'",
            '*'
        ],
        'frame-src': [
            "'self'",
            '*'
        ],
        'img-src': ["'self'", 'data:', '*'],
        'style-src': [
            "'self'",
            "'unsafe-inline'",
            'https://fonts.googleapis.com' # Permite o CSS das fontes
        ],
        # ##### LINHA ADICIONADA PARA CORRIGIR O LAYOUT #####
        'font-src': ["'self'", 'https://fonts.gstatic.com'], # Permite os arquivos das fontes
        'connect-src': ['*']
    }
    
    csp_string = "; ".join([f"{key} {' '.join(values)}" for key, values in csp_policy.items()])
    response.headers['Content-Security-Policy'] = csp_string
    return response

if __name__ == '__main__':
    app.run(debug=True)
