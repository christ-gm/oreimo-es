import json

PATH = "/mnt/c/Users/christ-gm/Desktop/code/oreimo/work/disc1/Data/Translation.json"

def build(narration: dict, speech: dict) -> dict:
    out = {}
    for i, t in narration.items():
        out[str(i)] = t
    for i, t in speech.items():
        out[str(i)] = "「" + t[0] + "」"
    return out

a83_n = {
    0: "Miyabi-chan",
    8: "¡E-Esta chica...! Desconsidera los sentimientos de los demás y dice esto...!",
    9: "Para un examinado como yo, ¡quitarme mi tiempo de estudio es lo que va a desperdiciar mi vida!",
    10: "Ese torneo también, Kirino quería que participara y así fui por su bien...",
    13: "¿C-Cómo fue eso...? ¡Es una razón muy sólida!",
    16: "Cierto... El razonamiento no le llega a esta chica...",
    20: "No estoy seguro, pero parece que la situación se ha aliviado...",
    21: "Procederá así por ahora...",
    33: "Aun así, está siendo demasiado desesperada...",
    34: "Si ha llegado a esto....",
    35: "«El silencio es oro».",
    36: "En momentos como este, debes aferrarte a este proverbio.",
    40: "Si los vecinos escucharan esto, malinterpretarían por completo...",
    43: "No sé si lo hace a propósito, ¡pero es mucho más efectivo hostigar que gritar!",
    50: "¡¿Qué puedo hacer--!",
}
a83_s = {
    1: ("U-Uh... jajajaja...", "Kyousuke"),
    2: ("Esa actitud indecisa tuya es irritante.", "Kirino"),
    3: ("Si eres un hombre, ten algo de confianza.", "Kirino"),
    4: ("L-Lo siento, es verdad que mi actitud puede no ser varonil.", "Kyousuke"),
    5: ("Hmph... Es bueno que lo entiendas.", "Kirino"),
    6: ("Pero...", "Kirino"),
    7: ("Si no juegas ese juego divino... ¡estás desperdiciando 1/3 de tu vida!", "Kirino"),
    11: ("¡¿No hice entrenamiento especial por un tiempo para el torneo de Siscaly?!", "Kyousuke"),
    12: ("Gn...", "Kirino"),
    14: ("¡Pero, pero, pero! ¡¿Crees que eso es una excusa?!", "Kirino"),
    15: ("¡¿Eh?!", "Kyousuke"),
    17: ("Pensar que estás retrasando jugar el juego divino... Eres realmente raro.", "Kirino"),
    18: ("Aunque digas eso...", "Kyousuke"),
    19: ("Bueno, reconoceré que participaste en el torneo.", "Kirino"),
    22: ("G-Gnnn...", "Kirino"),
    23: ("¿Kirino?", "Kyousuke"),
    24: ("¡Esto simplemente no va! ¡Imperdonable!", "Kirino"),
    25: ("Es verdad que «SisXSis» puede ser un juego divino para ti.", "Kyousuke"),
    26: ("¡Pero sin embargo! Imponer esas preferencias a otros es-", "Kyousuke"),
    27: ("¡C-Ciertamente es entretenido! La ruta de Miyabi-chan te hizo llorar, ¿cierto?", "Kirino"),
    28: ("¡Incluso si es un poco, solo prueba la ruta de Rinko-rin!", "Kirino"),
    29: ("¿Por qué estás tan desesperada?", "Kyousuke"),
    30: ("P-Porque...", "Kirino"),
    31: ("¿Hm?", "Kyousuke"),
    32: ("¡N-No importa, no?! ¡Tiene una buena historia, así que solo la estoy recomendando!", "Kirino"),
    37: ("...¿Por qué te quedas en silencio? Es asqueroso.", "Kirino"),
    38: ("...Está bien; no me importa.", "Kirino"),
    39: ("Incluso cuando lo hicimos juntos, no quisiste, ¿cierto?", "Kirino"),
    41: ("Es todo mentira... Aunque dijiste «Si no estás aquí, moriré»...", "Kirino"),
    42: ("¿Qu-...? ¿T-Tú...? ¿M-Mencionas eso ahora....?", "Kyousuke"),
    44: ("E-Eso no es verdad. Lo que te dije en ese momento- Todo es verdad. Si tuviera tiempo, jugaría «SisSis» de inmediato.", "Kyousuke"),
    45: ("...¿De verdad?", "Kirino"),
    46: ("Sí, de verdad.", "Kyousuke"),
    47: ("Hmm, ya veo. Entonces tienes hasta mañana para completarlo.", "Kirino"),
    48: ("¡Como dije, eso es imposible!", "Kyousuke"),
    49: ("¡Entonces era de verdad una mentira!", "Kirino"),
}

