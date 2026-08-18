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
    306: "Mira lo fuerte que es tu voz...",
    307: "Parece que Kirino habla en serio. Está seriamente atrapada por la idea imposible de que me iré a algún lugar.",
    317: "...Espera, ¿dormir juntos?",
    319: "Con la cara roja, Kirino se acurrucó silenciosamente contra mí.",
    320: "Err... ¿Qué es esta criatura viviente...?",
    321: "Sus hombros temblaban, y estaba muy nerviosa...",
    322: "......Linda.",
    323: "...Espera, ¡cálmate, yo! ¡Kirino es mi hermanita! ¡Es una experta en trabajar duro a su hermano mayor por la mandíbula, ¿no?!",
    335: "...Un día después de eso.",
    340: "Hablado hasta que nuestra relación se volviera así... Ah, quiere decir... hasta que descubrí el hobby otaku de Kirino.",
}
s = {
    281: ("......¿Huh?", "Kyousuke"),
    282: ("¿Qué estás diciendo de repente? Si todavía estás medio dormida, ve y duerme en tu propia cama.", "Kyousuke"),
    283: ("¡Cállate! ¡Es todo... es todo tu culpa!", "Kirino"),
    284: ("Diciendo que no eres mi hermano mayor de verdad, que no somos parientes de sangre...", "Kirino"),
    285: ("Si escucho que dices algo así, es como si tú... te fueras a algún lugar lejano...", "Kirino"),
    286: ("¿Estabas... preocupada?", "Kyousuke"),
    287: ("......Solo un poco.", "Kirino"),
    289: ("¿Tienes un problema con que me preocupe por ti?", "Kirino"),
    290: ("N-No dije que tuviera un problema, ¿verdad?", "Kyousuke"),
    291: ("Si no estuvieras aquí...", "Kirino"),
    292: ("¿Quién va a hacer fila en la venta de medianoche en Akiba y comprarme juegos nuevos de ahora en adelante?", "Kirino"),
    293: ("¿Quién va a venir conmigo al Comiket?", "Kirino"),
    294: ("......¿No puedes hacer eso sin mí?", "Kyousuke"),
    295: ("¡Cállate!", "Kirino"),
    296: ("Kuh.", "Kyousuke"),
    298: ("Aun así, estaba preocupada.", "Kirino"),
    300: ("Yo... no me voy a ir a ningún lado.", "Kyousuke"),
    301: ("No lo sabes. Podrías irte por tu cuenta a encontrar a tus padres biológicos...", "Kirino"),
    302: ("...Has visto demasiados anime y manga.", "Kyousuke"),
    303: ("Pero, si fuera yo, definitivamente querría saber eso.", "Kirino"),
    304: ("Tú y yo somos diferentes. Cálmate.", "Kyousuke"),
    305: ("¡Estoy calmada...!", "Kirino"),
    308: ("Oye, si dices que no irás a ningún lado...", "Kirino"),
    309: ("Solo por hoy... Solo por hoy, durmamos juntos...", "Kirino"),
    310: ("Err...", "Kyousuke"),
    311: ("¿Qué quieres decir?", "Kyousuke"),
    312: ("Guh, ¡no puedo creerlo! ¡¿Quieres que lo diga una segunda vez?!", "Kirino"),
    313: ("¡Dije que durmamos juntos! Más bien, ¡vamos a dormir juntos! ¡No tienes el derecho a negarte!", "Kirino"),
    314: ("¡¿Por qué estás perdiendo los estribos mientras pides un favor?!", "Kyousuke"),
    315: ("¡No des excusas tediosas! Es solo dormir juntos, ¿no?!", "Kirino"),
    316: ("¡C-O-M-O D-I-J-E! No puedo entender incluso si de repente dices que vamos a dormir juntos...", "Kyousuke"),
    318: ("Así es. Es un trabajo simple que implica solo subirse a la misma cama y dormir apretados.", "Kirino"),
    324: ("No hay manera de que mi hermanita pueda ser así de lin--", "Kyousuke"),
    325: ("E-Está bien, ¿no?", "Kirino"),
    326: ("¡Oye oye! Soy un chico, después de todo... Err...", "Kyousuke"),
    327: ("...Tu respuesta.", "Kirino"),
    328: ("¿Eh?", "Kyousuke"),
    329: ("¿Cuál es tu respuesta? ¿Estás de acuerdo? ¿O no?", "Kirino"),
    330: ("...¿Tú estás de acuerdo?", "Kyousuke"),
    331: ("¿Qué estás diciendo tan tarde?", "Kirino"),
    332: ("Oye.", "Kirino"),
    333: ("De ahora en adelante, voy... a llamarte Kyousuke...", "Kirino"),
    334: ("Ya no somos... hermanos, ¿verdad?", "Kirino"),
    336: ("Oye, ¿escucharás... lo que tengo que decir por un momento?", "Kirino"),
    337: ("¿Por qué estás siendo tan formal?", "Kyousuke"),
    338: ("E-¡Basta! ......Solo cállate y escucha.", "Kirino"),
    339: ("Los dos nunca... hablamos entre nosotros ni siquiera en casa hasta que nuestra relación se volvió así, ¿verdad?", "Kirino"),
    341: ("Cuando descubriste que el DVD de Meruru era mío, pensé que todo había terminado.", "Kirino"),
    342: ("Pensé que definitivamente te burlarías de mí, me llamarías asquerosa y me odiarías...", "Kirino"),
    343: ("Pero no lo hiciste. Dijiste que no me despreciabas. Aceptaste mi hobby otaku.", "Kirino"),
    344: ("......Estaba realmente feliz.", "Kirino"),
    345: ("¿Kirino?", "Kyousuke"),
    346: ("¿Qué pasa con esa cara? ¿Es que agradecerte es tan extraño?", "Kirino"),
    347: ("N-No... No es eso...", "Kyousuke"),
    348: ("Nunca pensé que llegaría el día en que me hablaras de tal manera, así que me siento un poco... inesperadamente feliz.", "Kyousuke"),
    349: ("...Idiota.", "Kirino"),
    350: ("Continúo.", "Kirino"),
    351: ("Claro...", "Kyousuke"),
    352: ("Después de que descubriste mi hobby otaku, te pedí una consulta de vida.", "Kirino"),
    353: ("Tenías una cara de disgusto, pero aun así... escuchaste adecuadamente mis problemas.", "Kirino"),
    354: ("Todavía era tu hermano mayor en ese entonces, así que pensé que eso era solo natural.", "Kyousuke"),
    355: ("...Ya veo. Como hermano mayor, huh...", "Kirino"),
    356: ("Pero, eso todavía fue algo que me hizo extremadamente feliz.", "Kirino"),
    357: ("Pensaste en mí. Trataste de entenderme.", "Kirino"),
    358: ("Cuando pensé en eso, no pude parar. La consulta de vida que solo se suponía que sería una vez no se detuvo en una.", "Kirino"),
    359: ("Me alegré de que fueras tan amable, y tan feliz que me pregunté si estaba soñando en ese momento.", "Kirino"),
    360: ("No importa qué cosa irrazonable dijera, seguías siendo mi aliado. Incluso aunque me odiaras...", "Kirino"),
    361: ("Fue... lo mismo para ti, ¿verdad?", "Kyousuke"),
    362: ("Lo fue...", "Kirino"),
    363: ("...Fue diferente para mí.", "Kirino"),
    364: ("¿Eh...?", "Kyousuke"),
    365: ("Fue... diferente... para mí...", "Kirino"),
    366: ("Lo escondí hasta ahora, pero... ya no puedo hacerlo... simplemente no puedo...", "Kirino"),
    367: ("Y-Yo... he...", "Kirino"),
    368: ("Siempre, siempre, me... gustaste.", "Kirino"),
    369: ("...Te lo digo ahora, esto no es una mentira.", "Kirino"),
    370: ("......Te amo, Kyousuke.", "Kirino"),
}

with open(PATH, "r", encoding="utf-8") as f:
    current = json.load(f)
entry = current.get("000scriptMGIM_0000.obj", {})
entry.update(build(n, s))
current["000scriptMGIM_0000.obj"] = entry
with open(PATH, "w", encoding="utf-8") as f:
    json.dump(current, f, ensure_ascii=False)
print("updated 000scriptMGIM_0000.obj (part C)")