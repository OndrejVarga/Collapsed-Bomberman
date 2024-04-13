# Collapsed Bomberman

## O Aplikácii

Collapsed Bomberman je vlastná implementácia klasickej arkádovej hry "Bomberman" s vylepšeným spôsobom generácie máp.
Ide o plne funkčnú hru pre jedného hráča. Ten sa zničiť všetkých nepriateľov za čo najkratší čas.
Každá mapa je generovaná pomocou Wave Function collapse algoritmu.

## Funkcionality:

- Procedurálne generované levely pomocou Wave Function collapse algoritmu
- Mierne upravené pravídlá klasickej hry Bomberman

## Inštalácia:

Hra vyžaduje prostredie obsahujúce

- pygame~=2.5.2
- scipy~=1.11.4
- numpy~=1.26.1
- pytest~=7.4.3
  Možno využiť:

```bash
pip install -r requirements.txt
```

# Spustenie

Hru je potrebné spustiť pomocou:

```bash
cd Semestralna_praca/
python main.py
```

# Ovládanie

- Hráč sa pohybuje pomocou klávesový šipiek.
- Bomba sa pokladá klávesou `space`.

# Testovanie

Pre spustenie testov postupujte:

```bash- Hráč sa pohybuje pomocou klávesový šipiek.
- Bomba sa pokladá klávesou `space`.

cd Semestralna_praca/
pytest app/tests.py
```

# Licencie

### 1-Bit Pack (C0 License)

Projekt využíva assety z 1-Bit Pack od autora [Kenney.nl](Kenney.nl).
- **Licencia:** [1-Bit Pack C0 License](https://creativecommons.org/publicdomain/zero/1.0/)
- **Zdroj:** [1-Bit Pack on OpenGameArt.org](https://opengameart.org/content/1-bit-pack)

### Press Start 2P Font (Open Font License)

Projekt využíva Press Start 2P font získaný z Google Fonts.
- **License:** [Open Font License (OFL)](https://opensource.org/licenses/OFL-1.1)
- **Source:** [Press Start 2P on Google Fonts](https://fonts.google.com/specimen/Press+Start+2P)
