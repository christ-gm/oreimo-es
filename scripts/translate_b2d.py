import json

PATH = "/mnt/c/Users/christ-gm/Desktop/code/oreimo/work/disc1/Data/Translation.json"

def build(narration: dict, speech: dict) -> dict:
    out = {}
    for i, t in narration.items():
        out[str(i)] = t
    for i, t in speech.items():
        out[str(i)] = "「" + t[0] + "」"
    return out

a30_n = {
    0: "Ruta de Kirino · Es Imposible Que Mi Hermanita Me Trate Como Un Extraño",
    1: "Después de una noche de pesadilla, he estado devanándome los sesos por Kirino desde el inicio de la escuela hasta mi caminata de vuelta a casa.",
    13: "La que en realidad no lo está haciendo como broma es mi hermanita.",
    14: "Ah... ¡Maldición! Mi cerebro no puede dejar el asunto de Kirino...",
    18: "Aunque eso fue lo que dijo, los ojos de Manami parecen decir «estoy esperando a que Kyou-chan me cuente al respecto».",
    24: "Ayer, la forma en que Kirino me miró fue justo como hace un año, como si estuviera mirando a un «extraño».",
    25: "Es cierto después de todo. Si no fuera por esos asuntos relacionados con el otaku, esa chica y yo somos como extraños.",
    27: "No me importa ser odiado, pero no puedo aceptar que los problemas por los que pasé durante este último año hayan sido simplemente borrados.",
    28: "Además, es mejor tener una impresión favorable de «menos 50%» que «menos 100%» de ella.",
    29: "Si ese es el caso, ¡haré lo que sea para recuperar los recuerdos de Kirino!",
}
a30_s = {
    2: ("¡--you-chan! Kyou-chan, ¿estás escuchando?", "Manami"),
    3: ("...Perdón, estaba pensando en otras cosas. ¿Qué estabas diciendo?", "Kyousuke"),
    4: ("Dios, es sobre mi hermanito～", "Manami"),
    5: ("Ahh, ¿le pasa algo a Rock?", "Kyousuke"),
    6: ("Ayer, cuando fui a su habitación para pasarle un recuerdo, me dijo «¡No te conozco!» en la cara.", "Manami"),
    7: ("¿Eh? ¿Podría haberlo olvidado?", "Kyousuke"),
    8: ("No. No es eso.", "Manami"),
    9: ("Dijo «¡Soy una estrella de rock sin familia ni amigos! Tanto ahora como en el pasado, ¡he estado viviendo completamente solo!»", "Manami"),
    10: ("...Ese tonto, fue influenciado por algo otra vez.", "Kyousuke"),
    11: ("Sin embargo, me asusté por un momento ahí.", "Manami"),
    12: ("B-Bueno, ¿no es bueno que todo terminara como una broma?", "Kyousuke"),
    15: ("...¿Qué pasa, Kyou-chan? ¿Te ves bastante desanimado?", "Manami"),
    16: ("N-No, no es nada.", "Kyousuke"),
    17: ("¿Es así...? Eso está bien entonces.", "Manami"),
    19: ("Sin embargo, incluso si sé que es una broma, es triste ser 【tratado como un extraño】...", "Manami"),
    20: ("...", "Kyousuke"),
    21: ("Ah, aquí estamos. Me iré por mi cuenta desde aquí. ¡Kyou-chan, nos vemos mañana!", "Manami"),
    22: ("Ah, sí...", "Kyousuke"),
    23: ("Extraño, eh...", "Kyousuke"),
    26: ("...Tch, no sé por qué, pero por alguna razón estoy irritado.", "Kyousuke"),
}

