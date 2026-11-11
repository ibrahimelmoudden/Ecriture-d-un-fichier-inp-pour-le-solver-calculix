import numpy as np

"""

Les fonctions suivantes servent à écrire le fichier INP pour une analyse avec le solver CCX  des Shell avec des élements

S8  - Il reste à compléter

"""

def createDictnode(nodeTags,nodeCoord):

    Nodes = dict()
    
    for k in range(len(nodeTags)):
    
        Nodes[nodeTags[k]] = (nodeCoord[3 * k], nodeCoord[3 * k + 1], nodeCoord[3 * k + 2])

    return Nodes


def writeAllNodesAndElements(nodeTags,nodeCoord,elementNodeTags,elementTags,ccxElementType,nameFile):

    """
    
    nodeTags : Liste contenant tous les noeuds du maillage avec leur numératation (Tag) unique

    nodeCoord : Liste contenant les coordonnées des noeuds du maillage par ordre successif. 

    elementNodeTags : numpy array contenant les noeuds des éléments du maillage

    elementTags : numpy array contenant une liste des éléments du maillage (d'un modèle 2D)

    ccxElementType : le type d'élément calculix utilisé (pour l'instant juste les éléments 2D, du type S4, S8, CPS4, CPS8)

    nameFile : string correspondant au nom du fichier inp 

    Les entrée nodeTags et nodeCoord de la fonction doivent correspondre à ce que retourne la fonction gmsh.model.mesh.getNodes 
    
    de même elementNodeTags, elementTag doivent correspondre à ce que retourne la fonction gmsh.model.mesh.getElements -> voir doc Gmsh

    La fonction écrit les noeuds et les éléments du maillage sur le fichier inp

    """

    # Créer un dictionnaire où à chaque noeud (Clé) on associe ses coordonnées (x,y,z) (Valeur)

    Nodes = createDictnode(nodeTags,nodeCoord)

    f = open(nameFile,"a")

    f.write("*NODE, NSET=Nall\n")

    for k in range(len(nodeTags)):
        if nodeTags[k] in elementNodeTags[0]:
            f.write(str(nodeTags[k]) + ", " + str(Nodes[nodeTags[k]][0]) + ", "+ str(Nodes[nodeTags[k]][1]) + ", " +  str(Nodes[nodeTags[k]][2])+ "\n")

    # Créer un dictionnaire où chaque à élément S8 , on associe ses 8 noeuds 

    Elements = dict()

    nb_nodes = 0 # nombre de noeuds contenu dans l'élément

    if ccxElementType == 'S8' or ccxElementType == 'CPS8':

        nb_nodes = 8

    if ccxElementType == 'S4' or ccxElementType == 'CPS4':

        nb_nodes = 4

    if ccxElementType == 'S3':

        nb_nodes = 3

    if ccxElementType == 'S6':

        nb_nodes = 6

    # Les cas sont à compléter -- mais je m'arrête ici pour l'utilisation que j'en fait pour l'instant

    try:

        for k in range(len(elementTags[0])):

            L = []

            for i in range(nb_nodes):

                L.append(elementNodeTags[0][nb_nodes * k + i])

            Elements[elementTags[0][k]] = L


        f.write(f"*ELEMENT, TYPE={ccxElementType}, ELSET = Eall\n")

        for k in range(len(elementTags[0])):

            f.write(str(elementTags[0][k]) + ' ,' )

            for i in range(nb_nodes):

                if i < nb_nodes - 1:

                    f.write(str(Elements[elementTags[0][k]][i]) + ' ,')

                else :

                    f.write(str(Elements[elementTags[0][k]][i]) + '\n')
    except:

        print("L'élément CCX ne correspond pas à l'élément du maillage Gmsh")


    f.close()


        


def writeHeading(text, nameFile):

    """
    
    text : (String) Le texte est écrit en haut du fichier, pour donner une information 

    nameFile : (String) Nom du fichier avec son extention (.inp)

    """

    f = open(nameFile,"a")

    f.write("*HEADING\n")

    f.write(text+ "\n")

    f.close()



