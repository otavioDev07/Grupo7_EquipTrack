from flask import Flask, render_template, request, redirect, url_for
from database.conection import conecta_db 

app = Flask(__name__)

# Rota para a página de cadastro de CIPEIRO (telaadm)
@app.route('/telaadm', methods=['GET', 'POST'])
def telaadm():
    if request.method == 'POST':
        nome_supervisor = request.form['nomeSupervisor']
        cpf = request.form['CPF']
        status = request.form['status']

        try:
            # Conectar ao banco de dados
            conn = get_db_connection()
            cursor = conn.cursor()

            # Query para inserir um novo supervisor (cipeiro)
            query = """
            INSERT INTO supervisor (nomeSupervisor, CPF, status)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (nome_supervisor, cpf, status))

            # Commit e fechamento da conexão
            conn.commit()
            cursor.close()
            conn.close()

            # Redireciona para a página de cadastro
            return redirect(url_for('telaadm'))  # Redireciona para a página de cadastro

        except Exception as e:
            return f"Erro ao cadastrar CIPEIRO: {str(e)}", 500

    return render_template('telaadm.html')

# Rota para exibir a lista de cipeiros cadastrados (verciepiros)
@app.route('/vercipeiros')
def vercipeiros():
    try:
        # Conectar ao banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query para buscar todos os cipeiros cadastrados
        query = "SELECT idSupervisor, nomeSupervisor, CPF, status FROM supervisor"
        cursor.execute(query)

        # Buscar todos os resultados
        cipeiros = cursor.fetchall()

        # Fechar a conexão com o banco de dados
        cursor.close()
        conn.close()

        # Renderiza a página com a lista de cipeiros
        return render_template('verciepiros.html', cipeiros=cipeiros)

    except Exception as e:
        return f"Erro ao buscar cipeiros: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
