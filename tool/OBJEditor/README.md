# OBJ.cs — copia corregida del exportador de scripts

`OBJ.cs` pertenece a la toolchain base ([zapan/FastAsyncOreimoTranslateTool]).
Aquí se guarda una copia con una corrección; `build_iso.bat` y `build_iso.sh`
la instalan sobre la toolchain descargada justo antes de compilar el driver.

Se vendoriza el archivo entero en lugar de usar un `.patch` (como
`toolchain-patches/repack-case.patch`) porque el flujo de Windows baja la
toolchain como ZIP, sin `git` ni `patch` disponibles para aplicar parches.

## Qué corrige

Un `.obj` es un array secuencial de bloques. Los saltos y las ramas se guardan
como **número de bloque**, así que cualquier bloque que se inserte desplaza a
todos los posteriores y obliga a reajustar esas referencias.

El exportador inserta bloques: cuando una línea traducida trae un marcador de
página `[...]`, la parte entre corchetes se escribe como un bloque extra de
continuación. `UpdateJumps()` reajustaba entonces las referencias de los saltos
(bloques `0x2BE`), pero **no** las de las decisiones del sistema **O.R.E.**
(bloques `0x515`, con el bloque destino de la rama "aceptar" en el offset
`0x0E`), que se copiaban tal cual.

Efecto en el juego: en una escena con al menos un corte `[...]` antes del
destino, aceptar una decisión O.R.E. saltaba a un bloque desplazado y el
jugador caía en la rama "rechazar" pasara lo que pasara.

Caso real: `000scriptAKYO_0030A.obj` (torneo de Siscalypse, disco 1). Dos
cortes de página antes del destino dejaban la referencia en el bloque 126
cuando ya debía ser el 128; aceptar la invitación de Kirino reproducía igual
`「Lo siento, pero pasaré.」` y cerraba la ruta.

La corrección extiende `UpdateJumps()` para desplazar también esa referencia.

## Y un off-by-one del mismo sitio

`UpdateJumps()` desplazaba toda referencia con `blockNumber >= minBlock`, donde
`minBlock` es el bloque que se acaba de partir. Pero ese bloque **conserva su
número**: solo se mueve lo que viene después. Con `>=`, una referencia que
apunte justo a ese diálogo acababa en su mitad de continuación, saltándose la
primera parte de la línea.

No lo dispara ninguna de las dos traducciones actuales (ningún salto ni decisión
apunta hoy a un diálogo con corte `[ ]`), pero sí lo dispararía otra traducción
que ponga un corte de página en una línea que resulte ser destino de una rama.
La condición ahora es `blockNumber <= minBlock`.

## Cómo comprobarlo

Alineando cada `.obj` regenerado con su original en inglés (`Data/Obj/`) y
comparando toda referencia a bloque, disco 1 da 1040 saltos `0x2BE` (7 que
debían desplazarse) y 123 decisiones `0x515` (1 que debía desplazarse), con
cero referencias rotas. Frente a la salida anterior al arreglo cambia
exactamente **1 byte**, el de esa referencia.

[zapan/FastAsyncOreimoTranslateTool]: https://github.com/zapan/FastAsyncOreimoTranslateTool