a31_n = {
    0: "Ruta de Kirino · Para Que Mi Hermanita Me Ignore No Es...Es Posible",
    18: "...¿Qué estás imaginando, pequeña...",
    22: "....No seas tan brusca.",
    23: "Es imposible. Incluso si hago que la Kirino actual escuche esa canción denpa, solo se enojará conmigo otra vez como ayer.",
    24: "Viendo cómo mi hermanita se ha vuelto así, empiezo a pensar de nuevo.",
    25: "En todo este año, la relación entre mi hermana y yo... definitivamente ha cambiado mucho.",
    29: "Está bien, presioné reproducir.",
}
a31_s = {
    1: ("Ya estoy en casa.", "Kyousuke"),
    2: ("...", "Kirino"),
    3: ("Oye, tengo algo que quiero que escuches...", "Kyousuke"),
    4: ("...", "Kirino"),
    5: ("Oye, no me ignores.", "Kyousuke"),
    6: ("¿Qué? ¿No le dije al pervertido que no me hablara?", "Kirino"),
    7: ("Tú eres la que pidió una sesión de orientación de vida, sin embargo.", "Kyousuke"),
    8: ("¿Huh? No espero nada de ti en este punto.", "Kirino"),
    9: ("...¿Oh en serio? Sin embargo, no pretendo rendirme a mitad de camino.", "Kyousuke"),
    10: ("De todos modos, no hablemos de esos temas aquí. Mamá nos oirá.", "Kirino"),
    11: ("...Entiendo. Entonces tu habitación debería estar bien?", "Kyousuke"),
    12: ("Tch, sabes cuáles son las consecuencias si haces algo extraño, ¿verdad?", "Kirino"),
    13: ("Hmph. Entonces, ¿qué quieres que escuche?", "Kirino"),
    14: ("Ahh, si escuchas esto, tus recuerdos deberían volver... Creo.", "Kyousuke"),
    15: ("...No son algunos sonidos extraños que grabaste, ¿verdad?", "Kirino"),
    16: ("Como si fuera a hacer eso. Además, ¿qué quieres decir con sonidos extraños?", "Kyousuke"),
    17: ("¿Me preguntas eso? ...Por eso eres un pervertido.", "Kirino"),
    19: ("¿Qué? Enciéndelo para que pueda escuchar ya.", "Kirino"),
    20: ("No.... eso es....", "Kyousuke"),
    21: ("Apúrate.", "Kirino"),
    26: ("...Está en este reproductor de música.", "Kyousuke"),
    27: ("No seré amable contigo si me haces escuchar cosas extrañas.", "Kirino"),
    28: ("Cálmate. No morirás aunque lo escuches un rato.", "Kyousuke"),
    30: ("...¡Absolutamente no puedo escuchar esto!", "Kirino"),
    31: ("¡Eso es demasiado rápido! Todavía está en la introducción, ¿no?", "Kyousuke"),
    32: ("Escuchar esto por 5 segundos pudrirá mi cerebro. ¿Qué pasa con esta canción extraña?", "Kirino"),
    33: ("¡Es una canción que compusiste, sin embargo!", "Kyousuke"),
}

