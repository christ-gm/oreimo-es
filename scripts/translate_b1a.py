import json, os

PATH = "/mnt/c/Users/christ-gm/Desktop/code/oreimo/work/disc1/Data/Translation.json"

# file -> {idx: text}, dialogue gets 「」 automatically when name present
# each entry: ("text", name) where name != "" means dialogue

def build(narration: dict, speech: dict) -> dict:
    out = {}
    for i, t in narration.items():
        out[str(i)] = t
    for i, t in speech.items():
        text, name = t
        out[str(i)] = "「" + text + "」"
    return out

akyo_0000a_narration = {
    30: "Si esa hermanita tiene entre manos DVDs de anime y juegos no aptos para niños, lo mejor es salir corriendo de inmediato.",
    31: "Si no...",
    35: "Obligado a jugar juegos que no quiero, noche tras noche...",
    38: "Enfadándose por su capacidad para hacer amigos afines...",
    41: "Obligado a participar en sus reuniones...",
    45: "Crucé palabras con mi padre tiránico.",
    48: "Ser etiquetado como «pervertido»...",
    49: "Mi vida cotidiana y ordinaria quedó destrozada.",
    50: "Pero...",
    58: "Al ver a mi hermana disfrutando feliz de su pasatiempo, siento que no está tan mal.",
    59: "Debe ser porque soy su hermano mayor.",
}
akyo_0000a_speech = {
    32: ("¡Imouto Maker EX～ Volumen 4!", "Shiori"),
    33: ("¡Bienvenido a casa, Onii-chan! Hagamos el amor... junto con tu hermanita～", "Shiori"),
    34: ("¡¿Qué demonios intentas que juegue?!", "Kyousuke"),
    36: ("...Oye, ¿qué crees que debería hacer?", "Kirino"),
    37: ("Hazte amigos, gente con los mismos gustos que tú, como deberías hacer.", "Kyousuke"),
    39: ("¡Soy yo, Saori Bajeena!", "Saori"),
    40: ("Nombre de usuario: Kuroneko.", "Kuroneko"),
    42: ("...Ah, o sea: estabas en el cuarto de tu hermana, usando su computadora y jugando un juego que hace cosas indecentes con las hermanitas?", "Daisuke"),
    43: ("¡Son súper interesantes! ¡¿Y qué problema hay?!", "Kyousuke"),
    44: ("¡Un hijo... tan estúpido!", "Daisuke"),
    46: ("¡No te acerques más, pervertido!", "Ayase"),
    47: ("...Qué asco. Por favor, muere.", "Ayase"),
    51: ("¡Radio Kaikan! ¡AniMate! Juju... ¡Así que esto es Akihabara!!", "Kirino"),
    52: ("Es muy lindo, ¿no? Eh, por ejemplo...", "Kirino"),
    53: ("Como muchos galges están dirigidos a jugadores hombres, hay saludos como «Onii-chan», «Onii», «Aniki», «Nii-kun»...", "Kirino"),
    54: ("Las chicas me llaman con el «saludo especial» que encaja con su personaje, lo que muestra su afecto hacia mí. ¡Es simplemente... demasiado LINDO!", "Kirino"),
    55: ("¡Es el set de dakimakura de edición limitada del Comiket de verano de «Stardust ☆ Witch Meruru»! ¿No es increíble?", "Kirino"),
    56: ("¿Eh? Es una dakimakura, así que por supuesto se supone que la abrazas para dormir.", "Kirino"),
    57: ("Bueno, a veces restriegas la cara contra ella, y tal vez la hueles...", "Kirino"),
}

