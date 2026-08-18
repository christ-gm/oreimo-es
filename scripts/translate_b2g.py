import json

PATH = "/mnt/c/Users/christ-gm/Desktop/code/oreimo/work/disc1/Data/Translation.json"

def build(narration, speech):
    out = {}
    for i, t in narration.items():
        out[str(i)] = t
    for i, t in speech.items():
        out[str(i)] = "「" + t[0] + "」"
    return out

a72_n = {
    0: "Ruta de Kirino · Es Imposible Que Yo No Ayude A Mi Hermanita",
    1: "Eligiendo pausar la conversación ahí por el momento, dije que tenía algo urgente que hacer y salí de la sala de chat.",
    2: "Aunque sospecharon fuertemente algo, no creo que se hayan dado cuenta de la verdad todavía.",
    4: "Ahora evaluaré la situación basándome en lo que Saori me contó.",
    5: "Parece que algo le pasó a Kirino el 14 de julio mientras chateaba.",
    6: "Kirino era tal como siempre hasta entonces.",
    7: "Y el 15 de julio, ya había olvidado todo sobre ser otaku cuando llegué a casa.",
    14: "Oye oye... ¿de verdad está bien?",
}
a72_s = {
    3: ("Uf... Estoy empezando a entender lo que pasó mientras yo no estaba.", "Kyousuke"),
    8: ("Bueno... Puedo adivinarlo sin pensar mucho en ello. Algo debe haber pasado mientras ella estaba en la sala de chat en ese entonces.", "Kyousuke"),
    9: ("¿Algo pasó, dices...? ¿Qué quieres decir...?", "???"),
    10: ("¡¿Uowah?!", "Kyousuke"),
    11: ("K-Kirino, ¿cuándo llegaste aquí?", "Kyousuke"),
    12: ("...", "Kirino"),
    13: ("Oye, ¿estás bien? Tu cara se ve muy pálida... y ¿no estás temblando?", "Kyousuke"),
}

a75_n = {
    0: "Ruta de Kirino · Es Imposible Que Yo No Ayude A Mi Hermanita",
    7: "Kirino... Parece que está realmente frustrada. Eso es... solo natural.",
    8: "Ya está perturbada por perder sus recuerdos, y ahora no puede recordar a sus cálidas y cariñosas amigas.",
    9: "Esta chica valora mucho a sus amigas, así que probablemente no puede perdonarse a sí misma por eso.",
    10: "Tch... no hay más remedio. La animaré como su hermano mayor solo esta vez...",
    19: "La actitud de Kirino de enojarme no es nada fuera de lo común, así que no comentaré sobre ello ahora.",
    20: "Pero... justo ahora, ¿qué fue lo que dijo?",
}
a75_s = {
    1: ("Kirino... ¿Estás... bien?", "Kyousuke"),
    2: ("...Esas personas me conocen.", "Kirino"),
    3: ("Pero... no las conozco. ¡No las conozco en absoluto...!", "Kirino"),
    4: ("Oye, ¿de verdad he... perdido mis recuerdos?", "Kirino"),
    5: ("No sirve de nada... Es completamente inútil... ¡No puedo recordarlas en absoluto!", "Kirino"),
    6: ("...Kirino.", "Kyousuke"),
    11: ("Ah bueno, olvídalo.", "Kirino"),
    12: ("...¿Eh?", "Kyousuke"),
    13: ("Quiero decir, ¿qué les pasa? Solo continuaron su conversación unilateralmente sin pensar en mis circunstancias también. Demasiado", "Kirino"),
    14: ("desconsideradas.", "Kirino"),
    15: ("No... no quiero que me digas eso tú, de todas las personas.", "Kyousuke"),
    16: ("Por esto es que odio a los otakus.", "Kirino"),
    17: ("Esa clase de personas no pueden ser 【mis amigas】.", "Kirino"),
    18: ("...?!", "Kyousuke"),
}

