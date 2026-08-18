import json

PATH = "/mnt/c/Users/christ-gm/Desktop/code/oreimo/work/disc1/Data/Translation.json"

def build(narration, speech):
    out = {}
    for i, t in narration.items():
        out[str(i)] = t
    for i, t in speech.items():
        out[str(i)] = "「" + t[0] + "」"
    return out

a0000_n = {
    0: "Ruta de Kuroneko · Ofrenda Para Kuroneko",
    1: "Cuando el viaje terminó en paz, finalmente volvimos a nuestro querido pueblo.",
    10: "Es un recuerdo que ella pidió, aunque tenía la intención de comprarlo incluso si no lo hubiera pedido.",
    14: "Suena extrañamente embarazoso cuando ella lo dice...",
    26: "Pero, para ser honesto... en realidad no sé tanto sobre Kuroneko.",
    27: "¿Estuvo... bien comprar este recuerdo?",
    28: "Bueno, no es como si pudiera hacer algo al respecto ahora.",
}
a0000_s = {
    2: ("Kyou-chan, de verdad compraste muchos recuerdos.", "Manami"),
    3: ("Sí, si no los traía, no sé cómo me trataría mi madre.", "Kyousuke"),
    4: ("Entonces, ¿esos recuerdos son para tu familia?", "Manami"),
    5: ("Sí. También compré algunos para Kuroneko.", "Kyousuke"),
    6: ("Te llevas bien con Kuroneko-san.", "Manami"),
    7: ("No es eso, es solo que le di algunos problemas antes del viaje...", "Kyousuke"),
    8: ("¿Problemas?", "Manami"),
    9: ("Formamos equipo durante el torneo de juegos y Kuroneko me ayudó de verdad.", "Kyousuke"),
    11: ("No es una muy buena disculpa. Pero, bueno...", "Kyousuke"),
    12: ("Ya veo... Es porque Kuroneko-san es una 【Kohai Linda】.", "Manami"),
    13: ("¡Guh! «Linda...»", "Kyousuke"),
    15: ("Bueno, ciertamente es del tipo que llama la atención.", "Kyousuke"),
    16: ("Tiene algunas cualidades sorprendentemente buenas si la miras de cerca.", "Kyousuke"),
    17: ("Ehehe, Kyou-chan es un buen senpai que se preocupa por todo.", "Manami"),
    18: ("Cállate.", "Kyousuke"),
    19: ("Un artículo relacionado con Abe no Seimei, huh....", "Kyousuke"),
    20: ("Ah Kyou-chan, compraste un pentagrama.", "Manami"),
    21: ("Porque dijo que los estaba coleccionando.", "Kyousuke"),
    22: ("Como se esperaba de Kyou-chan. De verdad entiendes a Kuroneko-san.", "Manami"),
    23: ("Eso no es verdad.", "Kyousuke"),
    24: ("No tienes que avergonzarte～", "Manami"),
    25: ("...¡No lo estoy!", "Kyousuke"),
    29: ("Entonces, nos vemos, Kyou-chan.", "Manami"),
    30: ("Sí.", "Kyousuke"),
    31: ("Sería bueno si a Kuroneko-san le gusta el recuerdo.", "Manami"),
    32: ("...Sí. Bueno entonces, nos vemos mañana.", "Kyousuke"),
    33: ("¡Sí! Nos vemos mañana.", "Manami"),
}

