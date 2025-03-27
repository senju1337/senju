# senju

## ideen

- daily sprachcontent (wort haiku kanji satz), static site generator
- fantasynamegenerators.com aber schlechter (aber gut)
- fakenews generator

- ki metapromptengine
- erstelle deine pizzasorte
- gib mir zutaten -> generiere rezept
- dutch master dnd
- news aggregator
- chatraum
- minecraft skin generator

## Fragen

- [ ] ist ein static site generator ok?
- [ ] wie KI einbinden? LLM api ok? Wie siehts mit cash money aus?

## senji - Haikus

- Tägliches Wort
- Hauku (vor)generiert aus dem täglichen Wort
- Haikus generieren aus Prompt
- Haikus generieren aus Bild
- Bild zu Haiku generieren
- Haikus vorlesen

## Komponenten

- APICallHandler (Haiku Generator und irgendwas anderes externes)
- PeriodicContentSource (Daily-Dingsbums-Generator)
- URLRoutingManager (das ding was url routen für flaks setzt)
- ConfigurationManager (das ding was konfigurationen speichert)
- TrascriptionServiceManager (das ding was aus bild text für nen haiku prompt macht)
