[English Version →](../../../en/projects/project-08-graph-engineering-first-graph/)

# Project 08. Dibuja Tu Flujo de Trabajo como un Grafo

> Lección relacionada: [L14. De los Loops Únicos a la Ingeniería de Grafos](./../../lectures/lecture-14-graph-engineering/index.md)

## Qué Harás

Este es el proyecto de transición de "Loop" a "Graph". En la lección anterior construiste un loop maker-checker — implementar, verificar, dar feedback, implementar de nuevo — donde todas las decisiones ocurrían dentro de la ventana de contexto del mismo agente. En esta lección, lo que harás es **dibujar explícitamente la estructura que estaba escondida dentro del loop**: nodos, aristas, estado compartido y reglas de routing, escritas palabra por palabra.

Harás tres experimentos progresivos: primero dibujarás el loop maker-checker de P07 como un grafo explícito, luego añadirás un nodo paralelo de fan-out/fan-in, y finalmente añadirás una arista de retroceso condicional y un nodo de aprobación humana. Cuando termines, lo habrás sentido de primera mano: **el grafo no es un invento nuevo — es en lo que tu loop se convierte por sí solo cuando se vuelve lo bastante complejo.**

## Herramientas Que Usarás

- Claude Code o Codex
- Git
- El loop maker-checker que construiste en P07 (o cualquier flujo de trabajo de agente que puedas ejecutar repetidamente)
- Un editor de texto o una herramienta de diagramas (dibujar no es para que se vea bonito — es para dejar la estructura escrita con claridad; tanto `mermaid` como un `graph.md` escrito a mano valen)

## Pasos

### Preparación

1. Parte del repositorio donde terminaste P07, o usa directamente cualquier flujo de trabajo de agente que estés ejecutando.
2. Crea tres ramas: `p08-explicit-graph`, `p08-parallel`, `p08-human-in-the-loop`.
3. Prepara un `state.md` como archivo de estado compartido: los requisitos, el progreso y los resultados de verificación se escriben aquí. Es el "espacio de trabajo común" del grafo.

### Experimento 1: Dibuja el Loop como un Grafo Explícito

Cambia a la rama `p08-explicit-graph`.

1. **Enumera todos los nodos**: escribe cada paso del loop maker-checker de P07 como un nodo. Para cada nodo deja claro: su responsabilidad, sus entradas, sus salidas, y si es un agente o código determinista.
2. **Dibuja todas las aristas**: enumera cada arista entre nodos. Marca con énfasis dos aristas especiales:
   - Arista condicional: la verificación pasa/falla, por cuál se va
   - Arista de retroceso: el fallo vuelve a qué nodo
3. **Escribe el estado compartido**: enumera explícitamente qué campos hay en el estado (requisitos, código, resultados de tests, conclusiones de revisión) y quién los lee y quién los escribe.
4. **Escribe las reglas de routing**: anota con el if-then más simple las reglas de "a dónde ir a continuación", por ejemplo:
   ```
   if la verificación pasa → nodo de merge
   if la verificación falla → nodo de implementación
   if el nodo de implementación tiene información insuficiente → nodo de investigación
   ```
5. **Escríbelo como `graph.md`**: organiza todo lo anterior en un documento. Dibuja un grafo con mermaid y adjunta la tabla de nodos y las reglas de routing.
6. **Responde esta pregunta**: cuando termines de dibujar, encuentra al menos una **arista que antes era implícita** — una ruta de decisión que estaba escondida en el contexto del agente y que ni siquiera tú sabías que existía.

### Experimento 2: Añade un Nodo de Fan-out / Fan-in Paralelo

Cambia a la rama `p08-parallel`.

1. **Elige un punto paralelizable**: busca en la tarea un lugar que se pueda dividir en dos partes independientes. Por ejemplo:
   - La implementación se divide en dos módulos independientes, dos agentes los escriben en paralelo
   - La verificación se divide en dos revisiones independientes: uno ejecuta tests y lint, otro hace la revisión de código (instrucciones diferentes, enfoques diferentes)
   - La investigación se divide en dos direcciones, dos agentes exploran cada una
2. **Escribe la regla de fan-out**: registra en el estado compartido que "esta tarea se dividió en N sub-tareas paralelas", cada sub-tarea con un context independiente y un nodo independiente.
3. **Escribe la regla de fan-in**: cuando todas las sub-tareas terminen, ¿quién fusiona los resultados? ¿Cuál es el criterio de fusión (por ejemplo: solo se fusiona si ambas revisiones pasan, o basta con que pase una)?
4. **Aísla con worktrees**: cada sub-tarea paralela corre en un git worktree independiente, evitando físicamente colisiones de archivos (repasa la primitiva de Worktree de la Lección 13).
5. **Ejecútalo una vez y regístralo**: registra el tiempo wall-clock antes y después del paralelismo, el consumo de tokens y la calidad de los resultados. ¿El paralelismo es realmente más rápido? ¿O el overhead de coordinación se comió el tiempo ahorrado?

