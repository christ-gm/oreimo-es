import json

PATH = "/mnt/c/Users/christ-gm/Desktop/code/oreimo/work/disc1/Data/Translation.json"

def build(narration: dict, speech: dict) -> dict:
    out = {}
    for i, t in narration.items():
        out[str(i)] = t
    for i, t in speech.items():
        out[str(i)] = "「" + t[0] + "」"
    return out

a23_n = {
    0: "Ruta de Kirino · Es Imposible Que Mi Hermanita Niega Su Afición Otaku",
    5: "...Estas palabras, siento como si las hubiera escuchado antes.",
    6: "Sin embargo, no he estado descuidando a mi hermanita últimamente. Más bien, es como si la estuviera molestando sin parar.",
    7: "...¿Qué es esta sensación extraña? Siento como si hubiera algo importante fuera de lugar entre la Kirino que recuerdo y su yo actual.",
    11: "...¿Por qué sacó su cuaderno?",
    13: "Dio básicamente los mismos detalles para el 12 y el 13...",
    14: "Saliendo con amigos de la escuela, actividades del club, ir al trabajo... Todo es solo una repetición de esto.",
    15: "Eso es solo natural. Después de todo, ese era el cuaderno de la modelo Kousaka Kirino...",
    16: "Por lo tanto, no habría nada sobre sus aficiones otaku escrito dentro.",
}
a23_s = {
    1: ("Oye, ¿te pasó algo mientras estaba en mi viaje escolar?", "Kyousuke"),
    2: ("¿Huh? ¿Por qué debo contarte sobre algo así?", "Kirino"),
    3: ("Aun así, todavía estoy preocupado por ti.", "Kyousuke"),
    4: ("¿Me has estado descuidando todo este tiempo y ahora intentas actuar como hermano mayor?", "Kirino"),
    8: ("Oye, si respondes mi pregunta, puedes denunciarme a la policía si quieres.", "Kyousuke"),
    9: ("Así que hablemos. Sobre lo que pasó mientras estaba en mi viaje escolar.", "Kyousuke"),
    10: ("...Entiendo. Te lo contaré ya que lo pusiste de esa manera.", "Kirino"),
    12: ("Déjame ver...11 de julio...Sí... Después de clases, cuando terminaron mis actividades del club...fui a la agencia de modelaje...", "Kirino"),
    17: ("Oye, déjame echar un vistazo a ese cuaderno.", "Kyousuke"),
    18: ("¿Q-Qué estás haciendo? Devuélvelo.", "Kirino"),
    19: ("Nunca dije que quisiera que leyeras tu agenda diaria. Solo pregunté si recuerdas lo que hiciste recientemente.", "Kyousuke"),
    20: ("Eso es...", "Kirino"),
    21: ("Oye, ¿no te reuniste con Kuroneko y Saori en absoluto?", "Kyousuke"),
}

