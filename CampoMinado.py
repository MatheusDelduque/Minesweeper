from contextlib import ContextDecorator
import random
import time
import os

#Funcao para o menu principal do jogo.
def menu_campo_minado ():
    print("(1) Começar jogo")
    print("(2) Recomeçar ultimo jogo")
    print("(3) Os cinco melhores tempos")
    print("(4) Sair")
    
    opcao = input("Escolha uma das opcoes:")
    
    return opcao
    
#Funcao para quando for necessario a escolha da dificuldade.
def menu_dificuldade ():
    print("\n(1) Facil")
    print("(2) Medio")
    print("(3) Voltar")
    
    opcao = input("Escolha uma das opcoes:")
    
    return opcao
    
        
#Funcao para criacao da lista de lista que sera responsavel pelo corpo do jogo, o tabuleiro.
def criar_tabuleiro(quantidadeLinhas):
    linhaCampoMinado = ["*"] * quantidadeLinhas
    
    return [linhaCampoMinado[:] for _ in range(quantidadeLinhas)] 
        

#Funcao para mostrar o tabuleiro sem os colchetes da lista.
def mostrar_tabuleiro (tabuleiroCampoMinado):
    print('\t', end = '')
    
    for elemento in range(1,len(tabuleiroCampoMinado[0])+1):
        print(elemento, end = '\t')
        
    print()

    for linha in range(len(tabuleiroCampoMinado)):
        print(linha + 1, end = '\t')
        
        for elemento in tabuleiroCampoMinado[linha]:
            print(elemento, end = '\t')
            
        print()
    

#Funcao para criar as bombas.
def posicoes_bombas_sorteadas (quantidadesBombas, tabuleiroCampoMinado):
    posicoesBombas = []
    
    #Sorteando as posicoes das bombas.
    while len(posicoesBombas) != quantidadesBombas:
        linhaBomba = random.randint(1,(len(tabuleiroCampoMinado)))
        colunaBomba = random.randint(1,(len(tabuleiroCampoMinado[0])))
        
        if not [linhaBomba, colunaBomba] in posicoesBombas:
            posicoesBombas.append([linhaBomba, colunaBomba])
            
    return posicoesBombas


#Funcao que pede a linha e a coluna para o usuario e faz validacao dos inputs recebidos.
def posicao_escolhida (tabuleiroCampoMinado):
    while True:
            try:
                linha = int(input("Digite o numero da linha:"))
                
                if linha < 1 or  linha > len(tabuleiroCampoMinado):
                    raise ValueError
                
                if linha >= 1 and linha <= len(tabuleiroCampoMinado):
                    break
                
            except ValueError:
                print("A posicao da linha deve ser um inteiro e estar entre 1 e " +(str(len(tabuleiroCampoMinado)))+ "!")
                
            
    while True:
        try:
            coluna = int(input("Digite o numero da coluna:"))
                
            if coluna < 1 or  coluna > len(tabuleiroCampoMinado):
                    raise ValueError
                
            if coluna >= 1 and coluna <= len(tabuleiroCampoMinado):
                    break
                
        except ValueError:
            print("A posicao da coluna deve ser um inteiro e estar entre 1 e " +(str(len(tabuleiroCampoMinado)))+ "!")
        
    return linha, coluna


#Funcao que guarda todas as informacoes necessarias, dentro de um arquivo, para recomecar o jogo
def salvar_jogo (tabuleiroCampoMinado, posicoesBombas, posicoesEscolhidas, tempoAnterior, arquivoJogoSalvo):
    ultimoJogo = open(arquivoJogoSalvo, "w")
    ultimoJogo.write("Tabuleiro;" +str(tabuleiroCampoMinado) + ";\n")
    ultimoJogo.write("Bombas;" + str(posicoesBombas) + ";\n")
    ultimoJogo.write("Posicoes Escolhidas;" + str(posicoesEscolhidas) + ";\n")
    ultimoJogo.write("Tempo de Jogo;" + str(tempoAnterior))
    ultimoJogo.close()
   
        
