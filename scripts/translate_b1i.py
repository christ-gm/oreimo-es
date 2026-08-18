import json

PATH = "/mnt/c/Users/christ-gm/Desktop/code/oreimo/work/disc1/Data/Translation.json"

def build(narration: dict, speech: dict) -> dict:
    out = {}
    for i, t in narration.items():
        out[str(i)] = t
    for i, t in speech.items():
        out[str(i)] = "「" + t[0] + "」"
    return out

a74_n = {
    0: "La Extraña Confesión de Saori",
    8: "Si no lo oí mal, ¿no acaba de decir Saori algo escandaloso?",
    9: "No puede ser... ¿Será que...? No Saori...",
    10: "Mientras rezaba por haber escuchado mal algo...",
    11: "Sin pensar, me incliné hacia Saori.",
    13: "Eh, Saori está inclinando su cabeza confundida... ¿La escuché mal?",
    14: "¿No acaba de decir algo sobre una entrevista de matrimonio?",
    15: "Pero me está poniendo cara de nada...",
    16: "Digamos que la escuché mal. ...Sí.",
}
a74_s = {
    1: ("Oh, por cierto, tengo que ir a una 【entrevista de matrimonio】.", "Saori"),
    2: ("¿Eh...? ¿Es así?", "Kyousuke"),
    3: ("...¡¿Qu-..., una entrevista de matrimonio?!", "Kyousuke"),
    4: ("¿Con entrevista de matrimonio te refieres a eso? ¿Conocer a una pareja con la perspectiva de casarte?", "Kyousuke"),
    5: ("¿Eh?", "Saori"),
    6: ("¿Por qué dices «eh»...? ¿No acabas de hablar de una entrevista de matrimonio?", "Kyousuke"),
    7: ("¿Lo hice? ¿Dije algo así?", "Saori"),
    12: ("¿Eh? ¿Entrevista de matrimonio? ¿Qué hay con eso?", "Saori"),
}

a78_n = {
    0: "La Extraña Confesión de Saori",
    39: "Ella ciertamente va a una entrevista de matrimonio...",
    40: "Parece que no quiere que le pregunten sobre ello...",
    43: "No parece que quiera que me entrometa en eso sin embargo...",
}
a78_s = {
    1: ("¿Sa-Saori...? ¿Acabas de decir «entrevista de matrimonio»?", "Kyousuke"),
    2: ("Ja ja ja. No no, perdóname, por favor.", "Saori"),
    3: ("No es justo presionar a alguien por una broma fallida.", "Saori"),
    4: ("¡No intentes esquivarlo! ¡Eso no sonó como una broma!", "Kyousuke"),
    5: ("¡Ho ho! ¿Será que Kyousuke-shi...", "Saori"),
    6: ("¿Se pone celoso de una chica cuando está por casarse?", "Saori"),
    7: ("¡No es eso!", "Kyousuke"),
    8: ("...No importa, no puedo hacer nada si no quieres hablar de ello.", "Kyousuke"),
    9: ("Bueno, cambiemos de tema.", "Saori"),
    10: (".........", "Kyousuke"),
    11: ("¿Oh? ¿Kyousuke-shi? ¿Qué es esa mirada fija?", "Saori"),
    12: ("...Simplemente no puedo dejarlo así. Me molesta.", "Kyousuke"),
    13: ("Bueno, incluso si es una entrevista de matrimonio, no es un gran problema.", "Saori"),
    14: ("¡¿Entonces SÍ vas?! ¡A una entrevista de matrimonio!", "Kyousuke"),
    15: ("Es algo por lo que todos pasan una vez. Tú lo has hecho antes, ¿cierto?", "Saori"),
    16: ("¡No, no lo he hecho!", "Kyousuke"),
    17: ("Ooh, una réplica afilada como siempre. ¡Estoy agradecida!", "Saori"),
    18: ("¿Entrevista de matrimonio? ¿Yo?", "Kyousuke"),
    19: ("Kyousuke-shi... ¿Por qué estás dudando...", "Saori"),
    20: ("Esa era una oportunidad tan espléndida para una réplica...", "Saori"),
    21: ("...¿De qué están susurrando ustedes dos?", "Kuroneko"),
    22: ("No, no, es nada. Estamos teniendo un debate acalorado sobre el rendimiento de disparo rápido de las pistolas ametralladoras.", "Saori"),
    23: ("¡Te dije! ¡No intentes esquivarlo así!", "Kyousuke"),
    24: ("Kyousuke-shi. Estás entrometiéndote en los asuntos privados de una mujer...", "Saori"),
    25: ("¡P-Pero, esto me molesta!", "Kyousuke"),
    26: ("Esta discusión termina aquí.", "Saori"),
    27: ("Oh...", "Kyousuke"),
    28: ("¿Pistolas ametralladoras?", "Kyousuke"),
    29: ("¡Parece que el nivel de Kyousuke-shi es bastante alto!", "Saori"),
    30: ("Sin embargo, un Kyousuke-shi sin palabras es bastante moe.", "Saori"),
    31: ("¡C-Cállate!", "Kyousuke"),
    32: ("Sin embargo, descuida...", "Saori"),
    33: ("¿Eh?", "Kyousuke"),
    34: ("Nada de mí cambiará. Y...", "Saori"),
    35: ("Mi relación contigo tampoco cambiará.", "Saori"),
    36: ("¡Entonces SÍ vas a una entrevista de matrimonio!", "Kyousuke"),
    37: ("Jajaja, ¡eso es correcto!", "Saori"),
    38: ("Sin embargo, esto es algo común. Me encargaré de ello rápidamente.", "Saori"),
    41: ("...Entonces, ¿cuál será nuestro próximo destino?", "Saori"),
    42: ("De todos modos, descuida, no es nada.", "Saori"),
    44: ("Es-Es verdad... No estoy mintiendo.", "Saori"),
    45: ("Entendido.", "Kyousuke"),
    46: ("P-Pero, ¿a dónde deberíamos ir después?", "Saori"),
}

