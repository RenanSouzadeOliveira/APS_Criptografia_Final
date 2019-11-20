
import random
import time
from datetime import datetime
def totient(numero):
    # Calcula o totiente do numero primo
    if(primo(numero)):
        return numero-1
    else:
        return False

def primo(n):
    # verifica se o numero gerado é primo
    if (n <= 1):
        return False
    if (n <= 3):
        return True

    if (n%2 == 0 or n%3 == 0):
        return False

    i = 5
    while(i * i <= n):
        if (n%i == 0 or n%(i+2) == 0):
           return False
        i+=6
    return True


def gerador_E(num):
    #Gera um numero E aleatorio, obedecendo as condições
    def mdc(n1,n2):
        rest = 1
        while(n2 != 0):
            rest = n1%n2
            n1 = n2
            n2 = rest
        return n1

    while True:
        e = random.randrange(2,num) 
        if(mdc(num,e) == 1):
            return e



def gerador_primo():
    # gera um numero primo aleatorio
    while True:
        x=random.randrange(100,200) # definindo o range de numeros
        if(primo(x)==True):
            return x



def mod(a,b):
    # função modular entre dois números
    if(a<b):
        return a
    else:
        c = a % b
        return c

    
def criptografar(senha,e,n):
    #Função responsável por descriptografar
    tam = len(senha)
    i = 0
    lista = []
    while(i < tam):
        letra = senha[i]
        k = ord(letra)
        k = k**e
        d = mod(k,n)
        lista.append(d)
        i += 1
    return lista


def descifra(cifra, n, d):
    #Função responsável por descriptografar
    lista = []
    i = 0
    tamanho = len(cifra)
    # texto=cifra ^ d mod n
    while i < tamanho:
        result = cifra[i]**d
        texto = mod(result,n)
        letra = chr(texto)
        lista.append(letra)
        i += 1
    return lista



def calcular_chave_privada(toti, e):
    #Função responsável por calcular a chave privada
    d = 0
    while(mod(d * e, toti)!=1):
        d += 1
    return d

def Cadastro(patente, login, senha):
    #Função responsável pelo cadastro de usuários
    p = gerador_primo()  # gera um primo aleatório para P
    q = gerador_primo()  # gera um primo aleatório para Q
    n = p * q  # calculando n
    y = totient(p)  # calculando totiente de P
    x = totient(q)  # calculando totiente de  Q
    totient_de_N = x * y  # calculando totiente de N
    e = gerador_E(totient_de_N)  # gerando o e E
    chave_publica = [n, e]
    print('Sua chave pública é {} e {},'.format(chave_publica[0], chave_publica[1]), end=" ")
    d = calcular_chave_privada(totient_de_N, e)
    print("e sua chave privada é {}.".format(d))
    print("Guarde essas chaves, pois serão necessárias para acessar o navio.")
    print("Seu uso é pessoal, não é permitido seu compartilhamento.")
    senha_crip = criptografar(senha, e, n)
    senha_crip = str(senha_crip)
    gravando = open("cadastro.txt", 'a')
    gravando.write(patente + "|" + login + "|" + senha_crip + "|" + str(len(senha)) + "\n")
    gravando.close()
    status = True
    print("Cadastro realizado com sucesso!!!")
    return status