a25_n = {
    0: "Ruta de Kirino · Es Imposible Que Mi Hermanita Niega Su Afición Otaku",
    27: "Pero esa persona de hecho existe.",
    48: "Esto....no es una broma.",
}
a25_s = {
    1: ("¿Kuroneko...?", "Kirino"),
    2: ("¿Hablas en serio? Los humanos no pueden hablar con gatos.", "Kirino"),
    3: ("N-No, ¡no es eso! ¡A lo que me refiero es a esa Lolita Gótica! ¡Nuestra amiga!", "Kyousuke"),
    4: ("¿Huh? ¿Amiga?", "Kirino"),
    5: ("Oye, incluso si no tienes muchos amigos humanos, ¿cómo puedes tratar a un gato como amigo? El gato seguramente estará en apuros.", "Kirino"),
    6: ("¡¿Estás idiota?!", "Kyousuke"),
    7: ("Además, para empezar, ¿cómo podrías comunicarte con animales?", "Kirino"),
    8: ("¿No es eso obvio? ¿De qué está llena tu cabeza? ¿Un campo de flores?", "Kyousuke"),
    9: ("¿N-No es eso lo que dijiste?", "Kirino"),
    10: ("Oye... Kuroneko es el nombre de usuario de tu amiga.", "Kyousuke"),
    11: ("Además, ¿cómo podrían hablar los gatos? ¿De verdad crees en algo así?", "Kyousuke"),
    12: ("Entonces, ¿quién es esa Kuroneko? ¡No tengo una amiga así!", "Kirino"),
    13: ("En cualquier caso, ¿podrías decir la verdad, en japonés?", "Kirino"),
    14: ("Tú también deberías ser honesta...", "Kyousuke"),
    15: ("¿Huh? ¡Estoy siendo extremadamente honesta!", "Kirino"),
    16: ("No te hagas la tonta. No has hecho más que esquivar mis preguntas desde el principio.", "Kyousuke"),
    17: ("¡D-Deja tus acusaciones falsas!", "Kirino"),
    18: ("¡Y-Yo estoy siendo honesto!", "Kyousuke"),
    19: ("¡¿Huh!? ¡¿Eso se considera honesto?!", "Kirino"),
    20: ("¿Tú, que solo te interesas en gatos y lentes?", "Kirino"),
    21: ("¡N-No trates a otros como si tuvieran intereses extraños!", "Kyousuke"),
    22: ("...Entiendo. Cambiemos de tema entonces. ¿Conoces a Saori? La que siempre dice 'gozaru, gozaru'.", "Kyousuke"),
    23: ("¿Huh? ¿'gozaru'? ¿Entonces tienes amigos que son ninjas o samuráis?", "Kirino"),
    24: ("¡No es una samurái! Vamos, es Saori, ¡la chica enorme con lentes en espiral!", "Kyousuke"),
    25: ("¡Eres tan persistente! ¡Nunca he visto a esa persona aparecer frente a mí ni una vez en mi vida!", "Kirino"),
    26: ("Más bien, no hay forma de que puedas encontrar a esa persona en cualquier lugar de Japón, ¿verdad?", "Kirino"),
    28: ("*suspiro*... Tú, cálmate un poco. ¿Cómo pudo nuestra conversación derivar al tema de los samuráis?", "Kyousuke"),
    29: ("Guh... es cierto...", "Kirino"),
    30: ("Actualmente estoy hablando de cosas sobre tus amigas. ¿Entiendes?", "Kyousuke"),
    31: ("¡¿C-Cómo sabría lo que pasa dentro de tu cabeza?!", "Kirino"),
    32: ("Tch... Tus delirios se han vuelto realmente severos, ¿lo sabes? ¿Debería hacer que consultes a un médico?", "Kirino"),
    33: ("¿Médico...?", "Kyousuke"),
    34: ("¡Sí, médico! Has estado diciendo cosas extrañas desde hace rato. ¿Te golpeaste la cabeza durante el viaje escolar?", "Kirino"),
    35: ("¡Oye, Kirino!", "Kyousuke"),
    36: ("¿Q-Qué? ¡No te acerques de repente a mí!", "Kirino"),
    37: ("Tú... ¿de verdad olvidaste todo sobre Saori y Kuroneko?", "Kyousuke"),
    38: ("Es todo una broma, ¿verdad?", "Kyousuke"),
    39: ("¿Cuántas veces debo repetirme? ¡Estoy completamente seria!", "Kirino"),
    40: ("Kirino...", "Kyousuke"),
    41: ("¿Q-Qué?", "Kirino"),
    42: ("...¡¿Podría ser...?!", "Kyousuke"),
    43: ("...? ¿Qué es esa cara de tonto?", "Kirino"),
    44: ("V-Volveré a preguntarte una vez más. ¿De verdad no conoces a Kuroneko ni a Saori?", "Kyousuke"),
    45: ("¡Eres realmente persistente! ¡Basta ya!!", "Kirino"),
    46: ("No importa cuánto jugaste en tu viaje escolar, ¿no es esto cruel? ¡Déjalo ya, idiota de Kioto!", "Kirino"),
    47: ("Si quieres ver ninjas o samuráis, ¿por qué no visitas el pueblo de cine de Uzumasa? Ah, y no tienes que volver después de eso.", "Kirino"),
    49: ("Kirino... ¡¿Podría ser que tú...?!", "Kyousuke"),
    50: ("...¿Qué? No me mires con ojos extraños así.", "Kirino"),
}

