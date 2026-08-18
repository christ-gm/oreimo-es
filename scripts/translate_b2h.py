import json

PATH = "/mnt/c/Users/christ-gm/Desktop/code/oreimo/work/disc1/Data/Translation.json"

def build(narration, speech):
    out = {}
    for i, t in narration.items():
        out[str(i)] = t
    for i, t in speech.items():
        out[str(i)] = "「" + t[0] + "」"
    return out

a100_n = {
    0: "Ruta de Kirino · Es Imposible Que Mi Hermanita No Escuche A Su Mejor Amiga",
    7: "Ahh, recordé lo que pasó hace un año...",
    8: "Arreglé las cosas entre Kirino, a quien le expusieron sus aficiones otaku, y Ayase. Sin embargo, yo fui el único tratado como criminal, y mi",
    9: "número de teléfono fue bloqueado por Ayase...",
    11: "Me eché la culpa por tu bien... Pero eso ya no importa.",
    14: "...Como nota al margen, Kirino me prohibió contarle a Ayase sobre su pérdida de memoria.",
    15: "Bueno, estoy de acuerdo con ella desde mi perspectiva.",
    16: "Eso es porque Ayase odia las aficiones otaku de Kirino. Si se enterara de que la Kirino actual ha olvidado eso, definitivamente hará todo lo posible por",
    17: "evitar que recupere sus recuerdos.",
    22: "¡¿C-Cuándo se movió Ayase detrás de Kirino?! ¡Y además, está poniendo su cara muy cerca de Kirino!!",
    29: "Así que todavía me trata con hostilidad como de costumbre...",
    32: "...S-Solo está dispuesta a hablar al fin. *suspiro* Qué agotador.",
    33: "En cualquier caso, la alegría de Kirino cuando recibió la figura de Meruru EX fue realmente memorable.",
}
a100_s = {
    1: ("...Por eso, por favor recuérdale la vez que le dimos la figura de Meruru EX como regalo.", "Kyousuke"),
    2: ("¿Qué pasa con el «Por eso»? Ni siquiera he escuchado ninguna explicación todavía...", "Ayase"),
    3: ("Tch, como era de esperar de una heroína secreta, no te dejarás llevar fácilmente por mí.", "Kyousuke"),
    4: ("¡¿Q-Quién es una heroína secreta!", "Ayase"),
    5: ("Dios... ¿Quieres que bloquee tu número de teléfono otra vez?", "Ayase"),
    6: ("Por supuesto que no. Fue mi culpa.", "Kyousuke"),
    10: ("Oye, ¿por qué se te están llenando los ojos de lágrimas?", "Kirino"),
    12: ("Dios mío...", "Ayase"),
    13: ("Entonces, ¿qué tal si me dejas escuchar tu explicación? Ya le conté a Kirino sobre el incidente de Meruru EX.", "Ayase"),
    18: ("Ahh, en realidad, parece que Kirino ha olvidado por completo ese asunto...", "Kyousuke"),
    19: ("......¿Eh?", "Ayase"),
    20: ("Mentiras... Algo como olvidar mi regalo para ti... Es una mentira, ¿no?", "Ayase"),
    21: ("Uh, bueno... eso es...", "Kirino"),
    23: ("¡T-Tú...! ¡Di algo!", "Kirino"),
    24: ("¡N-No! ¡Salió mal!", "Kyousuke"),
    25: ("E-En realidad, es Kirino. No cree que yo co-operé contigo al elegir la figura de Meruru EX como regalo.", "Kyousuke"),
    26: ("Qué, así que es así.", "Ayase"),
    27: ("Por supuesto, Onii-san está mintiendo. Elegí Meruru EX por mi cuenta, y se la di a Kirino como regalo.", "Ayase"),
    28: ("¡¡No difundas tales tonterías!!", "Kyousuke"),
    30: ("Ayase, tengo una petición. ¿Puedes contarme sobre ello, por favor?", "Kirino"),
    31: ("...*suspiro*... Una petición de Onii-san es una cosa, pero si es una petición de Kirino...", "Ayase"),
}

