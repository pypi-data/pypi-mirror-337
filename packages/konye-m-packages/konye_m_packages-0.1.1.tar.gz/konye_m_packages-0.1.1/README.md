Ez egy Python alapú csomag, amely különféle szövegelőfeldolgozási funkciókat biztosít természetes nyelvű szövegek tisztítására, előkészítésére és modellezésre való átalakítására. A csomag célja, hogy egységes és testreszabható eszközt biztosítson szövegklasszifikációs vagy más NLP-feladatokhoz.
Főbb funkciók

    Alapvető tisztítás: dátumok, telefonszámok, HTML tagek, URL-ek, képleírások eltávolítása

    Nyelvfelismerés és nem angol nyelvű sorok szűrése

    Szöveghossz statisztikák és szógyakorisági vizualizáció

    Többféle tokenizálási stratégia:

        stopword nélküli

        álhírek szerinti szakirodalmi szűrés alapján csökkentett stopword lista

        teljes stopword eltávolítás

        számok szavakká alakítása

    Lemmatizálás és stemming

    GloVe-alapú embedding mátrix generálása

    Modellinput előkészítés (tokenizálás, padding)

Használat
1. Statisztikák és vizualizáció

analyze_text_column(df, "Dataset neve")
plot_most_common_words(df, "Dataset neve")  # stopword szűrt
plot_most_common_words2(df, "Dataset neve") # teljes szókészlet

2. Adattisztítás

df_cleaned = clean_dataset(df)

3. Szöveg előfeldolgozás (választható módszerek)

df1 = filtered_preproc(df_cleaned, "text", "processed")       # stopword szűrt, POS alapján
df2 = preprocess_text(df_cleaned, "text", "processed")        # minden stopword megtartva
df3 = spacy_preproc(df_cleaned, "text", "processed")          # teljes stopword eltávolítás
df4 = number_preproc(df_cleaned, "text", "processed")         # számokat szöveggé alakít

4. Nyelvi feldolgozás

df_lemmatized = lemmat_processing(df1, "processed", "lemmatized")
df_stemmed = stemming_processing(df1, "processed", "stemmed")

5. Modellre való előkészítés (GloVe embeddinggel)

MAX_VOCAB_SIZE = 25000
MAX_LENGTH = 700
EMBEDDING_DIM = 300

sequences, embedding_matrix, tokenizer = prepare_for_modeling_with_glove(
    tokenized_texts=df_lemmatized["lemmatized"],
    glove_file="glove.6B.300d.txt",
    fit_tokenizer=True
)

Követelmények

A csomag használatához az alábbi csomagok szükségesek:

    pandas, numpy, re, matplotlib

    spacy, nltk, contractions, inflect

    tensorflow (csak a tokenizáláshoz és paddinghez)

    langdetect (nyelvfelismerés)

A spaCy angol nyelvi modell letöltéséhez:

python -m spacy download en_core_web_sm

Példa

from textpreprocessor import clean_dataset, preprocess_text, lemmat_processing

df = pd.read_csv("data.csv")
df_cleaned = clean_dataset(df)
df_processed = preprocess_text(df_cleaned, "text", "processed")
df_lemmatized = lemmat_processing(df_processed, "processed", "lemmatized")