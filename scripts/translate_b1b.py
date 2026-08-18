import json

PATH = "/mnt/c/Users/christ-gm/Desktop/code/oreimo/work/disc1/Data/Translation.json"

def build(narration: dict, speech: dict) -> dict:
    out = {}
    for i, t in narration.items():
        out[str(i)] = t
    for i, t in speech.items():
        text, _name = t
        out[str(i)] = "「" + text + "」"
    return out

a20_n = {
    0: "Irrumpiendo en la Habitación",
    12: "Aunque intenté «contraatacarla», parece que no funcionó en absoluto.",
    19: "¡M-Maldición! ¡Perdí mi oportunidad...!",
    21: "Lo sé. De acuerdo, esta vez, definitivamente...",
    36: "¿De verdad resolví el malentendido?",
    38: "¡M-Maldición! ¡Perdí mi oportunidad...!",
    41: "Eso es duro...",
    46: "¿El... contraataque funcionó?",
    58: "...Al final, Saori me cubrió.",
}
a20_s = {
    1: ("Kyousuke-shi, si no apaciguas la ira de Kiririn-shi...", "Saori"),
    2: ("I-Incluso si dices eso...", "Kyousuke"),
    3: ("¡En ese caso, es el momento para una «Conversación a Dueto»!", "Saori"),
    4: ("¿Una «Conversación a Dueto»? ¿Qué es eso?", "Kyousuke"),
    5: ("¡Adentrándose hacia una conversación sincera de uno a uno con Kiririn-shi!", "Saori"),
    6: ("¡Reacciona según las palabras de la otra parte y «contraataca» en el momento oportuno!", "Saori"),
    7: ("E-Entiendo. Lo intentaré...", "Kyousuke"),
    8: ("¡Ojo, también hay momentos en los que no debes «contraatacar»!", "Saori"),
    9: ("¿Qué estás murmurando? ¡Pervertido! ¡Solo muérete ya!", "Kirino"),
    10: ("C-Cálmate, Kirino... Esto es solo un malentendido.", "Kyousuke"),
    11: ("¡Cállate! ¡No lo niegues!", "Kirino"),
    13: ("¡Como era de esperar de Kyousuke-shi! ¡Un espléndido contraataque!", "Saori"),
    14: ("¡La ira de Kiririn-shi se ha suavizado un poco!", "Saori"),
    15: ("¡¿Eh?! ¿Se calmó solo por eso?!", "Kyousuke"),
    16: ("¡¿Quién podría entender algo así?!", "Kyousuke"),
    17: (".........", "Kyousuke"),
    18: ("¿Ni siquiera puedes negarlo?", "Kirino"),
    20: ("¡Kyousuke-shi, aguanta! ¡«Contraataca», «contraataca»!", "Saori"),
    22: ("Entonces, ¿los viste?", "Kirino"),
    23: ("¿Eh?", "Kyousuke"),
    24: ("¡Te pregunto si los viste!", "Kirino"),
    25: ("¡¿V-Vi qué?!", "Kyousuke"),
    26: ("¡Ya sabes...! Las... b-bragas de esa de negro...", "Kirino"),
    27: ("¡No las vi!", "Kyousuke"),
    28: ("¡Mentiroso! ¡Las viste!", "Kirino"),
    29: ("¡Es verdad! ¡Podemos cambiar de posición si no me crees! ¡Entonces sabrás que no podía verlas desde aquí!", "Kyousuke"),
    30: ("¿Lo intentaste?", "Saori"),
    31: ("¡C-Cállate ya de una vez!", "Kyousuke"),
    32: ("Hmm, ¿eso crees? No las viste...", "Kirino"),
    33: ("¿No eres un estúpido? No seas tan engañoso.", "Kirino"),
    34: ("¡Oooh! ¡Bien hecho, Kyousuke-shi! ¡Parece que arreglaste el malentendido con Kiririn-shi!", "Saori"),
    35: ("¿Eh? No, pero me acaban de llamar «estúpido»... ¿Verdad?", "Kyousuke"),
    37: ("... Eh...", "Kyousuke"),
    39: ("¡Entonces SÍ las viste! ¡Increíble!", "Kirino"),
    40: ("...Senpai es realmente la peor clase de escoria.", "Kuroneko"),
    42: ("Te haré una última pregunta.", "Kirino"),
    43: ("*trago*", "Kyousuke"),
    44: ("¿Trajiste a mis amigas a tu cuarto mientras no estaba?", "Kirino"),
    45: ("N-No lo hice...", "Kyousuke"),
    47: (".........", "Kirino"),
    48: ("Entonces, ¿por qué esas dos entraron espontáneamente a tu cuarto hoy?", "Kirino"),
    49: ("La de negro también lo dijo: «Siempre nos hemos estado reuniendo en este cuarto».", "Kirino"),
    50: ("...¿Qué significa eso? Explícate.", "Kirino"),
    51: ("Eh... Ehhh...", "Kyousuke"),
    52: ("¡N-No, en absoluto! ¡Kiririn-shi! ¡Escucha mis palabras!", "Saori"),
    53: ("¿Eh?", "Kirino"),
    54: ("Cuando Kiririn-shi se fue, Kyousuke-shi...", "Saori"),
    55: ("...se sintió muy, muy solo.", "Saori"),
    56: ("¡Por esa razón, Kuroneko-shi y yo decidimos levantar el ánimo de este desolado individuo viniendo a jugar!", "Saori"),
    57: ("¿Entiendes?", "Saori"),
    59: ("Hmm... Tú... Te sentiste solo cuando no estaba...", "Kirino"),
    60: (".........", "Kyousuke"),
    61: ("¡Así es!", "Kyousuke"),
    62: ("?!", "Kirino"),
    63: ("Pero, hay una razón para eso.", "Kyousuke"),
    64: ("¿Eh?", "Kirino"),
    65: ("Saori y Kuroneko se preocuparon de que estuviera solo sin ti.", "Kyousuke"),
    66: ("Por eso vinieron a jugar tan seguido.", "Kyousuke"),
    67: ("Pero al final, sigues enojada. ¿No está mal eso?", "Kyousuke"),
    68: ("Hmm... Tú... Te sentiste solo cuando no estaba...", "Kirino"),
    69: ("Qué asco... ¿Qué tan siscon eres...?", "Kirino"),
    70: ("Qué asco, ¿qué tan siscon eres?", "Kirino"),
}