a83_n = {
    0: "Ruta de Kirino · Es Imposible Que Yo No Ayude A Mi Hermanita",
    29: "Maldición... Así que al final, no pude hacer nada...?",
    39: "Es cierto que hasta hace un año, yo era como un extraño para ella. Es solo natural que Kirino se resista contra mí.",
}
a83_s = {
    1: ("Tú... ¿Qué fue lo que acabas de decir...?", "Kyousuke"),
    2: ("¿No me escuchaste? Dije «Esa clase de personas no pueden ser mis amigas».", "Kirino"),
    3: ("¡¡Qué estás diciendo!!", "Kyousuke"),
    4: ("No me hagas repetirme. ¿O eres tan obtuso que no entiendes el japonés?", "Kirino"),
    5: ("¡Esto no se trata de mí! ¡¿Cómo pudiste decir esas cosas sobre Saori y Kuroneko cuando están tan preocupadas por ti?!", "Kyousuke"),
    6: ("S-Soy libre de elegir lo que quiera decir...", "Kirino"),
    7: ("Oye... no hablas en serio, ¿verdad?", "Kyousuke"),
    8: ("Eres tan desconfiado... Eres impopular por eso, ¿sabes?", "Kirino"),
    9: ("No estamos hablando de mí ahora mismo, ¿verdad?", "Kyousuke"),
    10: ("Oh, ¿en serio...? Pero hablo en serio.", "Kirino"),
    11: ("Lo diré tantas veces como tenga que hacerlo. No puedo aceptar que esas personas sean mis amigas.", "Kirino"),
    12: ("¡Si vas a seguir siendo así, ellas se verán muy afectadas!", "Kyousuke"),
    13: ("...?!", "Kirino"),
    14: ("¡Tienen un año de recuerdos contigo! ¿Crees que está bien ignorar ese año solo por ti misma?", "Kyousuke"),
    15: ("E-Eso es...", "Kirino"),
    16: ("...Oye.", "Kyousuke"),
    17: ("¿Huh? ¿No te escuché?", "Kirino"),
    18: ("Kirino... Tú...", "Kyousuke"),
    19: ("No tengo recuerdos de conocerlas de todos modos. Francamente, no me preocupa de ninguna manera si no puedo recordar, ¿ves?", "Kirino"),
    20: ("Kirino...", "Kyousuke"),
    21: ("¿Hay algo malo en lo que he dicho?", "Kirino"),
    22: ("Ciertamente, ese puede ser el caso para ti... Sin embargo, para esas dos...", "Kyousuke"),
    23: ("Tch...", "Kirino"),
    24: ("...Ya no importa. Bien, esta discusión terminó～", "Kirino"),
    25: ("Tú... no eres Kirino.", "Kyousuke"),
    26: ("...¿Huh?", "Kirino"),
    27: ("¿No me escuchaste? Dije que no te reconozco como Kirino.", "Kyousuke"),
    28: ("¿Y-Yo no soy yo...? Pero yo soy yo.", "Kirino"),
    30: ("Esta discusión termina aquí. ¡Bien, reunión despedida!", "Kirino"),
    31: ("¡Te dije que la Kirino real no diría algo así!", "Kyousuke"),
    32: ("¿Huh? Todo lo que has dicho ha sido tontería desde hace rato.", "Kirino"),
    33: ("Guh... Esta chica...", "Kyousuke"),
    34: ("¿Qué me estás mirando fijamente? ¿Tienes alguna queja?", "Kirino"),
    35: ("¡¿Por qué tengo que hablar tanto con un mero extraño como tú?!", "Kirino"),
    36: ("¡Cállate! ¡Ya que se ha llegado a esto, no voy a ceder!", "Kyousuke"),
    37: ("¡Absolutamente haré que recuerdes tu verdadero yo!", "Kyousuke"),
    38: ("¡¿A-Eres estúpido?!", "Kirino"),
    40: ("*suspiro*... Solo no te involucres más conmigo, te lo ruego.", "Kirino"),
    41: ("¡Solo detente ya! ¡Estoy harta de ser arrastrada por ti!", "Kirino"),
    42: ("Hasta que recuperes tu memoria, seguiré arrastrándote. ¡Después de todo, soy tu hermano mayor!!", "Kyousuke"),
    43: ("H-Hermano mayor... T-Te dije que eso es asqueroso!", "Kirino"),
    44: ("¿Qué quieres decir con la verdadera yo...? Yo soy yo... ¿Cuántas veces debo decírtelo para que lo entiendas...", "Kirino"),
    45: ("¡Porque los recuerdos que estás desechando definitivamente son una parte de la verdadera tú!", "Kyousuke"),
    46: ("¿Q-Qué clase de argumento sin sentido estás tratando de hacer?", "Kirino"),
    47: ("Como dije, no necesito recuerdos de ser una otaku...", "Kirino"),
    48: ("¿Entonces te rendirás así nomás?", "Kyousuke"),
    49: ("...?!", "Kirino"),
    50: ("La Kirino Kousaka que yo conocía no renunciaría a algo una vez que su corazón está decidido a hacerlo. Con o sin recuerdos, esa parte es la misma.", "Kyousuke"),
    51: ("Por eso, si te rindieras aquí mismo, no eres Kirino Kousaka.", "Kyousuke"),
    52: ("...¡Y-Tú no entiendes nada de cómo me siento!", "Kirino"),
    53: ("...", "Kyousuke"),
    54: ("¿Qué...? ¡Di algo!", "Kirino"),
    55: ("No... Porque es inútil hablar más, ¿verdad?", "Kyousuke"),
    56: ("¡¿Qué-?!", "Kirino"),
    57: ("Incluso si soy asqueroso o molesto, sigo siendo tu hermano. Eso es algo que no cambiará sin importar cuánto me odies.", "Kyousuke"),
    58: ("De todos modos, ¡solo hay una Kirino! ¡Y yo soy yo! ¡Estoy bien con esto!", "Kirino"),
    59: ("...No está bien... Ni un poquito.", "Kyousuke"),
    60: ("Argh, ¡eres demasiado persistente! ¡Basta ya!", "Kirino"),
}

