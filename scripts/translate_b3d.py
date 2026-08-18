import json

PATH = "/mnt/c/Users/christ-gm/Desktop/code/oreimo/work/disc1/Data/Translation.json"

def build(narration, speech):
    out = {}
    for i, t in narration.items():
        out[str(i)] = t
    for i, t in speech.items():
        out[str(i)] = "「" + t[0] + "」"
    return out

a0061_n = {
    0: "Ruta de Kuroneko · Charla De Amantes A Altas Horas",
    4: "Ah, ¿qué debería hacer?",
    5: "Pensé en hablar con ella, pero me tocó la contestadora... ya que estoy siendo tan serio al respecto, sería mejor hablar con ella directamente.",
    6: "Aun así, ¿quizás debería dejarle saber que estoy preparado para cualquier cosa?",
    10: "¿Kirino está en el teléfono?",
    13: "--¿Está hablando con Kirino ahora mismo?",
    14: "Entonces, para ponerlo en términos simples, Kuroneko estaba hablando con Kirino, por lo tanto no pudo contestar mi llamada.",
    15: "Después de eso, me levanté e intenté preguntarle a Kirino sobre Kuroneko, pero...",
    16: "No pude sacar nada en absoluto de mi hermanita, que seguía enojada.",
    18: "Después de todo, es mi linda kohai.",
    28: "Qué vergüenza, creo que me moriré de la vergüenza.",
    46: "No se abrirá por teléfono. Le preguntaré directamente cuando la vea...",
}
a0061_s = {
    1: ("Bueno entonces, ya es hora de llamar a Kuroneko...", "Kyousuke"),
    2: ("En este momento no puedo contestar tu llamada...", "Speakers"),
    3: ("Entonces... no está contestando después de todo...", "Kyousuke"),
    7: ("...Me detendré por ahora y la contactaré directamente mañana.", "Kyousuke"),
    8: ("¡¿Huh?! ¡No puedo creerlo!", "Kirino"),
    9: ("...¿Hm?", "Kyousuke"),
    11: ("¡Tú, amante de lo oculto y delirante!", "Kirino"),
    12: ("¡No volveré a escucharte más!!", "Kirino"),
    17: ("Supongo que se lo diré de todos modos.", "Kyousuke"),
    19: ("Ah...", "Kyousuke"),
    20: ("Sé que tienes algo que te preocupa.", "Kyousuke"),
    21: ("Y estás tratando de resolverlo por tu cuenta...", "Kyousuke"),
    22: ("Pero, no te dejaré salirte con la tuya.", "Kyousuke"),
    23: ("Definitivamente haré que lo expliques todo, así que prepárate.", "Kyousuke"),
    24: ("Nos vemos, eso es todo...", "Kyousuke"),
    25: ("¿Hmm?", "Kyousuke"),
    26: ("...¿Qué estás diciendo?", "Kuroneko"),
    27: ("¿Kuroneko? ¿E-Estabas escuchando...", "Kyousuke"),
    29: ("Si estás al lado del teléfono... podrías haberlo contestado...", "Kyousuke"),
    30: ("Te pregunté qué estabas diciendo.", "Kuroneko"),
    31: ("Es una declaración.", "Kyousuke"),
    32: ("Pensé que te lo dejé claro en el intercambio de hoy.", "Kuroneko"),
    33: ("Aun así, todavía quiero saberlo.", "Kyousuke"),
    34: ("¿Vas a ignorar mi voluntad y abrirte paso a la fuerza en esto?", "Kuroneko"),
    35: ("Sí.", "Kyousuke"),
    36: ("Por eso los habitantes del mundo mortal... son bárbaros incivilizados, los peores.", "Kuroneko"),
    37: ("No me importa lo que digas. Ya tomé mi decisión.", "Kyousuke"),
    38: ("¿Oh en serio...? En ese caso, lo diré una vez más.", "Kuroneko"),
    39: ("Deja de involucrarte conmigo, no vuelvas a pisar nunca mi 【Mundo】.", "Kuroneko"),
    40: ("¿«Mi mundo»?", "Kyousuke"),
    41: ("Si continuaras pisando más allá...", "Kuroneko"),
    42: ("Prepárate para recibir el sufrimiento apropiado. El contacto físico con los de la tierra prohibida inevitablemente resulta en castigo.", "Kuroneko"),
    43: ("Ya estoy preparado para-", "Kyousuke"),
    44: ("Esto es muy inconveniente...", "Kuroneko"),
    45: ("¡De verdad colgó...!", "Kyousuke"),
    47: ("¡Esa chica... mejor que no me menosprecie cuando me estoy poniendo serio!", "Kyousuke"),
    48: ("De todos modos por ahora... ¡hora de dormir! ¡Nos vemos mañana!", "Kyousuke"),
}

