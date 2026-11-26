# Documentación de los datapacks – Desmadre 3.0

*Servidor Minecraft 1.21.1 · NeoForge · Cobblemon 1.8.x · pack_format 48 · Actualizado el 25 de noviembre de 2026*

## 1. Resumen

El servidor usa dos datapacks y un resource pack. Los datapacks comparten el namespace `desmadre` y no chocan: el de economía define funciones en la raíz (`desmadre:banco`, `desmadre:mercado`…) y el del castillo usa subcarpetas (`castillo/`, `coliseo/`, `rotacion/`, `apuestas/`, `tablero/`, `economia/`, `recompensa/`).

| Archivo | Para qué sirve |
|---|---|
| `desmadre_economia.zip` | Banco y Mercado (48×48), mercaderes, tiendas y banco de CobbleDollars. |
| `desmadre_castillo.zip` | Castillo de 120×80 y coliseo adaptable al bioma, 30 clases de NPC competitivos con equipos que rotan, reaparición automática, dificultad por jugador, apuestas, tablero de victorias, loot y luces anti-monstruos. |
| `desmadre_skins.zip` | Resource pack (no es datapack) con las skins de los NPC. |

**Instalación:** los datapacks van en `world/datapacks/` y se ejecuta `/reload`. El resource pack va en `resourcepacks` de cada jugador, o se distribuye con `resource-pack` y `resource-pack-sha1` en `server.properties`.

**Requisitos de mods:** Cobblemon, CobbleDollars, Mega Showdown, Create (solo detalles del mercado).

**Importante:**
- Los bloques de comandos del Banco y del Mercado hacen reaparecer a los mercaderes. En tu `server.properties` está `enable-command-block=false`: esos bloques no se ejecutan hasta que lo cambies a `true` y reinicies.
- `function-permission-level=2`: las funciones corren con permisos suficientes. Los comandos de administración requieren ser operador.

## 2. Datapack 1: desmadre_economia

### 2.1 Contenido
- `pack.mcmeta` («Desmadre 3.0 - Economia y Banco», pack_format 48).
- `data/desmadre/function/*.mcfunction`: 16 funciones.
- `data/cobbledollars/cobbledollars/shop/`: 4 tiendas (`default`, `equipamiento`, `formas`, `luces`).
- `data/cobbledollars/cobbledollars/bank/default.json`: banco con 613 entradas (objeto → precio).

### 2.2 Comandos del administrador
Los que construyen toman como origen la esquina noroeste de la obra, a nivel del suelo.

| Comando | Dónde | Qué hace |
|---|---|---|
| `/function desmadre:banco` | Esquina noroeste, mirando al norte | Construye el Banco (11×9) con plaza, cartel y banquero. |
| `/function desmadre:mercado` | Esquina noroeste de un bloque de 3×3 chunks (X y Z múltiplos de 16) | Construye el Mercado Create × Cobblemon (48×48), con banco, mercaderes y detalles. |
| `/execute positioned X Y Z run function desmadre:banco_demoler` | X Y Z = base de la columna de cuarzo noroeste | Elimina el banco y al banquero. |
| `/execute positioned X Y Z run function desmadre:mercado_demoler` | Base de la columna noroeste del mercado | Elimina el mercado y los mercaderes; restaura tierra y pasto. |
| `/execute positioned X Y Z run function desmadre:agregar_luces` | Base noroeste del banco | Agrega el puesto Mercado General a un banco existente. |
| `/execute positioned X Y Z run function desmadre:agregar_mercaderes` | Base noroeste del mercado | Agrega los mercaderes Equipo y Formas a un mercado existente. |
| `/function desmadre:blindar` | Cualquier lugar | Hace invulnerables e inmóviles a los aldeanos con tag `puesto`. |
| `/function desmadre:congelar` | Cualquier lugar (se reprograma solo) | Congela y blinda a los vendedores con profesión y les pone el tag `congelado`. |

### 2.3 Funciones internas
`banco_estructura`, `mercado_estructura`, `mercaderes_estructura`, `luces_estructura`, `mercado_create`, `mercado_cobblemon`, `banco_demoler_estructura`, `mercado_demoler_estructura`: dibujan y borran las estructuras; no se ejecutan a mano.