a0001_n = {
    0: "Ruta de Kuroneko · Ofrenda Para Kuroneko",
    2: "Ya no puedo más... Tengo sueño...",
    3: "Espera, eso me recuerda...",
    4: "Me tomé la molestia de comprar ese recuerdo. ¿Debería llamar a Kuroneko para avisarle?",
    9: "¿Debería decir algo? Pero, me encontraré con ella mañana en la escuela de todos modos.",
    10: "No es como si cargar ese pentagrama fuera una molestia...",
    13: "Pero esto se considera cortesía, ¿no? No hay forma de evitarlo, démosle un mensaje.",
    18: "Eso debería bastar.",
    19: "Dejar un mensaje es como que... embarazoso.",
    25: "Contestar mi monólogo con un mensaje... eres buena.",
    26: "...Probablemente está cocinando.",
    27: "Inicialmente planeaba dormir...",
    28: "Pero fui despertado inmediatamente a patadas por Kirino, insistiéndome que le diera los recuerdos en vez de quedarme dormitando...",
    29: "Bueno, eso realmente me hizo sentir que por fin estoy de vuelta en casa.",
}
a0001_s = {
    1: ("Estoy agotado...", "Kyousuke"),
    5: ("¡De acuerdo! Ya que está decidido, la llamaré de inmediato.", "Kyousuke"),
    6: ("En este momento no puedo contestar tu llamada...", "Speakers"),
    7: ("Contestadora, huh...", "Kyousuke"),
    8: ("Para dejar un mensaje, por favor grábate después del 'BEEP'...", "Speakers"),
    11: ("Bueno, como sea.", "Kyousuke"),
    12: ("Ya que podemos vernos en la escuela mañana, se lo daré entonces.", "Kyousuke"),
    14: ("Eeehm, es Kyousuke...", "Kyousuke"),
    15: ("*tose* Ah, el recuerdo del que hablamos, ya sabes, lo de Abe no Seimei. Lo compré.", "Kyousuke"),
    16: ("¿Cuándo debería dártelo? Por favor contáctame pronto.", "Kyousuke"),
    17: ("Eeehm... Bueno, eso es todo.", "Kyousuke"),
    20: ("...¿Un mensaje?", "Kyousuke"),
    21: ("Cuando nos veamos.", "Kuroneko"),
    22: ("¡Qué rápido-- Esa chica, si estás en casa, ¡entonces contesta el teléfono!", "Kyousuke"),
    23: ("Estoy en medio de algo ahora mismo.", "Kuroneko"),
    24: ("Entendido, entendido.", "Kyousuke"),
}

a0010_n = {
    0: "Ruta de Kuroneko · Ofrenda Para Kuroneko",
    7: "Bueno... solo un poco.",
    8: "Pero, desde ese asunto de la 'maldición'... la actitud de Kuroneko hacia mí no ha cambiado en absoluto.",
    9: "Por supuesto, tampoco es como si me hubieran confesado.",
    10: "Más bien, se siente como si estuviera más fría que antes.",
    11: "Es igual que una gata. No entiendo lo que tiene en mente.",
    26: "Estoy empezando a comportarme como mi hermanita...",
    34: "Aa-aa-h, Kuroneko ya se fue...",
}
a0010_s = {
    1: ("Entonces, al final, ¿no pudiste hablar con Kuroneko ayer por teléfono?", "Manami"),
    2: ("Sí. No soy bueno dejando mensajes de voz, así que me puse un poco nervioso.", "Kyousuke"),
    3: ("¿No estaría Kuroneko-san también decepcionada? ¿No ha pasado un tiempo desde que la llamaste por última vez?", "Manami"),
    4: ("Por cómo lo dices, es como si estuviera saliendo con Kuroneko.", "Kyousuke"),
    5: ("Pensé que te había dicho en Kioto que no es así.", "Kyousuke"),
    6: ("Aun así, estás preocupado por ella, ¿no?", "Manami"),
    12: ("Ah, hablando del rey de Roma.", "Manami"),
    13: ("¿Hmm?", "Kyousuke"),
    14: ("¿Esa era... Kuroneko?", "Kyousuke"),
    15: ("Ah, se fue... ¿No nos escuchó?", "Manami"),
    16: ("Sí, probablemente. No es sorprendente que no nos haya escuchado con tanta gente alrededor.", "Kyousuke"),
    17: ("Hmm, entonces ¿por qué no intentas llamarla una vez más?", "Manami"),
    18: ("Supongo que sí.", "Kyousuke"),
    19: ("¡¡Oye～～～～!!", "Kyousuke"),
    20: ("¿Me llamaste, colega?", "Akagi"),
    21: ("No.", "Kyousuke"),
    22: ("Ah, Akagi-kun, buenos días.", "Manami"),
    23: ("Buenos días, Tamura-san.", "Akagi"),
    24: ("Estás estorbando, lárgate.", "Kyousuke"),
    25: ("Ya, ya, ¿quién diría 'Estás estorbando, lárgate'? Veo que sigues siendo tan frío como siempre con los chicos.", "Akagi"),
    27: ("Estoy ocupado ahora mismo, ¿necesitas algo?", "Kyousuke"),
    28: ("Jeh, entonces me viste venir. De hecho, mi hermana...", "Akagi"),
    29: ("Eso no importa ahora mismo, hablaremos de eso después.", "Kyousuke"),
    30: ("¡¿Qué quieres decir con que ella no importa?!", "Akagi"),
    31: ("¡No estoy diciendo que tu hermana no importe! ¡Estoy diciendo que no tengo tiempo para escuchar a un siscon como tú hablar de su hermana!", "Kyousuke"),
    32: ("¿Qué, ¿eso era? Deberías haberlo dicho antes.", "Akagi"),
    33: ("¡Eres una molestia! Ah, mira...", "Kyousuke"),
    35: ("Ah-, ¿estaba estorbando en algo?", "Akagi"),
    36: ("Dios... como sea.", "Kyousuke"),
    37: ("¡Lo siento!", "Akagi"),
    38: ("¡No vengas aquí! ¡Eres demasiado pegajoso!", "Kyousuke"),
    39: ("Ahaha. Ustedes dos se llevan tan bien～", "Manami"),
    40: ("Estoy un poco envidiosa.", "Manami"),
    41: ("No bromees sobre esto... Se sospecha que este tipo es un homo furioso.", "Kyousuke"),
    42: ("Vaya, vaya, ¿de quién escuchaste este rumor sin fundamento?", "Akagi"),
    43: (".........", "Kyousuke"),
    44: ("De tu hermana.", "Kyousuke"),
}

