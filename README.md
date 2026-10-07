# Fictional-Language-Generator

By researchers Angel Paramo Quirarte and Diego A. Ayala from the University of Guadalajara.

A webpage that can automatically create realistic and coherent fictional languages based on a questionnaire answered by the user. 

In multiple fantasy, science fiction, or other projects, whether they are shows or books, creators seek to build fictional languages to make the world feel more alive. Often, the people in charge of making these languages are not professional linguists, so they just group sounds together at random without following concrete rules about how languages work in reality. This project seeks to compute the rules for creating a language, so that anyone can create their own for their projects by answering a simple questionnaire that takes just a few minutes. 

The program generates 
1) A dictionary of the language.
2) A text specifying the rules of that language.
3) Some short texts in the language with their direct translation into English
4) Audio files that show the pronunciation of the language. 
5) A complete alphabet with originals characters if needed. 

This project forced us to deeply understand the structure and components of real languages in order to compute them into logical rules. 

We believe that this project has exceeded its original scope and is now a tool to evaluate how a language works from its very first principles and to value the linguistic diversity of our planet, which we hope can contribute to raising awareness about the conservation and appreciation of indigenous languages.

Mexico is one of the regions with the greatest linguistic diversity in the world, officially recognizing 68 indigenous languages and 364 linguistic variants according to the National Institute of Indigenous Languages (INALI). 

More than 60 percent of these languages are currently at risk of disappearing due to decades of systemic marginalization, forced migration, and the lack of digital and educational tools that allow younger generations to keep their mother tongues alive in the modern world. When a language dies, humanity loses an irreplaceable system of ecological knowledge, history, and a unique way of perceiving reality that took thousands of years to evolve.

While institutions like INALI and the Ministry of Culture lead preservation efforts through community radio, bilingual education, and printed archives, the digital gap remains a massive threat to their survival. 

By translating complex morphological and phonetic structures, including polysynthetic and tonal mechanics directly inspired by native languages like Náhuatl, Maya, and Otomí into open-source code, this project builds technological infrastructure that turns cultural preservation into an interactive experience. Sustaining and scaling this tool requires dedicated funding and institutional backing to move from an experimental generator to an educational and archival platform that demonstrates how indigenous languages are not relics of the past, but sophisticated, living systems of human engineering that urgently deserve our investment and protection.

### Design Rationale: From Cultural Deduction to Direct Design

Our first prototype tried to guess how a language should work by asking about the speakers' environment and society, using four cultural axes: isolation versus trade, social hierarchy, climate, and writing tools. This failed for two reasons. 

First, real languages do not follow strict environmental rules, for example forcing a desert culture to speak with harsh, guttural sounds is bad science and ruins the creator's vision if they wanted a soft, melodic language instead.

Second, asking regular writers about academic concepts like "fusional grammar" or "fricative consonants" creates too much friction. 

To fix this, we replaced the four cultural axes with six direct structural axes that translate everyday creative instincts into code. Instead of simulating history to guess a grammar, the program now asks simple, practical questions about what the user actually wants: how the language sounds, how long the words look, what part of a sentence gets the main focus, how objects are grouped, how exact the verbs need to be, and what tools are used to write it. The Python engine then turns those direct choices into phonetic rules, grammar templates, and vector glyphs, giving creators full control over their language without needing a degree in linguistics.

### Matrix

**Category** a broad domain of the language
**Axis** a single, continuous 1D vector from 0 to 100 with two opposite poles.
**42 programmable variables** they control.

6 categories, Acoustic Texture, Word Architecture, Thought Flow, World Classification, Precision & Time and Social & Material Expression.

**14 Axes** (3 in Acoustic Texture, 2 in Word Architecture, 2 in Thought Flow, 2 in World Classification, 2 in Precision & Time, and 3 in Social & Material Expression).

42 Variables in total. Exactly 3 programmable variables per axis. 
### Category 1: Acoustic Texture (Phonetics & Phonology)

**Axis 1: Vocal Cord Energy (Volume & Voicing)**

Measures the physical force and vibration of the larynx, moving from a breathless whisper at 0 to a booming, resonant projection at 100.