### 2.4 Banco
- 11×9 bloques, plaza de polished andesite y camino de smooth quartz.
- **Banquero:** aldeano dorado, tags `banquero` y `puesto`, invulnerable.
- **Reaparición:** un bloque de comandos con una placa dorada invoca de nuevo al banquero si no hay uno a 20 bloques.
- **Mercado General:** segundo vendedor (tags `luces` y `puesto`) con su vitrina `cobblemon:display_case`.

### 2.5 Mercado
Ocupa 3×3 chunks: avenidas de smooth stone, plaza central con Poké Ball y carteles luminosos. Zonas: entrada norte, Cobblemon (oeste), Create (este), puestos laterales (Granja, Madera, Flores, Balls, Comida, Bayas) y los mercaderes Equipo y Formas.

### 2.6 Mercaderes y etiquetas
| Mercader | Tags |
|---|---|
| Banquero | `banquero`, `puesto` |
| Mercado General | `luces`, `puesto` |
| Equipo Pokémon | `equipo`, `puesto` |
| Formas Pokémon | `formas`, `puesto` |

El tag `congelado` lo agrega `congelar` cuando ya los inmovilizó.

### 2.7 Tiendas de CobbleDollars (resumen)
- **default (15 categorías):** Poké Balls, Exp, Medicina, Evolución, Minerales, Compactos, Construcción, Madera, Comida, Herramientas, Armaduras, Redstone y más, Create, Mochilas, Viajes.
- **equipamiento (5):** Ofensivos, Defensivos, Estratégicos, Entrenamiento, Evolutivos (5.000 – 300.000).
- **formas (6):** Llaves Mega, Megapiedras (47, a 200.000), Megas Z-A (34, a 250.000), Dynamax, Nidos Raid, Tera.
- **luces (9):** Luces, Iluminación, Invisibles, Semillas, Árboles, Cultivos, Básicos, Utilidades, Hogar.
- **bank/default.json:** 613 entradas `{ "item": "cobblemon:poke_ball", "price": "2000" }`.

### 2.8 Asignar tienda y banco a cada mercader
Se ejecuta como operador. Espera unos segundos después de que los aldeanos tomen su profesión.

```
/cm edit @e[type=villager,tag=banquero,limit=1] set shop cobbledollars:default
/cm edit @e[type=villager,tag=banquero,limit=1] set bank cobbledollars:default
/cm edit @e[type=villager,tag=luces,limit=1] set shop cobbledollars:luces
/cm edit @e[type=villager,tag=luces,limit=1] set bank cobbledollars:default
/cm edit @e[type=villager,tag=equipo,limit=1] set shop cobbledollars:equipamiento
/cm edit @e[type=villager,tag=equipo,limit=1] set bank cobbledollars:default
/cm edit @e[type=villager,tag=formas,limit=1] set shop cobbledollars:formas
/cm edit @e[type=villager,tag=formas,limit=1] set bank cobbledollars:default
```

Comprobar: `/cm open shop cobbledollars:equipamiento` y `/cm open shop cobbledollars:formas`; luego clic derecho en cada aldeano (Shift + clic derecho abre el banco).

Si da error de UUID: `/tellraw @s {"selector":"@e[type=villager,tag=formas,limit=1]"}`, copia el UUID y repite el comando con él en lugar del selector. También sirve el Omnitool de CobbleDollars. Si un aldeano reaparece con la placa dorada, hay que repetir sus dos comandos.

## 3. Datapack 2: desmadre_castillo

### 3.1 Contenido
- `data/desmadre/npcs/`: 30 clases de NPC (4 del castillo con 2 variantes cada una y 9 del coliseo con 1 variante).
- `data/desmadre/loot_table/`: 4 tablas de loot.
- `data/desmadre/function/{castillo,coliseo,rotacion,apuestas,tablero,economia,recompensa}/`.
- `data/minecraft/tags/function/load.json` y `tick.json`: ejecutan `castillo/init` al cargar y `castillo/tick`, `apuestas/tick`, `rotacion/tick` cada tick.

