def valida_sign_up(email, password, user):
    if email[-16:0] != "al.insper.edu.br":
        return True

print(valida_sign_up('a@al.insper.edu.br', 1234, 123))
