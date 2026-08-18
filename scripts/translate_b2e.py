import json

PATH = "/mnt/c/Users/christ-gm/Desktop/code/oreimo/work/disc1/Data/Translation.json"

def build(narration: dict, speech: dict) -> dict:
    out = {}
    for i, t in narration.items():
        out[str(i)] = t
    for i, t in speech.items():
        out[str(i)] = "「" + t[0] + "」"
    return out

a48_n = {
    0: "Ruta de Kirino · Es Imposible Que Mi Papá Sea Cabeza Dura",
    13: "Tengo el mismo sentimiento.",
}
a48_s = {
    1: ("¿Eh...?", "Kirino"),
    2: ("Estoy preguntando si eso es realmente cierto.", "Daisuke"),
    3: ("¡Y-Yo estoy diciendo la verdad!", "Kirino"),
    4: ("...Papá, soy la misma de siempre, ¿no? No estoy siendo extraña ni nada, ¿verdad?", "Kirino"),
    5: ("...Eso está de más decirlo.", "Daisuke"),
    6: ("Que me digas tales palabras a mí es la evidencia más concreta de que estás perdida.", "Daisuke"),
    7: ("......", "Kirino"),
    8: ("Parece que te has estado forzando recientemente.", "Daisuke"),
    9: ("Ese podría ser el caso... Kirino se fuerza a sí misma.", "Kyousuke"),
    10: ("¡H-Hasta tú...! ¡No digas cosas innecesarias!", "Kirino"),
    11: ("¡No me estoy forzando!", "Kirino"),
    12: ("Entonces, ¿por qué no me miras a los ojos mientras hablas?", "Daisuke"),
    14: ("...............", "Kirino"),
    15: ("N-No me estoy forzando. ¿N-No soy la misma de siempre?", "Kirino"),
    16: ("Entonces, ¿por qué no me miras a los ojos mientras hablas?", "Daisuke"),
    17: ("Kirino, ¿hay algo que te preocupe?", "Daisuke"),
    18: ("E-Eso es...", "Kirino"),
    19: ("¿Es algo que no puedes contarle ni a mí?", "Daisuke"),
    20: ("Papá.", "Kyousuke"),
    21: ("¿Qué pasa, Kyousuke?", "Daisuke"),
    22: ("Déjame pensar una solución para los problemas de Kirino.", "Kyousuke"),
    23: ("Por eso, quédate tranquilo.", "Kyousuke"),
    24: ("¿H-Huh? No quiero que...", "Kirino"),
    25: ("¿Es así? Entonces te lo dejo a ti.", "Daisuke"),
    26: ("¡¿Ehh?!", "Kirino"),
    27: ("...Sí, no puedo contarle... ni a ti, Papá, sobre esto.", "Kirino"),
    28: ("¿Es así...? Bueno entonces, consulta con Kyousuke sobre ello.", "Daisuke"),
    29: ("¿Ehh?", "Kirino"),
    31: ("¡¿P-Papá?! ¡¿Qué estás diciendo?!", "Kirino"),
    32: ("Kyousuke se ha preocupado más por ti que nadie más en la familia durante este año.", "Daisuke"),
    33: ("Protegiendo a su hermanita usando métodos que yo no puedo.", "Daisuke"),
    34: ("Deberías saberlo muy bien.", "Daisuke"),
    35: ("E-Eso es solo...", "Kirino"),
    36: ("He decidido dejarle todos los asuntos concernientes a Kirino a Kyousuke.", "Daisuke"),
    37: ("...Eso es todo.", "Daisuke"),
    38: ("...¿S-Sobre ti... protegerme, es cierto?", "Kirino"),
    39: ("Quién sabe.", "Kyousuke"),
    40: ("Simplemente he hecho lo que quería hacer, como siempre.", "Kyousuke"),
}

a50_n = {
    0: "Ruta de Kirino · Es Imposible Que Mi Hermanita No Se Conmueva Por Este Libro",
    3: "Como era de esperar, no confía en mí... Huh...",
    4: "Pero...",
    7: "...Tengo que estar a la altura de la confianza de Papá.",
    8: "No obstante, este libro que Kirino escribió...",
    9: "¿Podría ser... que puedo usar esto...?",
}
a50_s = {
    1: ("Diciendo que haces lo que quieres hacer...", "Kirino"),
    2: ("...Es una mentira, ¿no?", "Kirino"),
    5: ("Te dejaré decidir si creerme o no.", "Kyousuke"),
    6: ("......", "Kirino"),
    10: ("...Hmph.", "Kirino"),
    11: ("Oye, espera un momento, Kirino.", "Kyousuke"),
    12: ("...¿Qué es?", "Kirino"),
    13: ("Hay un libro que me gustaría que leyeras.", "Kyousuke"),
}