### 3.2 Comandos del administrador
| Comando | Qué hace |
|---|---|
| `/function desmadre:castillo/construir` | Construye el castillo (≈6.700 comandos; lag unos segundos). Parado en la esquina noroeste, mirando al sur. Al final lanza el ciclo de reaparición. |
| `/function desmadre:castillo/demoler` | Borra el castillo y marcadores, parado en el mismo punto. Detiene los ciclos. |
| `/function desmadre:castillo/ciclo` | Fuerza el ciclo de reaparición (castillo y coliseo): cada punto sin NPC a 6 bloques recupera su entrenador. Corre solo cada 600 ticks (30 s). |
| `/function desmadre:castillo/renovar` | Elimina los NPC de puntos sin jugadores a 40 bloques; el ciclo los recrea. |
| `/function desmadre:castillo/renovar_auto` | Renueva y se repite cada 1.800 s. Se inicia con `construir`. |
| `/function desmadre:castillo/antimobs` | Limpia hostiles del castillo y del coliseo (se repite cada 10 s). |
| `/function desmadre:castillo/diagnostico` | Cuenta marcadores y NPC cargados. |
| `/function desmadre:castillo/init` | Crea scoreboards y reinicia ciclos (corre solo al cargar). |
| `/spawnnpc desmadre:<clase> 5` | Aparece un NPC donde estás parado; el 5 es el nivel de IA (por defecto vale 1). Con coordenadas: `/spawnnpcat <x y z> <clase> 5`. |
| `/execute as <jugador> run function desmadre:recompensa/<clase>` | Prueba la recompensa sin pelear. |
| `/scoreboard players set <jugador> dm_nivel <1-3>` | Fija la dificultad de un jugador. |
| `/scoreboard players get <jugador> dm_nivel` | Consulta la dificultad. |

Clases para `spawnnpc`: `veterano`, `elite`, `campeon`, `jefe`, `col_red`, `col_blue`, `col_lance`, `col_steven`, `col_cynthia`, `col_wallace`, `col_iris`, `col_leon`, `col_diantha`; y sus variantes `_b` y `_c`.

### 3.3 Comandos de los jugadores
| Comando | Qué hace |
|---|---|
| `/function desmadre:castillo/menu` | Menú con botones: Normal x1, Difícil x2, Extremo x3. |
| `/trigger dm_dificultad set <1-3>` | Lo que ejecutan los botones. |

### 3.4 Funciones internas
`castillo/tick`, `castillo/set_nivel`, `castillo/spawn_<clase>` (eligen la variante de equipo según la rotación y llaman a `spawnnpcat ~ ~ ~ <clase> 5`; incluyen las del coliseo), `castillo/demoler_bloques`, `castillo/p00_cimientos` … `p13_luces` (14 etapas de la construcción).

### 3.5 Clases de entrenadores
IA al máximo (`skill: 5`), curan su equipo solos, IVs 31 y EVs de torneo. Cooldown en ticks (20 = 1 s), **por jugador**.

| Clase | Nombres | Nivel | Cooldown | Equipo A |
|---|---|---|---|---|
| `veterano` | Marco, Lía, Tomás | 50 | 6.000 (≈5 min) | Garchomp, Skarmory, Starmie, Gengar, Scizor, Blissey |
| `elite` | Valeria, Dante | 70 | 12.000 (≈10 min) | Tyranitar (mega), Ferrothorn, Gyarados, Heatran, Latios, Excadrill |
| `campeon` | Ares, Selene | 100 | 24.000 (≈20 min) | Dragonite, Metagross (mega), Alakazam, Volcarona, Swampert, Weavile |
| `jefe` | Jefe Desmadre | 100 | 48.000 (≈40 min) | Salamence (mega), Kyogre, Dialga, Mewtwo, Lugia, Garchomp |

Cada NPC tiene `player_win_command` (`execute as {{player}} run function desmadre:recompensa/<clase>`) y `player_lose_command` (`.../apuestas/perder_<clase>`). Cobblemon reemplaza `{{player}}` por el nombre.

### 3.6 Dificultad por jugador
Se guarda en `dm_nivel`; sin elegir cuenta como Normal. Normal: 1 tirada de loot y dinero x1; Difícil: 2 tiradas y x2; Extremo: 3 tiradas y x3. **Limitación:** solo escala el premio, no los equipos.

### 3.7 Recompensas
Dinero (Normal / Difícil / Extremo): Veterano 50.000 / 100.000 / 150.000; Élite 150.000 / 300.000 / 450.000; Campeón 400.000 / 800.000 / 1.200.000; Jefe 1.000.000 / 2.000.000 / 3.000.000.

