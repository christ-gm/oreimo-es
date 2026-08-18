import json

PATH = "/mnt/c/Users/christ-gm/Desktop/code/oreimo/work/disc1/Data/Translation.json"

def build(narration, speech):
    out = {}
    for i, t in narration.items():
        out[str(i)] = t
    for i, t in speech.items():
        out[str(i)] = "「" + t[0] + "」"
    return out

n = {
    253: "¿Supongamos que todas las dificultades de hoy fueran por el bien de Kirino?",
    254: "...Solo pensar en ello parecía aumentar repentinamente mi agotamiento.",
    255: "¿Por qué Akagi piensa que su propia hermanita es tan linda?",
    256: "No lo entendía en absoluto.",
    257: "Pero, bueno... No estaba mal pasar el rato juntos solo nosotros dos.",
    276: "La forma en que Akagi me suplicaba desesperadamente me hizo sentir tanto asco, como extrañamente en paz.",
    277: "Bueno... Lo que le dije antes no era una mentira.",
    278: "...No está tan mal, salir así juntos nosotros dos de vez en cuando.",
    285: "No me molesté en intentar replicar a esa declaración de «la chica más linda del mundo, Sena-chan».",
    286: "Sé muy bien cómo eres un idiota que adora a su hermanita sin rival.",
    294: "Dios... Retiro inmediatamente lo que dije hace un momento.",
    295: "--No está tan mal, salir así juntos nosotros dos de vez en cuando.--",
    296: "¡Eso es algo que no debe decirse en presencia de esta hermanita fujoshi!",
}
s = {
    258: ("Bueno, ¿no es agradable de vez en cuando? Salir a algún lugar contigo.", "Kyousuke"),
    259: ("¿Eh, es así?", "Akagi"),
    260: ("Solo de vez en cuando, de vez en cuando.", "Kyousuke"),
    261: ("Entonces, para el evento doujin en Ikebukuro este otoño...", "Akagi"),
    262: ("Me niego.", "Kyousuke"),
    263: ("Aunque acabas de decir que te gusta acompañarme...", "Akagi"),
    264: ("¡Solo de vez en cuando, de vez en cuando! ¡Como si pudiera soportar ir contigo todo el tiempo!", "Kyousuke"),
    265: ("Aunque digas eso, en realidad quieres ir, ¿no?", "Akagi"),
    266: ("N-No realmente...", "Kyousuke"),
    267: ("Ocultando tu vergüenza así; tal vez esta vez tú serás el tragado.", "Akagi"),
    268: ("¡¿Estás tratando de decir algo inteligente?!", "Kyousuke"),
    269: ("Algo así. De todos modos, cuento contigo.", "Akagi"),
    270: ("Me niego.", "Kyousuke"),
    271: ("No digas eso.", "Akagi"),
    272: ("¡¡Rechazado!!", "Kyousuke"),
    273: ("Kousaka-saa～n.", "Akagi"),
    274: ("¡Estás siendo asqueroso!", "Kyousuke"),
    275: ("Dios, de verdad no eres honesto.", "Akagi"),
    279: ("......De verdad se llevan bien, Onii-chan y Kousaka-senpai......", "Sena"),
    280: ("Ah, ¡Sena-chan! ¿Cuándo llegaste?", "Akagi"),
    281: ("¡Desde que los dos salieron del baño con buen ánimo entre ustedes! Fufufu... fufufufufufufu...", "Sena"),
    282: ("D-Detente... Lo que estás pensando ahora mismo es un gran malentendido!", "Kyousuke"),
    283: ("¡Kousaka, déjame presentártela! ¡Esta es mi hermanita, la chica más linda del mundo, Sena-chan!", "Akagi"),
    284: ("Ya la conozco. Estamos juntos en el Club de Investigación de Juegos.", "Kyousuke"),
    287: ("Kousaka-senpai, no has venido al Club de Investigación de Juegos recientemente, ¿verdad? Por favor ven de vez en cuando.", "Sena"),
    288: ("Sí, sí, lo entiendo.", "Kyousuke"),
    289: ("Entonces, deberíamos volver pronto. Perdón, pero tomaré prestado a Onii-chan.", "Sena"),
    290: ("No hay necesidad de disculparte. Apúrate y llévatelo.", "Kyousuke"),
    291: ("Ahí vas de nuevo～～. Aunque son amantes～～", "Sena"),
    292: ("¡Eso está mal!", "Akagi"),
    293: ("¡Como si eso pudiera ser!", "Kyousuke"),
    297: ("¡Entonces, nos vemos de nuevo! ¡En el salón del club!", "Sena"),
}

with open(PATH, "r", encoding="utf-8") as f:
    current = json.load(f)
entry = current.get("000scriptLAKA_0000.obj", {})
entry.update(build(n, s))
current["000scriptLAKA_0000.obj"] = entry
with open(PATH, "w", encoding="utf-8") as f:
    json.dump(current, f, ensure_ascii=False)
print("updated 000scriptLAKA_0000.obj (part 2)")