a0065_n = {
    0: "Ruta de Kuroneko · Charla De Amantes A Altas Horas",
    1: "¿Dónde... estoy...?",
    2: "Se siente como si me estuviera alejando suavemente... Aunque puedo ver las cosas con claridad, esto no se siente real en absoluto...",
    3: "¿Es esto... un sueño?",
    9: "Kuroneko ciertamente no haría algo así... Espera, ¿podría ser... un sueño?!",
    10: "Así que este es el famoso sueño lúcido... Por eso Kuroneko parece un poco diferente de lo habitual.",
    11: "Es completamente diferente en la realidad... De alguna manera esto se siente... un poco erótico...",
}
a0065_s = {
    4: ("Oye, ¿senpai?", "Kuroneko"),
    5: ("¡Uwah! ¿K-Kuroneko?", "Kyousuke"),
    6: ("¿Por qué estás tan nervioso, senpai?", "Kuroneko"),
    7: ("¿De verdad estás tan preocupado por mí?", "Kuroneko"),
    8: ("¿O... estás aquí esperando «ese tipo» de cosas?", "Kuroneko"),
    12: ("Fufufu...", "Kuroneko"),
}

a0067_n = {
    0: "Ruta de Kuroneko · Charla De Amantes A Altas Horas",
    7: "¡No puedo decir que no la encuentro extrañamente atractiva ahora mismo...!",
    17: "¡Me está tratando como a un completo idiota y aun así...!",
    18: "¡¿Por qué mi corazón late tan rápido?!",
    23: "¡Uooohhh! ¿Esto... está pasando de verdad?!",
    51: "Vaya, hasta aparece en mis sueños... Phew.",
    52: "Me volveré loco si no resuelvo esto rápidamente...",
}
a0067_s = {
    1: ("¿Deseas hacer algunas cosas agradables conmigo?", "Kuroneko"),
    2: ("...¿Y si dijera que sí?", "Kyousuke"),
    3: ("...Gente como tú es verdaderamente... necios sin redención.", "Kuroneko"),
    4: ("¿No es esto un sueño? En ese caso no hay nada de malo en ser honesto con los propios deseos. ¿Verdad?", "Kyousuke"),
    5: ("...¿Podría ser que senpai ha querido hacer cosas lascivas conmigo desde hace tiempo?", "Kuroneko"),
    6: ("Bueno, si lo pones así.. Err... Ya sabes...", "Kyousuke"),
    8: ("Un necio... supongo que se podría decir eso.", "Kyousuke"),
    9: ("Pero ¿no eres tú la que me está seduciendo?", "Kyousuke"),
    10: ("Hmph... Tales palabras banales.", "Kuroneko"),
    11: ("Perdón, no pude pensar en nada más.", "Kyousuke"),
    12: ("Bueno entonces, ¿vamos a hacer algo bueno juntos?", "Kyousuke"),
    13: ("Fufufu... ¿Qué debería hacer, me pregunto.", "Kuroneko"),
    14: ("¿Eh, estás tratando de molestarme?! Hay buenos y malos momentos cuando se trata de molestar a los hombres!", "Kyousuke"),
    15: ("Cosas así no me conciernen. Solo quería jugar contigo.", "Kuroneko"),
    16: ("¿J-Jugar... conmigo...?!", "Kyousuke"),
    19: ("¿Estás dudando? Bueno, ciertamente no te queda bien, incluso si esto es solo un sueño.", "Kyousuke"),
    20: ("...Podría hacerlo si me apeteciera.", "Kuroneko"),
    21: ("¿Oh en serio...? Pero para alguien como tú que no sabe cómo manejar a los hombres, dudo que pudieras.", "Kyousuke"),
    22: ("Seguro que bromeas. Solo necesitas abandonar tu cuerpo ante mí.", "Kuroneko"),
    24: ("Hmm... Haa... Fufu...", "Kuroneko"),
    25: ("*TRAGO*", "Kyousuke"),
    26: ("Bueno entonces... túmbate ahí justo así... y relaja tu cuerpo.", "Kuroneko"),
    27: ("¿De verdad...? *trago*", "Kyousuke"),
    28: ("¿Arrepintiéndote ahora? Qué debilucho.", "Kuroneko"),
    29: ("...¿Debería parar?", "Kuroneko"),
    30: ("¡No! ¡Por favor continúa!", "Kyousuke"),
    31: ("Fufufu, cierra los ojos.", "Kuroneko"),
    32: ("Ah...*trago*. Ah, ya que es mi primera vez, por favor sé gentil...", "Kyousuke"),
    33: ("...Lo sé.", "Kuroneko"),
    34: ("Entonces, cierra los ojos...", "Kuroneko"),
    35: ("Cierra los ojos obedientemente, buen chico. Ahora entonces, esto...", "Kuroneko"),
    36: ("¿Eh?", "Kyousuke"),
    37: ("Fufufu.", "Kuroneko"),
    38: ("¿K-Kuroneko? ¿Qué fue ese sonido?", "Kyousuke"),
    39: ("Estará bien, te haré sentir relajado.", "Kuroneko"),
    40: ("¡No eso! ¡Mi nerviosismo ya se está desmoronando!", "Kyousuke"),
    41: ("...Mentiroso. Todo ha sido una mentira.", "Kuroneko"),
    42: ("¡¿Qué?!", "Kyousuke"),
    43: ("Algo como esto fue suficiente para tentarte.", "Kuroneko"),
    44: ("¿De verdad pensaste que tenías las cualificaciones?", "Kuroneko"),
    45: ("¿Eh? ¿Eh? ¿Q-Qué estás diciendo?", "Kyousuke"),
    46: ("¿De verdad crees que un perdedor como tú puede interponerse en mis metas?", "Kuroneko"),
    47: ("Oye, ¡detente! ¡Esto se está volviendo demasiado real para un sueño!", "Kyousuke"),
    48: ("Jeje, de acuerdo, de acuerdo con la profecía anterior, grabaré el castigo en tu cuerpo.", "Kuroneko"),
    49: ("¿Eh? Espera, ¿cómo puede ser esto! ¿Qué es eso en tu mano!? ¡N-No! ¡Es demasiado grande! ¡Para! ¡AAAAAAAHHH!", "Kyousuke"),
    50: ("¿U-Un sueño... huh...", "Kyousuke"),
}