a27_n = {
    0: "Ruta de Kirino · Es Imposible Que Mi Hermanita Niega Su Afición Otaku",
    2: "Esa Kirino, parece irritada ahora...",
    3: "¿Debería decirle unas palabras?",
    4: "No, lo que me preocupa más es.....",
    5: "Son las palabras de Kirino sobre «no saber nada».",
    9: "¡¿Podría ser, podría ser, podría ser--?!",
    10: "Mamá dijo que podría ser su imaginación, pero no es broma.",
    11: "El comportamiento de Kirino es claramente diferente de lo usual.",
    12: "¡D-De todos modos, tengo que calmarme primero!",
    13: "Por el momento, parece que su actitud hacia la escuela, el club, el trabajo y nuestros padres no es diferente de lo usual.",
    14: "Pero por otro lado, cuando se trata de Meruru y todos los Galges que valora tanto, los rechaza firmemente.",
    15: "Además, no es que lo haga porque le avergüencen como en el pasado, sino que claramente muestra repulsión hacia ellos.",
    16: "....Poco a poco llegué a entender la situación.",
    17: "...¡Eso es!",
    20: "¿Hmm? Está en modo de espera. ¿Qué está pasando? ...Por ahora, la desbloquearé.",
    22: "...Como siempre, tenía un sonido de inicio completamente otaku. El escritorio está cubierto por completo con imágenes de Meruru...",
    28: "Seguramente pensará que fui yo quien instaló el tema de Meruru también...",
    29: "Bueno, eso no importa. En cualquier caso, ¿qué otras pistas tengo...? ¿Hmm?",
    34: "Ella... Ella de hecho está diciendo algo así.",
    35: "...Sin embargo, basado en los registros de chat que veo, parece que todavía tuvieron contacto ayer.",
}
a27_s = {
    1: ("Dios mío... ¿qué rayos está pasando?", "Kirino"),
    6: ("Perdón. No intento confundirte.", "Kyousuke"),
    7: ("Pero, déjame confirmarlo una vez más. ¿De verdad no conoces a Kuroneko y Saori?", "Kyousuke"),
    8: ("...No las conozco.", "Kirino"),
    18: ("Préstame tu laptop por un momento.", "Kyousuke"),
    19: ("¡Oye! ¡¿Qué estás haciendo?!", "Kirino"),
    21: ("¡Stardust ☆ Witch Meruru! Comenzando ahora----♪", "Meruru"),
    23: ("¡T-Tú, qué le has hecho a mi laptop?!", "Kirino"),
    24: ("...Tú misma lo dijiste antes, ¿no? Que estabas cambiando el sonido del sistema de la laptop por la canción que hiciste.", "Kyousuke"),
    25: ("¿Huh, la canción que hice?", "Kirino"),
    26: ("Sí, me hiciste escucharla antes de que me fuera a mi viaje escolar, ¿recuerdas? Es la canción denpa de la que presumías.", "Kyousuke"),
    27: ("¡No sé nada de ninguna cosa denpa! ¡Apúrate y aléjate de mi computadora!", "Kirino"),
    30: ("La ventana de chat sigue abierta. Registros de conversación de ayer, las otras partes... Kuroneko y Saori.", "Kyousuke"),
    31: ("Como dije, no conozco a esas personas.", "Kirino"),
    32: ("Pero mira, hay registros dejados en la computadora, ¿no?", "Kyousuke"),
    33: ("Eso es solo basura.", "Kirino"),
}