a53_n = {
    0: "Ruta de Kirino · Es Imposible Que Mi Hermanita No Se Conmueva Por Este Libro - G",
}
a53_s = {
    1: ("Esta vez, no es absolutamente nada extraño. De verdad. Confía en mí.", "Kyousuke"),
    2: ("¿Cómo puedo seguir creyéndote? ¿Qué tal recordar las cosas que has hecho hasta ahora?", "Kirino"),
    3: ("...Por favor.", "Kyousuke"),
    4: ("Tch... ¿Por qué... llegas... tan lejos...", "Kirino"),
    5: ("¿Eh?", "Kyousuke"),
    6: ("Ya que lo pones de esa manera, lo leeré... pero esta es tu última oportunidad.", "Kirino"),
    7: ("S-Sí. Asegúrate de leerlo con cuidado.", "Kyousuke"),
    8: ("......", "Kirino"),
    9: ("......", "Kyousuke"),
    10: ("¿C-Cómo está? ¿Has recordado algo?", "Kyousuke"),
    11: ("¡¿?! ¿N-No es esto...", "Kirino"),
    12: ("...*gulp*", "Kyousuke"),
    13: ("¡Oye, qué clase de novela le dejaste leer a tu hermanita?!", "Kirino"),
    14: ("¿Huh? ¡Ah, mierda! ¡¿Esto es?!", "Kyousuke"),
    15: ("A-A-A-Además, el título es «El Secreto de la Doncella con Anteojos☆»...¡Es de tu interés!", "Kirino"),
    16: ("¡Pervertido! ¡Maníaco de los anteojos! ¡Amante de las chicas comunes!", "Kirino"),
    17: ("¡E-Espera ahí, hay una cosa que no puedo aceptar que se haya mezclado ahí!", "Kyousuke"),
    18: ("¡Cállate!", "Kirino"),
    19: ("¡E-Esto es un error! ¡Un incidente desafortunado! ¡Esto es lo que realmente quería que leyeras!", "Kyousuke"),
}

a55_n = {
    0: "Ruta de Kirino · Es Imposible Que Mi Hermanita No Se Conmueva Por Este Libro",
    4: "Como pensé, ni siquiera puede recordar este libro.",
    5: "Bueno, el contenido consiste en una historia dirigida a chicas de secundaria, pero fue escrita con la obsesión de Kirino por las hermanitas en su máximo esplendor.",
    10: "Después de 30 minutos...",
    12: "¡¿Quedó profundamente conmovida?!",
    13: "No, eso es de esperarse. Porque era como si se hubiera conmovido profundamente al escribir el libro.",
    14: "Y es porque pensó que esto fue escrito por otra persona que tal vez pudo empatizar aún más con ello.",
    28: "¡¿Mierda?!",
}
a55_s = {
    1: ("¿Qué es esto? ¿Imouto City: My City...?", "Kirino"),
    2: ("Mira. ¿No es este un libro muy normal?", "Kyousuke"),
    3: ("...Bueno... solo por las apariencias. Pero, ¿quién sabe?", "Kirino"),
    6: ("...¿Es alguna novela otaku asquerosa?", "Kirino"),
    7: ("No, el contenido también es normal. Es una light novel escrita por una chica de secundaria, ¿sabes?", "Kyousuke"),
    8: ("Mira, está escrito en la cubierta también, ¿no? Una historia romántica conmovedora publicada por una autora que actualmente es estudiante de secundaria.", "Kyousuke"),
    9: ("Hmph, apesta a mentiras... Pero bueno, intentaré leer esto...", "Kirino"),
    11: ("...*sniff*...*sniff*", "Kirino"),
    15: ("¿C-Cómo estuvo? ¿Es interesante?", "Kyousuke"),
    16: ("N-No tan mal...*sniff*", "Kirino"),
    17: ("No, incluso si pones una fachada ahora, es obvio que te has conmovido emocionalmente.", "Kyousuke"),
    18: ("...Entonces, ¿y qué?", "Kirino"),
    19: ("Para decirte la verdad, la estudiante de secundaria que escribió esto en realidad eras tú.", "Kyousuke"),
    20: ("E-Estás mintiendo... ¿en realidad soy yo?", "Kirino"),
    21: ("Oye, recuerda. ¿No diste lo mejor de ti solo para escribir esto?", "Kyousuke"),
    22: ("¿Dio mi mejor...?", "Kirino"),
    23: ("Y-Yo...", "Kirino"),
    24: ("P-Pero yo... nunca me quedé en un hotel en Shibuya antes... ¿cómo pude escribirlo tan realista?", "Kirino"),
    25: ("¿Qué estás diciendo?", "Kyousuke"),
    26: ("En la víspera de Navidad, ¿no fuimos juntos a un hotel del amor en Shibuya?", "Kyousuke"),
    27: ("¡¿Huh?!", "Kirino"),
    29: ("¡T-T-T-T-Tú...!", "Kirino"),
    30: ("¡¿Qué clase de relación teníamos?!", "Kirino"),
    31: ("¡P-Permíteme explicarte!", "Kyousuke"),
    32: ("¡Mentiras! ¡¡Esa clase de cosa es absolutamente una mentira!!", "Kirino"),
    33: ("¡Pervertido grandote! ¡Vete lejos----!!", "Kirino"),
}