akyo_0010a_narration = {
    0: "Irrumpiendo en la Habitación",
    4: "Esta chica que patea a su hermano en la parte trasera de la cabeza justo después de entrar al cuarto es...",
    5: "Kousaka Kirino: mi hermanita.",
    10: "Ella es Saori Bajeena (nombre de usuario en línea).",
    11: "Con su sentido de la moda y su forma de hablar, es una otaku típica de más de 180cm.",
    12: "Buena para ayudar a la gente, es la líder de la comunidad de anime «Otaku Girls Unite!» a la que se unió Kirino.",
    13: "Y ahora, es una buena amiga mía.",
    14: "Por cierto, «Kiririn» es el nombre de usuario de Kirino.",
    17: "Ella es Kuroneko (nombre de usuario en línea).",
    18: "A primera vista, es inexpresiva y poco sociable. Una chica problemática con una lengua afilada.",
    19: "Pero en realidad, es una persona muy bondadosa...",
    20: "Por cierto, fue admitida recientemente en mi escuela, convirtiéndose en mi kouhai.",
    21: "También pertenece al mismo club que yo, pero eso es una especie de secreto entre nosotros...",
    22: "Es una kouhai preocupante para mí, una chica por la que me importa... supongo.",
    33: "...Me han malentendido por completo.",
    34: "Explicaré las cosas aquí.",
    35: "Por alguna razón, Kirino no estuvo en casa durante tres meses entre invierno y primavera.",
    36: "Regresó a casa hace poco, y por eso no sabe lo que ha pasado durante su ausencia.",
    37: "Es solo que cuando Kirino no estaba en casa, Saori y Kuroneko se volvieron «mis amigas» y solían venir a jugar.",
    38: "Obviamente no hay manera de que ocurriera lo que Kirino sospechaba.",
    39: "Aunque su actitud parece cruel, a Kirino de verdad le agradan sus amigas.",
    40: "Por eso se sintió mortificada cuando parecía que le había quitado a sus amigas.",
    56: "¡Mierda! Me acaban de malentender Kirino, y ahora...",
    59: "...Eso arruinó por completo el ambiente.",
    60: "Tengo que apaciguar su ira de alguna manera...",
}
akyo_0010a_speech = {
    1: ("¡Gwah!", "Kyousuke"),
    2: ("¡Eso duele, oye!", "Kyousuke"),
    3: ("Cállate.", "???"),
    6: ("¿Qué significa esto?", "Kirino"),
    7: ("¿De qué hablas?", "Kyousuke"),
    8: ("¡P-Por qué se han reunido en tu cuarto para jugar God Eater?!", "Kirino"),
    9: ("¡Perdón por la intrusión, Kiririn-shi! ¿A qué se debe tu repentina aparición?", "Saori"),
    15: ("Hmph... ¿Hay algún problema?", "Kuroneko"),
    16: ("¿No fuiste tú quien nos invitó a jugar «God Eater Burst»?", "Kuroneko"),
    23: ("¡Eso no es! ¡Pregunto por qué están todos reunidos en su cuarto!", "Kirino"),
    24: ("¿No estaba bien mi cuarto? ¡Eso es lo que hacíamos hasta ahora!", "Kirino"),
    25: ("Ah, eso.", "Kuroneko"),
    26: ("Je. ...Es porque últimamente nos hemos estado reuniendo mucho en su cuarto, así que vinimos aquí por error.", "Kuroneko"),
    27: ("......!!!", "Kirino"),
    28: ("¡¿Por qué me pateaste?!", "Kyousuke"),
    29: ("Tsk... No importa.", "Kirino"),
    30: ("¿Qué está pasando? Déjame escuchar.", "Kirino"),
    31: ("¿Qué te pasa? ¿Trajiste a las amigas de tu hermana a tu cuarto cuando no estaba?", "Kirino"),
    32: ("¡No me hagas parecer un villano!", "Kyousuke"),
    41: ("......Jeje...", "Kuroneko"),
    42: ("......?", "Kirino"),
    43: ("...Aunque preguntaste qué significaba esto... ¿Cierto?", "Kuroneko"),
    44: ("Jeje... Oye, ¿Kyou-chan? ¿Cómo vamos a explicarle nuestra relación a Kirino-chan?", "Kuroneko"),
    45: ("¡No digas eso como si hubiera una relación especial entre nosotros!", "Kyousuke"),
    46: ("Kyou-chan, eh... Qué asco...", "Kirino"),
    47: ("Oh, cielos, Kirino-chan está enojada ahora... ¿Qué haremos, Kyou-chan?", "Kuroneko"),
    48: ("P-Por favor, déjalo así...", "Kyousuke"),
    49: ("¿Qué te pasa? Tienes la cara toda roja.", "Kuroneko"),
    50: ("Ghk......", "Kuroneko"),
    51: ("¿No será porque puede ver las bragas de Kuroneko-shi desde su posición?", "Saori"),
    52: ("?!", "Kuroneko"),
    53: ("¡Espera! ¡Saori! ¡No digas cosas innecesarias así!", "Kyousuke"),
    54: ("¡T-T-Tú... Tú... Tú..!", "Kuroneko"),
    55: ("¡No vi nada! ¡Es un malentendido!", "Kyousuke"),
    57: ("¡Gwah!", "Kyousuke"),
    58: ("¡E-Eres lo peor! ¡Lo peor, lo peor, lo peor! ¡Solo muérete ya!", "Kirino"),
}

data = {
    "000scriptAKYO_0000A.obj": build(akyo_0000a_narration, akyo_0000a_speech),
    "000scriptAKYO_0010A.obj": build(akyo_0010a_narration, akyo_0010a_speech),
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