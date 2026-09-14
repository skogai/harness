[English Version →](../../../en/projects/project-08-graph-engineering-first-graph/)

# Projekt 08. Zeichne deinen Workflow als Graph

> Zugehörige Lektion: [L14. Von Einzel-Loops zu Graph Engineering](./../../lectures/lecture-14-graph-engineering/index.md)

## Was du tust

Das ist das Übergangsprojekt von „Loop“ zu „Graph“. In der letzten Lektion hast du einen Maker-Checker-Loop gebaut — implementieren, verifizieren, Feedback, neu implementieren, wobei alle Entscheidungen im Context Window desselben Agents stattfinden. Was du in dieser Lektion tust, ist, **die im Loop versteckte Struktur explizit herauszuzeichnen**: Knoten, Kanten, Shared State, Routing-Regeln — Wort für Wort niedergeschrieben.

Du machst drei fortschreitende Experimente: zuerst zeichnest du den Maker-Checker-Loop aus P07 als expliziten Graphen, dann fügst du dem Graphen einen parallelen Fan-out/Fan-in-Knoten hinzu und schließlich eine bedingte Rollback-Kante und einen menschlichen Freigabe-Knoten. Am Ende wirst du eines hautnah erleben: **ein Graph ist keine neue Erfindung — es ist das, was dein Loop wird, wenn er komplex genug geworden ist.**

## Werkzeuge, die du nutzt

- Claude Code oder Codex
- Git
- Deinen Maker-Checker-Loop aus P07 (oder jeden Agenten-Workflow, den du wiederholt ausführen kannst)
- Einen Texteditor oder ein Zeichen-Tool (zeichnen ist nicht für die Ästhetik, sondern um die Struktur klar zu schreiben; `mermaid` oder ein handgeschriebenes `graph.md` reichen)

## Schritte

### Vorbereitung

1. Starte von dem Repository, wie du es nach P07 verlassen hast, oder verwende direkt einen beliebigen Agenten-Workflow, den du gerade betreibst.
2. Erstelle drei Branches: `p08-explicit-graph`, `p08-parallel`, `p08-human-in-the-loop`.
3. Bereite eine `state.md` als gemeinsame Statusdatei vor: Anforderungen, Fortschritt und Verifikationsergebnisse werden hier hineingeschrieben. Das ist die „gemeinsame Werkbank“ des Graphen.

### Experiment 1: Den Loop als expliziten Graphen zeichnen

Wechsle zum Branch `p08-explicit-graph`.

1. **Liste alle Knoten auf**: Schreibe jeden Schritt des Maker-Checker-Loops aus P07 als einen Knoten. Notiere für jeden Knoten klar: seine Verantwortung, seine Eingabe, seine Ausgabe, ob er ein Agent oder deterministischer Code ist.
2. **Zeichne alle Kanten**: Liste jede Kante zwischen den Knoten auf. Markiere dabei besonders zwei spezielle Kanten:
   - Bedingte Kante: Verifikation bestanden/fehlgeschlagen, wohin sie führt
   - Rollback-Kante: bei Fehlschlag zurück zu welchem Knoten
3. **Schreibe den Shared State**: Liste explizit auf, welche Felder der Status hat (Anforderungen, Code, Testergebnisse, Review-Schlussfolgerung), wer sie liest und wer sie schreibt.
4. **Schreibe die Routing-Regeln**: Formuliere die „wohin als Nächstes“-Regeln in einfachster If-then-Sprache, zum Beispiel:
   ```
   if Verifikation bestanden → Merge-Knoten
   if Verifikation fehlgeschlagen → Implementierungs-Knoten
   if Implementierungs-Knoten hat nicht genug Infos → Recherche-Knoten
   ```
5. **Schreibe eine `graph.md`**: Halte die obigen Inhalte in einem Dokument fest. Zeichne mit mermaid einen Graphen, ergänze eine Knotentabelle und die Routing-Regeln.
6. **Beantworte diese Frage**: Zeige nach dem Zeichnen mindestens **eine Kante, die ursprünglich implizit war** — einen Entscheidungspfad, der vorher im Context des Agents versteckt war, von dem du selbst nicht wusstest, dass er existiert.

### Experiment 2: Einen parallelen Fan-out / Fan-in-Knoten hinzufügen

Wechsle zum Branch `p08-parallel`.

1. **Wähle einen Punkt, der parallelisiert werden kann**: Finde eine Stelle in der Aufgabe, die sich in zwei unabhängige Teile zerlegen lässt. Zum Beispiel:
   - Die Implementierung in zwei unabhängige Module aufteilen, zwei Agents schreiben parallel
   - Die Verifikation in zwei unabhängige Reviews aufteilen: eines führt Tests und Lint aus, eines macht Code-Review (verschiedene Anweisungen, verschiedene Blickwinkel)
   - Die Recherche in zwei Richtungen aufteilen, zwei Agents recherchieren jeweils einen Pfad
2. **Schreibe die Fan-out-Regel**: Halte im Shared State fest, dass diese Aufgabe in N parallele Teilaufgaben zerlegt wurde, jede mit einem unabhängigen Context und einem unabhängigen Knoten.
3. **Schreibe die Fan-in-Regel**: Wer mergt die Ergebnisse, wenn alle Teilaufgaben fertig sind? Was ist das Merge-Kriterium (z. B.: erst mergen, wenn beide Reviews bestanden sind, oder reicht schon eines)?
4. **Nutze Worktree-Isolation**: Führe jede parallele Teilaufgabe in einem unabhängigen Git-Worktree aus, um Dateikollisionen physisch zu vermeiden (denke an das Worktree-Primitiv aus Lektion 13 zurück).
5. **Führe es einmal aus und protokolliere**: Notiere die Wall-Clock-Zeit vor und nach der Parallelisierung, den Token-Verbrauch und die Ergebnisqualität. Ist die Parallelisierung wirklich schneller? Oder frisst der Koordinations-Overhead die gesparte Zeit wieder auf?