a0020_n = {
    0: "Ruta de Kuroneko · El Sartén Y El Pescado",
    1: "--Hora del almuerzo.",
    2: "No pude hablar con Kuroneko en la mañana por culpa de ese idiota.",
    3: "Intentaré ir a los salones de los de primer año para encontrarme con ella.",
    10: "Ugh... Esto es incómodo...",
    19: "Sigue igual de fría, ya veo...",
}
a0020_s = {
    4: ("Ah...", "Kuroneko"),
    5: ("...Oye.", "Kyousuke"),
    6: ("Ah... Um...", "Kuroneko"),
    7: ("¿Te pasa algo?", "Kyousuke"),
    8: ("N-No. No es nada.", "Kuroneko"),
    9: ("Y-Ya veo.", "Kyousuke"),
    11: ("U-Um... Ah, cierto, anoche cuando te llamé, me mandaste un mensaje diciendo que estabas en medio de algo. ¿Qué estabas haciendo?", "Kyousuke"),
    12: ("...Estaba friendo pescado en el sartén.", "Kuroneko"),
    13: ("Oh, lo adiviné correctamente.", "Kyousuke"),
    14: ("...¿Eh?", "Kuroneko"),
    15: ("Estaba pensando si era algo así.", "Kyousuke"),
    16: ("Y, ya veo.", "Kuroneko"),
    17: ("Um...", "Kuroneko"),
    18: ("...¿Necesitas algo?", "Kuroneko"),
    20: ("¿Por qué no almorzamos juntos?", "Kyousuke"),
    21: ("...Um... lo siento, ya hice planes....", "Kuroneko"),
    22: ("Ya veo. Nos vemos entonces.", "Kyousuke"),
}

a0030_n = {
    0: "Ruta de Kuroneko · El Sartén Y El Pescado",
    1: "Y así, de camino a casa después de la escuela.",
}
a0030_s = {
    2: ("Kyou-chan, ¿le diste ese recuerdo a Kuroneko-san?", "Manami"),
    3: ("Todavía no.", "Kyousuke"),
    4: ("Dios, eso no servirá. Las vacaciones empiezan mañana, ¿sabes?", "Manami"),
    5: ("Me pregunto si suele pasar por aquí...", "Kyousuke"),
    6: ("Ah... Kyou-chan, ahí está, ¡Kuroneko-san!", "Manami"),
    7: ("Mira, allá. Está un poco lejos pero esa es Kuroneko-san, ¿no?", "Manami"),
    8: ("Oh, tienes razón.", "Kyousuke"),
    9: ("Ve, Kyou-chan.", "Manami"),
    10: ("Y-Ya voy.", "Kyousuke"),
    11: ("¡Oye～, Kuroneko!", "Kyousuke"),
    12: ("...¿Senpai?", "Kuroneko"),
    13: ("*jadeando*... Hola.", "Kyousuke"),
    14: ("...¿Estabas yendo fuera de tu camino para correr detrás de mí?", "Kuroneko"),
    15: ("Bueno, sí.", "Kyousuke"),
    16: ("Y-Ya veo...", "Kuroneko"),
    17: ("Entonces, ¿qué es lo que necesitas de mí?", "Kuroneko"),
}

data = {
    "000scriptCKUR_0000A.obj": build(a0000_n, a0000_s),
    "000scriptCKUR_0001A.obj": build(a0001_n, a0001_s),
    "000scriptCKUR_0010A.obj": build(a0010_n, a0010_s),
    "000scriptCKUR_0020A.obj": build(a0020_n, a0020_s),
    "000scriptCKUR_0030A.obj": build(a0030_n, a0030_s),
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