a33_n = {
    0: "Ruta de Kirino · Para Que Mi Hermanita Me Ignore No Es...Es Posible",
    7: "*suspiro*... ¿Finalmente está dispuesta a creerme?",
    25: "¡Si yo fuera un otaku, eso sería una grosería con los otakus reales de todo el país!",
}
a33_s = {
    1: ("¿Huh? ¡¿Una canción que yo compuse?!", "Kirino"),
    2: ("¿Qué exactamente es tan interesante de preparar algo tan estúpido para contar una mentira así?", "Kirino"),
    3: ("¡No es sobre si es interesante o no! ¡Solo estoy diciendo la verdad!", "Kyousuke"),
    4: ("No tienes poder persuasivo.", "Kirino"),
    5: ("Confía en mí.", "Kyousuke"),
    6: ("...Entonces, ¿estás diciendo que esto es algo que hice?", "Kirino"),
    8: ("¡Como si!", "Kirino"),
    9: ("Lo diré una vez más. Esto fue hecho por ti.", "Kyousuke"),
    10: ("¡No, no, no! ¡Eso es imposible!", "Kirino"),
    11: ("¿T-Tú...? ¿Solo vas a negarlo por completo sin ninguna base para ello?", "Kyousuke"),
    12: ("...Qué molesto...", "Kirino"),
    13: ("La voz en la canción te pertenece, ¿no? ¿Cómo explicas eso?", "Kyousuke"),
    14: ("Aunque ese sea el caso, ¿no es posible editar o sintetizar voces en la computadora?", "Kirino"),
    15: ("¿No es este el tipo de método que los estafadores y secuestradores suelen usar?", "Kirino"),
    16: ("¡No lo digas como si yo fuera un criminal!", "Kyousuke"),
    17: ("Entonces produce rápidamente la evidencia que pruebe que no eres un criminal. Vamos.", "Kirino"),
    18: ("No existe tal cosa. Entonces, déjame preguntarte en su lugar, ¿por qué forjaría evidencia?", "Kyousuke"),
    19: ("¿Huh? Es realmente asqueroso discutir por discutir, ¿sabes?", "Kirino"),
    20: ("¡Eres tú la que está discutiendo por discutir!", "Kyousuke"),
    21: ("¿Hablas en serio? No hay forma de que pueda poseer tales habilidades.", "Kyousuke"),
    22: ("Pero, ¿no son los otakus expertos en ese campo?", "Kirino"),
    23: ("También hay muchos tipos de otakus. Espera, ¡¿estás diciendo que soy un otaku ahora?!", "Kyousuke"),
    24: ("Whoa～... ¿Ahora dices que no lo eres? Eso es demasiado tarde.", "Kirino"),
    26: ("Además, no tengo mi propia computadora. ¿Cómo se supone que creo estos sonidos?", "Kyousuke"),
    27: ("¿Cómo se supone que yo sé eso?", "Kirino"),
    28: ("Más bien, ¿estás diciendo seriamente que yo soy la que hizo esta canción?", "Kirino"),
    29: ("Si es así, no voy a poder tomarte en serio, ¿sabes?", "Kirino"),
    30: ("¡¿Qué estás diciendo?! ¡Haciéndote la inocente cuando se trata de tu propia afición...!", "Kyousuke"),
    31: ("¿Huh? ¿Qué afición?", "Kirino"),
    32: ("Como he dicho, tienes muchos artículos otaku que has escondido dentro de tu habitación. Esta canción también es una extensión de tu afición.", "Kyousuke"),
    33: ("¿Podría ser que te estás haciendo la tonta a propósito?", "Kyousuke"),
    34: ("Tus comentarios me están haciendo encogerme...", "Kyousuke"),
    35: ("¿Huh, qué? ¿He dicho algo mal?", "Kirino"),
    36: ("No seas tan desafiante. Te digo, de verdad no estoy mintiendo. Incluso haré un juramento.", "Kyousuke"),
    37: ("Entonces, si estás mintiendo, muere.", "Kirino"),
    38: ("...No me importa. Si puedes recuperar tus recuerdos de esa manera.", "Kyousuke"),
    39: ("¡¿Qué-?!", "Kirino"),
    40: ("¡Solo reconócelo ya! ¡Esta canción de verdad fue compuesta por ti!", "Kyousuke"),
    41: ("¡Co～mo～di～je, no dije que no recuerdo nada sobre esto!", "Kirino"),
    42: ("¡Solo recuérdalo ya! ¡Definitivamente deberías poder recordarlo! ¡De verdad te gustaba esta canción!", "Kyousuke"),
    43: ("Tú también, ¿no es hora de que lo dejes?", "Kirino"),
    44: ("No importa cuánto lo niegue, solo te aferras a ello persistentemente.", "Kirino"),
    45: ("¡Es como si me estuvieras lavando el cerebro!", "Kirino"),
    46: ("¡¿Eh?! ¡¿EH?!", "Kyousuke"),
    47: ("T-Tú de hecho mencionaste lavado de cerebro...", "Kyousuke"),
    48: ("...Deja de bromear conmigo.", "Kyousuke"),
    49: ("Tú también, deja de bromear conmigo. Has estado balbuceando persistentemente desde hace rato...", "Kirino"),
    50: ("Ah Dios...¡Esto es tan irritante!", "Kirino"),
    51: ("S-solo eres pura charla vacía...", "Kirino"),
    52: ("En cualquier caso, ¡no recuerdo haber hecho una canción como esta!", "Kirino"),
    53: ("...¿Hablas en serio? ¿Todavía lo niegas incluso con una prueba tan directa frente a ti?", "Kyousuke"),
    54: ("No me hagas seguir repitiéndome. Más bien, estoy cansada de tener que decirte que soy honesta, pero aún así tener que escucharte.", "Kirino"),
}

a35_n = {
    0: "Ruta de Kirino · Es Imposible Que Mi Hermanita Se Cuestiona A Sí Misma",
    17: "Sin embargo, esto se ha vuelto problemático.",
    18: "La impresión actual de Kirino sobre mí se ha convertido en la de un siscon extremo y bastardo otaku pervertido.",
    19: "Bueno, por otro lado, no hay nada que temer ahora que he llegado tan lejos. A diferencia de otros siscons, de verdad odio a mi hermanita, así que no",
    20: "realmente tengo un problema con que ella me odie.",
    21: "...Dios mío, ¿qué debería hacer al respecto?",
}
a35_s = {
    1: ("¡Basta ya!", "Kirino"),
    2: ("Tú también, ¡ya es hora de que lo recuerdes!", "Kyousuke"),
    3: ("Más bien, si lo pensáramos con calma, ¿es realmente posible que yo pierda solo los recuerdos de mis asquerosas aficiones otaku?", "Kirino"),
    4: ("¿Huh?", "Kyousuke"),
    5: ("Además, no sería una exageración llamarme la más bella, multi-talentosa y deslumbrante estudiante de secundaria de Japón ahora y...*jadeo jadeo*", "Kirino"),
    6: ("¿N-No es simplemente extraño que yo me incline hacia asquerosas aficiones otaku!?", "Kirino"),
    7: ("¡Lo extraño es tu cerebro! ¡¿Pensar que pudieras elogiarte hasta necesitar un respiro?!", "Kyousuke"),
    8: ("Porque es todo cierto, ¿no?", "Kirino"),
    9: ("Ciertamente.", "Kyousuke"),
    10: ("¡Eso es correcto! En otras palabras, ¡todas estas cosas deben ser tuyas! Vamos, apúrate y di la verdad. Si lo haces ahora, solo necesitarás dejar esta familia", "Kirino"),
    11: ("para obtener mi perdón.", "Kirino"),
    12: ("¡Eso no es perdón en absoluto!", "Kyousuke"),
    13: ("Estas no son mías. Puedes preguntarle a Papá si tienes dudas.", "Kyousuke"),
    14: ("Eso es... imposible.", "Kirino"),
    15: ("¡Basta, vete!", "Kirino"),
    16: ("Tch... Al final, es lo mismo que ayer.", "Kyousuke"),
}