a0080_n = {
    0: "Ruta de Kuroneko · Búsqueda De La Determinación",
    5: "Su intuición es certera...",
    16: "Y así fui al salón de Kuroneko.",
    18: "¿A dónde fue? Quizás debería preguntar por ahí...",
    22: "No puedo llamarla Kuroneko frente a sus compañeras de clase...",
    32: "¿Por qué le dijo eso a una compañera de clase? ¿No causará esto un malentendido?",
    33: "Por Dios... Esa chica... Tengo que darle alcance sí o sí.",
}
a0080_s = {
    1: ("Kyou-chan, ¿cómo pasaste tus vacaciones? Parece que estuviste agotado desde la mañana.", "Manami"),
    2: ("Además, pareces estar frunciendo el ceño...", "Manami"),
    3: ("No estoy haciendo nada de eso.", "Kyousuke"),
    4: ("Entonces estoy en lo cierto. ¿Podría ser por culpa de Kuroneko-san?", "Manami"),
    6: ("¿No contactaste a Kuroneko-san durante las vacaciones?", "Manami"),
    7: ("Bueno sí... Esa chica... Aunque me esforcé mucho por contactarla...", "Kyousuke"),
    8: ("Ya veo...", "Manami"),
    9: ("En momentos así, es realmente genial estar en la misma escuela que ella y tener oportunidades de verla mientras estemos en la escuela.", "Kyousuke"),
    10: ("Jejeje, Kyou-chan es realmente un senpai capaz～", "Manami"),
    11: ("No estaría tan cansado si fuera capaz.", "Kyousuke"),
    12: ("¡Apoyaré tanto a Kyou-chan como a Kuroneko-san!", "Manami"),
    13: ("En serio... Gracias.", "Kyousuke"),
    14: ("Bueno entonces, me voy.", "Kyousuke"),
    15: ("¡Sí, buena suerte!", "Manami"),
    17: ("Parece que no está por aquí...", "Kyousuke"),
    19: ("Oye tú, por allá... uhh...", "Kyousuke"),
    20: ("¿S-Sí?", "Schoolgirl"),
    21: ("Erm, ¿sabes a dónde fue Kurone-- Gokou?", "Kyousuke"),
    23: ("¿Gokou-san...?", "Schoolgirl"),
    24: ("Umm, desapareció en cuanto sonó el timbre.", "Schoolgirl"),
    25: ("¿Entonces no tienes idea de a dónde fue?", "Kyousuke"),
    26: ("Sí, lo siento...", "Schoolgirl"),
    27: ("Ya veo, gracias.", "Kyousuke"),
    28: ("Ah, sin embargo...", "Schoolgirl"),
    29: ("¿Eh?", "Kyousuke"),
    30: ("Me dijeron que si un senpai de tercer año viniera, le dijera que «nunca venga a buscarme a este 【Salón】 otra vez».", "Schoolgirl"),
    31: ("E-Esa chica... Seguro que tiene una manera de hacer el ridículo a alguien.", "Kyousuke"),
}

