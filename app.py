# app.py (VERSÃO FINAL COM CSP ABRANGENTE PARA ANÚNCIOS)

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
        pass 
    
    return render_template('bonus.html', destino=destino)

@app.after_request
def add_security_headers(response):
    # ############# INÍCIO DA ALTERAÇÃO FINAL #############
    # Adicionamos 'worker-src' e 'child-src' para máxima compatibilidade com anúncios
    csp_policy = {
        'default-src': ["'self'"],
        'script-src': [
            "'self'",
            "'unsafe-inline'",
            '*.victimfatalsentiments.com'
        ],
        'frame-src': [
            "'self'",
            '*.victimfatalsentiments.com'
        ],
        'img-src': [
            "'self'",
            'data:',
            '*' # Permite imagens de qualquer lugar
        ],
        'style-src': [
            "'self'",
            "'unsafe-inline'",
            '*.victimfatalsentiments.com'
        ],
        'connect-src': ['*'],
        # Novas diretivas para ajudar os anúncios a funcionar
        'worker-src': ["'self'", 'blob:'],
        'child-src': ["'self'", 'blob:']
    }
    # ############# FIM DA ALTERAÇÃO FINAL #############
    
    csp_string = "; ".join([f"{key} {' '.join(values)}" for key, values in csp_policy.items()])
    
    response.headers['Content-Security-Policy'] = csp_string
    return response


if __name__ == '__main__':
    app.run(debug=True)

