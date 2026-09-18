import database
import sys

def menu_principal(username):
    while True:
        print(f"\n--- Estacionamento Campus | Usuário: {username} ---")
        print("1. Ver status das vagas")
        print("2. Estacionar carro (Ocupar vaga)")
        print("3. Retirar carro (Liberar vaga)")
        print("4. Sincronizar dados (Simulação Offline -> Online)")
        print("5. Sair")
        print("6. Fazer Logout")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            vagas = database.get_vagas()
            print("\n--- Status Atual ---")
            for v_id, estado in vagas:
                print(f"Vaga {v_id:02d} - [{estado.upper()}]")
        
        elif opcao == '2':
            v_id = input("Digite o ID da vaga que deseja ocupar: ")
            if v_id.isdigit() and database.atualizar_vaga(int(v_id), 'ocupada'):
                print(f"Vaga {v_id} marcada como OCUPADA. (Salvo localmente)")
            else:
                print("Vaga inválida ou não encontrada.")
                
        elif opcao == '3':
            v_id = input("Digite o ID da vaga que deseja liberar: ")
            if v_id.isdigit() and database.atualizar_vaga(int(v_id), 'livre'):
                print(f"Vaga {v_id} marcada como LIVRE. (Salvo localmente)")
            else:
                print("Vaga inválida ou não encontrada.")
                
        elif opcao == '4':
            print("Conectando ao servidor central...")
            print("Enviando alterações em lote...")
            print("Sincronização concluída com sucesso!")
            
        elif opcao == '5':
            print("Encerrando aplicativo...")
            sys.exit()
            
        elif opcao == '6':
            database.do_logout()
            print("Logout realizado. Execute o app novamente para logar.")
            sys.exit()
        else:
            print("Opção inválida.")

if __name__ == '__main__':
    database.init_db()
    
    is_logged, user = database.check_login()
    
    if not is_logged:
        print("Nenhuma sessão encontrada. É necessário fazer login.")
        user = input("Digite seu nome de usuário ou RA: ")
        # Em um cenário real, aqui validaria a senha contra uma API
        database.do_login(user)
        print("Login realizado com sucesso e sessão salva!")
    else:
        print(f"Sessão recuperada automaticamente. Bem-vindo de volta, {user}!")
        
    menu_principal(user)