1. `voiceless_consonant_weight`: Multiplier for unvoiced sounds ($s, f, p, t, k, sh$). High at 0, low at 100.

2. `voiced_plosives_weight`: Multiplier for vibrating, booming stops ($b, d, g, v, z$). Low at 0, high at 100.

3. `tonal_probability`: Chance from 0.0 to 1.0 that the language uses pitch diacritics to change word meaning. Zero at 0 (you cannot whisper tones), maximum at 100.


**Axis 2: Airflow Continuity (Sonority & Flow)**

Measures how freely air escapes the mouth, from sharp, interrupted staccato bursts and clicks at 0 to uninterrupted, liquid melodic flow at 100.

  

1. `vowel_to_consonant_ratio`: Target percentage of vowels per word (e.g., 30% at 0 vs. 65% at 100).

2. `glottal_and_click_freq`: Frequency of hard air-stops and non-pulmonic clicks ($', !, k', t'$). Maximum at 0, zero at 100.

3. `max_consonant_cluster`: Maximum number of consonants allowed next to each other (e.g., 3 or 4 at 0 vs. strict 1 at 100).

**Axis 3: Articulatory Depth (Placement in the Mouth)**

Measures where the sounds are physically formed, from the front of the lips and teeth at 0 to deep in the throat and uvula at 100.


1. `labial_dental_weight`: Statistical weight of front sounds ($p, b, m, f, v, th, t, s$). High at 0, low at 100.

2. `velar_uvular_weight`: Statistical weight of deep throat sounds ($k, g, q, kh, gh, x$). Low at 0, high at 100.

3. `back_vowel_bias`: Ratio favoring deep vowels ($u, o, a$) over front vowels ($i, e$). Low at 0, high at 100.

### Category 2: Word Architecture (Morphology)

**Axis 4: Word Density (Synthetic Index)**

Measures how many concepts are packed into a single word, from tiny standalone one-syllable words at 0 (Isolating) to massive multi-part words that swallow entire sentences at 100 (Polysynthetic).

1. `base_root_length`: Number of syllables in a basic dictionary root (1 at 0, up to 3 or 4 at 100).

2. `max_affixes_per_word`: How many prefixes and suffixes can be legally glued to a single root (0 at 0, up to 6 at 100).

3. `compound_word_prob`: Probability that new concepts are made by smashing two existing nouns together into one string rather than keeping them separated by spaces.


**Axis 5: Morpheme Boundary Clarity (Fusion Index)**

Measures how cleanly word parts attach to each other, from crisp, unchanging Lego-like blocks at 0 (Agglutinative) to mutated, melted endings where one suffix holds multiple meanings at 100 (Fusional).

1. `vowel_harmony_strictness`: Probability that suffixes must change their vowels to match the root word. High at 0, low at 100.

2. `root_mutation_rate`: Chance that the inside of the root word itself mutates when conjugated (like _sing/sang/sung_ or Arabic consonant skeletons). Zero at 0, high at 100.

3. `irregular_exception_rate`: Percentage of words in the dictionary that break the standard grammar rules (0% at 0, up to 25% at 100).

### Category 3: Thought Flow (Syntax)

**Axis 6: Action Prominence (Verb Position)**

Measures when the action is introduced in a sentence, from placing the verb at the very beginning to grab attention at 0 (VSO), putting it in the middle at 50 (SVO), to saving the action for the very end at 100 (SOV).
  

1. `verb_slot_index`: Numerical position of the verb in the sentence array (`0` for start, `1` for middle, `2` for end).

2. `adposition_type`: Controls whether connector words go before the noun as prepositions ("_in_ the house" at 0) or after the noun as postpositions ("the house _in_" at 100).

3. `auxiliary_placement`: Determines if helper words (like _will, not, can_) precede the main verb (0) or trail behind it (100).

**Axis 7: Structural Rigidity (Word Order Freedom)**

Measures whether the meaning of a sentence depends on strict word slots at 0 or if words can be scrambled freely for poetic emphasis because suffixes mark who did what at 100.

1. `case_marking_count`: Number of noun suffixes that mark Subject, Object, or Possession (0 cases at 0, up to 8 cases at 100).

2. `syntax_scramble_prob`: Probability that a generated sentence swaps word positions for emphasis without losing meaning.

3. `helper_particle_density`: Frequency of standalone grammar words (like _of, to, the_) needed to hold the sentence together. High at 0, zero at 100.

### Category 4: World Classification (Semantics & Noun Classes)

**Axis 8: Noun Categorization Complexity**

Measures how obsessively the grammar labels objects in the universe, from zero gender/classes at 0 to a complex multi-class taxonomy (by shape, soul, or utility) at 100.

1. `noun_class_total`: Total number of grammatical genders or classes in the language (0 at 0, 2 at 30, up to 10 shape/animacy classes at 100).

2. `class_prefix_visibility`: Probability that every noun must carry a mandatory prefix or suffix showing its category.

3. `adjective_agreement_flag`: Boolean/probability determining if adjectives and verbs must copy the prefix/suffix of the noun they describe.


**Axis 9: Conceptual Abstraction (Lexical Derivation)**

Measures how the dictionary invents words for complex ideas, from literal combinations of nature and body parts at 0 ("eye-water" for tear) to unique, specialized academic roots at 100.

1. `body_nature_metaphor_rate`: Percentage of derived words built by combining tangible physical roots from the Swadesh list.

2. `unique_root_generation_rate`: How many completely independent root words the generator creates instead of recycling basic roots.

3. `abstract_derivational_affixes`: Number of dedicated suffixes for abstract concepts (equivalent to _-ism, -ology, -ness_). Zero at 0, high at 100.

### Category 5: Precision & Time (Verb Mechanics)

**Axis 10: Temporal Rigidity (Tense & Aspect)**

Measures how obsessed speakers are with tracking time, from a tenseless language that relies purely on context at 0 to a hyper-specific timeline marking exact temporal distance and completion at 100.

1. `tense_marker_count`: Number of mandatory past/present/future verb suffixes (0 at 0, up to 6 for remote past, near past, etc. at 100).

2. `aspect_affix_weight`: Probability of adding markers that specify if an action is ongoing, finished, or repetitive.

3. `standalone_time_adverbs`: Frequency of separate time words ("yesterday", "soon") used instead of conjugating the verb. High at 0, low at 100.

**Axis 11: Information Reliability (Evidentiality)**

Measures whether speakers state actions simply as they happen at 0 or if they are legally forced by grammar to prove _how_ they know the information (saw it, heard a rumor, guessed it) at 100.

  

1. `evidential_suffix_count`: Number of mandatory source-of-knowledge suffixes attached to verbs (0 at 0, up to 5 at 100).

2. `mood_marker_complexity`: Number of suffixes marking certainty, doubt, or desire.

3. `verb_string_length_modifier`: Additional character length added to verbs in the translated story to account for truthfulness markers.

### Category 6: Social & Material Expression (Pragmatics & Script)

**Axis 12: Social Stratification (Honorifics & Register)**

Measures social distance in speech, from total egalitarianism where everyone uses the exact same words at 0 to a rigid caste system where pronouns and verbs change based on the listener's rank at 100.

1. `pronoun_set_multipliers`: Number of distinct sets of "I / You" pronouns generated in the dictionary (1 set at 0, 3 sets for low/equal/high status at 100).

2. `honorific_affix_freq`: Probability that verbs and nouns require a politeness prefix when addressing authority.

3. `lexical_caste_split`: Percentage of everyday verbs (like "eat" or "speak") that have two completely different root words depending on social class.

**Axis 13: Inscription Friction (Material Resistance)**

Measures the physical resistance of the writing surface, from carving into hard stone or wood with a knife at 0 to gliding effortlessly with ink and a soft brush on paper at 100.
  

1. `bezier_curve_ratio`: Percentage of curved lines vs. straight lines in the SVG generator (0% curves at 0, 100% flowing curves at 100).

2. `sharp_vertex_angle_weight`: Preference for sharp acute/right angles in the 3x3 SVG grid vs. rounded loops. High at 0, low at 100.

3. `continuous_stroke_length`: Determines if a symbol is made of 4 separate short chisel cuts (at 0) or 1 single continuous unbroken brush line (at 100).

**Axis 14: Graphic Information Density (Script Type)**

Measures how much meaning a single written symbol holds, from a pure alphabet where 1 symbol equals 1 individual sound at 0, through syllabaries at 50, to complex logograms where 1 symbol equals 1 entire word at 100.

1. `total_unique_glyphs`: Total number of SVG symbols generated for the PDF chart (e.g., 22 letters at 0, 50 syllables at 50, 100+ word-symbols at 100).

2. `strokes_per_glyph_limit`: Complexity of each individual SVG drawing (2 to 3 simple lines per letter at 0, up to 9 intersecting lines and radicals per logogram at 100).

3. `glyph_to_phoneme_mapping`: Rule switch in code (`1` = map SVG to single letter, `2` = map SVG to consonant+vowel pair, `3` = map SVG to whole dictionary root).

## Project Architecture and Steps

### Phase 1: Conceptual Matrix and Mathematical Weighting (Completed)

1. **Define Language Categories:** Establish the 6 core domains of the language (Acoustic Texture, Word Architecture, Thought Flow, World Classification, Precision and Time, and Social and Material Expression).
2. **One-Dimensional Axes:** Break down the 6 categories into 14 bipolar axes measured on a strict mathematical scale from 1 to 100 so they can be intuitively evaluated through everyday questions without linguistic jargon.
3. **Variable Mapping:** Connect each of the 14 axes to 3 specific linguistic variables (42 variables in total) that dictate exact probabilities and structural limits for the generator.

### Phase 2: Static Data and Questionnaire Design (Pending)

4. **Intuitive Questionnaire:** Write the user-facing questions and answer options that add or subtract points across the 14 mathematical axes.
5. **Base Concept Database (Swadesh List):** Create the foundational file containing 100 to 200 universal English concepts (water, fire, mother, to hunt, to run) and a base pangram story so the semantic module has concrete meanings to assign to the generated roots.
6. **Base Phonetic Inventories:** Store the baseline statistical frequencies of letters, vowels, consonants, and International Phonetic Alphabet (IPA) reading equivalents.

### Phase 3: The Linguistic Generation Engine (Pending)

7. **Phonology and Phonetics Module:** Reads the Acoustic Texture variables (Axes 1 to 3) to filter allowed phonemes, set vowel-to-consonant ratios, enable or block tones and clicks, and define syllable structure rules.
8. **Morphology Module:** Reads the Word Architecture variables (Axes 4 and 5) to establish the internal structure of words, deciding root lengths, how many prefixes and suffixes can attach, whether endings fuse or stay separate like Lego blocks, and the rate of irregular exceptions.
9. **Semantics and Lexicon Module:** Reads the World Classification variables (Axes 8 and 9) and Social Stratification (Axis 12) to generate the dictionary roots for the Swadesh list, assign grammatical gender or animacy classes, build compound words from nature metaphors, and create honorific pronoun sets.
10. **Syntax and Translation Module:** Reads the Thought Flow variables (Axes 6 and 7) and Verb Mechanics (Axes 10 and 11) to govern sentence word order (SVO, SOV, VSO), apply tense and evidentiality suffixes, and run the translation algorithm that converts the English pangram story into the new language.

### Phase 4: Procedural Alphabet, Audio, and Output (Pending)

11. **Procedural Grid Alphabet (SVG Generator):** Reads the Material Resistance and Script Density variables (Axes 13 and 14) to generate a coherent writing system on an invisible 3x3 grid. Using a seed of 3 to 4 base strokes (straight chisel cuts for stone or curved Bézier strokes for brush and ink), the system combines those strokes to ensure all letters, syllables, or logograms look like they belong to the same typeface family.
12. **Audio Synthesis and Pronunciation Guide:** Generates text explanations of how to read the language according to international standards alongside synthesized audio files demonstrating how the words and sentences actually sound.
13. **PDF Report Builder:** Compiles all generated assets into a clean, predefined document template containing the grammatical rules, the pronunciation guide, the dictionary, the translated sample text, and the visual alphabet chart.
14. **Web Interface:** The public-facing webpage where users answer the questionnaire, listen to the audio previews, view their generated language, and download the final PDF guide.