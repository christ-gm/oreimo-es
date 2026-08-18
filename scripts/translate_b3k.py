import json

PATH = "/mnt/c/Users/christ-gm/Desktop/code/oreimo/work/disc1/Data/Translation.json"

def build(narration, speech):
    out = {}
    for i, t in narration.items():
        out[str(i)] = t
    for i, t in speech.items():
        out[str(i)] = "「" + t[0] + "」"
    return out

a0195_n = {
    0: "Ruta de Kuroneko · La Pesadilla De Un Día De Verano",
    1: "El manuscrito de Kuroneko... no se terminó al final.",
    2: "Por supuesto, como el círculo de Kuroneko no tenía nada nuevo... probablemente vendió algunos productos más viejos en la sección de reventa en el Comiket de Verano...",
    5: "Dicho esto, Kuroneko rechazó mi oferta al final.",
    6: "¿Por qué está siendo tan obstinada...? Todavía no entiendo eso al final.",
    7: "Esta es mi primera vez aquí solo...",
    8: "Espero no perderme...",
    10: "En realidad pensé en pedirle a Saori que me enseñara... sin embargo, sentí que ir solo era mejor.",
    12: "Por Dios, esta chica...",
    13: "...Aunque tiene maquillaje como siempre, da una impresión diferente ahora...",
    14: "Por más linda que sea... con esa expresión, todo se desperdicia...",
    15: "Si estás sola, solo dilo con honestidad...",
    16: "Pero esas palabras, su orgullo no le permitirá decirlas...",
    18: "Pero los gatos de verdad todavía intentan encontrar a alguien con quien jugar cuando se sienten solos.",
    21: "Ya que al final, terminaremos estando en desacuerdo sin fin de todos modos...",
    22: "Aun así, esto es mejor que tenerla sentada sola ahí.",
}
a0195_s = {
    3: ("Necesitas a alguien para atender el puesto, ¿verdad? ¿Qué tal si yo ayudo?", "Kyousuke"),
    4: ("No hace falta. Este trabajo es mío después de todo. Me encargaré de él personalmente.", "Kuroneko"),
    9: ("Maldición, seguro que hay mucha gente...", "Kyousuke"),
    11: ("Bueno entonces... debería estar por aquí, supongo.", "Kyousuke"),
    17: ("Es... como una gata, Dios...", "Kyousuke"),
    19: ("Y aun así...", "Kyousuke"),
    20: ("Más que una gata, es solo malhumorada.", "Kyousuke"),
    23: ("Yo, Kuroneko.", "Kyousuke"),
    24: ("Aunque no quieras que te ayude, ya que estoy aquí, realmente no puedes rechazarme, ¿verdad?", "Kyousuke"),
}

