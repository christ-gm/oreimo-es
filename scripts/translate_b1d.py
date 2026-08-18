import json

PATH = "/mnt/c/Users/christ-gm/Desktop/code/oreimo/work/disc1/Data/Translation.json"

def build(narration: dict, speech: dict) -> dict:
    out = {}
    for i, t in narration.items():
        out[str(i)] = t
    for i, t in speech.items():
        out[str(i)] = "「" + t[0] + "」"
    return out

a33_n = {
    0: "La Estrategia Sublime",
    2: "...Y entonces mi hermana anunció orgullosamente su estrategia.",
}
a33_s = {
    1: ("Bueno, de todos modos, ¡escucha la gran estrategia que pensé!", "Kirino"),
    3: ("¿Qué te pareció? ¿No es increíble?", "Kirino"),
    4: ("Lo siento, aunque la escuché, no la entiendo realmente.", "Kyousuke"),
    5: ("¿Hah? Eso es, como, imposible.", "Kirino"),
    6: ("...Hmph. Esto no es algo que puedas llamar estrategia para empezar.", "Kuroneko"),
    7: ("En otras palabras...", "Kuroneko"),
}

a34_n = {
    0: "Mejor Que Nada",
}
a34_s = {
    1: ("A tu nivel actual, es mejor que nada.", "Kuroneko"),
    2: ("¿Qué? ¡¿Estás diciendo que soy carne de cañón?!", "Kyousuke"),
    3: ("Jajaja. ¡Esa reacción era de esperarse!", "Saori"),
    4: ("¡¿Por qué tengo que ser carne de cañón?!", "Kyousuke"),
    5: ("La historia se construye sobre una gran cantidad de cadáveres.", "Saori"),
    6: ("¡No entiendo eso en absoluto!", "Kyousuke"),
    7: ("Bueno, en pocas palabras, solo estás aumentando los números.", "Saori"),
}