a101_n = {
    0: "Ruta de Kirino · Es Imposible Que Mi Hermanita No Escuche A Su Mejor Amiga - G",
    10: "Así es, y esa era el premio del campeonato «figura de Meruru EX de edición limitada» del torneo de cosplay.",
    13: "Fue realmente un momento aterrador para mí en ese entonces...",
    14: "Después de escuchar mi consejo, Ayase decidió participar en la competencia de cosplay para ganar esa figura de Meruru EX de edición limitada. Sin embargo, no",
    15: "se unió personalmente a la competencia...",
    16: "Le pidió a una compañera de clase llamada Kanako que se parecía exactamente a Meruru que participara en su lugar.",
    17: "Al final, reclamó con éxito el campeonato...",
    19: "Y así fue como pasó.",
    20: "Sin embargo, hay algo importante que Ayase no mencionó.",
    32: "...Oye, Kirino.",
    33: "Si golpeas a otros basándote en sentimientos, no creo que la humanidad tenga futuro ya.",
}
a101_s = {
    1: ("Oye, Kirino. Sobre eso... Todo empezó cuando consulté con Onii-san sobre qué regalarte por haber participado en el torneo de atletismo.", "Ayase"),
    2: ("¿Con este tipo? ¿Por qué?", "Kirino"),
    3: ("¿Eh...? E-Eso es...", "Ayase"),
    4: ("Si es Onii-san, estoy segura de que sabe lo que le gusta a Kirino... y lo que Kirino realmente desea más... Eso es lo que pensé.", "Ayase"),
    5: ("...H-Hmmm.", "Kirino"),
    6: ("Oye Kirino, no digas demasiado. Te expondrás.", "Kyousuke"),
    7: ("...Entiendo. Sin embargo, tendrás que explicarme las cosas después. ¿Por qué Ayase...", "Kirino"),
    8: ("Hmm, ¿dónde estaba?", "Ayase"),
    9: ("Cierto cierto, hice que Onii-san me ayudara a buscar la «cosa que Kirino realmente desea más ahora mismo».", "Ayase"),
    11: ("¿No es esto prácticamente desnudo, miiiiiiiiue--!!", "Ayase"),
    12: ("¡Definitivamente no usaré ropa tan lasciva!", "Ayase"),
    18: ("...Y así, pudo obtener la figura del gran premio.", "Ayase"),
    21: ("Ayase, habla de eso también. Sobre cómo Kirino estaba entre el público en la competencia de cosplay.", "Kyousuke"),
    22: ("¿Eh...eso...también?", "Ayase"),
    23: ("Está bien. A Kirino no le importa que la hayas visto en ese entonces. ¿Cierto, Kirino?", "Kyousuke"),
    24: ("...? S-Sí, supongo...", "Kirino"),
    25: ("Aunque siento que hay un problema con eso también...", "Ayase"),
    26: ("Uhh, Kirino en ese momento estaba...", "Ayase"),
    27: ("¡Yahoo! Ku-ra-ra! Ku-ra-ra! ¡Yeah yeah yeah yeah!", "Kirino"),
    28: ("¡No digas cosas tan estúpidas!", "Kirino"),
    29: ("¡Guwah!", "Kyousuke"),
    30: ("¡¿P-Por qué me pateaste?!", "Kyousuke"),
    31: ("¡Solo me dieron ganas por alguna razón!", "Kirino"),
    34: ("¡¿En realidad usé un abrigo hanten rosa y bailé junto con otakus asquerosos mientras agitaba una luz y un abanico?!", "Kirino"),
    35: ("¡Eso es lo más increíble de todas las cosas que me han dicho hasta ahora!", "Kirino"),
    36: ("¡Oye, Ayase! ¡Todo esto son mentiras, verdad!? ¡Dime que son mentiras!", "Kirino"),
    37: ("Bueno, eso es... Yo tampoco lo creí yo misma... Sin embargo, cuando realmente lo vi...", "Ayase"),
    38: ("Guh... C-Cómo pudo ser esto...", "Kirino"),
}

