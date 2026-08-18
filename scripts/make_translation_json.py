import json

names = {
    "Kirino": "Kirino",
    "Kyousuke": "Kyousuke",
    "Shiori": "Shiori",
    "Saori": "Saori",
    "Kuroneko": "Kuroneko",
    "Daisuke": "Daisuke",
    "Ayase": "Ayase",
    "???": "???",
    "Both": "Ambos",
    "Manami": "Manami",
    "Maid": "Sirvienta",
    "Akagi": "Akagi",
    "Yoshino": "Yoshino",
    "Meruru": "Meruru",
    "Kiririn": "Kiririn",
    "Rinko": "Rinko",
    "Announcer": "Locutor",
    "Speakers": "Altavoces",
    "Schoolgirl": "Colegiala",
    "Student": "Estudiante",
    "Doctor": "Doctor",
    "Older sis": "Hermana mayor",
    "Little sis": "Hermanita",
    "Passerby A": "Transeúnte A",
    "Passerby B": "Transeúnte B",
    "Rock": "Rock",
    "Miyabi": "Miyabi",
    "Kirara": "Kirara",
    "Commuter": "Pasajero",
    "Otaku A": "Otaku A",
    "Otaku B": "Otaku B",
    "Kanako": "Kanako",
    "Otaku": "Otaku",
    "Security": "Seguridad",
    "Bridget": "Bridget",
    "Woman A": "Mujer A",
    "Woman B": "Mujer B",
    "Sena": "Sena",
}

narration = {
    0: "Mi hermanita",
    1: "El nombre de mi hermanita es Kousaka Kirino, y va a la secundaria de aquí al lado.",
    2: "Con el pelo teñido de castaño, ambas orejas perforadas y sus uñas largas y cuidadas...",
    3: "Su bonita cara llama la atención incluso sin maquillaje; ¡pero con él, está absolutamente impresionante!",
    4: "Tiene una madurez poco común para una chica de secundaria; aunque su rostro es un poco redondeado.",
    5: "En fin, mi hermanita es una chica extraordinaria.",
    6: "Además, es modelo de una revista juvenil, la estrella del club de atletismo y ocupa el quinto lugar en los exámenes...",
    7: "En la escuela siempre existe ese grupo de estudiantes glamorosos con los que es difícil entablar una conversación, ¿verdad?",
    8: "Bueno, el núcleo de ese grupo es Kirino.",
    9: "Intenta imaginar tener una hermana así.",
    10: "...¿Y qué? ¿Ahora entiendes un poco mejor mi vergüenza?",
    11: "Dicho esto, mi nombre es Kousaka Kyousuke. Tengo dieciocho años y asisto a la preparatoria de aquí al lado.",
    12: "Aunque sea un poco vergonzoso, soy un estudiante de preparatoria muy común...",
    13: "Mi único deseo es vivir una vida normal.",
    14: "No necesito en mi vida situaciones cotidianas fuera de lo común ni conocer gente peculiar.",
    15: "Podrías decir que soy un holgazán, pero la mediocridad es mi lema.",
    16: "Mi meta es contemplar el paisaje inmutable y estancado.",
    17: "¡Banzai a la mediocridad! ¡Viva mi vida ordinaria...! O eso debería ser...",
    18: "Si tan solo no me hubiera involucrado con mi hermana y los «agradables camaradas» que la rodean...",
    20: "Todo empezó con esta misma frase.",
    21: "La chica de secundaria perfecta y hermosa ante mis ojos es en realidad...",
    26: "Tener una gran cantidad de juegos relacionados con hermanitas... una otaku.",
    27: "Para futuras referencias, debo decir esto...",
    28: "Si alguien te pidiera una «sesión de orientación en la vida», sería mejor que la rechazaras.",
    29: "Especialmente si esa persona es tu «hermanita».",
}

speech = {
    19: "Necesito orientación en la vida",
    22: "...Entonces quieres decir que tú, eh... Aunque sea difícil de creer...",
    23: "¿Te gustan las «hermanitas»?",
    24: "¿Y por eso tienes tantos de esos juegos?",
    25: "¡Sip!",
}

entry = {}
for i, t in narration.items():
    entry[str(i)] = t
for i, t in speech.items():
    entry[str(i)] = "「" + t + "」"

data = {"000scriptAKYO_0000A.obj": entry, "names": names}

path = "/mnt/c/Users/christ-gm/Desktop/code/oreimo/work/disc1/Data/Translation.json"
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("written", path)
print("lines:", len(entry))