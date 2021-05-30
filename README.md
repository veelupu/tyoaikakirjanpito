# Työaikakirjanpito

## Sovellus

Työaikakirjanpito on websovellus, jolla voi seurata omaa työ- tai opiskeluajankäyttöään. Käyttäjä voi luoda sovellukseen tunnuksen. Työnteon aloittaessaan käyttäjä kirjautuu sisään sovellukseen, kertoo, mistä työstä ja työtehtävästä on kyse ja aloittaa työajan tallentamisen. Halutessaan käyttäjä voi lisätä muistiinpanoja työntekoon liittyen. Työajan voi keskeyttää esimerkiksi tauon ajaksi, tai tehdäkseen välillä muuta työtä tai työtehtävää. Kun työajan tallentamisen lopettaa, se näkyy sovelluksen tilastonäkymässä, ja käyttäjä voi kirjautua ulos sovelluksesta.

Käyttäjä voi tallentaa sovellukseen useita eri työpaikkoja ja työpaikkojen sisällä voi olla useita eri työtehtäviä. Sovellus laskee summia ja keskiarvoja päivässä, viikossa ja kuukaudessa käytetystä työajasta sekä työpaikka- tai työtehtäväkohtaisesti. Sovellus piirtää myös graafeja käytetystä työajasta.

Käyttäjä voi selata menneitä työajantallennuksia. Tallennuksia voi järjestää ja suodattaa esimerkiksi ajankohdan, työpaikan tai työtehtävän mukaan. Käyttäjä voi myös käyttää hakusanaa löytääkseen tietyn tallennuksen siihen lisättyjen muistiinpanojen perusteella.

## Nykyinen tilanne

Sovelluksesta on toteutettu suurin osa rakenteesta: Sovellukseen pääsee kirjautumaan sisään, ja sovelluksessa voi navigoida Tallenna- ja Selaa-sivuille. Tallenna-sivulla voi valita työtehtävän ja aloittaa tallennuksen sekä pysäyttää tallennuksen. Sovellus ei vielä tallenna työaikakirjanpitoa tietokantaan. Sovelluksesta voi myös kirjautua ulos.

Sovellusta voi testata [Herokussa](https://tsoha-tyoaikakirjanpito.herokuapp.com). Kirjautumiseen käytetään tunnusta "kokeilija" ja salasanaa "kokeilen". Nämä on tallennettu tietokantaan.

Seuraavat askeleet sovelluksen kehityksessä ovat työtehtävien ja työajankirjausten tallentaminen tietokantaan sekä uusien työtehtävien lisäämisen ja käyttäjätunnusten luomisen mahdollistaminen käyttäjälle. Tässä yhteydessä lisätään myös salasanojen salaus.
