import json

PATH = "/mnt/c/Users/christ-gm/Desktop/code/oreimo/work/disc1/Data/Translation.json"

def build(narration: dict, speech: dict) -> dict:
    out = {}
    for i, t in narration.items():
        out[str(i)] = t
    for i, t in speech.items():
        out[str(i)] = "「" + t[0] + "」"
    return out

a0_n = {
    0: "Ruta de Kirino · Es Imposible Que Mi Hermanita No Acepte Un Recuerdo",
    3: "Ya que los zapatos de mi hermana están en la puerta, Kirino debería estar en casa.",
    4: "No la he visto por un par de días...",
    5: "Bueno entonces, probablemente debería darle los recuerdos primero.",
    6: "No es que realmente quiera ver la cara feliz de mi hermanita ni nada.",
    7: "Solo quiero terminar rápidamente las cosas que mi hermana me pidió hacer, para poder relajarme un poco.",
    9: "....Oh, whoa. Por poco.",
    10: "Aunque pasé por tantas molestias solo para comprarle la «Meruru Edición Regional» en Kioto, sería una tontería de mi parte molestarla al entregarle",
    11: "el recuerdo equivocado.",
    12: "Ver la cara enojada de mi hermanita, a quien no he visto en un tiempo, haría inútil la compra de los recuerdos....",
    13: "¿Será que estoy más cansado de lo que pensaba?",
    17: "Esta chica, de repente chasqueando la lengua así. No es nada linda.",
}
a0_s = {
    1: ("¡Ya estoy en casa!", "Kyousuke"),
    2: ("Ni un bienvenido a casa, eh. Qué familia de corazón frío.", "Kyousuke"),
    8: ("Si recuerdo correctamente, lo metí en el bolsillo de esta bolsa...", "Kyousuke"),
    14: ("Probablemente sea mejor darle a Kirino sus recuerdos e irme directo a la cama.", "Kyousuke"),
    15: ("Oh, Kirino. Oye, ya volví.", "Kyousuke"),
    16: ("....Tch.", "Kirino"),
    18: ("Oye... ¿Es esa la actitud correcta hacia tu hermano que te compró recuerdos?", "Kyousuke"),
    19: ("¿Eh?", "Kirino"),
    20: ("¿Por qué suenas sorprendida? Me lo pediste, ¿no?", "Kyousuke"),
    21: ("..............", "Kirino"),
    22: ("¿Eh? ¿Dije algo extraño?", "Kyousuke"),
    23: ("......*suspiro*", "Kirino"),
    24: ("No, como dije, compré la Meruru Edición Regional que me pediste?", "Kyousuke"),
    25: ("Meruru Edición Regional. Correcto, esta cosa. Se la daré de inmediato.", "Kyousuke"),
}

a2_n = {
    0: "Ruta de Kirino · Es Imposible Que Mi Hermanita Esté En El Baño",
    2: "Sin respuesta, eh. No debe estar en su habitación ahora mismo.",
    7: "No es que planees... planee espiar, así que debería estar bien si pongo el recuerdo de Meruru Edición Regional encima de su ropa limpia, ¿no?",
    8: "No obstante, esa Kirino... ¿de verdad necesita tirar su ropa por la habitación después de quitársela?",
    9: "...¿Acaso tiene algo de vergüenza?",
    19: "...Rayos, parece que la he enojado bastante.",
    21: "Después de aproximadamente una hora, intenté encontrar una buena oportunidad para hablar con Kirino, pero...",
    27: "Nada bien... todavía está enojada conmigo...",
}
a2_s = {
    1: ("Kirino～", "Kyousuke"),
    3: ("Kirino～", "Kyousuke"),
    4: ("Kirino-san, ¿dónde estás?", "Kyousuke"),
    5: ("¿Hm? ¿Escucho un tarareo? ...Suena como si viniera del baño.", "Kyousuke"),
    6: ("Ah, ya veo. Regreso de mi viaje escolar, agotado, y aquí está mi hermana, disfrutando tranquilamente de su baño.", "Kyousuke"),
    10: ("Oh bueno, supongo que no hay remedio, al menos puedo ponerlas en la lavadora por ella.", "Kyousuke"),
    11: (".........", "Kirino"),
    12: ("......Y-Ya llegué.", "Kyousuke"),
    13: ("¡Ah-aah, Ahhhhhhhhhhhhhhhhhhhhhhhhhhhhh!", "Kirino"),
    14: ("¡¿Quéééééééééééééééééééééééééé?!", "Kyousuke"),
    15: ("O-Oh...ah, esa chica... saliendo y golpeándome sin avisar...", "Kyousuke"),
    16: ("¡No tiene que enojarse TANTO por eso!", "Kyousuke"),
    17: ("Somos hermanos, así que un pequeño vistazo no debería significar nada, ¿verdad?", "Kyousuke"),
    18: ("¡¿Qué clase de excusa es esa?! ¡Muere!", "Kirino"),
    20: ("...Realmente la regué. Solo le daré el recuerdo y me disculparé luego, en persona.", "Kyousuke"),
    22: ("Oye, de verdad lamento lo que pasó allá atrás.", "Kyousuke"),
    23: ("......", "Kirino"),
    24: ("...Mira, te compré el recuerdo, ¿okay? Vamos, no te enojes.", "Kyousuke"),
    25: ("..............", "Kirino"),
    26: ("Estás siendo molesto.", "Kirino"),
    28: ("N-No seas así. Aquí, te conseguí el recuerdo.", "Kyousuke"),
}