a0200_n = {
    0: "Ruta de Kuroneko · Un Extraño Día De Verano",
    1: "Desde ahí, todo pasó realmente rápido...",
    2: "Finalmente, el manuscrito estaba terminado y entregado para la impresión...",
    3: "Estábamos esperando con ansias ese día en particular ---- hasta...",
    33: "¿N-No puede ser...?",
}
a0200_s = {
    4: ("¿Eh? ¿Los libros todavía no han llegado?", "Kyousuke"),
    5: ("Sí. Incluso milagrosamente logré conseguir que un empleado lo confirmara...", "Kuroneko"),
    6: ("S-Sí...", "Kyousuke"),
    7: ("Dijeron que hubo un error en el formulario de registro.", "Kuroneko"),
    8: ("...¿Eh? ¿Podría ser, el que yo había escrito...", "Kyousuke"),
    9: ("Me pregunto por qué la fecha de entrega fue el primer día. Considerando que hoy es el tercer día.", "Kuroneko"),
    10: ("¿P-Podría ser...? ¿Mi culpa...?", "Kyousuke"),
    11: ("En efecto. Ni siquiera puedes completar una tarea tan insignificante. Bastante tonto eres.", "Kuroneko"),
    12: ("...No puede ser.", "Kyousuke"),
    13: ("A diferencia de ti, yo sí soy capaz de reconocer cuándo debería estar mintiendo.", "Kuroneko"),
    14: ("Entonces, ¿qué planeas hacer para compensarla?", "Kirino"),
    15: ("Bueno... cuando dices 'compensar'... Oye, ¿Kuroneko?", "Kyousuke"),
    16: ("Lo terminamos, pero para que tal conclusión nos esperara... ¿Podría ser que mi precognición ha fallado en algún lugar...", "Kuroneko"),
    17: ("Entonces, ¿qué debería hacer con esos libros que deberían haber llegado hoy para venderse? Además, ¿cuál es el resultado final de toda mi pasión?", "Kuroneko"),
    18: ("Ah...L-Lo siento...", "Kyousuke"),
    19: ("Ah～ah. Qué lástima. No pude ver tu doujinshi épico.", "Kirino"),
    20: ("Vaya, no pensé que lo esperarías tanto.", "Kuroneko"),
    21: ("Solo esperaba ver tu cara presumida agriarse mientras te ignoran y todo esto se convierte en una obra de humillación～", "Kirino"),
    22: ("Sí, esta era la oportunidad perfecta para llamar algo de atención a mi doujinshi.", "Kuroneko"),
    23: ("De todos modos, solo buscabas acariciar tu ego, ¿no?", "Kirino"),
    24: ("Esto es lo que pasa cuando se reúnen muchos productos. Se trata de si captan o no la atención del público.", "Kuroneko"),
    25: ("Bueno bueno, ambas, cálmense.", "Saori"),
    26: ("Saori...", "Kirino"),
    27: ("Vaya, esto es...?", "Kuroneko"),
    28: ("Bueno... esta vez, es completamente debido al descuido de Kyousuke-shi. Por eso, Kyousuke-shi, debes asumir la responsabilidad.", "Saori"),
    29: ("Ah, bueno... No tengo nada que decir. No tengo excusas.", "Kyousuke"),
    30: ("Entonces, como castigo, Kyousuke-shi usará esto.", "Saori"),
    31: ("¡Ajajajajajaj! ¡Saori, bien hecho!", "Kirino"),
    32: ("...En efecto, esto es de hecho... bueno.", "Kuroneko"),
    34: ("¡Por favor! ¡P-Perdónenme!!", "Kyousuke"),
    35: ("Vaya vaya, ¿esto es solo el principio?", "Kuroneko"),
    36: ("Sí, sí. Esto todavía no ha terminado, Kyousuke-shi.", "Saori"),
    37: ("De paso, no te queda nada bien.", "Kirino"),
    38: ("¡Kirino! ¡No digas esas cosas mientras tomas fotos!", "Kyousuke"),
    39: ("Sabes... Esto no es algo de lo que deberías poder librarte solo con unas cuantas fotos, ¿no?", "Kirino"),
    40: ("¡Lo siento, lo siento! ¡Por favor perdónenme! Sean cuales sean las circunstancias, ¡ustedes de verdad se están pasando de la raya!", "Kyousuke"),
    41: ("En realidad, no hablaba en serio sobre borrarte de la sociedad.", "Kuroneko"),
    42: ("¡¿E-Es así!? ¡Entonces eso es una gran ayuda ahí...", "Kyousuke"),
    43: ("Sí, es verdad. Sin embargo, de hecho creo que 'esto' es un material bastante raro de obtener...", "Kuroneko"),
    44: ("¿Eh...? ¿K-Kuroneko? ¿Q-Qué estás diciendo...", "Kyousuke"),
    45: ("He aprendido algo de este incidente.", "Kuroneko"),
    46: ("Te forzaste a entrar en esto, y aun así nada bueno salió de ello.", "Kuroneko"),
    47: ("Por eso...", "Kuroneko"),
    48: ("De ahora en adelante, harás lo que yo diga, ¿verdad? ¿Senpai?", "Kuroneko"),
}