def nodeSetWithXconstraint(dictNodes, X, tolerance,Z = 0):

    """
    
    dictNodes : Dictionnaire des noeuds avec leurs coordonnées associées 

    X : valeur de X commune des noeuds

    Z : valeur de Z commune des noeuds (valeur par défaut à 0 car étude sur des plaques)

    tolerance : Tolérance sur les coordonnées (Dès fois les noeuds se situant proche mais pas exactement aux coordonnées préscrites)

    La fonction retourne un node set 
    
    """

    listNodeSet = [] 
    
    for node in dictNodes:

        if Z - tolerance < float(dictNodes.get(node)[2]) and float(dictNodes.get(node)[2]) < Z + tolerance:
    
            if  X - tolerance < float(dictNodes.get(node)[0])  and  float(dictNodes.get(node)[0]) < X + tolerance:
    
                    listNodeSet.append(node)
    
    return listNodeSet

def nodeSetWithYconstraint(dictNodes, Y, tolerance,Z = 0):

    """
    
    dictNodes : Dictionnaire des noeuds avec leurs coordonnées associées 

    Y : valeur de Y commune des noeuds

    Z : valeur de Z commune des noeuds (valeur par défaut à 0 car étude sur des plaques)

    La fonction retourne un node set 
    
    """

    listNodeSet = [] 
    
    for node in dictNodes:

        if Z - tolerance < float(dictNodes.get(node)[2]) and float(dictNodes.get(node)[2]) < Z + tolerance:
    
            if  Y - tolerance < float(dictNodes.get(node)[1]) and float(dictNodes.get(node)[1]) < Y + tolerance:
    
                    listNodeSet.append(node)
    
    return listNodeSet



def createNodeset(dictNodes, X, Y, tolerance, Z = 0):

    """
    
    dictNodes : Dictionnaire des noeuds avec leurs coordonnées associées 

    X : Coordonnée X des noeuds, si None le node set n'est pas défini à partir d'une coordonnée X commune 

    Y : Coordonnée Y des noeuds, si None le node set n'est pas défini à partir d'une coordonnée Y commune 

    Z : Coordonnée Z des noeuds (Z = 0 par défaut)
   
    tolerance : Tolérance sur les coordonnées (Dès fois les noeuds se situant proche mais pas exactement aux coordonnées préscrites)
   
    La fonction retourne une liste des neouds verifiant les contraintes
    
    """

    if X == None:

        return nodeSetWithYconstraint(dictNodes,Y,tolerance,Z)

    if Y == None:

        return nodeSetWithXconstraint(dictNodes,X,tolerance,Z)

    
    

def writeNset(listNodeset, fileName, nsetName):

    """
    
    listNodeset : Liste de noeuds

    fileName : (String) Nom du fichier avec son extension (.inp)

    nsetName : (String) Nom donné à l'ensemble de noeuds

    La fonction écrit le NSET dans le fichier input de calculiX (Généralement utilisé pour définir les BC)

    """

    f = open(fileName,"a")

    f.write("*NSET, NSET=" + nsetName + "\n")

    for k in range(len(listNodeset)):

        if k < len(listNodeset) - 1:

            f.write(str(listNodeset[k]) +', ')

            if k%10 == 0 and k != 0:

                f.write("\n")

        else:

            f.write(str(listNodeset[k]))

    f.write("\n")


def writeEset(listElementSet,fileName,esetName):

    """
    
    listElementSet : Liste des éléments

    fileName : Nom du fichier avec son extension

    esetName : nom donné à l'ensemble des éléments

    La fonction écrit le Eset dans le fichier input de CalculiX
    
    """

    f = open(fileName,"a")

    f.write("*ESET, ESET=" + esetName + "\n")
    
    for k in range(listElementSet):
    
        if k < len(listElementSet) - 1:
    
            f.write(str(listElementSet[k]) +', ')
    
            if k%20 == 0 and k!= 0:
    
                f.write("\n")
    
        else:
    
            f.write(str(listElementSet[k]))