def Acessar(pk1, p, l, s, d, escolha):
    #Função responsável por realizar o acesso no navio
    lista_total = [] # Recebe todos os dados cadastrados
    lista_total2 = [] # é usada para separar em login
    lista_login = [] # Lista contém somente os logins
    lista_patente = [] #Lista contém somente as patentes
    lista_senha = [] # lista contém apenas as senhas
    lista_tamanho = []
    senha_int = [] #senhas convertidas em inteiros
    log = False #Sinaliza see o login do usuário bate
    pat = False #Sinaliza se a patente do usuário bate
    sen = False #Sinaliza se a patente do usuário bate
    senha_certa =[] #recebe a senha do usuário quebrando ela em letras
    senhafinal = "" # senha descriptografada
    status = True # se o acesso foi cadastrado com sucesso ou não
    arquivo = open("cadastro.txt", 'r')
    dados = arquivo.readlines()
    arquivo.close()

    for linha in dados:
        lista_total.append(linha.replace("\n", "")) # remove o '\n' da lista
    for dado in lista_total:
        lista_total2 = dado.split("|") #o separador é usado para dividir os dados dentro do arquivo patente|login|senha|len(senha)
        lista_patente.append(lista_total2[0]) # recebe somente as patentes cadastradas
        lista_login.append(lista_total2[1]) # recebe apenas os logins cadastrados
        lista_senha.append(lista_total2[2]) # recebe as senha criptogradafas
        lista_tamanho.append(lista_total2[3]) # recebe o tamanho da senha

    for patente in lista_patente:
        #verifica se a patente informada está cadastrada
        if p.replace(" ","") == patente:
            pat = True
    for login in lista_login:
        #verifica se o login informado está cadastrado
        if l == login:
            log = True
    for senha in lista_senha:
        # remove os separadores das senhas e descriptografa elas
        senha = senha.replace("[","")
        senha = senha.replace("]","")
        senha = senha.split(",")
        for num in senha:
            senha_int.append(int(num))
        senha_dec = descifra(senha_int,pk1,d)
    tamanho = len(s)
    for i in range(0, tamanho):
        senha_certa.append(s[i])

    lista_mega = [x for x in senha_dec if x in senha_certa] #atribui a lista_mega somente as letras descriptografadas que estão na lista senha_certa
    cont = 0 #indice da string senha
    for letra in lista_mega:
        # recria a senha descriptografada
        if letra == s[cont]:
            senhafinal += letra
            cont +=1
    tamanho_senha = 0
    for i in lista_tamanho:
        tamanho_senha = int(i)
        if senhafinal == s and tamanho_senha == len(s):
            # se a senha recriada for igual a senha informada atribui 'True' ao status da senha
            sen = True


    if pat == True and log == True and sen == True:
        # se todos os dados do usuário forem válidos libera o acesso e grava no arquivo acessos
        print("Acesso liberado!!!")
        print("Bem-vindo {}".format(p))
        if escolha == 1:
            dh = datetime.now()
            dht = dh.strftime('%d/%m/%y %H:%M')
            acessos = open("acessos.txt", 'a')
            acessos.write(p + " - " + dht + "\n")
            acessos.close()
            time.sleep(5)
            exit()
    else:
        print("Acesso negado!!!")
        sen = False
    return sen

