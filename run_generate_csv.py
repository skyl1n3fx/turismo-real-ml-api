from request.utils import set_dwelling_data, generate_csv, dwelling_list

def main(count : int):
    data = set_dwelling_data(dwelling_list(count).get('results'))
    generate_csv('turismo_real',data)

# Generamos el csv con tope de 100 registros de viviendas
main(100)