a28_n = {
    0: "Ruta de Kirino · Es Imposible Que Mi Hermanita Pueda Ir «Haaah, Haaah»",
    4: "¡Mi región inferior...!!",
    8: "Después de mirar esta foto, estoy seguro de que Kirino...",
    14: "¡Nada bien! ¡¿Salió mal?!",
}
a28_s = {
    1: ("¡Oh! ¡¿Esto es?!", "Kyousuke"),
    2: ("¡P-P-P-Para ya! ¡Pervertido!", "Kirino"),
    3: ("¡Guh!", "Kyousuke"),
    5: ("Tú... Una chica de secundaria haciendo algo así...", "Kyousuke"),
    6: ("¡Devuélveme mi computadora de inmediato!", "Kirino"),
    7: ("¡E-Espera! ¡Mira a esta persona!", "Kyousuke"),
    9: ("¡¿Q-Qu...Qué es esto?! ¡Policía～～! ¡Hay un pervertido aquí!", "Kirino"),
    10: ("No, ¿qué «pervertido», no es esta tu afici- eh?! ¡Esto es!", "Kyousuke"),
    11: ("...Haciéndome mirar mi propia foto de traje de baño... ¿qué estás intentando hacer?", "Kirino"),
    12: ("A-Acerca de eso... te ves realmente saludable, ¿no es genial?", "Kyousuke"),
    13: ("Je, jejejeje... ¿Estás intentando halagarme?", "Kirino"),
    15: ("Emocionándote mostrándole a tu hermanita su propia foto de traje de baño... Ese es un lindo interés que tienes...", "Kirino"),
    16: ("¡E-Esto es un malentendido! ¡Solo estoy intentando mostrarte las fotos de «Sis×Sis»!", "Kyousuke"),
    17: ("¿Huh? ¿SisXSis?", "Kirino"),
    18: ("Para ser exactos, el juego «Sister×Sister: Historia de Amor Siscon»...", "Kyousuke"),
    19: ("¡¡Pervertido enorme!!", "Kirino"),
}

