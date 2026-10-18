import random
from typing import Dict, List, Any
from morphology import inflect_word

# =====================================================================
# PLANTILLAS DE ORACIONES DE PRUEBA (Pangrama + Textos Culturales)
# Estructuradas semánticamente para que el motor pueda reordenarlas
# a SVO, SOV, VSO o OVS sin perder el sentido gramatical.
# =====================================================================

SAMPLE_SENTENCES = [
    {
        "id": "pangram_sentence",
        "english": "The quick brown fox jumps over the lazy dog.",
        "subject": {"noun": "fox", "adjectives": ["quick", "brown"], "plural": False},
        "verb": {"root": "jump", "tense": "present", "aspect": "continuous", "evidential": "visual_witness"},
        "object": {"noun": "dog", "adjectives": ["lazy"], "plural": False, "adposition": "over"},
        "register": "neutral"
    },
    {
        "id": "mythic_sentence",
        "english": "The great mother saw the fire-mountain (volcano).",
        "subject": {"noun": "mother", "adjectives": ["great"], "plural": False},
        "verb": {"root": "see", "tense": "remote_past", "aspect": "completed", "evidential": "hearsay_rumor"},
        "object": {"noun": "volcano", "adjectives": [], "plural": False, "adposition": None},
        "register": "high_caste"
    },
    {
        "id": "nature_sentence",
        "english": "Small birds know the forest and the dawn.",
        "subject": {"noun": "bird", "adjectives": ["small"], "plural": True},
        "verb": {"root": "know", "tense": "present", "aspect": "habitual", "evidential": "assumed_memory"},
        "object": {"noun": "forest", "adjectives": [], "plural": False, "adposition": None},
        "register": "neutral"
    }
]


# =====================================================================
# MOTOR 4: CONSTRUCCIÓN DE REGLAS SINTÁCTICAS Y TRADUCCIÓN
# =====================================================================