a58_n = {
    0: "Ruta de Kirino · Tengo Que Pedirle Ayuda A Tamura Manami",
    1: "El último día del feriado de tres días. Una vez más, me sentí terrible cuando me desperté hoy.",
    3: "Ya han pasado cinco días desde que supe que Kirino perdió sus recuerdos, ¿ves?",
    4: "¿Por qué Kirino todavía no ha recuperado sus recuerdos?",
    5: "Además, termino siendo odiado por Kirino cada vez que fallo en ayudar.",
    6: "Es incómodo cada vez que me cruzo con Kirino ahora.",
    21: "Ahh... Todos mis problemas desaparecerían si pudiera sermonearle a Kirino así.",
    22: "Definitivamente moriría al instante por su represalia justo después de hacerlo, sin embargo.",
    26: "Eso es cierto... Podría ser bueno apoyarme en la bolsa de sabiduría de la abuelita.",
    27: "¿Debería... intentar contarle sobre ello?",
    34: "Guh, poniendo esa cara sonriente.",
    35: "En momentos así, una amiga de la infancia es realmente molesta. Pero...",
    45: "Ese chico, era un terrible siscon hasta hace unos años.",
    50: "¿【Persona de verdad importante】? ¿Eso es lo que Kirino... piensa de mí?",
    51: "...Eso de verdad es imposible. ¿Qué está diciendo?",
    52: "Pero, bueno...",
    54: "Como pensé, no puedo explicar todo, pero... intentaré hablar con ella al respecto.",
    65: "Mientras decía que era solo un ejemplo, fui y le conté casi todo.",
    73: "Al menos, es diferente a hace un año.",
    74: "Lo que obtuve durante este año con Kirino.",
    75: "Incluso si sus recuerdos se han ido... no desaparecerán.",
    76: "Incluso ahora, todavía están dentro de mí.",
}
a58_s = {
    2: ("*suspiro*... Qué deprimente.", "Kyousuke"),
    7: ("*suspiro*... ¿Qué debería hacer?", "Kyousuke"),
    8: ("...Intentaré ponerme en contacto con Manami.", "Kyousuke"),
    9: ("Kyou-chan, ¿estás bien? Te ves como si no te sintieras muy bien...", "Manami"),
    10: ("¿Es así?", "Kyousuke"),
    11: ("Sí. Tu voz sonó rara también cuando me llamaste.", "Manami"),
    12: ("Perdón por haberte preocupado, Abuelita.", "Kyousuke"),
    13: ("No, no. Nos ayudamos mutuamente.", "Manami"),
    14: ("Je, ahora que lo pienso, ese hermanito tuyo estrella de rock sin familia ni amigos, ¿qué le pasó después de eso?", "Kyousuke"),
    15: ("Eso ha sido resuelto en silencio.", "Manami"),
    16: ("Eso fue bastante rápido.", "Kyousuke"),
    17: ("Sí, inmediatamente volvió a su ser normal después de ser severamente regañado por Papá.", "Manami"),
    18: ("¿Por ese viejo? Es muy amable conmigo y no da ninguna impresión de ser aterrador, sin embargo.", "Kyousuke"),
    19: ("Hmm～, Papá dio mucho miedo en ese momento, diciendo algo sobre cómo uno no debe tratar a su familia como extraños, ni siquiera como una broma.", "Manami"),
    20: ("B-Bueno, eso es cierto. Supongo que la gente normalmente se enojaría por eso.", "Kyousuke"),
    23: ("Oh, Kyou-chan, ¿qué pasa?", "Manami"),
    24: ("Aunque no puedo entrar en demasiados detalles... Recientemente, Kirino me ha estado diciendo cosas similares.", "Kyousuke"),
    25: ("...Aunque no entiendo por completo, ¿tal vez te sentirás mejor si me hablas de ello?", "Manami"),
    28: ("...Err.", "Kyousuke"),
    29: ("Como aprecias a Kirino, es difícil hablar de ello, ¿verdad?", "Manami"),
    30: ("...¿Eh?", "Kyousuke"),
    31: ("Bueno, solo anímate. Kirino-chan seguramente entiende que estás preocupado por ella.", "Manami"),
    32: ("N-No es como si estuviera preocupado ni nada", "Kyousuke"),
    33: ("Jejeje.", "Manami"),
    36: ("...Gracias, Manami.", "Kyousuke"),
    37: ("Bueno, sobre Kirino... empezó a tratarme como un extraño justo después de que volví del viaje escolar.", "Kyousuke"),
    38: ("Es exactamente lo mismo que con Rock.", "Kyousuke"),
    39: ("Así que es eso... Creo que Kirino-chan probablemente no tiene mala intención detrás de ello, como mi hermanito.", "Manami"),
    40: ("¿Qué quieres decir?", "Kyousuke"),
    41: ("La casa quedó vacía por bastante tiempo cuando nos fuimos al viaje escolar, ¿no?", "Manami"),
    42: ("¿No es solitario? Y entonces, quiere que te preocupes por ella cuando se reencuentren después de varios días...", "Manami"),
    43: ("Entonces está hablando lo opuesto a sus sentimientos, así es como lo pienso.", "Manami"),
    44: ("Bueno, ese podría ser el caso con Rock.", "Kyousuke"),
    46: ("Pero, Kirino es diferente.", "Kyousuke"),
    47: ("...¿Es así?", "Manami"),
    48: ("Creo que Kirino-chan seguramente trata a Kyou-chan...", "Manami"),
    49: ("...como una 【persona de verdad importante】.", "Manami"),
    53: ("Gracias, Manami.", "Kyousuke"),
    55: ("Esto es solo un ejemplo, pero...", "Kyousuke"),
    56: ("Sí, sí.", "Manami"),
    57: ("Kirino ha olvidado todo lo que sucedió durante el último año.", "Kyousuke"),
    58: ("¿Kirino-chan tiene amnesia?", "Manami"),
    59: ("Es solo un ejemplo. Piensa en ello así y escucha.", "Kyousuke"),
    60: ("Kirino tiene amnesia--y nuestra relación, que pensé que finalmente había mejorado un poco durante este último año, ha vuelto a cómo era hace un año.", "Kyousuke"),
    61: ("Mi hermanita no me considera como su hermano y me mira como si yo fuera un extraño.", "Kyousuke"),
    62: ("Obviamente, tengo la intención de hacer todo lo que pueda para traer de vuelta los recuerdos de Kirino.", "Kyousuke"),
    63: ("Pero... como era de esperar, me siento deprimido al respecto.", "Kyousuke"),
    64: ("...Como dije, esto es solo un ejemplo, ¿de acuerdo?", "Kyousuke"),
    66: ("...Ya veo.", "Manami"),
    67: ("...No creo que la relación entre tú y Kirino-chan haya vuelto a cómo era hace un año.", "Manami"),
    68: ("...¿Qué quieres decir?", "Kyousuke"),
    69: ("Incluso si los recuerdos de Kirino-chan se han ido...", "Manami"),
    70: ("Recuerdas el tiempo que pasaste con Kirino-chan, ¿verdad?", "Manami"),
    71: ("Por eso no ha vuelto a como era antes.", "Manami"),
    72: ("...Eso puede ser así.", "Kyousuke"),
    77: ("...Gracias, Manami.", "Kyousuke"),
    78: ("Sí.", "Manami"),
    79: ("También... Esto es solo una suposición, pero...", "Manami"),
    80: ("¿Sí?", "Kyousuke"),
    81: ("La Kirino-chan de hace un año tampoco pensaba en Kyou-chan como un extraño.", "Manami"),
    82: ("Jaja.", "Kyousuke"),
    83: ("Puede que estés tratando de animarme con eso, pero eso simplemente no es posible.", "Kyousuke"),
    84: ("...Me pregunto sobre eso.", "Manami"),
    85: ("Kirino-chan seguramente piensa en ti...", "Manami"),
    86: ("Como un 【hermano de verdad】.", "Manami"),
}

data = {
    "000scriptBKIR_0048T.obj": build(a48_n, a48_s),
    "000scriptBKIR_0050A.obj": build(a50_n, a50_s),
    "000scriptBKIR_0053G.obj": build(a53_n, a53_s),
    "000scriptBKIR_0055A.obj": build(a55_n, a55_s),
    "000scriptBKIR_0058A.obj": build(a58_n, a58_s),
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