def main():
    #Desenhando o menu
    dec = "-" * 80
    print(dec)
    print("MARINHA DO BRASIL".center(80))
    print("Marinha do Brasil, protegendo nossas riquezas, cuidando da nossa gente.".center(80))
    print(dec)
    print("CONTROLE DE ACESSO.".center(80))
    print(dec)
    escolha = 0
    cont = 0

    while escolha != 4:
        #Se a escolha do usuário for diferente de 4 que é a opção para sair o while roda
        print("Escolha o número correspondente ao que você deseja realizar no sistema:".center(80))
        print("1 - Entrar no navio;".center(80))
        print("2 - Cadastrar;".center(74))
        print("3 - Consultar acessos;".center(82))
        print("4 - Sair.".center(70))
        print(dec)
        #Tratamento de erro caso o usuário digitar uma letra
        try:
            escolha = int(input("Opção:"))
        except ValueError:
            print("Opção inválida, digite apenas números.")

        #A lista abaixo contém as patentes aptas a se cadastrar no sistema
        patentes_validas = ["capitãodecorveta", "capitãodefragata", "capitãodemareguerra", "contra-almirante","vice-almirante", "almirantedeesquadra", "almirante"]

        #Determinando as funções para cada funcionalidade
        if escolha == 1:
            cont = 0
            v_acesso = False
            while cont < 3:
                print(dec)
                print("ACESSO".center(80))
                print(dec)
                try:
                    pk1 = int(input("Digite o primeiro valor do seu par de chaves públicas:"))
                    p = input("Agora digite sua patente:".lower())
                    l = input("Digite seu login:")
                    s = input("Digite sua senha:")
                    d = int(input("Digite sua chave privada:"))
                    if len(str(pk1)) > 5:
                        pk1 = 1
                        d = 1
                        print("Valor de chave pública inválido.")
                        print("Digite apenas o primeiro valor do seu par de chave pública.")
                        print("Por exemplo se seu par de chave é 12345 e 678910, digite apenas 12345.")
                    if len(str(d)) > 5:
                        d = 1
                        pk1 = 1
                    v_acesso = Acessar(pk1, p, l, s, d, escolha)
                except ValueError:
                    print("Nesse campo são permitidos apenas números.")
                if v_acesso == False:
                    #Limita o usuário a tentar login somente três vezes
                    cont += 1
                    if cont == 3:
                        print("Você tentou acessar o navio mais de 3 vezes.")
                        print("Por motivos de segurança o sistema irá encerrar.")
                        time.sleep(5)
                        exit()
                    print("Você só tem mais {} tentativas de tentar acessar o navio.".format(3-cont))

        elif escolha == 2:
            print(dec)
            print("CADASTRO".center(80))
            print(dec)
            #Cadastro de usuário
            cont_tent = 0
            cadastro = False
            while cont_tent < 3:
                # Limita o usuário a apenas 3 tentativas
                cad_pat = input("Digite sua patente:".lower())
                cad_pat = cad_pat.replace(" ","")
                # verifica se a patente iserida é válida
                for patente in patentes_validas:
                    if cad_pat == patente:
                        cadastro = True
                if cadastro != True:
                    #Se a patente não for apta
                    cont_tent += 1
                    tent = 3 - cont_tent
                    print("Sua patente não é apta a se cadastrar.")
                    if cont_tent == 3:
                        #Quando o usuário tenta cadastrar mais de três vezes
                        print("O algoritmo está encerrando por motivos de segurança.")
                        time.sleep(5)
                        exit()
                    print("Você ainda tem {} tentativas de cadastro.".format(tent))
                if cadastro == True:
                    #Quando a patetente do usuário é válida
                    login = input("Digite seu login:")
                    senha = input("Digite sua senha:")
                    s = Cadastro(cad_pat, login, senha)
                    if s == True:
                        main()

        elif escolha == 3:
            print(dec)
            print("CONSULTA".center(80))
            print(dec)
            print("Primeiro é necessário realizar login.")
            s = False
            while cont < 3:
                try:
                    pk1 = int(input("Digite o primeiro valor do seu par de chaves públicas:"))
                    p = input("Agora digite sua patente:".lower())
                    l = input("Digite seu login:")
                    s = input("Digite sua senha:")
                    dd = int(input("Digite sua chave privada:"))
                    if len(str(pk1)) > 5:
                        pk1 = 1
                        dd = 1
                        print("Valor de chave pública inválido.")
                        print("Digite apenas o primeiro valor do seu par de chave pública.")
                        print("Por exemplo se seu par de chave é 12345 e 678910, digite apenas 12345.")
                    if len(str(dd)) > 5:
                        pk1 = 1
                        dd = 1
                    s = Acessar(pk1, p, l, s, dd, escolha)
                except ValueError:
                    print("Nesse campo é permitido apenas números.")

                if s == False:
                    # Limita o usuário a tentar login somente três vezes
                    cont += 1
                    if cont == 3:
                        print("Você tentou acessar o navio mais de 3 vezes.")
                        print("Por motivos de segurança o sistema irá encerrar.")
                        time.sleep(5)
                        exit()
                    print("Você só tem mais {} tentativas de tentar acessar o navio.".format(3 - cont))
                else:
                    if s == True:
                        acessos = open("acessos.txt", 'r')
                        acesso = acessos.readlines()
                        acessos.close()
                        print(dec)
                        print("ACESSOS".center(80))
                        print(dec)
                        for i in acesso:
                            print(i)
                        main()
        else:
            print("Saindo...")
            time.sleep(5)
            exit()
main()