def writeSurface(EsetName,direction,fileName,surfaceName):

    """
    
    EsetName : Nom de l'ensemble des éléments définissant la surface

    direction : (Int) 2 = Spos ; 1 = Sneg

    La fonction écrit sur le fichier inp la surface sur laquelle va s'exercer la charge
    
    """

    f = open(fileName, "a")

    surface = ""

    if direction == 2:

        surface = "S2"

    else:

        surface = "S1"

    f.write("*SURFACE, " + "NAME=" + surfaceName + ", TYPE=ELEMENT"+"\n")
    f.write(EsetName + ", " + surface + "\n")


def writeMaterial(Elasticity,Norton,Alpha,fileName,materialName):

    """
    
    Elasticity = [(E1,nu1,T1),(E2,nu2,T2),...] ou simplement [(E,nu)] si constantes élastiques indépendantes de la température

    Norton = [(A1,n1,m2,T1),(A2,n2,m2,T2),...] : constante loi de norton ou simplement [(A,n,m)] si indépendante de la température

    Alpha = [(alpha1,T1),(alpha2,T2),...]: coefficient d'expansion ou simplement [alpha] si indépendante de la température

    fileName : nom du fichier 

    materialName : nom du matériau

    La fonction définit le matériau
    
    """

    f = open(fileName,"a")

    f.write("*MATERIAL,  Name=" + materialName + "\n")

    f.write("*ELASTIC\n")

    try: 

        for i in range(len(Elasticity)):

            f.write(str(Elasticity[i][0])+", "+str(Elasticity[i][1]) + ", "+str(Elasticity[i][2]) +"\n")
    except:

        for i in range(len(Elasticity)):
        
            f.write(str(Elasticity[i][0])+", "+str(Elasticity[i][1]) + "\n")


    f.write("*EXPANSION, ZERO=293\n")

    try:

        for i in range(len(Alpha)):

            f.write(str(Alpha[i][0])+", "+str(Alpha[i][1])+"\n")

    except:

        for i in range(len(Alpha)):
        
            f.write(str(Alpha[i])+"\n")

    f.write("*CREEP, LAW=NORTON\n")

    try:

        for i in range(len(Norton)):

            f.write(str(Norton[i][0]) + ", "+str(Norton[i][1]) + ", "+ str(Norton[i][2]) +", "+ str(Norton[i][3]) +"\n")

    except:

        for i in range(len(Norton)):
        
            f.write(str(Norton[i][0]) + ", "+str(Norton[i][1]) + ", " +str(Norton[i][2])+"\n")

    f.close()


def writeShellSection(thickness,materialName,fileName):

    """
    thickness : épaisseur de plaque 
    materialName : nom du matériau 
    fileName : nom du fichier avec l'extension inp
    
    """

    f = open(fileName,"a")
    f.write("*SHELL SECTION, ELSET=Eall, MATERIAL=" + materialName + ", OFFSET=0\n")
    f.write(str(thickness)+"\n")
    f.close()



def createBC(u1,u2,u3,ur1,ur2,ur3,nsetName):

    """
    u1,u2,u3 : déplacements purs respectivement selon x, y et z
    
    ur1,ur2,ur3 : rotations pures respectivement autour de x,y et z
    
    si pas de prescription la valeur doit prendre None

    la fonction retourne simplement une liste contenant les 6 degrés de libertés et le nom du Nset où la condition aux limites en

    déplacement va s'appliquer
    
    """

    return [u1,u2,u3,ur1,ur2,ur3,nsetName]



def writeBoundary(u1,u2,u3,ur1,ur2,ur3,fileName,nsetName):

    """
    
    u1,u2,u3 : déplacements purs respectivement selon x, y et z

    ur1,ur2,ur3 : rotations pures respectivement autour de x,y et z

    si pas de prescription la valeur doit prendre None
    

    """

    f = open(fileName,"a")
    f.write("*BOUNDARY\n")

    L = [u1,u2,u3,ur1,ur2,ur3]

    if all ( x == 0 for x in L):

        f.write(nsetName + ", 1, 6, 0\n")

    else:

        for k in range(len(L)):

            if L[k] != None:

                f.write(nsetName + ", " + str(k+1) + ", " + str(k+1) + ", " + str(L[k]) + "\n")

    f.close()

