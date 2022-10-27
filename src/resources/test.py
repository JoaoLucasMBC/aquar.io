def formata_data(string_data):
    valido = string_data[:10]
    um,dois,tres = valido.split('-')
    ano = um
    mes = dois
    dia = tres
    dict_data = {'year': ano, 'month': mes,'day': dia}
    return dict_data

print(formata_data_hora('2022-19-30ejoufge97duwjnmpq8'))