a3_n = {
    0: "Ruta de Kirino · Es Imposible Que Mi Hermanita No Acepte Un Recuerdo",
    5: "¿Qué le pasa?",
    6: "¡¿A pesar de babear por coleccionar todo el set de Meruru, me llama solo pervertido por tener Meruru?!",
    7: "En realidad, ¿podría haber olvidado que me pidió conseguir el recuerdo?",
}
a3_s = {
    1: ("...¿Qué es eso?", "Kirino"),
    2: ("¿Qué quieres decir con «¿Qué?»... ¿no es esto Meruru?", "Kyousuke"),
    3: ("...Asqueroso.", "Kirino"),
    4: ("¡Oye! ¡No hay nada asqueroso en tu amada Meruru!", "Kyousuke"),
}

a4_n = {
    0: "Ruta de Kirino · Es Imposible Que Mi Hermanita No Acepte Un Recuerdo",
    5: "...Siento que esta conversación no va a ninguna parte.",
    20: "¿Eh? ¿No parece esta conversación un poco extraña? ¿Qué está pasando?",
    30: "¿E-Esas cosas?",
    44: "Solo hemos estado separados por tres días... ¡¿Qué diablos está pasando?!",
    54: "No he hablado con ella en mucho tiempo... ¿dice....?",
    55: "N-No puede ser. ¿Podría ser este el remate de algún sueño....? ¡¿Imposible?!",
    56: "No, pero pensándolo, tener una hermanita que es otaku - ¿es esto como un Galge? Al menos es el tipo de ambientación que se siente.",
}
a4_s = {
    1: ("Bueno, como he dicho, ¡es tu recuerdo, no mío! ¡No tengo tal interés en Meruru!", "Kyousuke"),
    2: ("...¿Huh?", "Kirino"),
    3: ("¡¿Qué quieres decir con «¿Huh?»!? ¡¿No es esto lo que querías?!", "Kyousuke"),
    4: ("...¿Por qué?", "Kirino"),
    6: ("Ah... ¿podría ser que esta no es la versión que querías?", "Kyousuke"),
    7: ("Entonces no tienes que preocuparte. ¡Ya te conseguí el set completo de todos modos! He preparado apropiadamente todos los tipos diferentes.", "Kyousuke"),
    8: ("...Molesto.", "Kirino"),
    9: ("¡Desprecias todo mi arduo trabajo con solo una palabra...!", "Kyousuke"),
    10: ("¿Por qué no te gusta este recuerdo? Estaba seguro de que querías que comprara la Meruru Edición Regional...", "Kyousuke"),
    11: ("...*suspiro*", "Kirino"),
    12: ("En serio no entiendo de qué estás hablando... Apestas a otaku.", "Kirino"),
    13: ("¡¿Apestar a otaku!? ¡Eso es cruel!", "Kyousuke"),
    14: ("¡Voy a llorar si no lo dejas ya!", "Kyousuke"),
    15: ("...Haz lo que quieras.", "Kirino"),
    16: ("Dime, ¿acaso me equivoqué en algo por casualidad?", "Kyousuke"),
    17: ("...¿Huh?", "Kirino"),
    18: ("Como dije, tienes que decirme si hice algo mal.", "Kyousuke"),
    19: ("Tch...", "Kirino"),
    21: ("Bueno entonces, ¿qué voy a hacer con todos estos? Aunque pasé por tantas molestias para comprarlos...", "Kyousuke"),
    22: ("...Si no los necesitas, ¿por qué no los tiras?", "Kirino"),
    23: ("¡!?", "Kyousuke"),
    24: ("N-N-No, no importa lo que pase, creo que tirarlos es simplemente...", "Kyousuke"),
    25: ("Tch...", "Kirino"),
    26: ("¡Te digo que estas son las cosas que me pediste conseguir!", "Kyousuke"),
    27: ("¿De qué has estado balbuceando desde hace rato de todos modos? Eres seriamente molesto.", "Kirino"),
    28: ("¡Es Meruru! ¿Por qué tu reacción es tan débil?", "Kyousuke"),
    29: ("...Te dije, no sé nada de esas cosas.", "Kirino"),
    31: ("Oye, ¿de verdad no los quieres?", "Kyousuke"),
    32: ("No los quiero.", "Kirino"),
    33: ("¿De verdad, de verdad no los quieres?", "Kyousuke"),
    34: ("¡No los quiero!", "Kirino"),
    35: ("¿De verdad, de verdad, de verdad, de verdad no los quieres?", "Kyousuke"),
    36: ("¡Eres tan persistente! ¡Te digo que no los quiero!", "Kirino"),
    37: ("......¿Estás bromeando conmigo?", "Kyousuke"),
    38: ("...No me hables más.", "Kirino"),
    39: ("Justo cuando pensé que había pasado mucho tiempo desde que hablamos por última vez..", "Kirino"),
    40: ("¿Solo han pasado tres días y llamas eso mucho tiempo?", "Kyousuke"),
    41: ("No lo digas como si fuéramos cercanos.", "Kirino"),
    42: ("¡¿A-Actualmente llegarías tan lejos como para decir eso?!", "Kyousuke"),
    43: ("...*suspiro* eres increíble.", "Kirino"),
    45: (".................", "Kyousuke"),
    46: ("...¿Qué estás mirando fijamente?", "Kirino"),
    47: ("Guh...", "Kyousuke"),
    48: ("Ahhh, ¡en serio me estoy enojando!", "Kirino"),
    49: ("¡¿Qué es eso?!", "Kyousuke"),
    50: ("...No me vuelvas a hablar jamás.", "Kirino"),
    51: ("...Justo cuando pensé que no había hablado contigo en mucho tiempo... Eres lo peor viniendo aquí solo para molestarme.", "Kirino"),
    52: ("¿E-En mucho tiempo?", "Kyousuke"),
    53: ("¿Huh? ¿De qué te sorprendes?", "Kirino"),
    57: ("....Entonces, esto es la realidad y todo lo que estaba viviendo hasta ahora fue un sueño....? Entonces, todo el desarrollo hasta este punto fue mi propio deseo....", "Kyousuke"),
    58: ("¿Qué estás haciendo murmurando para ti en tu propio pequeño mundo...? ¿Estás recibiendo ondas de radio extrañas?", "Kirino"),
}

