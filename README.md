# Työaikakirjanpito

## Loppupalautus

Suuri osa sovelluksen suunnitellusta keskeisestä toiminnallisuudesta tuli valmiiksi. Kolmannen välipalautuksen jälkeen sovelluksen työajan tallennuslogiikkaa muutettiin vastaamaan enemmän aivan alkuperäistä ajatusta: käyttäjä tallentaa työajastaan samalla kertaa sekä aloitus- että lopetusajan, työtehtävät sekä mahdolliset muistiinpanot ja tauot. Sovellusta suunniteltaessa ja tehtäessä tämä ajatus muuttui, kuten alkuperäisestä sovelluksen kuvauksesta käy ilmi.

Käyttäjä voi nyt luoda itselleen tunnuksen, kirjautua sisään sovellukseen ja tehdä työajantallennuksia. Käyttäjä voi lisätä itselleen erilaisia työtehtäviä, joita hän voi liittää omiin työajantallennuksiinsa sekä kertoa, kuinka paljon hän piti taukoja työskentelynsä aikana. Taukoja ei lasketa mukaan varsinaiseen työaikaan. Käyttäjä voi lisäksi selata tekemiään tallennuksia kuluneelta päivältä, viikolta, kuukaudelta ja vuodelta sekä vaihtaa salasanansa. Etusivulla käyttäjälle näytetään yhteenveto tämän tekemästä työstä.

## Tilanne 3. välipalautuksen aikaan

Sovellukseen voi luoda itselleen käyttäjätunnuksen, kirjautua sisään ja ulos, vaihtaa salasanan, tarkastella tallennettuja työtehtäviä sekä tallentaa työaikaa tietyillä työtehtävillä ja muistiinpanoilla. Työaika tallentuu tietokantaan, mutta tallennuksen lopetettuaan käyttäjä ei vielä voi nähdä sitä.

Sovellusta voi testata [Herokussa](https://tsoha-tyoaikakirjanpito.herokuapp.com). Kirjautumiseen voi käyttää tunnusta "kokeilija" ja salasanaa "kokeilen" tai luoda oman tunnuksen. Huomaa, että kokeilutunnuksen salasanaa ei ole mahdollista vaihtaa.

Seuraavaksi sovelluksen koodia refaktoroidaan toiston poistamiseksi (Python-koodi) ja tuodaan työajantallennukset käyttäjän nähtäville.

## Tilanne 2. välipalautuksen aikaan

Sovelluksesta on toteutettu suurin osa rakenteesta: Sovellukseen pääsee kirjautumaan sisään, ja sovelluksessa voi navigoida Tallenna- ja Selaa-sivuille. Tallenna-sivulla voi valita työtehtävän ja aloittaa tallennuksen sekä pysäyttää tallennuksen. Sovellus ei vielä tallenna työaikakirjanpitoa tietokantaan, vaikka tietokanta tauluineen onkin jo luotu. Sovelluksesta voi myös kirjautua ulos.

Sovellusta voi testata [Herokussa](https://tsoha-tyoaikakirjanpito.herokuapp.com). Kirjautumiseen käytetään tunnusta "kokeilija" ja salasanaa "kokeilen". Nämä on tallennettu tietokantaan.

Seuraavat askeleet sovelluksen kehityksessä ovat työtehtävien ja työajankirjausten tallentaminen tietokantaan sekä uusien työtehtävien lisäämisen ja käyttäjätunnusten luomisen mahdollistaminen käyttäjälle. Tässä yhteydessä lisätään myös salasanojen salaus.

## Sovellus – suunnitelma kurssin alussa

Työaikakirjanpito on websovellus, jolla voi seurata omaa työ- tai opiskeluajankäyttöään. Käyttäjä voi luoda sovellukseen tunnuksen. Työnteon aloittaessaan käyttäjä kirjautuu sisään sovellukseen, kertoo, mistä työstä ja työtehtävästä on kyse ja aloittaa työajan tallentamisen. Halutessaan käyttäjä voi lisätä muistiinpanoja työntekoon liittyen. Työajan voi keskeyttää esimerkiksi tauon ajaksi, tai tehdäkseen välillä muuta työtä tai työtehtävää. Kun työajan tallentamisen lopettaa, se näkyy sovelluksen tilastonäkymässä, ja käyttäjä voi kirjautua ulos sovelluksesta.

Käyttäjä voi tallentaa sovellukseen useita eri työpaikkoja ja työpaikkojen sisällä voi olla useita eri työtehtäviä. Sovellus laskee summia ja keskiarvoja päivässä, viikossa ja kuukaudessa käytetystä työajasta sekä työpaikka- tai työtehtäväkohtaisesti. Sovellus piirtää myös graafeja käytetystä työajasta.

Käyttäjä voi selata menneitä työajantallennuksia. Tallennuksia voi järjestää ja suodattaa esimerkiksi ajankohdan, työpaikan tai työtehtävän mukaan. Käyttäjä voi myös käyttää hakusanaa löytääkseen tietyn tallennuksen siihen lisättyjen muistiinpanojen perusteella.