Loot por tirada:
- **Veterano:** Rare Candy ×1–2 y 1–2 premios (Exp Candy L, Max Revive, Ultra/Luxury Ball, objetos Choice, Leftovers, Life Orb, Lucky Egg, diamantes).
- **Élite:** Rare Candy ×2–4 y 2–3 premios (Exp Candy XL, Ability Capsule, Destiny Knot, Shiny Stone, objetos de combate, Max Mushroom, bloques de diamante, netherite scrap, Tera Shards).
- **Campeón:** Rare Candy ×4–8, Exp Candy XL ×3–6 y 2–3 premios (Ability Patch/Capsule, Master Ball, Dynamax Candy, Wishing Star, Stellar Tera Shard, netherite, manzana dorada encantada, Tera Shards, megapiedras).
- **Jefe:** Rare Candy ×10–16, una megapiedra (de 81), un premio entre Ability Patch, Master Ball, Stellar Tera Shard, Tera Orb, Dynamax Band, Keystone, Mega Bracelet y Wishing Star, y 2–3 premios entre netherite, bloques de diamante, Nether Star, Elytra, Tótem y manzanas doradas.

### 3.8 Ciclo de reaparición y protección
| Mecanismo | Frecuencia | Qué hace |
|---|---|---|
| `ciclo` | Cada 600 ticks (30 s) | Retira NPC de temporadas anteriores (sin jugadores a 40 bloques) y crea los que falten (sin NPC a 6 bloques). |
| `renovar_auto` | Cada 1.800 s | Borra NPC de puntos sin jugadores cerca; el ciclo los recrea. |
| `antimobs` | Cada 10 s | Elimina hostiles; no toca Pokémon ni NPC. |

**Luces anti-monstruos:** bloques `minecraft:light[level=15]` en rejilla de 8 bloques por todo el castillo, el coliseo y sus alrededores.

### 3.9 El castillo
120×80 bloques, 4 pisos de 12 de alto (suelos en y = 0, 12, 24, 36; techo en 48), cúpula de 22 de radio, torres de 58. Terreno plano y libre de ~140×115.

Etapas: `p00_cimientos`, `p01`–`p04_piso`, `p05_techo`, `p06_exterior`, `p07_emblema`, `p08_torres`, `p09_cupula`, `p10_plaza`, `p11_marcadores`, `p12_decoracion`, `p13_luces`.

Pisos: 1 Pradera (4 Veteranos), 2 Glaciar (3 Élite), 3 Voltaje (2 Campeones), 4 Abismo bajo la cúpula (1 Jefe). Decoración: 32 peluches de lana (12 especies), Poké Balls decorativas, candeleros y postes luminosos, 2 máquinas de curación.

### 3.10 Marcadores, scoreboards y programaciones
- Marcadores `dm_spawn` + `dm_<clase>` (entidades `marker`): 4 veterano, 3 elite, 2 campeon, 1 jefe en el castillo; 8 + 1 (`dm_col_<nombre>`) en el coliseo.
- `dm_origin` y `dm_origin_col`: definen las zonas de `antimobs`.
- Scoreboards: `dm_nivel`, `dm_dificultad` (trigger), `dm_tmp`, `dm_cfg` (configuración), `dm_apuesta` (trigger), `dm_ap_monto`, `dm_ap_clase`, `dm_ap_exp`, `dm_vic*`, `dm_der`.
- Programaciones: `renovar_auto` 1.800 s, `antimobs` 10 s; el ciclo corre por contador en tick.

### 3.11 Coliseo (se adapta al bioma)
Estadio circular de ~105×105. Se construye **parado en el centro** y no necesita terreno plano: rellena huecos, agua y vegetación bajo la base sin tocar la roca, y elimina lo que haya sobre el suelo (hasta 42 bloques).

```
/function desmadre:coliseo/construir
/function desmadre:coliseo/demoler
```

`demoler` se ejecuta parado en el mismo punto y deja los cimientos. `construir` lanza el ciclo, así que los entrenadores aparecen al terminar.

Diseño: arena de 20 de radio con Poké Ball, podio luminoso, gradas escalonadas (radios 23–40), muro de 20 de alto, arcada con 24 pilares, 24 contrafuertes, 4 puertas cardinales, 8 plataformas de colores a 13 bloques del centro y trono dorado central.