a84_n = {
    0: "Fandisk",
    8: "Espera, ¿esto significa que soy raro?",
}
a84_s = {
    1: ("...Bueno, yo también tengo la culpa. Lo jugaré cuando lleguemos a casa.", "Kyousuke"),
    2: ("¡Digo que eres demasiado lento! ¡Todavía está el fandisk!", "Kirino"),
    3: ("¿Fandisk? ¿Es algo como una secuela?", "Kyousuke"),
    4: ("¡Eso es! ¡«SisXSis Moushouden»!", "Kirino"),
    5: ("Entiendo. También jugaré eso...", "Kyousuke"),
    6: ("Olvídalo.", "Kirino"),
    7: ("E-Esa chica...", "Kyousuke"),
    9: ("...*suspiro*", "Kyousuke"),
    10: ("Pero quizás fui un poco infantil.", "Kyousuke"),
    11: ("Esa chica probablemente quiere interactuar con gente que ha jugado juegos similares...", "Kyousuke"),
    12: ("Sin embargo, interactuar con mi hermanita sobre juegos relacionados con hermanitas...", "Kyousuke"),
    13: ("*suspiro*... Es difícil ser un hermano mayor...", "Kyousuke"),
}

a86_n = {
    0: "Aragaki Ayase Aparece",
    2: "Al final, no fui al torneo de Siscaly a apoyarlos.",
    3: "Sobre el resultado, creo que fue algo bueno que no fuera... ¿Por qué preguntas?",
    4: "Kirino y las demás lograron llegar a las finales, pero la victoria se les escapó por un pelo.",
    5: "Aunque creo que es increíble que ganaran el segundo lugar, mi altanera hermana debe estar insoportablemente fastidiada.",
    6: "Ayer, después del torneo, se encerró en su habitación. Incluso cuando la llamé, no hubo respuesta.",
    7: "No pude soportar esa atmósfera sombría, así que salí de casa sin rumbo...",
    11: "Hace tanto calor que podrías secar cosas al sol...",
    12: "Es más, estoy fantaseando una voz angelical viniendo de algún lugar.",
    13: "Jaja... ¿Será que estoy cayendo por deshidratación...?",
    16: "Giré la cabeza y allí estaba Aragaki Ayase.",
    17: "La mejor amiga de Kirino, y también una compañera de modelaje.",
    18: "En otras palabras, la amiga «oficial» de Kirino.",
    19: "Es mi favorita entre la gente que conozco.",
    20: "Honestamente, en cuanto a apariencias, es totalmente mi tipo pero...",
    26: "Eso es correcto. Debido a varias razones, Ayase me ha etiquetado como un «hermano mayor pervertido incestuoso».",
    27: "Y por otros problemas, no pudimos resolver el malentendido, así que es alguien bastante difícil de tratar.",
    29: "Esto es. Con esa expresión, diciendo tales palabras... No pude dejarla atrás.",
}
a86_s = {
    1: ("*suspiro*", "Kyousuke"),
    8: ("Hah... Hah...", "Kyousuke"),
    9: ("Hace demasiado calor... Maldición...", "Kyousuke"),
    10: ("Disculpe, Onii-san.", "???"),
    14: ("¡E-Espera, Onii-san!", "???"),
    15: ("¡¿Whoa?! ¡A-Ayase!", "Kyousuke"),
    21: ("Onii-san... Enfrentar a alguien levantando la voz... ¿No es eso cruel?", "Ayase"),
    22: ("A-Ah... Perdón.", "Kyousuke"),
    23: ("De hecho intentaste hablarme a pesar de odiarme, pensé que algo había pasado.", "Kyousuke"),
    24: ("Ah, por eso. En efecto, hablar con un Onii-san tan pervertido en la calle, no es algo que haría normalmente.", "Ayase"),
    25: ("Guh...", "Kyousuke"),
    28: ("Sin embargo... Tengo algo de qué hablar.", "Ayase"),
    30: ("Entendido. Soy todo oídos.", "Kyousuke"),
}