### Experiment 3: Eine Rollback-Kante und einen menschlichen Freigabe-Knoten hinzufügen

Wechsle zum Branch `p08-human-in-the-loop`.

Das ist das wichtigste der drei Experimente. Du fügst dem Graphen zwei Arten von Knoten hinzu:

1. **Bedingte Rollback-Kante**: Gib dem Verifikations-Knoten einen „teilweise bestanden“-Pfad — nicht immer komplett zurück zum Implementierungs-Knoten, sondern mit konkretem Feedback zurück zu **dem Knoten, der das Problem verursacht hat**. Zum Beispiel: Alle Tests bestanden, aber das Code-Review zeigt ein Missverständnis der Anforderungen — zurück zum Recherche-Knoten statt zum Implementierungs-Knoten. Das erfordert, dass dein Shared State festhält, „auf welcher Ebene das Problem liegt“.
2. **Menschlicher Freigabe-Knoten (Human-in-the-loop)**: Füge vor dem Merge-Knoten einen menschlichen Knoten hinzu. Dort **stoppt** der Graph, bis du in `state.md` „Genehmigen“ oder „Zurückweisen“ schreibst. Der Freigabe-Knoten kann eine Timeout-Regel haben: Wenn innerhalb von N Stunden keine Antwort kommt, automatisch zurückweisen oder eskalieren.
3. **Schreibe das Interrupt-Format**: Wie ist die Freigabe-Anfrage klar zu formulieren — was passiert ist, was geändert wurde, warum ein Mensch nötig ist, was die Folgen von Genehmigen/Zurückweisen jeweils sind.
4. **Führe mindestens 2 vollständige Durchläufe aus**: Gehe bei jedem Durchlauf bis zum menschlichen Freigabe-Knoten und genehmige oder weise selbst einmal zurück. Notiere: Stimmt deine Freigabe-Entscheidung mit der Beurteilung des Verifikations-Knotens überein? Hat der Freigabe-Knoten etwas abgefangen, das der Verifikations-Knoten nicht abgefangen hat?

## Wie man Ergebnisse misst

| Metrik | Exp 1 (Expliziter Graph) | Exp 2 (Parallel) | Exp 3 (Mensch+Maschine) |
|------|----------------|--------------|------------------|
| Struktur-Sichtbarkeit | Wie viele implizite Kanten hast du gefunden? | Kann der Shared State parallele Teilaufgaben tragen? | Kann die Rollback-Kante die Problemebene präzise lokalisieren? |
| Fehlerlokalisierung | Kannst du bei einem Fehlschlag direkt sagen, welche Kante falsch ist? | Wenn eine parallele Teilaufgabe fehlschlägt, kannst du die eine lokalisieren? | Kannst du bei einer Zurückweisung sagen, auf welcher Ebene das Problem liegt? |
| Kooperations-Overhead | Wie lange hat das Zeichnen gedauert? | Gesparte Zeit durch Parallelität vs. Koordinations-Overhead | Freigabe-Wartezeit vs. Wert der abgefangenen Probleme |
| Observability | Ist jetzt sichtbar, was bei jedem Schritt passiert? | Ist der Status jeder parallelen Teilaufgabe sichtbar? | Ist die Freigabe-Anfrage klar genug geschrieben? |
| Zuverlässigkeit | Stimmt die Graph-Beschreibung mit dem tatsächlichen Lauf überein? | Ist das Fan-in-Merge-Kriterium verlässlich? | Werden die Timeout-/Eskalationsregeln wirklich auslösen? |

## Was einzureichen ist

- `graph.md` (die vollständige Graph-Beschreibung von Experiment 1: mermaid-Graph + Knotentabelle + Kantentabelle + Shared-State-Felder + Routing-Regeln)
- Die Liste der impliziten Kanten aus Experiment 1 (mindestens eine)
- Die Fan-out/Fan-in-Regeln von Experiment 2 und ein Aufzeichnungsprotokoll eines parallelen Laufs (Zeit/Kosten/Qualitätsvergleich)
- Die Rollback-Kanten-Regel von Experiment 3, das Freigabe-Knoten-Format und 2 Durchläufe der Mensch+Maschine-Aufzeichnung
- Abschließendes Retro: Was hat sich von Loop zu Graph in deiner Arbeitsweise verändert? Welche Aufgaben sind einen Graphen wert, welche nicht?

## Zugehörige Lektionen

- [Lektion 14 — Von Einzel-Loops zu Graph Engineering](../../lectures/lecture-14-graph-engineering/index.md)
- [Lektion 13 — Von manuellen Prompts zu autonomen Loops](../../lectures/lecture-13-loop-engineering/index.md) (dein Loop ist ein Knoten im Graphen; dieses Projekt breitet die interne Struktur des Knotens aus)
- [Lektion 09 — Verhindern, dass Agenten zu früh Erfolg melden](../../lectures/lecture-09-why-agents-declare-victory-too-early/index.md) (warum der Verifikations-Knoten unabhängig vom Implementierungs-Knoten sein muss; in einem Graphen ist das ein strukturelles Problem)
- [Lektion 11 — Die Runtime des Agenten beobachtbar machen](../../lectures/lecture-11-why-observability-belongs-inside-the-harness/index.md) (je komplexer der Graph, desto mehr musst du sehen, was jeder Knoten tut)