a35_n = {
    0: "Entrenamiento",
    13: "Después de que finalmente me rendí, Kirino y las demás comenzaron de inmediato a entrenar en Siscaly.",
    14: "La expresión de Kuroneko cambió por completo en el momento en que empezó el juego.",
    15: "Usaba el control con tanta velocidad que ni siquiera podía ver sus dedos moverse.",
    16: "El personaje de Kuroneko, «Alicia Blackcat», bailaba como mariposas mientras atacaba al personaje de Kirino, «Tenjouin Mikoto».",
    17: "Wow... Es completamente diferente cuando ves jugar a un experto.",
    21: "Ella enfatizó especialmente la palabra «solo».",
    22: "Sin embargo, los movimientos de Kuroneko son realmente buenos...",
    23: "¿No somos extremadamente afortunados de tenerla como aliada?",
    30: "Esto es... una derrota abrumadora.",
    34: "Ah, ah. Kirino está fulminando con la mirada a Kuroneko.",
    36: "¡¿Lanzó el control?! ¡¿Y además, por qué a mí?!",
    50: "Esto no está bien...",
    64: "Después de eso, cambiamos nuestras parejas muchas veces y entrenamos duro, pero no hubo avance.",
    65: "Enfrentar a la Kuroneko de nivel nacional está fuera de cuestión, pero aún tengo problemas para leer los movimientos de Kirino y Saori.",
    66: "Después de ser humillado durante docenas de rondas, esta vez es Kirino y Kuroneko contra Saori y yo.",
    67: "No importa cómo lo pienses, no deberíamos tener oportunidad de ganar... Sin embargo-",
    77: "Siempre es así...",
    78: "Al final, se olvidaron de los controles y empezó la pelea.",
    79: "Con las dos así-",
    81: "Los personajes descontrolados son eliminados rápidamente.",
    82: "Esta memorable primera victoria nos la trajo la fea pelea interna de nuestras dos ases.",
    84: "Aunque socializan sin reservas cuando juegan, cuando se trata de llevarse bien fuera de eso...",
    85: "Hay algo más en ello, ¿eh?",
}
a35_s = {
    1: ("¿No es esa una forma extraña de pensar?", "Kyousuke"),
    2: ("Los oponentes se unen en condiciones similares. Incluso si soy el cebo o lo que sea, es obvio que un jugador sin habilidad como yo solo puede ser una desventaja.", "Kyousuke"),
    3: ("...¿Todavía quejándote?", "Kirino"),
    4: ("Vaya, vaya... Qué pobre criterio.", "Kuroneko"),
    5: ("Kyousuke-shi es realmente lento...", "Saori"),
    6: ("¿Qué quieres decir con eso?", "Kyousuke"),
    7: ("Hay una razón para que participes en el torneo, Kyousuke-shi. ¡Carne de cañón o cebo, esas son solo excusas!", "Saori"),
    8: ("Juju, es porque Kiririn-shi y Kuroneko-shi no están siendo sinceras.", "Saori"),
    9: ("...H-Hmph, podrías haber dicho eso desde el principio. En ese caso yo habría...", "Kyousuke"),
    10: ("Vaya, vaya... Kyousuke-shi es realmente denso.", "Saori"),
    11: ("¿No puedes apurarte? Está por empezar.", "Kirino"),
    12: ("Muy bien. Déjamelo a mí.", "Kyousuke"),
    18: ("Aunque pretendes ser hábil, en verdad ni siquiera estás a mi altura.", "Kuroneko"),
    19: ("¡Ooh! ¡Como era de esperar de Kuroneko-shi de 【Nivel Nacional】!", "Saori"),
    20: ("Solo eres una chica maliciosa y delirante. Como siempre, «solo eres buena en los videojuegos».", "Kirino"),
    24: ("¿No te das cuenta? Conozco tus movimientos como la palma de mi mano.", "Kuroneko"),
    25: ("Ugh...", "Kirino"),
    26: ("Hmph... Llena de huecos...", "Kuroneko"),
    27: ("¡Hnng!", "Kirino"),
    28: ("Bueno, ya es hora de que tomes un descanso.", "Kuroneko"),
    29: ("¡Disfruta tu sueño en la desesperación!", "Kuroneko"),
    31: (".........", "Kirino"),
    32: ("¿Debo ir suave contigo en el próximo juego?", "Kuroneko"),
    33: ("...Ghnnn...", "Kirino"),
    35: ("Kirino, conozco bien ese sentimiento-", "Kyousuke"),
    37: ("Es tu culpa...", "Kirino"),
    38: ("¡¿Eh?! ¡¿Yo?!", "Kyousuke"),
    39: ("¡Es porque estabas dando vueltas, eso me hizo perder la concentración!", "Kirino"),
    40: ("¡¿E-Esto es mi culpa?!", "Kyousuke"),
    41: ("Si estuviera en serio... esta chica malvada...", "Kirino"),
    42: ("Je. Para ser una bestia débil, ladras mucho.", "Kuroneko"),
    43: ("¿Dijiste algo?", "Kirino"),
    44: ("Dije que eso es un aullido de perdedora.", "Kuroneko"),
    45: ("...Gnn-Hmph! ¿Estás tratando de provocarme?", "Kirino"),
    46: ("¿De verdad crees que caería en la trampa?", "Kirino"),
    47: ("¿No lo estás haciendo ya...?", "Kyousuke"),
    48: ("¡No lo estoy!", "Kirino"),
    49: ("...Ah, hah... Maldición, maldición...!", "Kirino"),
    51: ("Oye, Kuroneko, déjala ganar una ronda.", "Kyousuke"),
    52: ("Debo declinar. Por favor, no me interrumpas durante un duelo.", "Kuroneko"),
    53: ("Ustedes dos... Es solo un juego, ¡están exagerando!", "Kyousuke"),
    54: ("...¿Solo?", "Kuroneko"),
    55: ("...¿Un juego?", "Kirino"),
    56: ("¡Uwoh!", "Kyousuke"),
    57: ("¿Qué quieres decir con que es solo un juego? ¿Todavía no entiendes?", "Kirino"),
    58: ("Esto es un juego, y a la vez no lo es. ¿Todavía no te has dado cuenta?", "Kuroneko"),
    59: ("Bueno, bueno. Ustedes dos no necesitan estar tan acaloradas...", "Saori"),
    60: ("¡¿Hah?!", "Kirino"),
    61: ("Kyousuke-shi ya se está arrepintiendo.", "Saori"),
    62: ("De todos modos, ¡lo que Kiririn-shi necesita es «calmarse»!", "Saori"),
    63: ("Lo sé, incluso si no lo hubieras dicho.", "Kirino"),
    68: ("¡E-Espera! ¿Qué estás haciendo?", "Kirino"),
    69: ("Estás en mi camino.", "Kuroneko"),
    70: ("¡Solo estoy tratando de ayudarte!", "Kirino"),
    71: ("No necesito tu ayuda. Mantendré el control del campo de batalla yo sola.", "Kuroneko"),
    72: ("¡¿Hah?!", "Kirino"),
    73: ("Hablando con franqueza, no eres más que una molestia.", "Kuroneko"),
    74: ("¡¿Qué es esa excusa?!", "Kirino"),
    75: ("Entonces, ¿qué tal una batalla de 3 contra 1? Puedo liberar mis poderes sellados si no hay nadie en mi camino.", "Kuroneko"),
    76: ("...De verdad me sacas de quicio.", "Kirino"),
    80: ("¡Toma eso! ¡Ahí!", "Saori"),
    83: ("Ustedes dos... ¡Al menos sean amables cuando jueguen juntas!", "Kyousuke"),
}