a0085_n = {
    0: "Ruta de Kuroneko · Testigo Afortunado",
    1: "No presté atención en clase hasta que terminó la escuela.",
    2: "No está mal hacer algo diferente de vez en cuando después de las lecciones o exámenes pero...",
    3: "Usando mi uniforme y jugando fútbol, ¿cómo pasó esto?",
    4: "...No tengo ganas de jugar. Encontraré algún rincón y me quedaré de brazos cruzados.",
    12: "Bueno, dejando eso de lado... ¿cómo puedo encontrar una manera de iniciar una conversación con Kuroneko?",
    29: "Espera... ¿Huh? Por allá, junto a la piscina...",
    31: "Dios, si existes, ¡por favor acepta mi gratitud!",
    32: "¡Sabía que has estado observando todo este tiempo, y ahora decidiste recompensarme!",
    33: "Aahh. Se escondió...",
    35: "¡Pero es demasiado tarde! ¡Tu rara imagen ya ha sido grabada en mis retinas!",
    37: "No otra vez... Owowoww.",
    38: "¿Es este mi castigo por ver a Kuroneko en traje de baño...?",
}
a0085_s = {
    5: ("Oye Kousaka. No te distraigas. ¡Viene la pelota!", "Akagi"),
    6: ("Oh, Akagi. Estoy pensando profundamente ahora mismo. Así que no me hagas caso.", "Kyousuke"),
    7: ("¿Huh?", "Akagi"),
    8: ("Así que solo finge que no estoy aquí y juega tu fútbol, ex miembro del equipo de fútbol.", "Kyousuke"),
    9: ("¿Qué estás diciendo? Mejor ven cuando nos llegue la pelota.", "Akagi"),
    10: ("Sí sí, lo que digas, solo vete. No me molestes.", "Kyousuke"),
    11: ("Dios, ya lo dejé claro, ¿de acuerdo?", "Akagi"),
    13: ("¡Oye, Kousaka! ¡La pelota va en tu dirección!", "Akagi"),
    14: ("¿Eh?", "Kyousuke"),
    15: ("¡Guaaaaaaaaaaah!", "Kyousuke"),
    16: ("¡Oye! ¡Kousaka! ¿Estás bien?", "Akagi"),
    17: ("Owowowowowow...", "Kyousuke"),
    18: ("Después de comerte eso justo en la cara, por supuesto que duele.", "Akagi"),
    19: ("...Oye, ¿no estás siendo demasiado cruel?", "Kyousuke"),
    20: ("¿Quién y dónde está ese tipo que desperdició mi hermoso pase?", "Akagi"),
    21: ("Además fue tu culpa por distraerte. Normalmente habrías podido esquivarlo.", "Akagi"),
    22: ("Guh...", "Kyousuke"),
    23: ("Bueno, tómate un descanso por ahora.", "Akagi"),
    24: ("S-Sí. Gracias...", "Kyousuke"),
    25: ("Bueno, vuelve al campo si ya no te duele.", "Akagi"),
    26: ("Sí.", "Kyousuke"),
    27: ("Jaja, esto no es nada. Se curará en poco tiempo.", "Akagi"),
    28: ("Tch, ese bastardo...", "Kyousuke"),
    30: ("¿Estás hablando en serio......", "Kyousuke"),
    34: ("¡Oye! ¡La pelota viene hacia ti otra vez!", "Akagi"),
    36: ("¡Guuuuaaaah～～!!", "Kyousuke"),
    39: ("Oye, lo siento mucho. No fue a propósito esta vez.", "Akagi"),
    40: ("¡¿Otra vez tú～～!!", "Kyousuke"),
}

data = {
    "000scriptCKUR_0061A.obj": build(a0061_n, a0061_s),
    "000scriptCKUR_0065G.obj": build(a0065_n, a0065_s),
    "000scriptCKUR_0067T.obj": build(a0067_n, a0067_s),
    "000scriptCKUR_0080A.obj": build(a0080_n, a0080_s),
    "000scriptCKUR_0085G.obj": build(a0085_n, a0085_s),
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