| Bioma | Material |
|---|---|
| Por defecto | Piedra y cuarzo |
| Desierto | Arenisca |
| Badlands y sabana | Terracota y arenisca roja |
| Nevados | Cuarzo y calcita |
| Bosque y jungla | Ladrillos musgosos y musgo |
| Taiga y montaña | Pizarra |
| Océano, río y playa | Prismarina |
| Pantano y manglar | Barro |

Biomas de mods: material por defecto salvo que compartan etiquetas de Minecraft.

| Clase | Entrenador | Mega (equipo A) | Plataforma | Recompensa |
|---|---|---|---|---|
| `col_blue` | Blue | Pidgeot | Azul | Campeón |
| `col_lance` | Lance | Aerodactyl | Naranja | Campeón |
| `col_steven` | Steven | Metagross | Gris | Campeón |
| `col_cynthia` | Cynthia | Garchomp | Negra | Campeón |
| `col_wallace` | Wallace | Swampert | Turquesa | Campeón |
| `col_iris` | Iris | Aggron | Magenta | Campeón |
| `col_leon` | Leon | Charizard X | Morada | Campeón |
| `col_diantha` | Diantha | Gardevoir | Rosa | Campeón |
| `col_red` | Red | Venusaur | Trono central | Jefe |

Los 8 dan la recompensa de Campeón y Red la de Jefe, vía `recompensa/col_gate` y `recompensa/col_boss` (suman además al contador del coliseo).

### 3.12 Rotación de equipos
Cada clase del castillo tiene 3 equipos (`veterano`, `veterano_b`, `veterano_c`; igual en `elite`, `campeon`, `jefe`); cada entrenador del coliseo tiene 2 (`col_red`, `col_red_b`…). Total: 30 clases.

| `#rot_modo` | Comportamiento |
|---|---|
| 0 | Siempre el equipo A. |
| 1 (defecto) | Por temporada; entrenadores de la misma clase llevan equipos distintos. |
| 2 | Aleatorio al reaparecer. |

La temporada dura `#rot_period` ticks (72.000 = 1 h). Al cambiar se avisa en el chat, los NPC actuales se marcan `dm_viejo` y el ciclo los retira cuando no hay jugadores a 40 bloques (si alguien pelea con ellos, esperan).

| Comando | Qué hace |
|---|---|
| `/function desmadre:rotacion/rotar` | Cambia de temporada ahora. |
| `/function desmadre:rotacion/estado` | Temporada, modo y minutos restantes. |
| `/scoreboard players set #rot_modo dm_cfg 0` | Cambia el modo (0, 1, 2). |
| `/scoreboard players set #rot_period dm_cfg 72000` | Duración de la temporada. |
| `/scoreboard players set #ciclo_p dm_cfg 600` | Cada cuántos ticks revisa el ciclo. |

**NPC creados a mano:** la rotación solo reemplaza a los NPC que están junto a un marcador de aparición. Un NPC creado con `/spawnnpc` no tiene marcador, así que no rotaba. Ahora:

| Comando | Qué hace |
|---|---|
| `/function desmadre:npc/colocar {clase:"veterano"}` | Crea un punto de aparición donde estás parado y hace aparecer al NPC; desde ahí rota por temporadas y reaparece solo. Clases base: `veterano`, `elite`, `campeon`, `jefe`, `col_red`, `col_blue`, `col_lance`, `col_steven`, `col_cynthia`, `col_wallace`, `col_iris`, `col_leon`, `col_diantha`. |
| `/function desmadre:npc/quitar` | Quita el punto de aparición más cercano (a menos de 4 bloques) y su NPC. |
| `/function desmadre:npc/adoptar` | Registra como punto de aparición a cada NPC nuestro sin marcador cerca; también corre solo en cada ciclo. Lee la clase del NBT `NPCClass`. |
| `/function desmadre:npc/ver_nbt` | Muestra los datos del NPC más cercano, para comprobar la clave de la clase. |

La adopción automática depende de que Cobblemon guarde la clase en `NPCClass`; no está confirmado. Si un NPC manual no rota, elimínalo (`/kill @e[type=cobblemon:npc,distance=..5]`) y colócalo con `npc/colocar`. Un NPC con jugadores a menos de 40 bloques espera a que se alejen antes de cambiar de equipo.

