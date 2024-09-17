# import bcrypt

# def gerar_hash(senha_plana):
#     salt = bcrypt.gensalt()
#     senha_hash = bcrypt.hashpw(senha_plana.encode('utf-8'), salt)
#     return senha_hash

# # Verificar a senha inserida pelo usuário
# def verificar_senha(senha_plana, senha_hash):
#     # Verificar se o hash da senha inserida corresponde ao hash armazenado
#     return bcrypt.checkpw(senha_plana.encode('utf-8'), senha_hash)

# senha_plana = "admin"
# senha_hash = gerar_hash(senha_plana)

# print(f"Hash gerado: {senha_hash}")

# senha = input('senha: ')
# # Verificação da senha
# if verificar_senha(senha, senha_hash):
#     print("Senha correta!")
# else:
#     print("Senha incorreta!")