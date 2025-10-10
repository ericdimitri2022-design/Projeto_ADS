# app.py (VERSÃO FINAL COM CSP MELHORADO PARA ANÚNCIOS)

from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

# Rota para servir o arquivo sw.js da pasta principal
@app.route('/sw.js')
def serve_sw():
    return send_from_directory(app.root_path, 'sw.js')

# Rota principal '/'
@app.route('/')
def home():
    destino_final = request.args.get('destino')
    if destino_final:
        return redirect(url_for('pagina_espera', destino=destino_final))
    
    return render_template('index.html')


# Rota '/espera' — mostra a contagem regressiva
@app.route('/espera')
def pagina_espera():
    destino_url = request.args.get('destino')
    if not destino_url:
        return redirect(url_for('home'))
    
    return render_template('espera.html', destino_url=destino_url)


# Rota '/bonus' — página secundária com anúncios extras
@app.route('/bonus')
def pagina_bonus():
    destino = request.args.get('destino')
    if not destino:
        return redirect(url_for('home'))
    
    return render_template('bonus.html', destino=destino)

# ############# INÍCIO DA ALTERAÇÃO MELHORADA #############
@app.after_request
def add_security_headers(response):
    # Usamos '*' para permitir todos os subdomínios das redes de anúncios.
    # Esta é uma abordagem mais robusta.
    csp_policy = {
        'default-src': ["'self'"],
        'script-src': [
            "'self'",
            "'unsafe-inline'",
            '*.highperformanceformat.com',
            '*.effectivegatecpm.com'
        ],
        'frame-src': [
            "'self'",
            '*.highperformanceformat.com',
            '*.effectivegatecpm.com'
        ],
        'img-src': [
            "'self'",
            'data:',
            '*.highperformanceformat.com',
            '*.effectivegatecpm.com'
        ],
        'style-src': [
            "'self'",
            "'unsafe-inline'",
            '*.highperformanceformat.com',
            '*.effectivegatecpm.com'
        ],
        'connect-src': ['*'] # Permite qualquer conexão, muito importante para ads
    }
    
    # Monta a string final do CSP
    csp_string = "; ".join([f"{key} {' '.join(values)}" for key, values in csp_policy.items()])
    
    response.headers['Content-Security-Policy'] = csp_string
    return response
# ############# FIM DA ALTERAÇÃO MELHORADA #############


if __name__ == '__main__':
    app.run(debug=True)
