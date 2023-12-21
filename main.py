import csv
import os

def cadastrar_usuario():
    # Esta função permite cadastrar um novo usuário.
    nome_usuario = input('Escolha um nome de usuário: ')
    senha = input('Escolha uma senha: ')

    id_usuario = 1
    if os.path.isfile('usuarios.csv'):
        with open('usuarios.csv', 'r') as arquivo:
            leitor_csv = csv.reader(arquivo)
            id_usuario = sum(1 for linha in leitor_csv)

    with open('usuarios.csv', 'a', newline='') as arquivo:
        escritor_csv = csv.writer(arquivo)
        if id_usuario == 1:  # Caso seja o primeiro usuário.
            escritor_csv.writerow(['id_usuario', 'nome_usuario', 'senha'])
        escritor_csv.writerow([id_usuario, nome_usuario, senha])
    
    print('Usuário cadastrado com sucesso!')

def login():
    # Esta função verifica o nome de usuário e senha para login.
    nome_usuario = input('Nome de usuário: ')
    senha = input('Senha: ')

    with open('usuarios.csv', 'r') as arquivo:
        leitor_csv = csv.DictReader(arquivo)
        for linha in leitor_csv:
            if linha['nome_usuario'] == nome_usuario and linha['senha'] == senha:
                print('Login bem-sucedido!')
                return int(linha['id_usuario'])
    print('Login ou senha incorretos!')
    return None

def ler_dados(arquivo_nome):
    # Esta função lê os dados de um arquivo CSV e retorna uma lista de dicionários.
    try:
        with open(arquivo_nome, 'r', newline='') as arquivo:
            return list(csv.DictReader(arquivo))
    except FileNotFoundError:
        return []

def adicionar_valor(arquivo_nome, novo_valor):
    cabecalho = ['Categoria', 'Pedido', 'Nota', 'Valor', 'Descricao', 'status', 'id_usuario']
    
    modo = 'a' if os.path.isfile(arquivo_nome) else 'w'
    with open(arquivo_nome, modo, newline='') as arquivo:
        escritor_csv = csv.DictWriter(arquivo, fieldnames=cabecalho)
        if modo == 'w':
            escritor_csv.writeheader()
        escritor_csv.writerow(novo_valor)

def imprimir_dados(arquivo_nome):
    # Esta função imprime os dados de um arquivo CSV.
    try:
        with open(arquivo_nome, 'r') as arquivo:
            leitor_csv = csv.DictReader(arquivo)
            for linha in leitor_csv:
                print(', '.join(f'{k}: {v}' for k, v in linha.items()))
                print('-' * 30)
    except FileNotFoundError:
        print(f'O arquivo "{arquivo_nome}" não foi encontrado.')

def baixa_lancamento(arquivo_nome):
    imprimir_dados(arquivo_nome)  # Mostrar os lançamentos abertos
    try:
        escolha = input('Escolha uma opção para dar baixa:\n1. Por número do pedido\n2. Por número da nota fiscal\nOpção escolhida: ')
        campo_busca = 'Pedido' if escolha == '1' else 'Nota' if escolha == '2' else None

        if campo_busca:
            numero = input(f'Insira o número do {campo_busca} do lançamento para dar baixa: ')

            dados = ler_dados(arquivo_nome)
            encontrado = False
            for lancamento in dados:
             if lancamento['status'] == 'Aberto' and lancamento[campo_busca] == numero:
                lancamento['status'] = 'Finalizado'
                encontrado = True
                # Atualize o arquivo CSV com o novo status
                with open(arquivo_nome, 'w', newline='') as arquivo:
                    cabecalho = ['Categoria', 'Pedido', 'Nota', 'Valor', 'Descricao', 'status', 'id_usuario']
                    escritor_csv = csv.DictWriter(arquivo, fieldnames=cabecalho)
                    escritor_csv.writeheader()
                    escritor_csv.writerows(dados)
                print('Baixa do lançamento realizada com sucesso.')
                break
            
            if not encontrado:
                print(f'Nenhum lançamento com {campo_busca} "{numero}" encontrado ou já está finalizado.')
        else:
            print('Opção inválida. Tente novamente.')
    except ValueError:
        print('Entrada inválida. Digite um número válido.')

def excluir_lancamento(arquivo_nome):
    imprimir_dados(arquivo_nome)  # Mostrar os lançamentos
    try:
        escolha = input('Escolha uma opção para excluir:\n1. Por número do pedido\n2. Por número da nota fiscal\nOpção escolhida: ')
        campo_busca = 'Pedido' if escolha == '1' else 'Nota' if escolha == '2' else None

        if campo_busca:
            numero = input(f'Insira o número do {campo_busca} do lançamento para excluir: ')

            dados = ler_dados(arquivo_nome)
            dados_atualizados = [lancamento for lancamento in dados if lancamento[campo_busca] != numero]

            if len(dados_atualizados) < len(dados):
                # Atualizar o arquivo CSV
                with open(arquivo_nome, 'w', newline='') as arquivo:
                    cabecalho = ['Categoria', 'Pedido', 'Nota', 'Valor', 'Descricao', 'status', 'id_usuario']
                    escritor_csv = csv.DictWriter(arquivo, fieldnames=cabecalho)
                    escritor_csv.writeheader()
                    escritor_csv.writerows(dados_atualizados)
                print('Lançamento excluído com sucesso.')
            else:
                print(f'Nenhum lançamento com {campo_busca} "{numero}" encontrado.')
        else:
            print('Opção inválida. Tente novamente.')
    except ValueError:
        print('Entrada inválida. Digite um número válido.')
      