a80_n = {
    0: "Fin Del Descanso",
    4: "Aunque digas eso...",
    5: "¿Por qué tienes una expresión tan solitaria en tu cara...",
    12: "Ah... ustedes tres, qué jóvenes...",
    13: "Bueno, tienen un punto ahí.",
    18: "Estas chicas... inventando tales razones, pero solo quieren ir juntas, ¿no?",
    19: "Esperé fuera de la tienda a que las tres salieran.",
    20: "Por supuesto, en sus manos había grandes cantidades de artículos otaku.",
    25: "--Y así, las tres se fueron de compras.",
    26: "Como me superaba el calor, gasté mucha energía y esfuerzo para alcanzar a las tres.",
}
a80_s = {
    1: ("Bueno, todo es 【solo una experiencia de vida】.", "Saori"),
    2: ("【Solo una experiencia de vida】...", "Kyousuke"),
    3: ("Por ahora, ¡por favor olvida todo lo que dije! ¡No tiene nada que ver con por qué estamos aquí hoy!", "Saori"),
    6: ("Entonces, ¡el descanso ahora se acabó!", "Kirino"),
    7: ("Relajémonos un poco más, ¿de acuerdo? ¿No es esto una celebración?", "Kyousuke"),
    8: ("Vinimos hasta Akihabara, ¡estaríamos perdiéndonos algo si solo nos quedáramos de brazos cruzados!", "Kirino"),
    9: ("Si no vamos de compras más...", "Kirino"),
    10: ("Es tal como dijo Kiririn-shi, ¡hay maneras de disfrutar en Akihabara!", "Saori"),
    11: ("Por una vez, estoy de acuerdo.", "Kuroneko"),
    14: ("En ese caso, ¡recorramos todo el distrito!", "Kyousuke"),
    15: ("Entonces, iré a revisar la alineación de juegos recién lanzados.", "Saori"),
    16: ("¡Yo también voy!", "Kirino"),
    17: ("...Hmph. Supongo que no hay de otra.", "Kuroneko"),
    21: ("Muy bien todos, ¿cómo estuvo la cosecha de hoy?", "Saori"),
    22: ("Bueno, ¿bastante buena diría?", "Kirino"),
    23: ("Todavía tengo algunos lugares que quiero ver.", "Kuroneko"),
    24: ("¡Es la celebración después de todo! Entonces, nos moveremos al siguiente lugar.", "Saori"),
    27: ("Dime, esto no parece ser diferente comparado con los fines de semana, ¿no?", "Kyousuke"),
    28: ("Jajaja, ¿no es genial así?", "Saori"),
    29: ("Después de todo, es mejor si es igual que de costumbre.", "Saori"),
    30: ("No es que me moleste realmente... Cómo debería decirlo...", "Kyousuke"),
    31: ("Bueno, mientras se estén divirtiendo.", "Kyousuke"),
}