def dload(surface,elsetName,load,fileName):

    """

    load : charge surfacique

    elsetName : Nom de l'emsemble des éléments sur lesquelles s'applique la charge surfacique

    surface : 2 = Spos, 1 = Sneg : orientation de la surface sur laquelle s'applique la charge 

    la fonction écrit la charge à appliquer DLOAD sur le fichier input de calculiX
    
    """

    f = open(fileName,"a")

    f.write("*DLOAD\n")

    if surface == 2:

        f.write(elsetName + ", " + "P2, " + str(load)+"\n")

    if surface == 1:

        f.write(elsetName + ", " + "P1, " + str(load)+"\n")

    f.close()

def writeStepStatic(loads,boundaries,temperature,fileName):

    """
    loads : Liste des Load (On traite que les Dload pour l'instant)

    boundaries : Listes des Boundary Conditions

    temperature : [g,dictnode] g: fonction décrivant la distribution de température et dictnode : dictionnaire des noeuds

    si pas de température dans l'analyse, mettre None

    La fonction écrit le step static dans l'input file
    
    """

    f = open(fileName,"a")

    f.write("*STEP, NLGEOM\n")   # non linéarité géométrique
    f.write( "*STATIC\n")  # , SOLVER=Pardiso

    f.close()

    for k in range(len(boundaries)):

        writeBoundary(boundaries[k][0],boundaries[k][1],boundaries[k][2],boundaries[k][3],boundaries[k][4]

                      ,boundaries[k][5],fileName,boundaries[k][6])

    for k in range(len(loads)):
    
        dload(loads[k][0],loads[k][1],loads[k][2],fileName)


    if temperature != None:

        writeTempToNode(temperature[0],temperature[1],fileName)


    f = open(fileName,"a")


    # Fichier dat -- Un peu hard codé -- à revoir ultérieurement

    f.write("*NODE PRINT,NSET=Nall\n" + "U\n")  

    f.write("*EL PRINT,ELSET=Eall\n" + "S\n")
            
    f.write("*NODE FILE\n")

    f.write( "RF, U, NT\n")

    f.write("*EL FILE\n")

    f.write("S, E\n")

    f.write("*END STEP\n")

    f.close()


def writeCreepStep(fileName,temperature,duration):

    f = open(fileName,"a")

    f.write("*STEP \n"+ "*Visco, cetol=0.5e-5 \n" + "1, " + str(duration) +", 1e-10\n")

    f.close()
    
    if temperature != None:

        writeTempToNode(temperature[0],temperature[1],fileName)

    f = open(fileName,"a")

    f.write("*END STEP\n")

    f.close()
    


def writeInitialTemp(temp,file_name,nsetName):

    """
    
    nsetName : nom du Nset pour lequel on fixe une température initiale, sinon écrire [g,Nodes] pour une définition de la température
    en chaque point comme pour la fonction writeTempToNode, dans ce cas mettre n'importe quelle valeur en temp

    """

    f = open(file_name,"a")

    f.write("*INITIAL CONDITIONS, TYPE=TEMPERATURE\n")

    try:

        f.write(nsetName+", "+str(temp)+"\n")

    except:

        for node in nsetName[1]:
        
            f.write(str(node) + ", " + str(nsetName[0](nsetName[1].get(node)[0],nsetName[1].get(node)[1]))+"\n")


    f.close()


def writeTempToNode(g,dictNode,file_name):

    """
    g : fonction caractérisant la distribution de la température dans le modèle 

    dictNode : dictionnaire des noeuds du modèle 

    La fonction écrit la température de chaque noeud dans le fichier input 
    
    """

    f = open(file_name,"a")

    f.write("*TEMPERATURE\n")

    for node in dictNode:

        f.write(str(node) + ", " + str(g(dictNode.get(node)[0],dictNode.get(node)[1]))+"\n")

    f.close()