a85_n = {
    0: "Ruta de Kirino · Es Imposible Que Mi Hermanita No Valore A Sus Amigas",
    2: "Al menos, pensé que Kirino, incluso sin su lado otaku, no era la clase de persona que ignoraría a sus amigas.",
    3: "Pero la Kirino actual...",
    6: "Viene desde afuera de la ventana, cerca del borde del jardín...",
    8: "Oye oye, para que haya ruido a esta hora, ¿podría ser... un acosador de Kirino o algo así? Ella es modelo después de todo.",
    9: "D-De todos modos, echaré un vistazo en secreto mientras me oculto.",
    11: "Aunque no podía ver bien en la oscuridad, no hay muchas personas con siluetas de modelo en el mundo.",
    12: "Esa chica - ¿por qué está hurgando en el contenedor de basura?",
    14: "La silueta levantó su cabeza.",
    15: "¿Cuánto tiempo ha estado buscando? Su hermosa cara está ahora tan sucia que es solo un mero fragmento de su yo habitual.",
    16: "Sin embargo, parece que a Kirino no le importó en absoluto, ya que apretó firmemente en su mano el pequeño muñeco de Meruru de Edición Regional...",
    19: "Había olvidado que esta chica es alguien tan contradictoria y rebelde que está en la cima de su especie entre toda la humanidad.",
    20: "Mi hermanita no es hábil para preocuparse o expresar gratitud honestamente.",
    24: "¡¿Mierda?! ¡¡He sido descubierto!!",
    27: "Tú... no puedes tirar piedras a la gente, ¿sabes?",
    28: "Mientras mi conciencia se desvanecía, sonreí débilmente.",
}
a85_s = {
    1: ("¡Maldición!", "Kyousuke"),
    4: ("Aah, ¿qué debería hacer...", "Kyousuke"),
    5: ("¿Hmm? ¿Qué es ese ruido?", "Kyousuke"),
    7: ("Ese debería ser el lugar donde está el enorme contenedor de basura que usa nuestra familia.", "Kyousuke"),
    10: ("¿Eh? ¿No es esa...... Kirino?", "Kyousuke"),
    13: ("¡A-Aquí está!", "Kirino"),
    17: ("Esta cosa... podría ayudarme a recuperar mis recuerdos.", "Kirino"),
    18: ("...Lo había olvidado.", "Kyousuke"),
    21: ("...Esa chica... De verdad quiere recuperar sus recuerdos.", "Kyousuke"),
    22: ("?!", "Kirino"),
    23: ("Ah...", "Kyousuke"),
    25: ("¡¿Q-Q-Q-Q-Qué estás mirando?! ¡Pervertido! ¡Acosador! ¡Voyeur!", "Kirino"),
    26: ("¡¿Guah?!", "Kyousuke"),
}

