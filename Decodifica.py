from bs4 import BeautifulSoup as bs
from bs4 import NavigableString
from bs4 import Tag
import random

xml_file = open("teste.xmi")
soup = bs(xml_file, "lxml-xml")
dicio = {}

class Decodifica(object):

    def __init__(self):
        self.auxiliar1 = soup.find("packagedElement", {"xmi:type": "uml:Class"},recursive=True)  # parametro para buscar a primeira classe do xmi(e' padrao)
        self.percorreXMI(self.auxiliar1)

    def insertGetSet(self, auxiliar, vetor):
        for n in range(0, len(vetor)): #percorre o vetor com o nome dos metodos e adc os getters e setters
            tag = soup.new_tag("ownedOperation")
            tag['xmi:id'] = "AAAAAAFcH"+str(random.randint(0,9))+"G"+str(random.randint(0,9))+"Mi"+str(random.randint(0,9))+"Z"+str(random.randint(0,9))+"Xc="
            tag['name'] = "get"+vetor[n]
            tag['visibility'] = "public"
            tag["isStatic"] = "false"
            tag["isLeaf"] = "false"
            tag["concurrency"] = "sequential"
            tag["isQuery"] = "false"
            tag["isAbstract"] = "false"
            tag["xmi:type"] = "uml:Operation"
            auxiliar.insert(len(auxiliar),tag)
            auxiliar.insert(len(auxiliar), '\n')

            tag = soup.new_tag("ownedOperation")
            tag['xmi:id'] = "AAAAAAFcH" + str(random.randint(0, 9)) + str(random.randint(0, 9)) + "GMi" + str(random.randint(0, 9)) + "Z" + str(random.randint(0, 9)) + "Xc="
            tag['name'] = "set" + vetor[n]
            tag['visibility'] = "public"
            tag["isStatic"] = "false"
            tag["isLeaf"] = "false"
            tag["concurrency"] = "sequential"
            tag["isQuery"] = "false"
            tag["isAbstract"] = "false"
            tag["xmi:type"] = "uml:Operation"
            tag.append('\n\t')
            tag.append(self.insertParameter('param')) #insere os parametros do metodo set
            tag.append('\n')
            auxiliar.insert(len(auxiliar), tag)
            auxiliar.insert(len(auxiliar), '\n')

    def insertParameter(self, parametro): #cria a tag do parametro (param) e retorna esta
        tag = soup.new_tag("ownedParameter")
        tag['xmi:id'] = "A"+str(random.randint(0, 9))+"AAAAFdPGR+I"+str(random.randint(0, 9))+"z"+str(random.randint(0, 9))+"NS"+str(random.randint(0, 9))+"="
        tag['name'] = parametro
        tag['visibility'] = "public"
        tag["isStatic"] = "false"
        tag["isLeaf"] = "false"
        tag["isReadOnly"] = "false"
        tag["isOrdered"] = "false"
        tag["isUnique"] = "false"
        tag['direction'] = 'in'
        tag["xmi:type"] = "uml:Parameter"
        return tag

    def insertLigacao(self, auxiliar, idTipoA, idTipoB): #cria a ligacao e retorna o id da classe que deve ser ligada
        tagg = soup.new_tag("ownedMember")
        tagg['xmi:id'] = "AAAAAAF"+str(random.randint(0, 9))+"P"+str(random.randint(0, 9))+"KN"+str(random.randint(0, 9))+ str(random.randint(0, 9))+"TZOfY="
        tagg['visibility'] = "public"
        tagg['xmi:type'] = "uml:Association"
        tagg['isDerived'] = "false"
        tagg.append('\n')

        tag = soup.new_tag("ownedEnd")
        tag['xmi:id'] = "AAAAAAF"+str(random.randint(0, 9))+"PW"+str(random.randint(0, 9))+"tOLP"+str(random.randint(0, 9))+"XW"+str(random.randint(0, 9))+"="
        tag['visibility'] = "public"
        tag["isStatic"] = "false"
        tag["isLeaf"] = "false"
        tag["isReadOnly"] = "false"
        tag["isOrdered"] = "false"
        tag["isUnique"] = "false"
        tag["xmi:type"] = "uml:Parameter"
        tag['aggregation'] = 'none'
        tag['isDerived'] = "false"
        tag['isID'] = "false"
        tag['type'] = idTipoA
        tagA = tag['xmi:id']
        tagg.append(tag)
        tagg.append('\n')

        tag = soup.new_tag("ownedEnd")
        tag['xmi:id'] = "AAAAAAF" + str(random.randint(0, 9)) + "PW" + str(random.randint(0, 9)) + "tOLP" + str(
            random.randint(0, 9)) + "XW" + str(random.randint(0, 9)) + "="
        tag['visibility'] = "public"
        tag["isStatic"] = "false"
        tag["isLeaf"] = "false"
        tag["isReadOnly"] = "false"
        tag["isOrdered"] = "false"
        tag["isUnique"] = "false"
        tag["xmi:type"] = "uml:Parameter"
        tag['aggregation'] = 'none'
        tag['isDerived'] = "false"
        tag['isID'] = "false"
        tag['type'] = idTipoB
        tagB = tag['xmi:id']
        tagg.append(tag)
        tagg.append('\n')

        tag = soup.new_tag("memberEnd")
        tag['xmi:idref'] = tagA
        tagg.append(tag)
        tagg.append('\n')

        tag = soup.new_tag("memberEnd")
        tag['xmi:idref'] = tagB
        tagg.append(tag)
        tagg.append('\n')

        auxiliar.insert(len(auxiliar), tagg)
        auxiliar.insert(len(auxiliar), '\n')

    def criaClasseDAO(self, nome, idXmi): #cria a classe DAO com metodos e atributos desta
        tagg = soup.new_tag("packagedElement") #classe DAO
        tagg['xmi:id'] = idXmi
        tagg['name'] = nome+'DAO'
        tagg['visibility'] = "public"
        tagg["isAbstract"] = "false"
        tagg["isFinalSpecialization"] = "false"
        tagg["xmi:type"] = "uml:Class"
        tagg["isActive"] = "false"
        tagg.append('\n')

        tag = soup.new_tag("ownedAttribute") #atributo de conexao
        tag['xmi:id'] = "AAAAAAF"+ str(random.randint(0, 9)) + str(random.randint(0, 9))+"B/QA"+ str(random.randint(0, 9)) +"M0"+ str(random.randint(0, 9)) +"lM="
        tag['name'] = 'EntityManager'
        tag['visibility'] = 'public'
        tag["isStatic"] = "false"
        tag['isLeaf'] = "false"
        tag['isReadOnly'] = "false"
        tag['isOrdered'] = "false"
        tag['isUnique'] = "false"
        tag['xmi:type'] = "uml:Property"
        tag['aggregation'] = "none"
        tag['isDerived'] = "false"
        tag['isID'] = "false"
        tagg.append(tag)
        tagg.append('\n')

        tag = soup.new_tag("ownedOperation") #metodoCreate
        tag['xmi:id'] = "AAAAAAFcH" + str(random.randint(0, 9)) + "G" + str(random.randint(0, 9)) + "Mi" + str(
            random.randint(0, 9)) + "Z" + str(random.randint(0, 9)) + "Xc="
        tag['name'] = 'create'+nome
        tag['visibility'] = "public"
        tag["isStatic"] = "false"
        tag["isLeaf"] = "false"
        tag["concurrency"] = "sequential"
        tag["isQuery"] = "false"
        tag["isAbstract"] = "false"
        tag["xmi:type"] = "uml:Operation"
        tagg.append(tag)
        tagg.append('\n')

        tag = soup.new_tag("ownedOperation")
        tag['xmi:id'] = "AAAAAAFcH" + str(random.randint(0, 9)) + "G" + str(random.randint(0, 9)) + "Mi" + str(
            random.randint(0, 9)) + "Z" + str(random.randint(0, 9)) + "Xc="
        tag['name'] = "read"+nome
        tag['visibility'] = "public"
        tag["isStatic"] = "false"
        tag["isLeaf"] = "false"
        tag["concurrency"] = "sequential"
        tag["isQuery"] = "false"
        tag["isAbstract"] = "false"
        tag["xmi:type"] = "uml:Operation"
        tagg.append(tag)
        tagg.append('\n')

        tag = soup.new_tag("ownedOperation") #metodoUpdate
        tag['xmi:id'] = "AAAAAAFcH" + str(random.randint(0, 9)) + "G" + str(random.randint(0, 9)) + "Mi" + str(
            random.randint(0, 9)) + "Z" + str(random.randint(0, 9)) + "Xc="
        tag['name'] = 'update'+ nome
        tag['visibility'] = "public"
        tag["isStatic"] = "false"
        tag["isLeaf"] = "false"
        tag["concurrency"] = "sequential"
        tag["isQuery"] = "false"
        tag["isAbstract"] = "false"
        tag["xmi:type"] = "uml:Operation"
        tagg.append(tag)
        tagg.append('\n')

        tag = soup.new_tag("ownedOperation")
        tag['xmi:id'] = "AAAAAAFcH" + str(random.randint(0, 9)) + "G" + str(random.randint(0, 9)) + "Mi" + str(
            random.randint(0, 9)) + "Z" + str(random.randint(0, 9)) + "Xc="
        tag['name'] = "delete"+nome
        tag['visibility'] = "public"
        tag["isStatic"] = "false"
        tag["isLeaf"] = "false"
        tag["concurrency"] = "sequential"
        tag["isQuery"] = "false"
        tag["isAbstract"] = "false"
        tag["xmi:type"] = "uml:Operation"
        tagg.append(tag)
        tagg.append('\n')

        tagAux = soup.find("packagedElement", {"xmi:type" : "uml:Model"})
        tagAux.append(tagg)
        tagAux.append('\n')

    def criaActiveRecord(self, nome, idXmi):
        tagg = soup.new_tag("packagedElement")  # classe DAO
        tagg['xmi:id'] = idXmi
        tagg['name'] = "ActiveRecord" + "("+nome+")"
        tagg['visibility'] = "public"
        tagg["isAbstract"] = "false"
        tagg["isFinalSpecialization"] = "false"
        tagg["xmi:type"] = "uml:Class"
        tagg["isActive"] = "false"
        tagg.append('\n')

        tag = soup.new_tag("ownedAttribute")  # atributo de conexao
        tag['xmi:id'] = "AAAAAAF" + str(random.randint(0, 9)) + str(random.randint(0, 9)) + "B/QA" + str(
            random.randint(0, 9)) + "M0" + str(random.randint(0, 9)) + "lM="
        tag['name'] = 'Base'
        tag['visibility'] = 'public'
        tag["isStatic"] = "false"
        tag['isLeaf'] = "false"
        tag['isReadOnly'] = "false"
        tag['isOrdered'] = "false"
        tag['isUnique'] = "false"
        tag['xmi:type'] = "uml:Property"
        tag['aggregation'] = "none"
        tag['isDerived'] = "false"
        tag['isID'] = "false"
        tagg.append(tag)
        tagg.append('\n')

        tagAux = soup.find("packagedElement", {"xmi:type": "uml:Model"})
        tagAux.append(tagg)
        tagAux.append('\n')

    def classeAssociada(self, associada, idAssoc, idName):
        vetor = []
        ePai = True
        for i in associada.contents:
            try:
                if isinstance(i, Tag):
                    if i.name == "ownedAttribute":
                        for j in i.attrs:
                            if j == 'visibility' and i.attrs[j] == 'public' and i.attrs[
                                'xmi:type'] == "uml:Property":  # verifica se a visibilidade e' publica e se e' um atributo da classe
                                i.attrs[j] = 'private'
                                vetor.append(i.attrs['name'])
                    if i.name == 'generalization':
                        ePai = False

            except: NavigableString
        self.insertGetSet(associada, vetor)
        idDAO = "ADAAAAF" + str(random.randint(0, 9)) + "H" + str(random.randint(0, 9)) + "G" + str(
            random.randint(0, 9)) + "Mi" + str(
            random.randint(0, 9)) + "Z" + str(random.randint(0, 9)) + "X" + str(random.randint(0, 9)) + "="
        ## insere um ID para padronizar o DAO com sua ligacao
        self.insertLigacao(associada, idAssoc,
                           idDAO)  # passa o id das duas ligacoes, da classe atual e da dao que sera criada
        #self.criaClasseDAO(idName, idDAO)  # passa o id que foi utilizado na ligacao
        if ePai == True:
            self.criaActiveRecord(idName, idDAO)

    def convertePIMtoPSM(self, aux, vet, ePai):
        self.insertGetSet(aux, vet)
        idDAO = "ADAAAAF" + str(random.randint(0, 9)) + "H" + str(random.randint(0, 9)) + "G" + str(
            random.randint(0, 9)) + "Mi" + str(
            random.randint(0, 9)) + "Z" + str(random.randint(0, 9)) + "X" + str(random.randint(0, 9)) + "="
        ## insere um ID para padronizar o DAO com sua ligacao
        self.insertLigacao(aux, aux['xmi:id'],
                           idDAO)  # passa o id das duas ligacoes, da classe atual e da dao que sera criada
        #self.criaClasseDAO(aux['name'], idDAO)  # passa o id que foi utilizado na ligacao
        if ePai == True:
            self.criaActiveRecord(aux['name'], idDAO)

    def percorreXMI(self, aux):
        ePai = True
        vet = []
        #print aux.attrs
        aux1 = aux.contents #pega todos os filhos da classe
        for k in aux1:
            try:
                if isinstance(k, Tag): #verifica se o filho e' uma tag
                    if k.name == "ownedAttribute":
                        for j in k.attrs: # se for, e' procurado os metodos para torna-los privados
                            if j == 'visibility' and k.attrs[j] == 'public' and k.attrs['xmi:type'] == "uml:Property": #verifica se a visibilidade e' publica e se e' um atributo da classe
                                k.attrs[j] = 'private'
                                vet.append(k.attrs['name'])

                    if k.name == 'ownedMember' and k.attrs['xmi:type'] == 'uml:Class': #realiza os ajustes nas classes associadas
                        self.classeAssociada(k, k['xmi:id'], k['name'])

                    if k.name == 'generalization':
                        ePai = False

            except: NavigableString
        self.convertePIMtoPSM(aux, vet, ePai)

        auxProx = aux.find_next_sibling('packagedElement')
        if auxProx != None and auxProx['xmi:id'][1] != 'D': #verifica se ainda tem alguma classe e se a proxima classe nao e' DAO
            self.percorreXMI(auxProx)
        else:
            pyFile = open('tcc/PSMgerado.xmi', "w" )
            StringSoup = str(soup)
            #print soup
            pyFile.write(StringSoup)


def main():
    xmi = Decodifica()


if __name__ == "__main__":
    main()