a0210_n = {
    0: "Ruta de Kuroneko · Cuñada Y El Juramento",
    1: "Finalmente. Todo terminó pacíficamente.",
    2: "Con este caso cerrado, misión completa, ¿verdad?",
    4: "Eso fue lo que pensé pero... ¿Por qué Kuroneko quiere pisar una mina terrestre ahora mismo?",
    42: "Por Dios. ¿Las dos se quedarán así en el futuro?",
    43: "Aún así, ambas ya son buenas amigas... además, es solo otra manera de vincularse entre ellas, estoy seguro de que nada cambiará.",
    44: "Y, realmente deseo que ---- Kuroneko y yo estemos en una relación que le permita llamarle a Kirino hermana pequeña.",
}
a0210_s = {
    3: ("Qué cansado... Esa hermanita de allá, agarra este equipaje.", "Kuroneko"),
    5: ("¿Qué es eso de una hermanita?", "Kirino"),
    6: ("Por supuesto, me refiero a ti. ¿Quién más podría convertirse en mi hermanita además de ti?", "Kuroneko"),
    7: ("Qué, ¿finalmente has enloquecido? ¿Yo, tu hermanita? ¿De dónde sacaste eso?", "Kirino"),
    8: ("Muestra algo de respeto. No es como si quisiera convertirme en tu hermana mayor, ¿sabes?", "Kuroneko"),
    9: ("...Aunque ya lo soy.", "Kuroneko"),
    10: ("No lo entiendo.", "Kirino"),
    11: ("O-Oye... ¿podría ser, que tú...", "Kirino"),
    12: ("Ajajajajaja... Perdón Kirino. Olvidé decirte, actualmente estoy saliendo con Kuroneko.", "Kyousuke"),
    13: ("¡¿Hah!?", "Kirino"),
    14: ("En ese caso, de ahora en adelante te referirás a mí como 'onee-sama', ¿entendido? Hermanita.", "Kuroneko"),
    15: ("Ah, estás mintiendo... todo esto es una mentira, ¿verdad? E-Esto es algún tipo de broma, ¿no?", "Kirino"),
    16: ("¿Kirino? ¿Estás bien?", "Kyousuke"),
    17: ("E-Eso es imposi...", "Kirino"),
    18: ("Está realmente atónita.", "Kuroneko"),
    19: ("...Oye, Kuroneko, ¿no crees que hubiera sido mejor explicar esto en otro momento?", "Kyousuke"),
    20: ("Si hablamos de esta hermanita, ¿qué mejor momento hay para elegir? Además---", "Kuroneko"),
    21: ("¡Oh! ¡Entonces ustedes dos están saliendo de verdad! ¡Felicidades a los dos! ¡Kuroneko-shi, Kyousuke-shi!", "Saori"),
    22: ("Solo estoy siendo abierta al respecto. Eso es todo. Bueno, gracias de todos modos.", "Kuroneko"),
    23: ("Jeje... bueno, gracias, Saori.", "Kyousuke"),
    24: ("No, de nada. Eres demasiado cortés. Deseo animarlos a los dos～", "Saori"),
    25: ("Sí. Es todo gracias a todos que estamos aquí hoy.", "Kyousuke"),
    26: ("Eso es todo por hoy, ¿verdad? Vámonos a casa temprano. ¿Te quedas en mi casa hoy otra vez?", "Kuroneko"),
    27: ("Sí. Mis estudios para los exámenes están avanzando bien. Puedo acompañarte todo el día hoy.", "Kyousuke"),
    28: ("Jeje... Mis hermanitas desean conocerte, así que ve a verlas un rato después, ¿de acuerdo?", "Kuroneko"),
    29: ("Seguro.", "Kyousuke"),
    30: ("Ooo, se está poniendo bastante caliente aquí...", "Saori"),
    31: ("T-T-T...", "Kirino"),
    32: ("¡¡Eso está absolutamente prohibido-------!!!!", "Kirino"),
    33: ("Oh, ¿ha resucitado de entre los muertos?", "Kyousuke"),
    34: ("Vaya, ¿qué pasa, hermanita?", "Kuroneko"),
    35: ("¡No me digas 'qué pasa'! He estado escuchando en silencio lo que ustedes dos hablaban hace un momento, ustedes dos...!", "Kirino"),
    36: ("¿Así que te sientes sola por haber sido dejada de lado? Qué hermanita tan problemática.", "Kuroneko"),
    37: ("¡Por eso dije que eres molesta! No vale la pena que me llames 'hermanita'...", "Kirino"),
    38: ("¿Qué tal si vienes a mi casa si te gustaría?", "Kuroneko"),
    39: ("¿Eh? ¿A-Ah...? q-quién querría ir a tu casa?!", "Kirino"),
    40: ("También tengo hermanitas, es perfecto. Todas son 'hermanitas', así que estoy segura de que se llevarán bien?", "Kuroneko"),
    41: ("～～～～～～～～～～～～～!!!!!!!!", "Kirino"),
    45: ("Vaya, eso es lo que yo también tengo en mente.", "Kuroneko"),
    46: ("¡Yo absoluta～mente no reconoceré esto!", "Kirino"),
    47: ("Si solo me llamaras 'onee-sama' obedientemente, sería capaz de decir esa frase... qué lástima.", "Kuroneko"),
    48: ("¿Huh? ¿Qué planeas decir?", "Kirino"),
    49: ("Jeh... ¿no es obvio?", "Kuroneko"),
    50: ("Es 'Mi Hermana Pequeña No Puede Ser Tan Linda'.", "Kuroneko"),
}

data = {
    "000scriptCKUR_0195E.obj": build(a0195_n, a0195_s),
    "000scriptCKUR_0200E.obj": build(a0200_n, a0200_s),
    "000scriptCKUR_0210E.obj": build(a0210_n, a0210_s),
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