a102_n = {
    0: "Ruta de Kirino · Es Imposible Que Mi Hermanita No Escuche A Su Mejor Amiga",
    1: "Así que esto tampoco funcionó... Todo fue bien hasta que empezó a hablar con Ayase.",
    2: "Sin embargo, por no hablar de recuperar sus recuerdos, Kirino prácticamente se estaba desmayando de agonía al enterarse de su episodio súper otaku...",
    7: "E-El ambiente se siente peligroso de alguna manera...",
    8: "Ahora mismo, es mejor retroceder antes de que terminemos siendo descubiertos por Ayase.",
    17: "¿Qué debería hacer? ¿Debería esconderlo? ¿O debería revelarlo? ¿O debería confesarle mi amor?",
    18: "No, hay vidas en juego. Necesito considerarlo seriamente.",
    26: "¿P-Por qué está pasando esto? Nuestros meñiques están entrelazados ahora mismo... sin embargo, mi corazón no está revoloteando por ello en absoluto.",
    28: "...Habla en serio. Esta persona realmente hará eso.",
    30: "...Así es, ya que ha olvidado sus aficiones otaku, sus recuerdos de Ayase volviéndose salvaje también se han ido.",
}
a102_s = {
    3: ("Oye, Onii-san, ¿qué le pasa a Kirino? Dijiste que a Kirino no le importaría, ¿no?", "Ayase"),
    4: ("No, bueno, Kirino está toda avergonzada después de escuchar a Ayase hablar de ese incidente otra vez, ¿cierto, Kirino?", "Kyousuke"),
    5: ("Cállate... ¿quieres que te cose esa boca?", "Kirino"),
    6: ("......", "Ayase"),
    9: ("E-Entonces... Perdón por haberte molestado. Bueno, hay algo más que tenemos que atender, así que...", "Kyousuke"),
    10: ("Oye, Onii-san...", "Ayase"),
    11: ("¿Estás escondiendo... algo de mí otra vez?", "Ayase"),
    12: ("...¿Eh?", "Kyousuke"),
    13: ("¿A-Ayase...san? ...Me alegra que me toques, jaja... Pero tus uñas se están clavando en mi brazo, ¿sabes?", "Kyousuke"),
    14: ("A-Además de eso, ¿por qué parece que tus ojos han perdido su brillo...", "Kyousuke"),
    15: ("Respóndeme honestamente, ¿de acuerdo? A los mentirosos les extraerán la lengua el Rey del Inframundo, ¿no es así, Kirino?", "Ayase"),
    16: ("Eh, s-sí, supongo.", "Kirino"),
    19: ("E-Es cierto que te estoy escondiendo algo.", "Kyousuke"),
    20: ("Como pensé...", "Ayase"),
    21: ("Sin embargo, debido a varias razones, no puedo decirte nada ahora mismo. En un rato, en solo un ratito, ¡te contaré todo!", "Kyousuke"),
    22: ("...¿Lo... prometes?", "Ayase"),
    23: ("Entendido, ¡lo prometo, lo prometo!", "Kyousuke"),
    24: ("...Entonces, hazlo una promesa con el meñique.", "Ayase"),
    25: ("D-De acuerdo.", "Kyousuke"),
    27: ("Si estás mintiendo, tendrás que tragar mil agujas, atar trozos de plomo a tus piernas, y hundirte en la Bahía de Tokio imitando la natación sincronizada.", "Ayase"),
    29: ("¿Q-Qué está pasando? Ayase está actuando de alguna manera diferente a lo habitual...?", "Kirino"),
    31: ("N-No mires atrás. Estaremos acabados si descubre nuestra debilidad.", "Kyousuke"),
}

a103_n = {
    0: "Ruta de Kirino · Es Imposible Que Mi Hermanita No Escuche A Su Mejor Amiga",
    1: "Uf... Finalmente controlamos a Ayase, pero ya es de noche.",
    50: "N-No puedo encontrar palabras para una respuesta tan lastimera...",
}
a103_s = {
    2: ("...Entonces, déjame ser clara, ¿por qué estás tú y Ayase en buenos términos?", "Kirino"),
    3: ("...¿Dónde exactamente nos viste en buenos términos ahí?", "Kyousuke"),
    4: ("Tch... tan molesto...", "Kirino"),
    5: ("¿Acabas de decir algo?", "Kyousuke"),
    6: ("...En realidad no.", "Kirino"),
    7: ("Bueno entonces, ¿has recordado algo? Ayase trabajó extremadamente duro por el bien de obtener esa figura, ¿sabes?", "Kyousuke"),
    8: ("...No puedo recordar nada en absoluto. ¿Qué era ese evento de Meruru que mencionaste antes? ¿No es simplemente estúpido?", "Kirino"),
    9: ("¡Ya te dije que tú también estabas ahí!", "Kyousuke"),
    10: ("Uuu... Aaaaah... E-Eso es imposible...", "Kirino"),
    11: ("Bueno, de hecho no hay otra palabra para describirte en ese entonces excepto «estúpida»...", "Kyousuke"),
    12: ("No me llames estúpida.", "Kirino"),
    13: ("N-No, eso es lo que dijiste tú misma...", "Kyousuke"),
    14: ("Incluso si ese es el caso, es irritante viniendo de ti.", "Kirino"),
    15: ("...Eso es bastante duro.", "Kyousuke"),
    16: ("¡E-Eso es mentira! ¡No hay razón para que yo me vuelva loca por ese tipo de evento!", "Kirino"),
    17: ("¡No, estás demasiado emocionada ahora mismo también!", "Kyousuke"),
    18: ("D-De todos modos, ¡cálmate! Vamos, respira profundamente.", "Kyousuke"),
    19: ("Hu...ja... Hu...ja...", "Kirino"),
    20: ("N-No puedo hacerlo. No puedo calmarme en absoluto...", "Kirino"),
    21: ("Kirino, el pasado no puede cambiarse. Es un obstáculo que no puede superarse.", "Kyousuke"),
    22: ("¡¡No...!!", "Kirino"),
    23: ("Jaj, jaj..", "Kirino"),
    24: ("O-Oye... Así que eso significa... ¿soy igual que esos otakus asquerosos que se ven mucho en la televisión?", "Kirino"),
    25: ("¡No, eres diferente de ellos!", "Kyousuke"),
    26: ("Entre la multitud otaku llena de transpiración y grasa, tener la figura de una enérgica chica de secundaria bailando salvajemente...", "Kyousuke"),
    27: ("Eras claramente llamativa incluso entre esos otakus.", "Kyousuke"),
    28: ("En otras palabras... Estabas muy fuera de lugar.", "Kyousuke"),
    29: ("¡¡No digas eso con tanta confianza!!", "Kirino"),
    30: ("Está bien, en ese entonces eras...", "Kyousuke"),
    31: ("...¿Eh?", "Kirino"),
    32: ("Estabas en un nivel por encima de esos tipos, tan absurdamente asquerosa que no tenías igual.", "Kyousuke"),
    33: ("¡¡¡Deja de molestarme!!!", "Kirino"),
    34: ("Desearía poder negarlo también, pero la verdad es la verdad.", "Kyousuke"),
    35: ("N-No puedo soportarlo más... No tengo más remedio que cometer seppuku si así están las cosas...", "Kirino"),
    36: ("¡Espera! ¡Conozco personas que son mucho más vergonzosas que tú!", "Kyousuke"),
    37: ("¡¿M-Más que yo?!", "Kirino"),
    38: ("Una persona varonil que empezaría a jugar juegos H en cualquier momento, en cualquier lugar, en las calles más oscuras. Una fujoshi que deja volar su imaginación al ver un", "Kyousuke"),
    39: ("tenedor y una cuchara...", "Kyousuke"),
    40: ("Hmph, eres solo una principiante comparada con ellos.", "Kyousuke"),
    41: ("...¡N-No me compares con esa clase de personas!", "Kirino"),
    42: ("Realmente recomiendo que no hagas eso.", "Kyousuke"),
    43: ("N-No me detengas.", "Kirino"),
    44: ("Sin embargo, si no te detengo ahora, podrías ser falsamente retratada como la chica que se suicidó debido a su pena de no poder recuperar sus", "Kyousuke"),
    45: ("recuerdos de Meruru, y ser adorada por la comunidad otaku, ¿sabes?", "Kyousuke"),
    46: ("¿Realmente quieres ser una leyenda por la eternidad dentro de la comunidad otaku?", "Kyousuke"),
    47: ("¡No! ¡Retiro lo que acabo de decir!", "Kirino"),
    48: ("¡No...! N-No puedo soportarlo más...!", "Kirino"),
    49: ("Uuuu... Por favor, ten piedad de mí....", "Kirino"),
}