### 3.13 Apuestas
El jugador apuesta CobbleDollars a que derrota a una clase. Si gana cobra apuesta × porcentaje; si pierde, la casa se la queda. Las del coliseo cuentan como Campeón (los 8) y Jefe (Red).

| Clase | Veterano | Élite | Campeón | Jefe |
|---|---|---|---|---|
| Paga (`#cuota1`–`#cuota4`) | 150% | 200% | 300% | 500% |

Montos por defecto: 10.000, 50.000, 100.000, 500.000 y 1.000.000 (`#m1`–`#m5`). Tiene 15 min (`#exp`, 18.000 ticks) para pelear. Cancelación con reembolso solo el primer minuto; al expirar la casa se la queda (con `#reembolso` en 1 se devuelve). Una apuesta activa por jugador.

| Comando | Quién | Qué hace |
|---|---|---|
| `/function desmadre:apuestas/menu` | Jugadores | Elegir clase y monto con botones. |
| `/function desmadre:apuestas/estado` | Jugadores | Ver apuesta y tiempo restante. |
| `/trigger dm_apuesta set <n>` | Jugadores | Botones: 1–4 (clase), 11–15 (monto), 90 (cancelar). |
| `/function desmadre:apuestas/diagnostico` | Admin | Prueba real: lee tu saldo, te da 1 y te quita 1. |
| `/function desmadre:apuestas/activar` | Admin | Abre las apuestas (solo si el diagnóstico salió OK). |
| `/function desmadre:apuestas/desactivar` | Admin | Las cierra; las en curso siguen. |

Arrancan **bloqueadas**. Mantén `monto × porcentaje` bajo ~2.100 millones. Si un jugador se desconecta en plena pelea no se registra derrota hasta que la apuesta expire.

### 3.14 Tablero de victorias
La barra lateral muestra las victorias de todos (también desconectados) y la lista de jugadores las muestra junto al nombre. Cuentan castillo y coliseo.

Scoreboards: `dm_vic` (total, el que se muestra), `dm_der`, `dm_vic_vet`, `dm_vic_eli`, `dm_vic_cam`, `dm_vic_jef`, `dm_vic_col`.

| Comando | Quién | Qué hace |
|---|---|---|
| `/function desmadre:tablero/ver` | Jugadores | Tus victorias, derrotas y desglose. |
| `/function desmadre:tablero/todos` | Jugadores | Victorias y derrotas de los jugadores en línea. |
| `/function desmadre:tablero/mostrar` y `ocultar` | Admin | Enciende o apaga la barra lateral. |
| `/function desmadre:tablero/reiniciar` | Admin | Borra todo (no se puede deshacer). |

### 3.15 Skins de los NPC (resource pack)
`desmadre_skins.zip`: 13 texturas de 64×128 (piel de jugador arriba y Poké Ball extra abajo) en `assets/cobblemon/textures/npc/desmadre/`, más 30 registros (uno por clase) en `assets/cobblemon/bedrock/npcs/variations/` y `bedrock/npc/variations/`. Cobblemon usa el identificador del NPC (`desmadre:<clase>`) como nombre del modelo; cada registro lleva `name`, poser `cobblemon:standard`, modelo `cobblemon:trainer.geo` y textura.

**Estado:** sin confirmar. Si los NPC se ven como muñecos, el registro no coincide con tu versión; hace falta la lista de carpetas de `assets/cobblemon/bedrock/` del jar y un `.json` de ejemplo. Tras cambiar el pack, elimina y recrea los NPC y recarga con `F3 + T`.

### 3.16 Economía (macros de CobbleDollars)
Todo comando de CobbleDollars pasa por `economia/`. Son macros que se leen al ejecutarse, así un formato equivocado no impide cargar el datapack.

| Función | Línea a editar si el formato cambia |
|---|---|
| `economia/dar` | `_dar.mcfunction`: `cobbledollars give @s $(monto)` |
| `economia/quitar` | `_quitar.mcfunction`: `cobbledollars remove @s $(monto)` |
| `economia/saldo` | `_saldo.mcfunction`: `cobbledollars query @s` |

### 3.17 Diagnóstico de reaparición
`/function desmadre:castillo/diagnostico` muestra cuántos marcadores y NPC hay cargados y cada cuántos ticks revisa el ciclo. Si no hay marcadores, estás lejos de la obra (más de ~100 bloques) o se construyó con una versión anterior.

