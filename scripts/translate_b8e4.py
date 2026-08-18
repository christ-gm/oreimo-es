import json

PATH = "/mnt/c/Users/christ-gm/Desktop/code/oreimo/work/disc1/Data/Translation.json"

def build(narration, speech):
    out = {}
    for i, t in narration.items():
        out[str(i)] = t
    for i, t in speech.items():
        out[str(i)] = "「" + t[0] + "」"
    return out

n = {
    483: "Mientras era abrazada por Ayase, Kirino lloró.",
    484: "Lágrimas enormes cayeron de sus ojos, mientras Ayase la sostenía fuerte sin soltarla.",
    485: "Esta es la primera vez que vi a Kirino así.",
    486: "Y también la primera vez que me di cuenta de lo débil que es Kirino.",
    492: "Ayase acarició suavemente la cabeza de Kirino, que se estaba derrumbando llorando.",
    493: "Tenía una expresión tranquila y amable en su cara, como una santa.",
    494: "Mientras miraba esa expresión tranquila, de repente me di cuenta.",
    495: "Podría haber sido un acosador, pero la persona que enviaba los correos amenazantes parecía poder descubrir las nuevas direcciones.",
    496: "Además, no solo conocía a las amigas normales de Kirino, sino también las direcciones de sus amigas ocultas, Kuroneko y Saori.",
    497: "¿Cómo lo sabe eso?",
    498: "Solo puede haber una razón. Tuvo que haber visto el teléfono de Kirino.",
    499: "Entonces, ¿quién podría tener acceso al teléfono de Kirino?",
    501: "Recuerdo que hace un tiempo Kirino dijo que Ayase tomó prestado su teléfono para hacer decoraciones a juego.",
    502: "Desde entonces, el teléfono de Kirino se volvió llamativo y brillante.",
    503: "Es decir, el teléfono fue confiado a Ayase, y ella le puso decoraciones a juego.",
    505: "¿Puede      ser       ?",
    506: "Miré a Ayase por un momento. Ayase todavía sostenía a Kirino y le frotaba la espalda.",
    507: "Mirando esta escena, no puedo evitar romper en un sudor frío.",
    508: "No, ¿puede ser... pero... solo puede ser...",
    512: "Aunque no quería considerar esto, lo más probable es...",
    513: "No, mejor me detengo. Lo estoy sobre-pensando...",
    514: "Incluso si es muy probable, no hay prueba para ello.",
    515: "Ya que está tan preocupada por Kirino, no puede ser eso...",
    516: "Aunque seguí pensando así, esa expresión de Ayase seguía flotando en mi mente.",
}
s = {
    487: ("Ayase... Ayase...", "Kirino"),
    488: ("Sip...", "Ayase"),
    489: ("¡Solo Ayase me entiende...! ¡Ayase es lo único que me queda...!", "Kirino"),
    490: ("Pase lo que pase, siempre estaré a tu lado. Incluso tomaré la parte de las otras amigas, y siempre estaré contigo.", "Ayase"),
    491: ("Sí... Ayase... Ayase...", "Kirino"),
    500: ("...Está bien, Kirino.", "Ayase"),
    504: ("......", "Kyousuke"),
    509: (".........", "Ayase"),
    510: ("¡--!", "Kyousuke"),
    511: ("...jeje.", "Ayase"),
}

with open(PATH, "r", encoding="utf-8") as f:
    current = json.load(f)
entry = current.get("000scriptIYAN_0000E.obj", {})
entry.update(build(n, s))
current["000scriptIYAN_0000E.obj"] = entry
with open(PATH, "w", encoding="utf-8") as f:
    json.dump(current, f, ensure_ascii=False)
print("updated 000scriptIYAN_0000E.obj (part D)")