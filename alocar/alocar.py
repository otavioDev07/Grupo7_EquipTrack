import mysql.connector
from mysql.connector import Error
from datetime import datetime

def conectar():
    """Cria uma conexão com o banco de dados."""
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            database='equiptrack',
            user='seu_usuario',
            password='sua_senha'
        )
        if conexao.is_connected():
            print('Conexão bem-sucedida ao banco de dados')
            return conexao
    except Error as e:
        print(f'Erro ao conectar ao MySQL: {e}')
        return None

def alocar_epi(id_funcionario, id_equipamento, quantidade):
    """Aloca EPI para um funcionário."""
    try:
        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()

            # Verificar se o equipamento está disponível
            cursor.execute("SELECT quantidade FROM epi WHERE idEPI = %s", (id_equipamento,))
            resultado = cursor.fetchone()
            if resultado is None:
                print("Equipamento não encontrado.")
                return
            quantidade_disponivel = resultado[0]
            if quantidade > quantidade_disponivel:
                print("Quantidade solicitada excede a quantidade disponível.")
                return

            # Registrar a alocação no banco de dados
            data_hora = datetime.now()
            cursor.execute("""
                INSERT INTO epi_funcionário (idEquipamento, idFuncionario, dataHora, quantidade)
                VALUES (%s, %s, %s, %s)
            """, (id_equipamento, id_funcionario, data_hora, quantidade))

            # Atualizar a quantidade do equipamento
            nova_quantidade = quantidade_disponivel - quantidade
            cursor.execute("""
                UPDATE epi SET quantidade = %s WHERE idEPI = %s
            """, (nova_quantidade, id_equipamento))

            # Commit das alterações
            conexao.commit()
            print("Alocação registrada com sucesso.")
    except Error as e:
        print(f'Erro: {e}')
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()

# Exemplo de uso
id_funcionario = 1  # ID do funcionário
id_equipamento = 1  # ID do EPI
quantidade = 2      # Quantidade a ser alocada

alocar_epi(id_funcionario, id_equipamento, quantidade)
