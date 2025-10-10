# app.py (VERSÃO FINAL COM CORREÇÃO PARA ANÚNCIOS)

from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

# Rota para servir o arquivo sw.js da pasta principal
@app.route('/sw.js')
def serve_sw():
    return send_from_directory(app.root_path, 'sw.js')

# Rota principal '/'
@app.route('/')
def home():
    # Página inicial (index.html)
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

# ############# INÍCIO DA NOVA ALTERAÇÃO #############
# Adiciona cabeçalhos de segurança para permitir os scripts de anúncios

@app.after_request
def add_security_headers(response):
    # Define os domínios permitidos para os scripts
    script_sources = [
        "'self'",  # Permite scripts do próprio domínio
        "'unsafe-inline'",  # Necessário para os scripts inline dos seus anúncios
        "www.highperformanceformat.com",
        "pl27813082.effectivegatecpm.com",
        "pl27806509.effectivegatecpm.com",
        "pl27806574.effectivegatecpm.com"
    ]
    # Define os domínios permitidos para iframes e conexões
    frame_sources = [
        "'self'",
        "www.highperformanceformat.com",
        "effectivegatecpm.com" # Domínio mais genérico para cobrir tudo
    ]
    
    csp = [
        f"default-src 'self'",
        f"script-src {' '.join(script_sources)}",
        f"frame-src {' '.join(frame_sources)}",
        f"connect-src *", # Permite qualquer conexão (útil para ads)
        f"style-src 'self' 'unsafe-inline'", # Permite estilos inline
        f"img-src 'self' data:" # Permite imagens do próprio domínio e data URIs
    ]
    
    response.headers['Content-Security-Policy'] = '; '.join(csp)
    return response
# ############# FIM DA NOVA ALTERAÇÃO #############


if __name__ == '__main__':
    # Em produção, o Render usa o Gunicorn, então isto é apenas para testes locais
    app.run(debug=True)