#Funcao que guarda as informacoes do arquivo salvo em uma lista        
def tabuleiro_salvo (arquivoUltimoJogo):
    ultimoJogoSalvo = open(arquivoUltimoJogo, "r")
    tabuleiroSalvo = []
    posicoesBombas = []
    posicoesEscolhidas = []
    tempoAnterior = 0
    
    for jogoSalvo in ultimoJogoSalvo:
        elemento = jogoSalvo.split(";")
        if "Tabuleiro" in elemento:
            tabuleiroSalvo = eval(elemento[1])
            
        elif "Bombas" in elemento:
            posicoesBombas = eval(elemento[1])
            
        elif "Posicoes Escolhidas" in elemento:
            posicoesEscolhidas = eval(elemento[1])
            
        elif "Tempo de Jogo" in elemento:
            tempoAnterior = float(elemento[1])
            
                
    return tabuleiroSalvo, posicoesBombas, posicoesEscolhidas, tempoAnterior

#Funcao para verificar se ha bombas ao redor
def calculo_distancia (primeiroPosicao, segundaPosicao):
    x = primeiroPosicao[0] - segundaPosicao[0]
    y = primeiroPosicao[1] - segundaPosicao[1]
    
    return abs(x), abs(y)


#Funcao que possui a logica do Campo Minado
def verificar_posicao_escolhida (posicoesBombas, posicoesEscolhidas, tabuleiroCampoMinado, tempoAnterior, arquivoTemposVitoria, arquivoJogoSalvo):
    print ("Aperte CTRL+C, a qualquer momento, para encerrar o jogo!")
    listaPosicoesEscolhidas = posicoesEscolhidas
    tempoInicial = time.time()
    
    while True:
        try:
            print (posicoesBombas)
            mostrar_tabuleiro(tabuleiroCampoMinado)
            linha, coluna = posicao_escolhida(tabuleiroCampoMinado)
            contadorBombasAoRedor = 0
            listaPosicaoEscolhida = [linha, coluna]
            
            #Verificando se a posicao ja foi escolhida
            if listaPosicaoEscolhida in listaPosicoesEscolhidas:
                os.system("cls")
                print("Essa posicao ja foi preenchida!")
                
            else:
                os.system("cls")
                listaPosicoesEscolhidas.append(listaPosicaoEscolhida)
            
            #Verificando se o jogador perdeu
            if listaPosicaoEscolhida in posicoesBombas :
                os.system("cls")
                for posicaoBomba in posicoesBombas: 
                    tabuleiroCampoMinado[posicaoBomba[0] - 1][posicaoBomba[1] - 1] = "X"
                mostrar_tabuleiro(tabuleiroCampoMinado)
                print ("Voce perdeu!")
                break
            
            #Verificando quantas bombas ha ao redor da posicao escolhida
            for bomba in posicoesBombas:
                x, y = calculo_distancia(bomba, listaPosicaoEscolhida)
                if  x <= 1 and  y <= 1:
                    contadorBombasAoRedor += 1 
                        
            tabuleiroCampoMinado[linha - 1][coluna - 1] = contadorBombasAoRedor

            #Verificando se o jogador ganhou
            if len(listaPosicoesEscolhidas) == ((len(tabuleiroCampoMinado)**2) - len(posicoesBombas)):  
                os.system("cls")
                tempoFinal = time.time()
                tempoVitoria =  (tempoFinal  - tempoInicial) + tempoAnterior
                
                tempos = open(arquivoTemposVitoria, "a")
                tempos.write(str(round(tempoVitoria, 2)) + ",") 
                tempos.close()
                
                mostrar_tabuleiro(tabuleiroCampoMinado)
                print (round(tempoVitoria, 2))
                print("Parabens, voce ganhou!")
                break
        
        
        #Caso o jogador saia, salva a partida ate aquele momento
        except KeyboardInterrupt:
            tempoFinal = time.time()
            tempoAnterior =  (tempoFinal  - tempoInicial) + tempoAnterior
            salvar_jogo (tabuleiroCampoMinado, posicoesBombas, listaPosicoesEscolhidas, tempoAnterior, arquivoJogoSalvo)
            break
        
            
#Funcao que seleciona os cinco melhores tempos            
def cinco_melhores_tempos (arquivoTemposVitoria):
    temposVitoria = open(arquivoTemposVitoria, "r")
    cincoMelhoresTempos = []
    
    for tempoVitoria in temposVitoria:
        linha = tempoVitoria.split(",")
        for tempo in linha:
            if tempo != "":
                cincoMelhoresTempos.append(float(tempo))
        
    cincoMelhoresTempos.sort()
    cincoMelhoresTempos = cincoMelhoresTempos[:5]
    print("Melhores tempos:")

    posicoes = {1: "Primeiro: ", 2: "Segundo: ", 3: "Terceiro: ", 4:"Quarto: ", 5:"Quinto: "}
    
    for colocacao in range(len(cincoMelhoresTempos)):
        print(posicoes[colocacao + 1] + str(cincoMelhoresTempos[colocacao]))
    