## 4. Guías rápidas
**Montar el castillo:** copiar el zip, `/reload`, elegir terreno plano de ~140×115, pararse en la esquina noroeste mirando al sur, `/function desmadre:castillo/construir`.

**Desmontarlo:** parado en el mismo punto, `/function desmadre:castillo/demoler`.

**Montar el coliseo:** parado en el centro de un terreno libre de ~105×105, `/function desmadre:coliseo/construir`; luego `/function desmadre:castillo/diagnostico` debe mostrar los marcadores.

**Montar el mercado:** `/function desmadre:mercado`; solo el banco: `/function desmadre:banco`.

**Abrir las apuestas:** `apuestas/diagnostico` hasta ver «OK», `apuestas/activar`, y los jugadores usan `apuestas/menu`.

**Instalar las skins:** copiar el zip a `resourcepacks`, activarlo arriba, `F3 + T`, eliminar y recrear los NPC.

## 5. Supuestos y cosas sin verificar
Todo se validó por código (JSON correctos, tamaños de `fill`, funciones enlazadas) pero **no se probó en el juego**.

- **`cobbledollars give/remove/query`:** el formato se dedujo de los permisos del mod; el diagnóstico de apuestas los comprueba.
- **Pago duplicado:** CobbleDollars puede dar dinero por derrotar NPC (`config/cobbledollars`); apágalo si solo quieres los montos del castillo.
- **Aparición desde marcadores:** se usa `/spawnnpcat ~ ~ ~ <clase> 5`; falta confirmarlo en el servidor.
- **Megas de los NPC:** no se confirmó que mega-evolucionen con la piedra equipada.
- **Escaleras, cúpula, coliseo y peluches:** revisar visualmente tras construir.
- **Pokémon salvajes:** las luces frenan monstruos, no Pokémon.
- **Skins:** formato del registro sin confirmar (3.15).
- **Especies y movimientos:** Dragapult, Corviknight, Darkrai, Palkia y la megapiedra de Steelix podrían no existir; `light_ball`, `lum_berry` y `sitrus_berry` no están en tu tienda.
- **Rotación:** probar `/function desmadre:rotacion/rotar` y comprobar el cambio de equipos.
- **Mercader–tienda:** se asigna con `/cm edit` (2.8); falta confirmar que acepte selectores en lugar de UUID.

## 6. Solución de problemas
| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| Un mercader desaparece y no vuelve | `enable-command-block=false` | Ponerlo en `true`, reiniciar y pisar la placa dorada. |
| `construir` no hace nada | Datapack no cargado | `/datapack list`, `/reload`, revisar el log. |
| Castillo enterrado o flotando | Terreno no plano | `demoler`, nivelar y reconstruir. |
| Los entrenadores no aparecen solos | Versión anterior con `spawnnpc` desde marcador, o marcadores no cargados | Actualizar, `/reload`, `/function desmadre:castillo/diagnostico`, `/function desmadre:castillo/ciclo` y revisar el log. |
| Aparecen con IA débil | `spawnnpc` sin nivel (vale 1) | Marcadores: ya usan 5. Manual: `/spawnnpc desmadre:<clase> 5`. |
| Se duplican los NPC | Un NPC se alejó más de 6 bloques de su marcador | Revisar su comportamiento o subir la distancia en `castillo/ciclo`. |
| Siguen con el equipo anterior | Hay jugadores a menos de 40 bloques | Se cambian cuando nadie está cerca, o `/function desmadre:castillo/renovar`. |
| Ganas y no hay loot | `player_win_command` no se ejecuta | `/execute as <jugador> run function desmadre:recompensa/veterano`. |
| Llega el loot pero no el dinero | Formato de `cobbledollars give` | Editar `economia/_dar.mcfunction`. |
| Se cae el servidor al ganar | Callback propio leyendo variables ajenas | Este datapack no usa callbacks propios. |
| NPC como muñecos | El registro de skins no coincide | Ver 3.15. |
| Apuestas «desactivadas» | Falta el diagnóstico | `apuestas/diagnostico` y luego `activar`. |
| El tablero no se ve | Barra lateral oculta | `/function desmadre:tablero/mostrar`. |
| Lag al construir | Muchos comandos a la vez | Hacerlo con pocos jugadores conectados. |