a45_n = {
    0: "Ruta de Kirino · Es Imposible Que Mi Papá Sea Cabeza Dura",
    1: "...Varios días han pasado desde entonces.",
    2: "Después de observar tranquilamente la situación por un poco más de tiempo, todavía no había la más mínima señal de que Kirino recuperara sus recuerdos.",
    8: "...¿Podría ser que ha notado que Kirino ha perdido sus recuerdos?",
    11: "....No puedo contarle este tipo de cosas.",
    18: "¿Q-Qué pasa con él...? Tiene mucha fe en mí.",
    24: "Hubo una gran conmoción antes de que este libro fuera publicado.",
    25: "Incluso fui en secreto con Kuroneko al departamento editorial...",
}
a45_s = {
    3: ("Ya es hora de que idee un plan.", "Kyousuke"),
    4: ("¿Sí?", "Kyousuke"),
    5: ("...Kyousuke, voy a entrar.", "Daisuke"),
    6: ("¿P-Papá?", "Kyousuke"),
    7: ("Parece que Kirino ha estado actuando extraño recientemente... ¿Sabes algo al respecto?", "Daisuke"),
    9: ("N-No, no sé nada.", "Kyousuke"),
    10: ("Hmm, ya veo.", "Daisuke"),
    12: ("B-Bueno... Sí siento que ha estado inusualmente distante recientemente...", "Kyousuke"),
    13: ("¿Es así?", "Daisuke"),
    14: ("...¿Por qué vendrías a preguntarme?", "Kyousuke"),
    15: ("Pensé que sabrías algo si te preguntaba.", "Daisuke"),
    16: ("¿Eh...?", "Kyousuke"),
    17: ("Te dejo a Kirino en tus manos.", "Daisuke"),
    19: ("¿No eres tú el 【hermano mayor】 de Kirino?", "Daisuke"),
    20: ("......", "Kyousuke"),
    21: ("*ejem*... Hablando de eso, Kyousuke, ¿has leído esto?", "Daisuke"),
    22: ("Hmm... Esta novela es...", "Kyousuke"),
    23: ("«Imouto City: My City», parece ser una novela que Kirino escribió antes.", "Daisuke"),
    26: ("...Después de preguntarle a Kirino, parece que lo escribió cerca del final del año pasado.", "Daisuke"),
    27: ("...Sí.", "Kyousuke"),
    28: ("Honestamente, no sé si este libro es bueno o malo. Sin embargo...", "Daisuke"),
    29: ("La Kirino que escribió este libro en ese entonces, parecía que vivía su vida al máximo cada día incluso más que antes.", "Daisuke"),
    30: ("En realidad, era lo mismo que cuando empecé a verlos a ti y a Kirino pasar tiempo juntos.", "Daisuke"),
    31: ("......", "Kyousuke"),
    32: ("Sin embargo, la Kirino actual es diferente. Siento que está insegura de algún modo y ha perdido de vista quién es.", "Daisuke"),
    33: ("¡¿Kirino? ¿Por qué estás aquí?!", "Kyousuke"),
    34: ("Podía oírlos a ustedes dos hablando desde el pasillo...", "Kirino"),
    35: ("Entonces... ¿Tienes algo que decir?", "Daisuke"),
    36: ("¡Y-Yo...!", "Kirino"),
    37: ("No he perdido de vista quién soy.", "Kirino"),
    38: ("...¿Es eso realmente cierto?", "Daisuke"),
}

data = {
    "000scriptBKIR_0030A.obj": build(a30_n, a30_s),
    "000scriptBKIR_0031A.obj": build(a31_n, a31_s),
    "000scriptBKIR_0033T.obj": build(a33_n, a33_s),
    "000scriptBKIR_0035A.obj": build(a35_n, a35_s),
    "000scriptBKIR_0045A.obj": build(a45_n, a45_s),
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