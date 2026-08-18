import json

PATH = "/mnt/c/Users/christ-gm/Desktop/code/oreimo/work/disc1/Data/Translation.json"

def build(narration, speech):
    out = {}
    for i, t in narration.items():
        out[str(i)] = t
    for i, t in speech.items():
        out[str(i)] = "「" + t[0] + "」"
    return out

T = "Ruta de Kanako"

n = {
    0: T,
    1: "Y entonces...",
    7: "Solo vino para una visita normal... ¿huh?",
    8: "Fui ingenuo por creer eso.",
    9: "Ya que estaba preocupado, llevé jugo hasta la habitación de Kirino...",
    11: "Allí, un desarrollo inimaginable me esperaba.",
    16: "¿Qué está pasando aquí...?!",
    23: "Kirino... Eres realmente mala mintiendo.",
    24: "Aunque Kanako solo quería indagar en el incidente de que yo me convirtiera en su manager.",
    25: "Mi hermanita cavó su propia tumba al revelar sus intereses otaku en su lugar.",
    29: "...Esa chica. Todavía sigue guardando rencor por lo de antes.",
    30: "Quiero poner fin a esta situación de alguna manera, pero...",
    31: "...No puedo pensar en ninguna buena idea...",
    32: "Pasaron varios segundos...",
    33: "Kirino abrió la boca.",
    38: "¡Esta maldita mocosa, declarando eso sin un momento de vacilación!!",
    58: "Puse mi mano sobre la cabeza de Kanako y la froté bruscamente.",
    65: "Kurusu Kanako.",
    66: "Puede que la haya... malinterpretado un poco.",
    74: "...Está actuando raro.",
    81: "¿Q-Qué le pasa? Está siendo inusualmente admirable.",
    86: "...Cuando es madura así, es un poco linda...",
}
s = {
    2: ("...Bienvenida.", "Kyousuke"),
    3: ("Hola♪. ¿Está Kirino?", "Kanako"),
    4: ("Está en su habitación... Pasa.", "Kyousuke"),
    5: ("Perdón por molestar.", "Kanako"),
    6: ("..................", "Kyousuke"),
    10: ("Kirino, te he traído jugo y aperitivos...", "Kyousuke"),
    12: ("Je, así que así es～", "Kanako"),
    13: (".........", "Kirino"),
    14: ("Así que Kirino es otaku.", "Kanako"),
    15: ("¿Qué...", "Kyousuke"),
    17: ("Ah, «el hermano mayor de Kirino», hola.", "Kanako"),
    18: ("¿Sabes? ¿Recién ahora? Le saqué la verdad sobre por qué te volviste el manager de Kanako a Kirino.", "Kanako"),
    19: ("Entonces Kirino se auto-combustió por sí sola. Aprendí mucho♪", "Kanako"),
    20: ("¡Y-Yo dije que no es así!", "Kirino"),
    21: ("¿Eh? ¿No era el premio principal de entonces... algún tipo de figura de Meruru? ¿No es eso lo que tienes ahora～? ¿Fue un regalo de Ayase?", "Kanako"),
    22: ("Eso es cierto... pero... eso es...", "Kirino"),
    26: ("Kehehe, solo resígnate. Esta noticia definitivamente se sabrá.", "Kanako"),
    27: ("Déjala en paz.", "Kyousuke"),
    28: ("Ah, todavía estás aquí. Tch, vete ya, inútil.", "Kanako"),
    34: ("...¿C-Crees... que es raro?", "Kirino"),
    35: ("¿Huh?", "Kanako"),
    36: ("...Dije... ¿crees que es raro... si fuera otaku?", "Kirino"),
    37: ("¿Huh? Por supuesto que lo sería.", "Kanako"),
    39: ("Porque, ¿no es eso como ser igual a los otakus asquerosos que vienen a mi actuación?", "Kanako"),
    40: ("Kirino... Eres realmente asquerosa.", "Kanako"),
    41: (".........!", "Kirino"),
    42: ("¡Oye!", "Kyousuke"),
    43: ("¿Huh? ¿Por qué te estás entrometiendo? Asqueroso es asqueroso. ¿Hay algún problema?", "Kanako"),
    44: ("¡Aun así!", "Kyousuke"),
    45: ("O más bien, deberías habérmelo dicho antes. Entonces podría haber conseguido un buen asiento para ti en mi actuación del Comiket de Verano.", "Kanako"),
    46: ("¿Eh?", "Kirino"),
    47: ("Bueno, te gusta Meruru, ¿no? Después de todo, Kanako se parece un poco a Meruru. Los fans nerds de Meruru se ponen súper felices cuando subo al escenario en cosplay.", "Kanako"),
    48: ("¡E-Eso no es! ¿Por qué...?", "Kirino"),
    49: ("¿Por qué eres... capaz de tratarme normalmente? Hace un momento... ¡dijiste que yo era asquerosa, ¿no!", "Kirino"),
    50: ("Bueno, después de todo somos amigas.", "Kanako"),
    51: ("...Kanako.", "Kirino"),
    52: ("Bueno, pensé que Kirino me estaba mirando con ojos raros últimamente. Estaba actuando extrañamente pegajosa.", "Kanako"),
    53: ("Ahora que sé por qué, finalmente lo entiendo. Es realmente asqueroso. Si fuera alguien que no fuera Kirino, definitivamente cortaría todos los lazos.", "Kanako"),
    54: ("...Eso es todo.", "Kanako"),
    55: (".....................", "Kirino"),
    56: (".....................", "Kyousuke"),
    57: ("...Pfft.", "Kyousuke"),
    59: ("¡¿Qué?! ¿Qué estás haciendo de repente!", "Kanako"),
    60: ("...Eres bastante valiente... aunque seas una bajita.", "Kyousuke"),
    61: ("¡¿Qué estás diciendo?! ¿Te estás burlando de mí?!", "Kanako"),
    62: ("Por supuesto que no.", "Kyousuke"),
    63: ("...De ahora en adelante, por favor sigue cuidando de Kirino.", "Kyousuke"),
    64: ("...Hmph.", "Kanako"),
    67: ("Sí.", "Kyousuke"),
    68: ("...Soy yo.", "Kanako"),
    69: ("Oh, eres tú... Ha pasado mucho tiempo desde tu última llamada.", "Kyousuke"),
    70: ("...Sí.", "Kanako"),
    71: ("¿Vas a invitarme a salir en una cita otra vez?", "Kyousuke"),
    72: ("...No... No es eso.", "Kanako"),
    73: ("...Erm... Oye.", "Kanako"),
    75: ("¿Qué es?", "Kyousuke"),
    76: ("...¿Todavía estás enojado?", "Kanako"),
    77: ("¿? ¿Sobre qué?", "Kyousuke"),
    78: ("...Hace un rato, cuando te di una orden sobre lo del beso.", "Kanako"),
    79: ("Ah.", "Kyousuke"),
    80: ("Perdón.", "Kanako"),
    82: ("Ya no estoy enojado.", "Kyousuke"),
    83: ("...¿En serio?", "Kanako"),
    84: ("Sip, en serio.", "Kyousuke"),
    85: ("...Qué bueno.", "Kanako"),
    87: ("Así que entonces, aquí viene la siguiente orden.", "Kanako"),
    88: ("...¡Sabía que iba a ser algo así!", "Kyousuke"),
    89: ("Kehehehehehe.", "Kanako"),
}

with open(PATH, "r", encoding="utf-8") as f:
    current = json.load(f)
current["000scriptKIFK_0002A.obj"] = build(n, s)
with open(PATH, "w", encoding="utf-8") as f:
    json.dump(current, f, ensure_ascii=False)
print("updated 000scriptKIFK_0002A.obj")