a90_n = {
    0: "Ruta de Kirino · Es Imposible Que Yo Pueda Entender Completamente A Mi Hermanita",
    2: "De verdad, ya he tenido suficiente de los actos egoístas de esta chica.",
    3: "En lugar de perder mi tiempo aquí, más me vale volver a mi habitación y dormir un poco.",
    6: "Para ser claro, mi objetivo esta vez no es para mi autosatisfacción como de costumbre.",
    7: "Es por el bien de Kuroneko y Saori, y además, es por el bien de «la Kirino real» con todos sus recuerdos.",
    8: "La chica en cuestión está tarareando una melodía al otro lado de la pared.",
    9: "...Hablando de eso, esta ciertamente es una melodía extraña.",
    10: "Recuerdo haberla escuchado antes, así que debería ser una canción popular, pero suena extrañamente amateur...",
    12: "Bueno, es obvio que no hay respuesta.",
    13: "¿Hmm? ¿Su puerta está abierta...?",
    14: "Así que está usando sus auriculares... Parece que no ha notado que entré todavía.",
    15: "Sin embargo... ¿Por qué esta chica está tarareando la canción con una mirada tan seria en su cara?",
    18: "Como pensé, la había escuchado en algún lugar antes, y es solo natural que tenga una sensación amateur.",
    19: "Después de todo, esta es la canción denpa que Kirino hizo para el Comiket de Verano.",
    33: "Esta chica... lo que está diciendo es todo un sinsentido.",
    34: "Aunque me está golpeando salvajemente con toda su fuerza, mientras se agita sola...",
    35: "...¿Por qué sigue llorando?",
    39: "...Soy un tonto...",
    40: "Al final, no he entendido nada.",
    41: "No era consciente de los sentimientos reales de Kirino porque arbitrariamente pensé que estaba poniendo una cara valiente.",
    42: "*suspiro*, tampoco tengo las cualificaciones para ser su hermano mayor.",
    49: "...Así es, es correcto que mi hermanita actúe de esta manera.",
}
a90_s = {
    1: ("Tch, no puedo seguirle el juego a esto por más tiempo.", "Kyousuke"),
    4: ("No digas cosas extrañas como 【la Kirino real】. Yo soy yo...", "Kirino"),
    5: ("Maldición... Esa Kirino, no la entiendo en absoluto.", "Kyousuke"),
    11: ("¿Hmm? Esta canción...", "Kyousuke"),
    16: ("¡?! No entres así nomás a tu antojo!", "Kirino"),
    17: ("Tú, sobre esa canción...", "Kyousuke"),
    20: ("¿Por qué estás escuchando esto?", "Kyousuke"),
    21: ("¿No dijiste que no te importaba tu yo otaku del pasado?", "Kyousuke"),
    22: ("......Tch.", "Kirino"),
    23: ("...No chasquees la lengua.", "Kyousuke"),
    24: ("Sobre eso... Me gustaría hacerte una pregunta...", "Kirino"),
    25: ("¿La verdadera yo? ¿Cómo era yo antes cuando me gustaba esto?", "Kirino"),
    26: ("Incluso si me preguntas... no sé mucho sobre Kirino...", "Kyousuke"),
    27: ("!!", "Kirino"),
    28: ("Guh... Tú... Me duele, ¿sabes?", "Kyousuke"),
    29: ("¡Yo soy Kirino! ¡¿Cuántas veces me haces repetirme?!", "Kirino"),
    30: ("Es cierto que no recuerdo haber hecho esta canción, y no conozco a esas dos de hace un momento!", "Kirino"),
    31: ("Sin embargo... ¡cuanto más la escucho, más siento que esta canción no es mala! ¡Es la yo actual la que lo siente así, no la yo anterior!", "Kirino"),
    32: ("Por eso la yo actual y la yo anterior están conectadas... Aunque no tengo ningún recuerdo... Las cosas en las que pienso definitivamente son las mismas...", "Kirino"),
    36: ("...¿No soy Kirino Kousaka cuando he perdido mis recuerdos? Entonces, ¿qué clase de persona soy ante tus ojos?", "Kirino"),
    37: ("También me siento asustada cuando no tengo mis recuerdos...", "Kirino"),
    38: ("Ayúdame a pensar en una solución...", "Kirino"),
    43: ("*sniff sniff*...*sniff*...", "Kirino"),
    44: ("Kirino... Ya está bien.", "Kyousuke"),
    45: ("¿Eh?", "Kirino"),
    46: ("Yo... definitivamente encontraré una manera de ayudarte.", "Kyousuke"),
    47: ("*sniff*... Si no puedes hacerlo, tendrás que asumir la responsabilidad...", "Kirino"),
    48: ("...Por supuesto.", "Kyousuke"),
}

data = {
    "000scriptBKIR_0072A.obj": build(a72_n, a72_s),
    "000scriptBKIR_0075A.obj": build(a75_n, a75_s),
    "000scriptBKIR_0083T.obj": build(a83_n, a83_s),
    "000scriptBKIR_0085G.obj": build(a85_n, a85_s),
    "000scriptBKIR_0090A.obj": build(a90_n, a90_s),
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