def build_syntax(
    config: Any,
    phonology: Dict[str, Any],
    morphology: Dict[str, Any],
    lexicon: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Define el orden de los elementos en la oración (Ejes 6 y 7) y traduce
    las oraciones de muestra generando su glosa lingüística paso a paso.
    """
    # 1. Definir el Orden Básico de la Oración según verb_slot_index (Eje 6)
    if config.verb_slot_index < 0.30:
        word_order = "VSO"  # Verbo al inicio (Ej. Árabe clásico, Irlandés)
    elif config.verb_slot_index < 0.70:
        word_order = "SVO"  # Verbo en medio (Ej. Inglés, Español, Mandarín)
    else:
        word_order = "SOV"  # Verbo al final (Ej. Japonés, Turco, Latín)

    # Si la libertad de orden es altísima y tiene casos, puede usar órdenes raros como OVS
    if config.syntax_scramble_prob > 0.85 and len(morphology["cases"]) >= 3:
        word_order = "OVS (Free/Case-Driven)"

    # 2. Definir Preposiciones vs Posposiciones y posición del Adjetivo (Eje 6)
    # En la lingüística real, los idiomas SOV casi siempre usan posposiciones ("el perro sobre" en vez de "sobre el perro")
    adposition_order = "postposition" if config.adposition_type >= 0.5 else "preposition"
    auxiliary_order = "after_verb" if config.auxiliary_placement >= 0.5 else "before_verb"
    adj_order = "after_noun" if config.verb_slot_index < 0.5 else "before_noun"

    syntax_rules = {
        "base_word_order": word_order,
        "adposition_type": adposition_order,
        "auxiliary_placement": auxiliary_order,
        "adjective_placement": adj_order,
        "word_order_freedom": round(config.syntax_scramble_prob, 2),
        "uses_standalone_particles": config.helper_particle_density >= 0.4
    }

    # 3. Traducir y Glosar el Pangrama y las Oraciones de Muestra
    translated_texts = []
    for template in SAMPLE_SENTENCES:
        translation_data = _translate_sentence(
            template, config, phonology, morphology, lexicon, syntax_rules
        )
        translated_texts.append(translation_data)

    return {
        "rules": syntax_rules,
        "translated_corpus": translated_texts
    }


# =====================================================================
# MOTOR DE TRADUCCIÓN Y GLOSADO INTERLINEAL
# =====================================================================

def _translate_sentence(
    template: Dict[str, Any],
    config: Any,
    phonology: Dict[str, Any],
    morphology: Dict[str, Any],
    lexicon: Dict[str, Any],
    syntax_rules: Dict[str, Any]
) -> Dict[str, str]:
    """
    Toma una oración estructurada en inglés, ensambla el Sujeto, el Verbo y el Objeto
    aplicando casos, géneros, tiempos y evidencialidad, y los ordena según la sintaxis.
    """
    # 1. Construir el bloque del SUJETO (Caso Nominativo)
    subj_text, subj_gloss = _build_noun_phrase(
        noun_data=template["subject"],
        case_role="nominative",
        phonology=phonology,
        morphology=morphology,
        lexicon=lexicon,
        syntax_rules=syntax_rules
    )

    # 2. Construir el bloque del OBJETO (Caso Acusativo o Oblicuo con preposición)
    obj_text, obj_gloss = _build_noun_phrase(
        noun_data=template["object"],
        case_role="accusative",
        phonology=phonology,
        morphology=morphology,
        lexicon=lexicon,
        syntax_rules=syntax_rules
    )

    # 3. Construir el bloque del VERBO (Tiempo, Aspecto, Evidencialidad y Casta)
    verb_text, verb_gloss = _build_verb_phrase(
        verb_data=template["verb"],
        register=template["register"],
        config=config,
        phonology=phonology,
        morphology=morphology,
        lexicon=lexicon,
        syntax_rules=syntax_rules
    )

    # 4. Ordenar los bloques según el orden sintáctico del idioma (VSO, SVO, SOV, OVS)
    order = syntax_rules["base_word_order"]

    # Si el idioma tiene orden libre (Eje 7), existe probabilidad de alterar el orden por énfasis poético
    if random.random() < (syntax_rules["word_order_freedom"] * 0.4) and len(morphology["cases"]) >= 2:
        blocks = [(verb_text, verb_gloss), (subj_text, subj_gloss), (obj_text, obj_gloss)]
        random.shuffle(blocks)
    elif order.startswith("VSO"):
        blocks = [(verb_text, verb_gloss), (subj_text, subj_gloss), (obj_text, obj_gloss)]
    elif order.startswith("SOV"):
        blocks = [(subj_text, subj_gloss), (obj_text, obj_gloss), (verb_text, verb_gloss)]
    elif order.startswith("OVS"):
        blocks = [(obj_text, obj_gloss), (verb_text, verb_gloss), (subj_text, subj_gloss)]
    else:  # SVO por defecto
        blocks = [(subj_text, subj_gloss), (verb_text, verb_gloss), (obj_text, obj_gloss)]

    final_sentence = " ".join(b[0] for b in blocks).strip()
    # Capitalizar la primera letra y añadir punto final
    if final_sentence:
        final_sentence = final_sentence[0].upper() + final_sentence[1:] + "."

    interlinear_gloss = "   ".join(b[1] for b in blocks).strip()

    return {
        "id": template["id"],
        "english_original": template["english"],
        "conlang_text": final_sentence,
        "interlinear_gloss": interlinear_gloss
    }


def _build_noun_phrase(
    noun_data: Dict[str, Any],
    case_role: str,
    phonology: Dict[str, Any],
    morphology: Dict[str, Any],
    lexicon: Dict[str, Any],
    syntax_rules: Dict[str, Any]
) -> tuple[str, str]:
    """Arma un sustantivo con sus artículos, adjetivos, plurales, casos y preposiciones."""
    dictionary = lexicon["dictionary"]
    func_words = lexicon["function_words"]

    noun_entry = dictionary[noun_data["noun"]]
    # Si la palabra es irregular y se declina, usa su raíz irregular (Eje 5)
    base_word = noun_entry["irregular_form"] if (noun_entry["is_irregular"] and case_role != "nominative") else noun_entry["word"]

    affixes = []
    gloss_tags = [noun_data["noun"].upper()]

    # Agregar marcador de plural si aplica
    if noun_data.get("plural"):
        affixes.append(morphology["plural_marker"])
        gloss_tags.append("PL")

    # Agregar caso gramatical (Nominativo, Acusativo, etc.) si el idioma tiene casos
    case_affix = morphology["cases"].get(case_role, "")
    if case_affix:
        affixes.append(case_affix)
        gloss_tags.append(case_role[:3].upper())

    inflected_noun = inflect_word(base_word, affixes, morphology, phonology)
    noun_gloss = "-".join(gloss_tags)

    # Construir adjetivos (con concordancia de clase nominal si adjective_agreement está activo)
    adj_words = []
    adj_glosses = []
    noun_class = noun_entry.get("noun_class")
    class_affix = morphology["noun_classes"].get(noun_class, "") if noun_class else ""

    for adj_id in noun_data.get("adjectives", []):
        adj_root = dictionary[adj_id]["word"]
        if morphology["adjective_agreement"] and class_affix:
            adj_final = inflect_word(adj_root, [class_affix], morphology, phonology)
            adj_glosses.append(f"{adj_id}.AGR")
        else:
            adj_final = adj_root
            adj_glosses.append(adj_id)
        adj_words.append(adj_final)

    # Ordenar Adjetivos respecto al Sustantivo
    if syntax_rules["adjective_placement"] == "before_noun":
        core_words = adj_words + [inflected_noun]
        core_gloss = adj_glosses + [noun_gloss]
    else:
        core_words = [inflected_noun] + adj_words
        core_gloss = [noun_gloss] + adj_glosses

    # Agregar artículo definido ("the") si el idioma usa partículas sueltas
    the_word = func_words.get("the", "")
    if the_word and not noun_data.get("plural"):
        core_words.insert(0, the_word)
        core_gloss.insert(0, "DEF")

    # Agregar Preposición o Posposición (ej. "over" en el pangrama)
    adp_key = noun_data.get("adposition")
    if adp_key and adp_key in func_words:
        adp_word = func_words[adp_key]
        if syntax_rules["adposition_type"] == "preposition":
            core_words.insert(0, adp_word)
            core_gloss.insert(0, adp_key.upper())
        else:
            core_words.append(adp_word)
            core_gloss.append(adp_key.upper())

    return " ".join(core_words), " ".join(core_gloss)


def _build_verb_phrase(
    verb_data: Dict[str, Any],
    register: str,
    config: Any,
    phonology: Dict[str, Any],
    morphology: Dict[str, Any],
    lexicon: Dict[str, Any],
    syntax_rules: Dict[str, Any]
) -> tuple[str, str]:
    """Conjuga el verbo aplicando casta, honoríficos, tiempo, aspecto y evidencialidad."""
    verb_id = verb_data["root"]
    dictionary = lexicon["dictionary"]
    v_markers = morphology["verb_markers"]

    # Verificar si hay una palabra especial de casta alta para este verbo (Eje 12)
    if register == "high_caste" and verb_id in lexicon["caste_lexical_splits"]:
        base_verb = lexicon["caste_lexical_splits"][verb_id]["high_caste_royal"]
        gloss_tags = [f"{verb_id.upper()}.ROYAL"]
    else:
        base_verb = dictionary[verb_id]["word"]
        gloss_tags = [verb_id.upper()]

    affixes = []

    # 1. Sufijo de Tiempo (Eje 10)
    tense_key = verb_data.get("tense", "present")
    if tense_key in v_markers["tenses"]:
        affixes.append(v_markers["tenses"][tense_key])
        gloss_tags.append(tense_key[:4].upper())

    # 2. Sufijo de Aspecto (Eje 10)
    aspect_key = verb_data.get("aspect")
    if aspect_key and aspect_key in v_markers["aspects"]:
        affixes.append(v_markers["aspects"][aspect_key])
        gloss_tags.append(aspect_key[:4].upper())

    # 3. Sufijo de Evidencialidad (Eje 11: cómo sabe el hablante la información)
    evid_key = verb_data.get("evidential")
    if evid_key and evid_key in v_markers["evidentials"]:
        affixes.append(v_markers["evidentials"][evid_key])
        gloss_tags.append("EVID")

    # 4. Sufijo Honorífico formal si el registro es elevado (Eje 12)
    if register == "high_caste" and "formal_verb_suffix" in morphology["honorifics"]:
        affixes.append(morphology["honorifics"]["formal_verb_suffix"])
        gloss_tags.append("HON")

    # Ensamblar el verbo respetando la armonía vocálica y el límite de afijos
    conjugated_verb = inflect_word(base_verb, affixes, morphology, phonology)
    verb_gloss = "-".join(gloss_tags)

    # Si el idioma usa adverbios de tiempo sueltos en vez de conjugar (Eje 10)
    yesterday_part = lexicon["function_words"].get("yesterday_particle", "")
    if yesterday_part and "past" in tense_key and not v_markers["tenses"]:
        if syntax_rules["auxiliary_placement"] == "before_verb":
            return f"{yesterday_part} {conjugated_verb}", f"PAST {verb_gloss}"
        else:
            return f"{conjugated_verb} {yesterday_part}", f"{verb_gloss} PAST"

    return conjugated_verb, verb_gloss