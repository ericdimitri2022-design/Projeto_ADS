# app.py (VERSÃO FINAL E AUTOMÁTICA)

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Rota principal que captura o link de destino e redireciona para a espera
@app.route('/')
def home():
    # Pega o valor do parâmetro 'destino' da URL
    # Exemplo: seusite.com/?destino=https://google.com
    destino_final = request.args.get('destino')

    # Se nenhum 'destino' for fornecido na URL, mostra uma mensagem de erro simples.
    if not destino_final:
        return "Erro: O link de destino não foi especificado. Use a URL no formato: /?destino=SEU_LINK_AQUI"

    # Redireciona o usuário para a página de espera, passando o destino para ela.
    return redirect(url_for('pagina_espera', destino=destino_final))


# Rota da página de espera que mostra o contador
@app.route('/espera')
def pagina_espera():
    # Pega o destino que foi passado pela rota principal
    destino_url = request.args.get('destino')
    
    # Se, por algum motivo, chegou aqui sem um link, redireciona para o erro
    if not destino_url:
        return redirect(url_for('home'))

    # Renderiza o template da página de espera, injetando a URL de destino final
    return render_template('espera.html', destino_url=destino_url)

if __name__ == '__main__':
    app.run(debug=True)