a81_n = {
    0: "SisSis",
    1: "Después de separarnos de Kuroneko y Saori, de camino a casa...",
    14: "N-No está bien...",
    15: "Parece que he incurrido en su ira...",
    16: "Si no hago algo pronto...",
    26: "¿Oh?",
    27: "Estaba listo para soportar al menos una patada giratoria pero...",
    28: "Pero su reacción es suave...",
    34: "Sé perfectamente que no aceptará una afirmación legítima.",
    35: "Como siempre, Kirino perderá los estribos--",
    37: "No siento que pueda decir que no lo hice.",
    38: "No creo que un argumento sólido pueda llegarle.",
    39: "Qué podría ser lo más adecuado para engañarla...",
    47: "Como era de esperar, la tez de Kirino cambió en un instante.",
    48: "Pero, extrañamente, se ve adolorida; ¿es mi imaginación?",
}
a81_s = {
    2: ("¡Ah! ¡Acabo de recordarlo!", "Kirino"),
    3: ("¿Por qué levantas la voz? ¿Olvidaste algo?", "Kyousuke"),
    4: ("No es eso. ¿Has completado «SisSis»?", "Kirino"),
    5: ("Sobre eso...", "Kyousuke"),
    6: ("¿Qué? No me digas que no lo has jugado.", "Kirino"),
    7: ("¡N-No es eso!", "Kyousuke"),
    8: ("Entonces ¿qué es?", "Kirino"),
    9: ("«SisSis»... ¡Es un gran juego!", "Kyousuke"),
    10: ("...Hmm, entonces no lo has jugado.", "Kirino"),
    11: ("No, mira...", "Kyousuke"),
    12: ("No puedo creerlo. ¿Por qué no lo has jugado?", "Kirino"),
    13: ("¿Cuánto tiempo crees que ha pasado desde que te presté «SisSis»?", "Kirino"),
    17: ("No, he jugado «la ruta de Miyabi».", "Kyousuke"),
    18: ("Esa ruta fue realmente genial～", "Kyousuke"),
    19: ("¿No era esa la que jugué contigo?", "Kirino"),
    20: ("M-Mira... Estoy preparándome para los exámenes de ingreso...", "Kyousuke"),
    21: ("¿Qué es eso? No puedo creerlo. «La ruta de Rinko-rin» todavía está---", "Kirino"),
    22: ("--No, no importa.", "Kirino"),
    23: ("¿Qué pasa?", "Kyousuke"),
    24: ("Nada en absoluto.", "Kirino"),
    25: ("Pensar que no jugaste «SisXSis»...", "Kirino"),
    29: ("De todos modos, lo jugaré apropiadamente después...", "Kyousuke"),
    30: ("Cállate.", "Kirino"),
    31: ("Además, ¿por qué no lo has jugado? ¿No es normal entrar a otras rutas después de completar la de Miyabi?", "Kirino"),
    32: ("No suelo jugar juegos. Lo sabes, ¿no?", "Kyousuke"),
    33: ("¡¿Hah?! ¡Esa razón no es aceptable!", "Kirino"),
    36: ("Ahhh, eso...", "Kyousuke"),
    40: ("No lo has jugado, ¿cierto?", "Kirino"),
    41: ("No, lo jugué ayer.", "Kyousuke"),
    42: ("...Mentiras.", "Kirino"),
    43: ("¡No es mentira!", "Kyousuke"),
    44: ("Ayer, cuando volví a casa, empecé «la ruta de Rinko»...", "Kyousuke"),
    45: ("Si admites que es mentira ahora mismo, quizás te perdone.", "Kirino"),
    46: ("...¡Es mentira!", "Kyousuke"),
    49: ("Entonces... ¿no me vas a perdonar en absoluto...?", "Kyousuke"),
    50: ("Lo que quise decir es que perdonaría tu mentira.", "Kirino"),
    51: ("No te perdonaré por no jugar «SisSis» sin embargo.", "Kirino"),
}