a25_n = {
    0: "Kousaka Kirino",
    1: "Ahhh... Estoy agotado...",
    2: "«Una hermana tan problemática».",
    3: "Si alguien por ahí está de acuerdo conmigo, en serio creo que podríamos ser mejores amigos.",
    4: "El nombre de esta chica extremadamente arrogante es Kousaka Kirino, mi hermana con quien no tengo nada en común.",
    5: "Mi hermana es, a diferencia de mí, que soy bastante mediocre, una persona sobresaliente.",
    6: "...Sin embargo, esto es solo una «fachada».",
    7: "En realidad, tiene un «lado oculto»...",
    8: "¿Le encantan los simuladores de citas?",
    9: "Ya no necesito decirlo, ¿verdad?",
    10: "Contrario a su apariencia, esta chica extraordinariamente linda es...",
    11: "Cuando está llena de sí misma...",
    12: "Cuando llega ese momento, se comporta exactamente como una princesa.",
    13: "Les haré saber... cómo me he vuelto tan asqueado.",
    14: "En otras palabras... ¿Cómo lo digo...? Ella...",
    15: "¡Le encantan los simuladores de citas, comúnmente conocidos como galge!",
    16: "Especialmente los «relacionados con hermanitas». No tiene autocontrol alguno y ya ha coleccionado muchos.",
    18: "Mi hermana y las «amigas de su lado oculto»,",
    19: "comparten el mismo interés, camaradas como las llamamos.",
    21: "Ah, todo gracias a ti.",
    22: "Los consejos de esta chica siempre me han salvado.",
    24: "¿Cuánto tiempo planea esta chica relajarse en mi cama?",
    28: "Está diciendo cosas irracionales otra vez.",
    29: "No está bien, parece que van a pelear otra vez.",
    35: "¿Oh? ¿No era para jugar God Eater juntos?",
    38: "He aprendido la lección. Según las experiencias que he tenido hasta ahora...",
    39: "En este punto, algún evento va a perturbar mi hermosa «vida ordinaria».",
    40: "Se volvió así en el momento en que acepté la «orientación en la vida».",
    41: "Los que causaron la perturbación fueron, por supuesto, Kirino y las «amigas de su lado oculto».",
    42: "¿Qué clase de tormenta me espera esta vez?",
    43: "En serio... Bueno...",
    44: "Incluso estar esperándolo con ansias... Tiene que ser mi imaginación.",
}
a25_s = {
    17: ("...Qué asco. ¿Será que tienes pensamientos raros al mirarme?", "Kirino"),
    20: ("Jaja, qué bueno que hayas aclarado ese malentendido con Kiririn-shi, ¿no, Kyousuke-shi?", "Saori"),
    23: ("Supongo que ya es hora de que termine esta pelea entre hermanos...?", "Kuroneko"),
    25: ("¡No andes recostándote en la cama de otra persona!", "Kirino"),
    26: ("No es tu cama, ¿verdad? ¿Por qué te enojas?", "Kuroneko"),
    27: ("¡Las cosas de este cuarto, todo me pertenece!", "Kirino"),
    30: ("¡Oh! Esto me recuerda algo.", "Saori"),
    31: ("¿Eh?", "Kirino"),
    32: ("No pude preguntar debido al alboroto de antes...", "Saori"),
    33: ("¿Por qué razón nos has convocado hoy?", "Saori"),
    34: ("¡Ah! ¡Cierto, cierto! Sobre eso--", "Kirino"),
    36: ("Ejeje, de hecho... ¡Tengo algo increíble que contarles!", "Kirino"),
    37: ("..................", "Kyousuke"),
}

data = {
    "000scriptAKYO_0020T.obj": build(a20_n, a20_s),
    "000scriptAKYO_0025A.obj": build(a25_n, a25_s),
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