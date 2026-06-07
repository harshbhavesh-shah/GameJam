from PIL import Image

image = Image.open("C:\\Users\\jolan\\Downloads\\level1foret.png")
result = []

for ligne in range(36):
    result.append([])
    for colonne in range(64):
        match image.getpixel((colonne,ligne))[:-1]:
            case (255, 255, 255):   result[ligne].append(" ")   # Blanc : vide
            case (0, 0, 0):         result[ligne].append("b")   # Noir : bloc
            case (237, 28, 36):     result[ligne].append("s")   # Rouge : pique
            case (153, 217, 234):   result[ligne].append("p")   # Turquoise clair : porte
            case (63, 72, 204):     result[ligne].append("m")   # Bleu indigo : blocMouv
            case (195, 195, 195):   result[ligne].append("S")   # Gris clair : spawn
            case (127, 127, 127):   result[ligne].append("E")   # Gris : end
            case (200, 191, 231):   result[ligne].append("r")   # Lavande : requin
            case (34, 177, 76):     result[ligne].append("l")   # Vert : lianes
            case (255, 127, 39):    result[ligne].append("P")   # Orange : PNJs
            case (181, 230, 29):    result[ligne].append("t")   # Vert clair : tortue
            case (185, 122, 87):    result[ligne].append("A")   # Brun : arbre
            case (255, 174, 201):   result[ligne].append("T")   # Rose saumon : blocTombant
            case (163, 73, 164):    result[ligne].append("f")   # Violet : branchenflame
            case (112, 146, 190):   result[ligne].append("B")   # Bleu gris : deuxième type de bloc
            

file = open("convertisseur_output.txt","w")
            
file.write(str(result).replace("'","\"").replace(", ",",").replace("],[","],\n["))

file.close()