a36_n = {
    0: "Entrenamiento",
    29: "Oye, ¿no es eso sacado de un drama...?",
    31: "Se ve tan orgullosa, pero esta es una línea tan cliché.",
    55: "En serio... Soy yo quien está harto de tener una hermanita tan horrible...",
}
a36_s = {
    1: ("¿Qué pasa? ¿Tratando de detenerme?", "Kirino"),
    2: ("No tengo esa intención, ¡¿pero es ahora el momento de pelear?!", "Kyousuke"),
    3: ("Tienes que decírselo directamente a esa chica, ¿sabes?", "Kirino"),
    4: ("¡Por - eso - te pido que enfríes la cabeza!", "Kyousuke"),
    5: ("¡Por - eso - te digo que no te metas en esta conversación!", "Kirino"),
    6: ("Bueno, espera. Escucha...", "Kyousuke"),
    7: ("Está bien, así que quédate callado y observa.", "Kirino"),
    8: ("De todos modos, tú también eres bastante peculiar.", "Kirino"),
    9: ("¡¿Yo?!", "Kyousuke"),
    10: ("¿Siquiera sabes el significado de trabajo en equipo?", "Kirino"),
    11: ("¡No me tomes por tonto! ¡Sé eso y más!", "Kyousuke"),
    12: ("¿Esa es la actitud de alguien que entiende el trabajo en equipo? Solo lo estás perturbando.", "Kirino"),
    13: ("¡No quiero oír eso de ti!", "Kyousuke"),
    14: ("Te estoy enseñando personalmente qué es el trabajo en equipo, así que me gustaría algo de gratitud.", "Kirino"),
    15: ("T-Tú...", "Kyousuke"),
    16: ("......", "Kyousuke"),
    17: ("¿Qué? No te quedes callado, di algo.", "Kirino"),
    18: ("No puedo decir nada por pura incredulidad.", "Kyousuke"),
    19: ("Ahora mismo, nadie más que tú está perturbando nuestro trabajo en equipo.", "Kyousuke"),
    20: ("...No tengo idea de qué hablas.", "Kirino"),
    21: ("Te lo explicaré para que incluso TÚ puedas entenderlo...", "Kirino"),
    22: ("El kanji «persona» se escribe de tal manera que una persona sostiene a la otra.", "Kirino"),
    23: ("¡Eso es sacado de algún drama!", "Kyousuke"),
    24: ("No interrumpas a la gente.", "Kirino"),
    25: ("¡Augh!", "Kyousuke"),
    26: ("Esta es la razón por la que nuestro trabajo en equipo está siendo perturbado.", "Kirino"),
    27: ("¿Por qué no puedes simplemente entenderlo?", "Kirino"),
    28: ("......", "Kyousuke"),
    30: ("Jeje, no lo sabías.", "Kirino"),
    32: ("¡Tus movimientos en «Siscaly» son tan pobres que mueres al instante!", "Kirino"),
    33: ("¡No hay relación entre esas dos cosas!", "Kyousuke"),
    34: ("Bueno, si me vieras jugar como un millón de veces, quizás te volverías un ser humano un poco mejor.", "Kirino"),
    35: ("¡¿Eres una Ladrona del Tiempo?!", "Kyousuke"),
    36: ("¿Eh? ¿Qué fue eso?", "Kirino"),
    37: ("¡Estás quitando tiempo precioso de mis preparativos para los exámenes! ¿Puedes ir al grano?", "Kyousuke"),
    38: ("¿De qué estábamos hablando de todos modos?", "Kirino"),
    39: ("¡Ah! ¡C-Cierto! ¡Ella! ¡La de negro!", "Kirino"),
    40: ("¿U-Un millón de veces...", "Kyousuke"),
    41: ("Ah, cierto. Además, sube mis videos de juego a Nico Douga.", "Kirino"),
    42: ("¿Eh? ¿Qué acabas de decir?", "Kyousuke"),
    43: ("Grabar, editar y comentar - te los dejo a ti.", "Kirino"),
    44: ("Tengo los exámenes después...", "Kyousuke"),
    45: ("¿Lo vas a hacer? ¿O no?", "Kirino"),
    46: ("¡No me mires con esa cara asesina! ¡Lo haré!", "Kyousuke"),
    47: ("Por cierto, si el número de visitas no aumenta... Sabes lo que pasará...", "Kirino"),
    48: ("...Haré mi mejor esfuerzo.", "Kyousuke"),
    49: ("De todos modos, si no sabes qué es el trabajo en equipo, entonces no sirve de nada ayudarse mutuamente.", "Kirino"),
    50: ("............", "Kyousuke"),
    51: ("¡Oye! ¡¿Estás escuchando?!", "Kirino"),
    52: ("¡Estoy escuchando! ¡Lo estoy!", "Kyousuke"),
    53: ("De todos modos, ¡baja el puño!", "Kyousuke"),
    54: ("De verdad, estoy harta de tener un hermano mayor tan estúpido...", "Kirino"),
}

data = {
    "000scriptAKYO_0033A.obj": build(a33_n, a33_s),
    "000scriptAKYO_0034A.obj": build(a34_n, a34_s),
    "000scriptAKYO_0035A.obj": build(a35_n, a35_s),
    "000scriptAKYO_0036T.obj": build(a36_n, a36_s),
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