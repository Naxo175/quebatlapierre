class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


import pathlib
import textwrap

from google import genai

import markdown

client = genai.Client(api_key="AIzaSyDiE2t1fRfvbArshpnkXo5b_B3RIESW1lE")

def to_markdown(text):
  text = text.replace('•', '  *')
  return markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


currentElement = "la pierre"

# 0 = Bonnes réponses ; 1 = Mauvaises réponses
counter = [0, 0]

while True:

    userInput = str(input(bcolors.OKBLUE + "Que bat : " + bcolors.OKCYAN + currentElement + bcolors.OKBLUE + " ? \n -> " + bcolors.OKCYAN))

    prompt = f"""
    Nous jouons à une version étendue de pierre, papier, ciseaux, sauf que les joueurs peuvent choisir littéralement n'importe quoi. Vous êtes l'animateur du jeu. Votre rôle est de déterminer si chaque choix bat le précédent ou non.

    Fournissez une réponse claire : écrivez "True" si le choix actuel bat le précédent, ou "False" dans le cas contraire.
    Justifiez votre décision en une seule phrase (70 caractères max).
    Vos justifications doivent être logiques, cohérentes avec votre réponse, originales et empreintes de sarcasme ou d'esprit.
    Exemple 1 :

    Entrée utilisateur : papier
    Entrée précédente : pierre
    Réponse : True
    Justification : Le papier couvre la pierre. Incroyable révolution, non ?
    Exemple 2 :

    Entrée utilisateur : amour
    Entrée précédente : pierre
    Réponse : False
    Justification : L'amour, c'est bien, mais il ne brise pas une pierre. Next.
    Règles pour éviter les contradictions :

    La justification doit être en accord avec la réponse donnée.
    Si vous répondez "True", expliquez pourquoi le choix actuel gagne.
    Si vous répondez "False", expliquez pourquoi il perd.
    Évitez les contradictions dans vos explications (par exemple : ne dites pas qu'une pierre écrase une carotte si vous répondez "False").
    Exemple à tester :

    Entrée utilisateur : {userInput}
    Entrée précédente : {currentElement}
    Répondez et justifiez.
    """

    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)

    print(bcolors.WARNING + str(response.prompt_feedback))

    lines = response.text.splitlines()

    result = lines[0]
    justification = lines[1]
    # print(result, "|", justification)

    if ("True" or "Vrai") in result:
        print("✅ " + bcolors.OKGREEN + justification.replace("Justification : ", ""))
        currentElement = userInput
        counter[0] += 1
    elif ("False" or "Faux") in result:
        print("❌ " + bcolors.FAIL + justification.replace("Justification : ", ""))
        counter[1] += 1
    else:
        print(bcolors.WARNING + "⚠️  ERREUR: Gemini n'a pas retourné \"True\" ni \"False\". Voici ce que Gemini a retourné: " + lines[0])
    
    print(f"{bcolors.HEADER} Bonnes réponses : {bcolors.OKGREEN} {counter[0]} {bcolors.HEADER} | Mauvaises réponses : {bcolors.FAIL} {counter[1]}\n")
    
    # print("\n Response text : ", response.text)



# print(bcolors.WARNING + str(model), "\n", bcolors.OKGREEN + str(response))