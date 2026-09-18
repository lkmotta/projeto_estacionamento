import database
import sys

def menu_principal(username, user_type):
    while True:
        tipo_str = "Servidor" if user_type == "servidor" else "Aluno"
        print(f"\n--- Estacionamento Campus | Usuário: {username} ({tipo_str}) ---")
        print("1. Ver status das vagas")
        print("2. Estacionar carro (Ocupar vaga)")
        print("3. Retirar carro (Liberar vaga)")
        print("4. Sincronizar dados (Offline -> Online)")
        print("5. Sair")
        print("6. Fazer Logout")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            vagas = database.get_vagas()
            print("\n--- Status Atual das Vagas ---")
            for v_id, estado, reservada in vagas:
                tag_res = " [RESERVADA SERVIDOR]" if reservada == 1 else ""
                print(f"Vaga {v_id:02d} - [{estado.upper()}]{tag_res}")
        
        elif opcao == '2':
            v_id = input("Digite o ID da vaga que deseja ocupar: ")
            if v_id.isdigit():
                sucesso, msg = database.atualizar_vaga(int(v_id), 'ocupada', user_type)
                print(msg)
            else:
                print("ID de vaga inválido.")
                
        elif opcao == '3':
            v_id = input("Digite o ID da vaga que deseja liberar: ")
            if v_id.isdigit():
                sucesso, msg = database.atualizar_vaga(int(v_id), 'livre', user_type)
                print(msg)
            else:
                print("ID de vaga inválido.")
                
        elif opcao == '4':
            print("Conectando ao servidor central...")
            print("Enviando alterações em lote...")
            print("Sincronização concluída com sucesso!")
            
        elif opcao == '5':
            print("Encerrando aplicativo...")
            sys.exit()
            
        elif opcao == '6':
            database.do_logout()
            print("Logout realizado. Execute o app novamente para entrar.")
            sys.exit()
        else:
            print("Opção inválida.")

if __name__ == '__main__':
    database.init_db()
    
    is_logged, user, user_type = database.check_login()
    
    if not is_logged:
        print("--- Tela de Autenticação ---")
        print("- Alunos: digite o RA com 7 dígitos (ex: 1234567)")
        print("- Servidores: digite o e-mail institucional (@utfpr.edu.br ou @professores.utfpr.edu.br)")
        
        while True:
            login_input = input("\nDigite seu RA ou E-mail: ").strip()
            valido, tipo = database.validar_credencial(login_input)
            
            if valido:
                user = login_input
                user_type = tipo
                database.do_login(user, user_type)
                print(f"Login efetuado com sucesso como {user_type.upper()}!")
                break
            else:
                print("Credencial inválida! Certifique-se de usar RA (7 dígitos) ou e-mail institucional UTFPR.")
    else:
        print(f"Sessão recuperada automaticamente. Bem-vindo de volta, {user} ({user_type.upper()})!")
        
    menu_principal(user, user_type)