a29_n = {
    0: "Ruta de Kirino · ¡¿Mi Hermanita Ha Perdido La Memoria?!",
    1: "Dijo que la Meruru Edición Regional era asquerosa y se negó a aceptarla. Iba a simplemente tirar sus artículos otaku anteriores.",
    2: "Además... incluso olvidó a sus buenas amigas, Kuroneko y Saori...",
    3: "Pero por otro lado, todavía podía recordar cosas relacionadas con la familia y la escuela sin problemas.",
    4: "Y por supuesto, parece recordarme... En otras palabras, que soy el hijo mayor de la familia Kousaka.",
    5: "En resumen, ahora mismo, esta chica...",
    12: "No estoy particularmente preocupado en absoluto.",
    13: "Después de todo, ¿qué tiene que ver esto conmigo?",
    14: "Para empezar, la razón por la que mi vida diaria normal ha sido interrumpida es originalmente por los intereses otaku de mi hermanita, así que ¿no volverá todo",
    15: "a ser como el año pasado si se van?",
    17: "...Sin embargo, ¿cómo se sentirían Kuroneko y Saori si supieran que Kirino las olvidó?",
    18: "Después de todo, su buena amiga Kirino se ha convertido en una chica normal de secundaria que ahora tiene prejuicios contra los otaku.",
    19: "Si Kirino dice seriamente «asqueroso» con sentimientos desagradables a diferencia de su banter normal de hasta ahora, ¿no hará eso llorar a Kuroneko?",
    20: "Además... mi relación con Kirino también volverá a lo que era hace un año.",
    21: "Los recuerdos de Kirino relacionados con el otaku, y en el centro de ellos, sus recuerdos conmigo también se han ido...",
    24: "Lo diré primero, estoy haciendo esto por el bien de Kuroneko y Saori, y absolutamente no es porque esté solo ni nada.",
    33: "Incluso yo, si me dijeran «¡Tu interés son los juegos BL!» un día, gastaría toda mi energía negándolo.",
    34: "Probablemente agradecería a los dioses por permitirme perder la memoria en su lugar.",
    48: "Es la misma hermanita arrogante e irritante de siempre, pero todo esto es por el bien de Kuroneko y Saori.",
    49: "Solo lo soportaré por un tiempo.",
    50: "--Sujeté el brazo de la Kirino que se resistía detrás de su espalda--aunque realmente no quería hacer esto--y la llevé al hospital.",
    51: "Por supuesto, logré que Papá nos acompañara también.",
    52: "Como excusa, dije que Kirino se había golpeado la cabeza y que debería ir al hospital solo para estar seguros.",
    53: "Y el resultado del examen fue... sin problemas.",
    54: "En otras palabras, no había nada malo físicamente. El médico también dijo amablemente que es temporal...",
    55: "Kirino entonces dio el discurso de «mira lo que hiciste» y me maldijo, pero mi inquietud no se calmó.",
    56: "¿Cómo podría recuperar sus recuerdos en este tipo de situación...? Esta inquietante pregunta quedó rondando en mi corazón en su lugar.",
}
a29_s = {
    6: ("...ha olvidado por completo solo sus recuerdos relacionados con el otaku.", "Kyousuke"),
    7: ("¿Huh?", "Kirino"),
    8: ("Lo que quiere decir, algún tipo de pérdida de memoria--¿es eso?", "Kyousuke"),
    9: ("¡¿Q-Qu...Qué clase de cosas inútiles estás diciendo?! Basta, sal.", "Kirino"),
    10: ("Convocándome a tu habitación cuando quieras, y luego de repente echándome...", "Kyousuke"),
    11: ("...Sin embargo, hacer que solo desaparezcan los recuerdos relacionados con el otaku, esta pérdida de memoria es bastante conveniente.", "Kyousuke"),
    16: ("......", "Kyousuke"),
    22: ("...Tch, en serio... ¿por qué se volvió un asunto tan problemático?", "Kyousuke"),
    23: ("...Realmente me toca a mí hacer algo ahora.", "Kyousuke"),
    25: ("Oye, Kirino, ¿estás escuchando? Básicamente esto es lo que estás pensando.", "Kyousuke"),
    26: ("Todo lo que estoy diciendo son mentiras. Los artículos otaku en tu habitación y las cosas en tu computadora son todo obra mía.", "Kyousuke"),
    27: ("Sin embargo, ¿qué pasaría si todo lo que digo es completamente cierto...? ¿Qué harás?", "Kyousuke"),
    28: ("Para tu información, tus intereses otaku ya han sido aceptados por Mamá y Papá. Si quieres, puedes confirmarlo con ellos también.", "Kyousuke"),
    29: ("......", "Kirino"),
    30: ("Así que finalmente decidiste salir.", "Kyousuke"),
    31: ("...Es incómodo que me digan que cosas que no conozco son mías.", "Kirino"),
    32: ("Bueno, es cierto.", "Kyousuke"),
    35: ("Sin embargo, después de escuchar tus palabras, me siento un poco confundida... Yo misma ya no sé qué está pasando.", "Kirino"),
    36: ("Eso es comprensible.", "Kyousuke"),
    37: ("¿Por qué hablas como si supieras algo?", "Kirino"),
    38: ("Es todo tu culpa...... Piensa en una solución.", "Kirino"),
    39: ("Hmph, déjamelo a mí. Ya sé lo que necesita hacerse.", "Kyousuke"),
    40: ("...Kirino, vamos al hospital ahora mismo.", "Kyousuke"),
    41: ("¿P-Por qué tuviste que patearme?", "Kyousuke"),
    42: ("¡¿Quieres consultar a un médico sobre lo que hay dentro de tu cerebro?!", "Kirino"),
    43: ("No, en caso de pérdida de memoria, ¿no es un hecho ir al hospital?", "Kyousuke"),
    44: ("Todavía no admitiré que he perdido la memoria. Pero ya que eres tan persistente, te permití pensar en una solución.", "Kirino"),
    45: ("Perderás a tus amigas si eres tan autoritaria. Como mínimo, solo sé así frente a mí. ¿Está bien?", "Kyousuke"),
    46: ("...No deseo que me lo diga alguien que no tiene amigos.", "Kirino"),
    47: ("¡Sí los tengo! ¡Sí tengo amigos!", "Kyousuke"),
}

data = {
    "000scriptBKIR_0023A.obj": build(a23_n, a23_s),
    "000scriptBKIR_0025T.obj": build(a25_n, a25_s),
    "000scriptBKIR_0027A.obj": build(a27_n, a27_s),
    "000scriptBKIR_0028G.obj": build(a28_n, a28_s),
    "000scriptBKIR_0029A.obj": build(a29_n, a29_s),
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