a5_n = {
    0: "Ruta de Kirino · Es Imposible Que Mi Hermanita No Acepte Un Recuerdo",
    2: "...Esta chica, se está volviendo toda engreída en el momento en que me vuelvo modesto!",
    4: "...¿Qué? ¡Esos ojos parecen estar mirando a un pervertido!",
    5: "No solo hacia mí, sino que también soltó esos malos comentarios hacia Meruru...",
    6: "¿Está realmente tan enojada...?",
    12: "Más importante, la Meruru Edición Regional en mi mano se ha vuelto un problema considerable.",
    13: "Bueno entonces, ¿qué debería hacer?",
    14: "Ya que quedármelo yo está fuera de cuestión, tampoco podría dárselo a mi madre.",
    15: "¿Debería dárselo a Manami?",
    16: "Pero...",
    18: "Esa Kirino, lo quería tanto antes. Probablemente dijo que no lo quería porque está enojada conmigo.",
    19: "Estoy seguro de que cambiará de opinión después de que su enojo se haya calmado.",
    20: "Lo conservaré por ahora.",
    21: "Bueno, no tiene sentido pensar en eso tan profundamente.",
    22: "Adiós, Meruru Edición Regional, descansa en paz.",
    25: "Dios mío, Mamá siempre se preocupa por Kirino.",
    26: "Sin embargo, probablemente es solo Mamá preocupándose demasiado.",
}
a5_s = {
    1: ("Aunque pasé por todas estas molestias consiguiendo este recuerdo...", "Kyousuke"),
    3: ("......Hmph.", "Kirino"),
    7: ("Oh vaya, Kyousuke. ¿Le has dado a Kirino su recuerdo?", "Yoshino"),
    8: ("No, parece que no está de humor; de repente se enfureció y se encerró en su habitación.", "Kyousuke"),
    9: ("...Oye, ¿sientes que Kirino está actuando un poco extraño?", "Yoshino"),
    10: ("¿No? Es la misma de siempre... ¿En qué forma está actuando extraño?", "Kyousuke"),
    11: ("Hmm, no puedo explicarlo si lo pones de esa manera... ¿Será solo mi imaginación...", "Yoshino"),
    17: ("También está la opción de simplemente tirarlo.", "Kyousuke"),
    23: ("Espero que sea solo mi imaginación, pero cuida de Kirino por un tiempo.", "Yoshino"),
    24: ("Entendido.", "Kyousuke"),
}

data = {
    "000scriptBKIR_0000A.obj": build(a0_n, a0_s),
    "000scriptBKIR_0002G.obj": build(a2_n, a2_s),
    "000scriptBKIR_0003A.obj": build(a3_n, a3_s),
    "000scriptBKIR_0004T.obj": build(a4_n, a4_s),
    "000scriptBKIR_0005A.obj": build(a5_n, a5_s),
}

with open(PATH, "r", encoding="utf-8") as f:
    current = json.load(f)
for file, entry in data.items():
    if file not in current:
        current[file] = entry
    else:
        current[file].update(entry)
with open(PATH, "w", encoding="utf-8") as f:
    json.dump(current, f, ensure_ascii=False)
print("updated:", list(data.keys()))