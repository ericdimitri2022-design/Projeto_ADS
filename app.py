# app.py (VERSÃO FINAL E SEGURA)

from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

# ... (suas rotas continuam exatamente iguais) ...
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
    # Política de segurança final, permitindo todos os seus domínios de anúncio
    csp_policy = {
        'default-src': ["'self'"],
        'script-src': [
            "'self'",
            "'unsafe-inline'",
            '*.highperformanceformat.com',  # Domínio da página de espera
            '*.effectivegatecpm.com',       # Domínio da página de espera
            '*.victimfatalsentiments.com'   # Domínio da página de bônus
        ],
        'frame-src': [
            "'self'",
            '*.highperformanceformat.com',
            '*.effectivegatecpm.com',
            '*.victimfatalsentiments.com'
        ],
        'img-src': ["'self'", 'data:', '*'],
        'style-src': ["'self'", "'unsafe-inline'"],
        'connect-src': ['*']
    }
    
    csp_string = "; ".join([f"{key} {' '.join(values)}" for key, values in csp_policy.items()])
    response.headers['Content-Security-Policy'] = csp_string
    return response

if __name__ == '__main__':
    app.run(debug=True)