#Funcao principal que recebe as demais funcoes para executa-las
def campo_minado ():
    print("-----Trabalho de Comp1-----")
    print("-----Matheus Delduque-----")
    print("-----Campo Minado-----")
    tabuleiroCampoMinado4x4 = []
    posicoesBombasSorteadas4x4 = []
    listaPosicoesEscolhidas4x4 = []
    
    tabuleiroCampoMinado6x6 = []
    posicoesBombasSorteadas6x6 = []
    listaPosicoesEscolhidas6x6 = []
    
    tempoAnterior = 0
    
    while True:
        opcao1 = menu_campo_minado()
        os.system("cls")
        
        if opcao1 == "1":
            while True:
                opcao2 = menu_dificuldade()
                os.system("cls")
            
                if opcao2 == "1":
                    listaPosicoesEscolhidas4x4 = []
                    tempoAnterior = 0
                    tabuleiroCampoMinado4x4 = criar_tabuleiro(4)
                    posicoesBombasSorteadas4x4 = (posicoes_bombas_sorteadas(6,tabuleiroCampoMinado4x4))
                    verificar_posicao_escolhida(posicoesBombasSorteadas4x4, listaPosicoesEscolhidas4x4, tabuleiroCampoMinado4x4, tempoAnterior, "temposvitoria4bombas.txt", "ultimojogo4x4.txt")                    
            
                elif opcao2 == "2": 
                    listaPosicoesEscolhidas6x6 = []
                    tempoAnterior = 0
                    tabuleiroCampoMinado6x6 = criar_tabuleiro(6)
                    posicoesBombasSorteadas6x6 = (posicoes_bombas_sorteadas(10,tabuleiroCampoMinado6x6))
                    verificar_posicao_escolhida(posicoesBombasSorteadas6x6, listaPosicoesEscolhidas6x6, tabuleiroCampoMinado6x6, tempoAnterior, "temposvitoria6bombas.txt", "ultimojogo6x6.txt")    
            
                elif opcao2 == "3":
                    break
                
                else:
                    print("Opcao Invalida!")
                    
        elif opcao1 == "2":
            while True:
                opcao3 = menu_dificuldade()
                os.system("cls")

                if opcao3 == "1":
                   tabuleiroCampoMinado4x4, posicoesBombasSorteadas4x4, listaPosicoesEscolhidas4x4, tempoAnterior = tabuleiro_salvo("ultimojogo4x4.txt")    
                   verificar_posicao_escolhida(posicoesBombasSorteadas4x4, listaPosicoesEscolhidas4x4, tabuleiroCampoMinado4x4, tempoAnterior,  "temposvitoria4bombas.txt", "ultimojogo4x4.txt")
                   
                
                elif opcao3 == "2":
                    tabuleiroCampoMinado6x6, posicoesBombasSorteadas6x6, listaPosicoesEscolhidas6x6, tempoAnterior = tabuleiro_salvo("ultimojogo6x6.txt")
                    verificar_posicao_escolhida(posicoesBombasSorteadas6x6, listaPosicoesEscolhidas6x6, tabuleiroCampoMinado6x6, tempoAnterior, "temposvitoria6bombas.txt", "ultimojogo6x6.txt")
                
                elif opcao3 == "3":
                    break
                
                else:
                    print("Opcao Invalida!")
                
        elif opcao1 == "3":
            while True:
                opcao4 = menu_dificuldade()
                os.system("cls")

                if opcao4 == "1":
                    cinco_melhores_tempos("temposvitoria4bombas.txt")
                
                elif opcao4 == "2":
                    cinco_melhores_tempos("temposvitoria6bombas.txt")
                    
                elif opcao4 == "3":
                    break
            
                else:
                    print("Opcao Invalida!")

        elif opcao1 == "4":
            break
        
        else:
            print("Opcao Invalida!")


if __name__ == "__main__":
    campo_minado()