### Experimento 3: Añade una Arista de Retroceso y un Nodo de Aprobación Humana

Cambia a la rama `p08-human-in-the-loop`.

Este es el más importante de los tres experimentos. Añadirás dos tipos de nodos al grafo:

1. **Arista de retroceso condicional**: añade al nodo de verificación una ruta de "aprobado parcialmente" — no devolver todo al nodo de implementación, sino volver con feedback concreto al **nodo donde se originó el problema**. Por ejemplo: los tests pasan todos pero la revisión de código detecta un malentendido de los requisitos — se retrocede al nodo de investigación, no al de implementación. Esto exige que tu estado compartido registre "en qué capa está el problema".
2. **Nodo de aprobación humana (Human-in-the-loop)**: añade un nodo humano antes del nodo de merge. Cuando el flujo llega aquí, el grafo **se detiene** y espera a que escribas "aprobar" o "rechazar" en `state.md`. El nodo de aprobación puede tener una regla de timeout: si no hay respuesta después de N horas, se rechaza automáticamente o se escala automáticamente.
3. **Escribe el formato del interrupt**: cómo redactar claramente la petición de aprobación — qué pasó, qué cambió, por qué se necesita a una persona, y cuáles son las consecuencias de aprobar o rechazar.
4. **Ejecuta al menos 2 rondas completas**: en cada ronda el flujo llega al nodo de aprobación humana, y tú apruebas o rechazas una vez. Registra: ¿tu decisión de aprobación coincidió con el juicio del nodo de verificación? ¿El nodo de aprobación detuvo algo que el nodo de verificación no había detenido?

## Cómo Medir los Resultados

| Métrica | Experimento 1 (grafo explícito) | Experimento 2 (paralelo) | Experimento 3 (colaboración humano-máquina) |
|---------|-------------------------------|--------------------------|--------------------------------------------|
| Visibilidad de la estructura | ¿Cuántas aristas implícitas encontraste? | ¿El estado compartido soporta las sub-tareas paralelas? | ¿La arista de retroceso puede localizar con precisión la capa del problema? |
| Localización del fallo | Cuando falla, ¿puedes señalar directamente qué arista está mal? | Cuando falla una sub-tarea paralela, ¿puedes localizar cuál es? | Cuando se rechaza la aprobación, ¿puedes señalar de qué capa es el problema? |
| Coste de colaboración | ¿Cuánto tardaste en dibujar el grafo? | Tiempo ahorrado por el paralelismo vs. overhead de coordinación | Tiempo de espera de aprobación vs. valor de los problemas detenidos |
| Observabilidad | ¿Ahora se puede ver qué pasó en cada paso? | ¿El estado de cada sub-tarea paralela es visible? | ¿La petición de aprobación está escrita con la claridad suficiente? |
| Fiabilidad | ¿La descripción del grafo coincide con la ejecución real? | ¿El criterio de fusión de fan-in es sólido? | ¿Las reglas de timeout/escalado se disparan de verdad? |

## Qué Entregar

- `graph.md` (la descripción completa del grafo del Experimento 1: grafo mermaid + tabla de nodos + tabla de aristas + campos del estado compartido + reglas de routing)
- La lista de aristas implícitas encontradas en el Experimento 1 (al menos una)
- Las reglas de fan-out/fan-in del Experimento 2 y el registro de una ejecución paralela (comparación de tiempo/coste/calidad)
- Las reglas de la arista de retroceso del Experimento 3, el formato del nodo de aprobación y el registro de 2 rondas de colaboración humano-máquina
- Revisión final: de loop a grafo, ¿qué cambió en tu forma de trabajar? ¿Qué tareas merecen dibujarse y cuáles no?

## Lecciones Relacionadas

- [Lecture 14 — De los Loops Únicos a la Ingeniería de Grafos](../../lectures/lecture-14-graph-engineering/index.md)
- [Lecture 13 — Del Prompting Manual a los Loops Autónomos](../../lectures/lecture-13-loop-engineering/index.md) (tu loop es un nodo dentro del grafo; este proyecto despliega la estructura interna del nodo)
- [Lecture 09 — Evita que los agentes declaren victoria demasiado pronto](../../lectures/lecture-09-why-agents-declare-victory-too-early/index.md) (por qué el nodo de verificación debe ser independiente del nodo de implementación; en el grafo es un problema estructural)
- [Lecture 11 — Haz observable el runtime del agente](../../lectures/lecture-11-why-observability-belongs-inside-the-harness/index.md) (cuanto más complejo es el grafo, más necesario es ver qué está haciendo cada nodo)