a105_n = {
    0: "Ruta de Kirino · Es Imposible Que Mi Hermanita No Escuche A Su Mejor Amiga",
    6: "Sería inevitable reaccionar de esa manera si me pusiera en los zapatos de Kirino.",
    7: "Sin embargo... ¿qué me pasa? Mi pecho se siente incómodo...",
    10: "...¿Qué pasa con esa expresión incierta tuya? Eso no es como tú en absoluto.",
    15: "...En serio, ¿por qué me estoy alterando tanto?",
    16: "¿No me dije a mí mismo que los recuerdos de Kirino no me importaban?",
}
a105_s = {
    1: ("No puedo creer que en realidad soy una otaku asquerosa...", "Kirino"),
    2: ("N-No tienes que preocuparte tanto por eso, ¿sabes? Ser otaku no es realmente algo malo.", "Kyousuke"),
    3: ("No, no es persuasivo si viene de ti.", "Kirino"),
    4: ("No debería haber preguntado sobre ello... Pensar que en realidad he hecho cosas tan asquerosas...", "Kirino"),
    5: ("...No digas eso. Todo es para recuperar tus recuerdos, ¿no?", "Kyousuke"),
    8: ("...Pero, sí recuerdo las cosas relacionadas con Ayase muy claramente.", "Kirino"),
    9: ("Bueno... Es una buena cosa si pudiera recuperar mis recuerdos, pero no hay más remedio si no puedo.", "Kirino"),
    11: ("D-De todos modos, no moriré incluso si no tengo mis recuerdos. Si pudiera aceptar la realidad para la «nueva yo»...", "Kirino"),
    12: ("No, todavía hay otras maneras.", "Kyousuke"),
    13: ("¿Eh...?", "Kirino"),
    14: ("Me tienes a tu lado, ¿no? No te rindas tan fácilmente.", "Kyousuke"),
}

data = {
    "000scriptBKIR_0100A.obj": build(a100_n, a100_s),
    "000scriptBKIR_0101G.obj": build(a101_n, a101_s),
    "000scriptBKIR_0102A.obj": build(a102_n, a102_s),
    "000scriptBKIR_0103T.obj": build(a103_n, a103_s),
    "000scriptBKIR_0105A.obj": build(a105_n, a105_s),
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