a88_n = {
    0: "Las Preocupaciones de Una Bella",
    2: "Ayase pidiendo una «sesión de orientación de vida»... Es una frase que he estado escuchando mucho últimamente.",
    9: "Había estado ocupada entrenando para Siscaly...",
    10: "Por eso había estado tratando a Ayase un poco con frialdad...",
    16: "¿Qué está pasando exactamente en su mente, qué podría hacerle yo a Kirino...?",
    17: "*suspiro* Sus delirios son tan intensos como siempre.",
}
a88_s = {
    1: ("En realidad... ¡Quiero tener una sesión de orientación de vida!", "Ayase"),
    3: ("¿Hay algo malo?", "Ayase"),
    4: ("No, nada.", "Kyousuke"),
    5: ("¿Entonces? ¿Para qué necesitas orientación de vida?", "Kyousuke"),
    6: ("Recientemente, Kirino no ha estado saliendo conmigo en absoluto. Incluso si la invito, no viene...", "Ayase"),
    7: ("¿Oh?", "Kyousuke"),
    8: ("No solo eso, me ha estado tratando con frialdad... Estoy preocupada...", "Ayase"),
    11: ("Onii-san... ¿Tienes alguna pista?", "Ayase"),
    12: ("Supongo que sí.", "Kyousuke"),
    13: ("¡?! ¡¿E-Entonces Onii-san le hizo algo a Kirino!", "Ayase"),
    14: ("¿Qué quieres decir con «le hizo algo»?", "Kyousuke"),
    15: ("Eso... No puedo decirlo yo misma.", "Ayase"),
    18: ("Lo entendiste todo mal.", "Kyousuke"),
    19: ("¿De verdad?", "Ayase"),
    20: ("Sí, lo juro.", "Kyousuke"),
}

a90_n = {
    0: "¿Qué Hay Con Kirino?",
    3: "Está predispuesta contra las aficiones de Kirino, así que...",
    4: "¿Puedo decirle honestamente sobre eso?",
    5: "Bueno, odia las mentiras...",
    6: "Diablos, ¿por qué debo frustrarme por los asuntos de mi hermana?",
    14: "Probablemente está escuchando y tarareando el tema de algún anime transmitido recientemente.",
    15: "¿Me creerá Ayase si le dijera francamente?",
    21: "N-No está bien. Me equivoqué ahí.",
    32: "Ayase se llevó ambas manos al pecho con su cara poniéndose roja.",
    37: "Si es por Ayase, esto no es nada.",
}
a90_s = {
    1: ("¿Le pasó algo a Kirino?", "Ayase"),
    2: ("B-Bueno...", "Kyousuke"),
    7: ("Ah, creo que probablemente estaba ocupada con entrenamiento especial para un juego llamado Siscaly.", "Kyousuke"),
    8: ("¿Sis-, caly?", "Ayase"),
    9: ("Eso es correcto, hubo un torneo ayer, por eso se sometió a entrenamiento especial.", "Kyousuke"),
    10: ("...Entonces es un juego. En ese caso, podría entenderlo, pero...", "Ayase"),
    11: ("¿Hay algo más?", "Kyousuke"),
    12: ("Bueno... Ha estado llenando sus oídos con alguna canción, tarareando y ¡no me escucha en absoluto!", "Ayase"),
    13: ("Eso es probablemente...", "Kyousuke"),
    16: ("¿Estoy... estorbándola...?", "Ayase"),
    17: ("No, eso es... Me pregunto...", "Kyousuke"),
    18: ("¿Eh? Vives con Kirino y ¿ni siquiera sabes?", "Ayase"),
    19: ("B-Bueno. No somos tan cercanos, sabes...", "Kyousuke"),
    20: ("Dios, ¡fue un error preguntarle a Onii-san sobre eso!", "Ayase"),
    22: ("Solo quiero hablar con Kirino.... ¿Soy un estorbo para ella...?", "Ayase"),
    23: ("No la estás estorbando.", "Kyousuke"),
    24: ("...¿Por qué puedes decir eso con tanta certeza?", "Ayase"),
    25: ("...Kirino...", "Ayase"),
    26: ("Cuando Kirino peleó contigo en el pasado, ¿olvidaste cuánto esfuerzo puso para reconciliarse contigo?", "Kyousuke"),
    27: ("Oh...", "Ayase"),
    28: ("No tienes que preocuparte, Kirino de verdad te aprecia. Aproximadamente tanto como tú a ella.", "Kyousuke"),
    29: ("¿D-De verdad...?", "Ayase"),
    30: ("Sí, absolutamente. Puedo dar fe de eso.", "Kyousuke"),
    31: ("D-De verdad... Ehehe... Entonces eso es genial...", "Ayase"),
    33: ("...¿Qué estás imaginando?", "Kyousuke"),
    34: ("¿Eh? A-Ah...!", "Ayase"),
    35: ("A-Ejem. B-Bueno... Muchas gracias, Onii-san.", "Ayase"),
    36: ("Je, no hay de qué.", "Kyousuke"),
}

data = {
    "000scriptAKYO_0083A.obj": build(a83_n, a83_s),
    "000scriptAKYO_0084A.obj": build(a84_n, a84_s),
    "000scriptAKYO_0086A.obj": build(a86_n, a86_s),
    "000scriptAKYO_0088A.obj": build(a88_n, a88_s),
    "000scriptAKYO_0090A.obj": build(a90_n, a90_s),
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