a82_n = {
    0: "SisSis",
    7: "Puede que pienses que son buenas intenciones, pero es presión adicional para mí.",
    14: "¡Mierda...! ¿Me pasé?",
    15: "Pero es verdad que no tengo tiempo para jugar...",
    20: "E-Es verdad que ella está siendo seria a su manera.",
    21: "Esa respuesta a medias fue un error...",
    29: "¡¿Ensayo?! ¡Ni modo!",
    32: "¡Esto no se trata de ganar o perder!",
    37: "Me pregunto cuándo tomaré realmente la iniciativa para jugarlo...",
}
a82_s = {
    1: ("¿Por qué no has jugado ese juego divino?", "Kirino"),
    2: ("Te dije que no tengo tiempo para eso.", "Kyousuke"),
    3: ("¿Qué tan lento eres? Deberías poder completarlo en unas dos tardes.", "Kirino"),
    4: ("¡No tengo ganas de dedicar dos noches a los juegos!", "Kyousuke"),
    5: ("¿No es todo tu culpa porque no has estado jugando en absoluto?", "Kirino"),
    6: ("¡De hecho te presenté algo interesante! ¿Por qué desperdicias las buenas intenciones de alguien?", "Kirino"),
    8: ("No, hay circunstancias profundas detrás de esto...", "Kyousuke"),
    9: ("Además, todavía no puedo creer esto.", "Kirino"),
    10: ("Quizás no conozca tus gustos, ¡pero estás desperdiciando 1/3 de tu vida al no jugar «SisSis»!", "Kirino"),
    11: ("¿Eres consciente de eso?", "Kirino"),
    12: ("¡No lo entiendo en absoluto! ¡Ni quiero!", "Kyousuke"),
    13: ("¿N-No quieres...? ¡No tienes que llegar tan lejos!", "Kirino"),
    16: ("En resumen, no va con mis intereses.", "Kyousuke"),
    17: ("¡Hmph! ¡Eso es porque tu nivel de comprensión es demasiado bajo!", "Kirino"),
    18: ("...Sí...", "Kyousuke"),
    19: ("¡No me des la espalda así! ¡Estoy hablando en serio!", "Kirino"),
    22: ("Entonces, te ordenaré una vez más.", "Kirino"),
    23: ("¿O-Orden, dices?", "Kyousuke"),
    24: ("Debes completar ambas rutas antes de mañana por la mañana. Y también escribir un ensayo de 30 páginas sobre tus impresiones.", "Kirino"),
    25: ("¡Tú! ¡¿No acabas de decir que completarlo requiere al menos dos noches?!", "Kyousuke"),
    26: ("El punto es, esto es una cuestión de motivación.", "Kirino"),
    27: ("¡Es absurdo!", "Kyousuke"),
    28: ("Quiero decir, con la fecha límite acercándose, ¿no deberías apurarte en lugar de quejarte?", "Kirino"),
    30: ("Solo pensaste que es imposible, ¿no? Y por eso no puedes hacerlo.", "Kirino"),
    31: ("¿No es eso lo mismo que admitir tu derrota desde el principio?", "Kirino"),
    33: ("Ah, para tu información, Wiki está prohibida.", "Kirino"),
    34: ("Si te atreves a revisar la Wiki, te llamaré Bastardo Tramposo.", "Kirino"),
    35: ("¡¿Qué es eso?!", "Kyousuke"),
    36: ("De todos modos, este juego te hará derramar lágrimas; los pañuelos son esenciales.", "Kirino"),
    38: ("¿Q-Qué es ese mal sentido de nombres...", "Kyousuke"),
    39: ("Si no quieres, entonces hazlo. ¿Okay? ¿Okay?", "Kirino"),
    40: ("¡Lo importante no es si puedes hacerlo o no!", "Kirino"),
    41: ("¿Jugar o no jugar?", "Kirino"),
    42: ("Solo haz lo que quieras...", "Kyousuke"),
    43: ("¿Entonces? ¿Jugarás? ¿No jugarás? ¿Cuál es?", "Kirino"),
}

data = {
    "000scriptAKYO_0074A.obj": build(a74_n, a74_s),
    "000scriptAKYO_0078T.obj": build(a78_n, a78_s),
    "000scriptAKYO_0080A.obj": build(a80_n, a80_s),
    "000scriptAKYO_0081A.obj": build(a81_n, a81_s),
    "000scriptAKYO_0082T.obj": build(a82_n, a82_s),
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