def contas_a_pagar(id_usuario):
    print('A opção escolhida foi Contas a Pagar')
    Categoria_pg = input('Insira a Categoria do lançamento: ').strip().capitalize()
    if not Categoria_pg:
        print("Categoria inválida.")
        return

    pedido_pg = input('Insira o número do pedido: ').strip()
    if not pedido_pg:
        print("Número do pedido inválido.")
        return

    nf_pg = input('Insira o número da NF: ').strip()
    if not nf_pg:
        print("Número da NF inválido.")
        return

    valor_str = input('Insira o valor: ').replace(',', '.').strip()
    if not valor_str:
        print("Valor inválido.")
        return

    try:
        valor_pg = float(valor_str)
    except ValueError:
        print("Valor inválido. Certifique-se de usar um número correto.")
        return

    descricao_pg = input('Descrição: ').strip()
    if not descricao_pg:
        print("Descrição inválida.")
        return
    novo_valor_pagar = {
        'Categoria': Categoria_pg,
        'Pedido': pedido_pg,
        'Nota': nf_pg,
        'Valor': valor_pg,
        'Descricao': descricao_pg,
        'status': 'Aberto',
        'id_usuario': id_usuario
    }
    adicionar_valor('contas_pagar.csv', novo_valor_pagar)
    print('Lançamento concluído!')

def contas_a_receber(id_usuario):
    print('A opção escolhida foi Contas a Receber')
    Categoria_cr = input('Insira a Categoria do lançamento: ').strip().capitalize()
    pedido_cr = input('Insira o número do pedido: ')
    nf_cr = input('Insira o número da NF: ')
    valor_str = input('Insira o valor: ').replace(',', '.').strip()
    try:
        valor_cr = float(valor_str)
    except ValueError:
        print("Valor inválido. Certifique-se de usar um número correto.")
        return
    descricao_cr = input('Descrição: ')
    novo_valor_receber = {
        'Categoria': Categoria_cr,
        'Pedido': pedido_cr,
        'Nota': nf_cr,
        'Valor': valor_cr,
        'Descricao': descricao_cr,
        'status': 'Aberto',
        'id_usuario': id_usuario
    }
    adicionar_valor('contas_receber.csv', novo_valor_receber)
    print('Lançamento concluído!')


def menu():
    id_usuario = None
    while True:
        if id_usuario is None:
            print("1. Login\n2. Cadastrar\n3. Sair")
            opcao = input("Opção escolhida: ")
            if opcao == '1':
                id_usuario = login()
            elif opcao == '2':
                cadastrar_usuario()
            elif opcao == '3':
                break
        else:
            op = input(f'Escolha uma das opções \n'
                        f'1. Contas a Pagar \n'
                        f'2. Contas a Receber \n'
                        f'3. Ver Lançamentos PG \n'
                        f'4. Ver Lançamentos CR \n'
                        f'5. Baixa \n'
                        f'6. Excluir Lançamento \n'
                        f'7. Logout \n'
                        f'8. Sair \n'
                        f'Opção escolhida: ')

            if op.isdigit():
                opcoes = int(op)
                if opcoes == 1:
                    contas_a_pagar(id_usuario)
                elif opcoes == 2:
                    contas_a_receber(id_usuario)
                elif opcoes == 3:
                    imprimir_dados('contas_pagar.csv')
                    input("Pressione Enter para continuar...")
                elif opcoes == 4:
                    imprimir_dados('contas_receber.csv')
                    input("Pressione Enter para continuar...")
                elif opcoes == 5:
                    escolha = input('Escolha uma opção:\n1. Contas a Pagar\n2. Contas a Receber\nOpção escolhida: ')
                    if escolha == '1':
                        baixa_lancamento('contas_pagar.csv')
                    elif escolha == '2':
                        baixa_lancamento('contas_receber.csv')
                    else:
                        print('Opção inválida. Tente novamente.')
                elif opcoes == 6:
                    escolha = input('Escolha uma opção:\n1. Contas a Pagar\n2. Contas a Receber\nOpção escolhida: ')
                    if escolha == '1':
                        excluir_lancamento('contas_pagar.csv')
                    elif escolha == '2':
                        excluir_lancamento('contas_receber.csv')
                    else:
                        print('Opção inválida. Tente novamente.')
                elif opcoes == 7:
                    id_usuario = None
                    print('Logout realizado com sucesso.')
                elif opcoes == 8:
                    print('Saindo do programa.')
                    break
                else:
                  print('Entrada inválida. Por favor, digite um número válido para a opção do menu.')

if __name__ == "__main__":
    menu()
