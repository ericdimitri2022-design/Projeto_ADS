# app.py (VERSÃO FINAL DE TESTE - POLÍTICA SEMI-ABERTA)

from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

# ... (suas rotas não mudam e continuam corretas) ...
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
    # ############# INÍCIO DA POLÍTICA DE TESTE SEMI-ABERTA #############
    # Esta política permite que a maioria dos recursos venha de qualquer lugar.
    # É o nosso teste final para confirmar que o CSP é a causa.
    csp_policy = {
        'default-src': ["'self'"],
        'script-src': [
            "'self'",
            "'unsafe-inline'",
            "'unsafe-eval'",
            '*'  # Permite scripts de qualquer domínio
        ],
        'frame-src': [
            "'self'",
            '*'  # Permite iframes de qualquer domínio
        ],
        'img-src': ["'self'", 'data:', '*'],
        'style-src': ["'self'", "'unsafe-inline'"],
        'connect-src': ['*'] # Permite conexões com qualquer servidor
    }
    # ############# FIM DA POLÍTICA DE TESTE #############
    
    csp_string = "; ".join([f"{key} {' '.join(values)}" for key, values in csp_policy.items()])
    response.headers['Content-Security-Policy'] = csp_string
    return response

if __name__ == '__main__':
    app.run(debug=True)
