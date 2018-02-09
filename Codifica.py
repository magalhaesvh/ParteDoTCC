#codigo sem OO, foi dividido em classe apenas para auxiliar na modularização dos scripts

from bs4 import BeautifulSoup as bs
from RubyMap import MapeamentoRb
from PythonMap import MapeamentoPy

dicioID = {}
dicioParams = {}

class Codifica(object):

    def __init__(self, lg):
        self.ePython = False
        if lg == 1:
            self.mapp = MapeamentoRb()
        elif lg == 2:
            self.mapp = MapeamentoPy()
            self.ePython = True
        else:
            print 1

    def verificaNos(self, sp):
        dicioID[sp['xmi:id']] = sp['name']
        dicioParams[sp['name']] = 0
        spaux = sp.contents
        for k in spaux:
            if k.name == "ownedMember" and k.attrs['xmi:type'] == 'uml:Class':
                dicioID[k['xmi:id']] = k['name']
                dicioParams[k['name']] = 0
                for x in k.contents:
                    if x.name == "ownedAttribute" and x.attrs['xmi:type'] == 'uml:Property':
                        k['name'] = k['name'] + 1
            if k.name == 'ownedAttribute':
                dicioParams[sp['name']] =  dicioParams[sp['name']] + 1

        auxProx = sp.find_next_sibling('packagedElement')
        if auxProx != None and auxProx['xmi:id'][
            1] != 'D':  # verifica se ainda tem alguma classe e se a proxima classe nao e' DAO
            self.init(auxProx)
        else:
            return 0

    def criaInicializador(self, aux1, py_file):
        cont = 0
        contador = 0
        py_file.write(self.mapp.criaInit())
        for q in aux1:  # percorre xmi para achar a quantidade de parametros do inicializador
            if q.name == 'ownedAttribute':
                cont += 1
                py_file.write('param' + str(cont))
                if (contador+2) < len(aux1):
                    if aux1[contador+2].name == "ownedAttribute": #verifica se a proxima tag ainda e' um atributo
                        py_file.write(",")
            contador += 1
        py_file.write(self.mapp.finalizaParams())
        cont = 0
        for k in aux1:  # busca os atributos
            if k.name == 'ownedAttribute' or k.name == 'ownedOperation':  # verifica se e' atributo ou metodo da classe
                if k.name == 'ownedAttribute' and k.attrs['xmi:type'] == "uml:Property":  # verifica se e' um atributo
                    cont += 1
                    py_file.write(self.mapp.initAttrs(k,cont))
        py_file.write(self.mapp.finalizaInit())

    def criaInicializadorHeranca(self, aux1, nomePai,py_file):
        cont = 0
        contador = 0
        paramsFilhos = ""
        paramsPai = self.mapp.defineQtdParamsPai(dicioParams[nomePai])
        for q in aux1:  # percorre xmi para achar a quantidade de parametros do inicializador
            if q.name == 'ownedAttribute':
                cont += 1
                paramsFilhos = paramsFilhos + 'param' + str(cont)
                if (contador+2) < len(aux1):
                    if aux1[contador+2].name == "ownedAttribute": #verifica se a proxima tag ainda e' um atributo
                        paramsFilhos = paramsFilhos + ","
            contador += 1
        cont = 0
        inserir = self.mapp.replaceParams(paramsPai, paramsFilhos, nomePai)
        py_file.write(inserir)
        for k in aux1:  # busca os atributos
            if k.name == 'ownedAttribute' or k.name == 'ownedOperation':  # verifica se e' atributo ou metodo da classe
                if k.name == 'ownedAttribute' and k.attrs['xmi:type'] == "uml:Property":  # verifica se e' um atributo
                    cont += 1
                    py_file.write(self.mapp.initAttrs(k,cont))
        py_file.write(self.mapp.finalizaInit())
        vet = [paramsPai, paramsFilhos]
        return vet

    def classeAssociada(self, associada):
        py_file = self.mapp.abreArquivo(associada)
        aux1 = associada.contents  # pega todos os filhos da classe

        vetorHeranca = self.generalizacao(aux1)
        if vetorHeranca[0] == True:
            py_file.write(self.mapp.defineHerancaTrue(associada,vetorHeranca))
        else:
            py_file.write(self.mapp.defineHerancaFalse(associada))

        self.criaInicializador(aux1, py_file)
        for k in aux1: #busca os metodos
            if k.name == 'ownedMember' and k['xmi:type'] == 'uml:Class':
                self.classeAssociada(k)
            if k.name == 'ownedOperation' and k.attrs['xmi:type'] == "uml:Operation": # verifica se e' um metodo
                self.mapp.getAndSet(k.attrs['name'], py_file)
        py_file.write(self.mapp.finalizaClasse())

    def generalizacao(self, aux1):
        vet = []
        heranca = False
        pai = ""
        for k in aux1:
            if k.name == "generalization":
                heranca = True
                for j in dicioID.keys():
                    if k.attrs['general'] == j:
                        pai = dicioID[j]
        vet.append(heranca)
        vet.append(pai)
        return vet

    def convertPSMtoCode(self, aux):
        arquivo = self.mapp.abreArquivo(aux)

        aux1 = aux.contents  # pega todos os filhos da classe

        vetorHeranca = self.generalizacao(aux1)
        if vetorHeranca[0] == True:
            arquivo.write(self.mapp.defineHerancaTrue(aux,vetorHeranca))
        else:
            arquivo.write(self.mapp.defineHerancaFalse(aux))

        if self.ePython == False or self.ePython == True and vetorHeranca[0] == False:
            self.criaInicializador(aux1,arquivo)
        else:
            self.criaInicializadorHeranca(aux1, vetorHeranca[1], arquivo)

        for k in aux1: #busca os metodos
            if k.name == 'ownedMember' and k['xmi:type'] == 'uml:Class':
                self.classeAssociada(k)
            if k.name == 'ownedOperation' and k.attrs['xmi:type'] == "uml:Operation": # verifica se e' um metodo
                self.mapp.getAndSet(k.attrs['name'], arquivo)

        arquivo.write(self.mapp.finalizaClasse())

        auxProx = aux.find_next_sibling('packagedElement')
        if auxProx != None and auxProx['xmi:id'][1] != 'D':
            self.convertPSMtoCode(auxProx)
        elif auxProx != None and auxProx['xmi:id'][1] == 'D':
            return 0
        else:
            return 1
