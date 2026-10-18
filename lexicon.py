import random
from typing import Dict, List, Any
from phonology import generate_phonetic_root
from morphology import inflect_word

# =====================================================================
# 1. BASE DE DATOS DE CONCEPTOS (Swadesh + Pangrama + Derivados)
# =====================================================================

# Conceptos primitivos universales (incluye las palabras para traducir el pangrama)
PRIMITIVE_CONCEPTS = [
    # Naturaleza y Entorno
    {"id": "water",    "pos": "noun", "semantic_group": "liquid_abstract"},
    {"id": "fire",     "pos": "noun", "semantic_group": "inanimate_nature"},
    {"id": "earth",    "pos": "noun", "semantic_group": "flat_object"},
    {"id": "mountain", "pos": "noun", "semantic_group": "round_object"},
    {"id": "sun",      "pos": "noun", "semantic_group": "round_object"},
    {"id": "night",    "pos": "noun", "semantic_group": "liquid_abstract"},
    {"id": "tree",     "pos": "noun", "semantic_group": "long_thin_object"},
    
    # Cuerpo y Humanos
    {"id": "eye",      "pos": "noun", "semantic_group": "round_object"},
    {"id": "hand",     "pos": "noun", "semantic_group": "inanimate_tool"},
    {"id": "heart",    "pos": "noun", "semantic_group": "round_object"},
    {"id": "mouth",    "pos": "noun", "semantic_group": "round_object"},
    {"id": "mother",   "pos": "noun", "semantic_group": "animate_human"},
    {"id": "person",   "pos": "noun", "semantic_group": "animate_human"},
    
    # Animales y Pangrama ("The quick brown fox jumps over the lazy dog")
    {"id": "fox",      "pos": "noun", "semantic_group": "animate_animal"},
    {"id": "dog",      "pos": "noun", "semantic_group": "animate_animal"},
    {"id": "bird",     "pos": "noun", "semantic_group": "animate_animal"},
    
    # Verbos Base
    {"id": "eat",      "pos": "verb", "semantic_group": "action"},
    {"id": "speak",    "pos": "verb", "semantic_group": "action"},
    {"id": "see",      "pos": "verb", "semantic_group": "action"},
    {"id": "know",     "pos": "verb", "semantic_group": "action"},
    {"id": "walk",     "pos": "verb", "semantic_group": "action"},
    {"id": "jump",     "pos": "verb", "semantic_group": "action"},
    
    # Adjetivos Base
    {"id": "quick",    "pos": "adj",  "semantic_group": "quality"},
    {"id": "brown",    "pos": "adj",  "semantic_group": "quality"},
    {"id": "lazy",     "pos": "adj",  "semantic_group": "quality"},
    {"id": "great",    "pos": "adj",  "semantic_group": "quality"},
    {"id": "small",    "pos": "adj",  "semantic_group": "quality"},
]

# Conceptos complejos que pueden nacer de metáforas físicas o raíces abstractas (Eje 9)
DERIVED_CONCEPTS = [
    {"id": "tear",      "pos": "noun", "components": ("eye", "water"),      "literal": "eye-water"},
    {"id": "volcano",   "pos": "noun", "components": ("fire", "mountain"),  "literal": "fire-mountain"},
    {"id": "language",  "pos": "noun", "components": ("mouth", "hand"),     "literal": "mouth-craft"},
    {"id": "courage",   "pos": "noun", "components": ("great", "heart"),    "literal": "great-heart"},
    {"id": "dawn",      "pos": "noun", "components": ("sun", "eye"),        "literal": "sun-eye"},
    {"id": "forest",    "pos": "noun", "components": ("tree", "earth"),     "literal": "tree-land"},
    {"id": "wisdom",    "pos": "noun", "components": ("see", "heart"),      "literal": "see-heart"},
]


# =====================================================================
# MOTOR 3: CONSTRUCCIÓN DEL DICCIONARIO Y SEMÁNTICA
# =====================================================================

def build_lexicon(
    config: Any,
    phonology: Dict[str, Any],
    morphology: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Genera el diccionario completo del idioma, asignando clases nominales,
    creando palabras compuestas/metafóricas y aplicando divisiones de casta.
    """
    entries: Dict[str, Dict[str, Any]] = {}
    used_words = set()

    def _get_unique_word(syllables: int) -> str:
        """Garantiza que no existan dos raíces idénticas por accidente."""
        for _ in range(50):
            candidate = generate_phonetic_root(phonology, syllable_count=syllables)
            if candidate not in used_words:
                used_words.add(candidate)
                return candidate
        return generate_phonetic_root(phonology, syllable_count=syllables + 1)

    # 1. Generar las Raíces Primitivas y asignarles su Género/Clase (Eje 8)
    base_syllables = morphology["base_root_syllables"]
    available_classes = list(morphology["noun_classes"].keys())

    for item in PRIMITIVE_CONCEPTS:
        concept_id = item["id"]
        pos = item["pos"]
        
        # Los verbos y adjetivos suelen ser ligeramente más cortos que los sustantivos largos
        syl = max(1, base_syllables - 1) if pos in ["verb", "adj"] and random.random() < 0.5 else base_syllables
        raw_root = _get_unique_word(syl)

        # Asignar clase nominal/género si es sustantivo y el idioma tiene clases
        assigned_class = None
        surface_word = raw_root
        if pos == "noun" and available_classes:
            assigned_class = _match_noun_class(item["semantic_group"], available_classes)
            class_affix = morphology["noun_classes"].get(assigned_class, "")
            if class_affix:
                surface_word = inflect_word(raw_root, [class_affix], morphology, phonology, as_prefix=True)

        # Marcar si esta palabra es irregular (Eje 5: irregular_exception_rate)
        is_irregular = random.random() < config.irregular_exception_rate
        irregular_stem = _get_unique_word(1) if is_irregular else None

        entries[concept_id] = {
            "word": surface_word,
            "root": raw_root,
            "pos": pos,
            "noun_class": assigned_class,
            "origin": "primitive_root",
            "is_irregular": is_irregular,
            "irregular_form": irregular_stem
        }

    # 2. Generar Conceptos Derivados: Metáforas de la Naturaleza vs. Raíces Abstractas (Eje 9)
    abstract_affixes = list(morphology["abstract_affixes"].values())

    for item in DERIVED_CONCEPTS:
        concept_id = item["id"]
        comp1, comp2 = item["components"]
        root1 = entries[comp1]["root"]
        root2 = entries[comp2]["root"]

        # Decidir si se crea por metáfora corporal/natural o como palabra académica independiente
        use_metaphor = random.random() < config.body_nature_metaphor_rate
        force_unique = random.random() < config.unique_root_generation_rate

        if use_metaphor and not force_unique:
            # Decide si las pega en una sola palabra compuesta o las deja separadas con guion/espacio (Eje 4)
            if random.random() < config.compound_word_prob and morphology["typology"] != "Isolating":
                derived_word = inflect_word(root1, [root2], morphology, phonology)
            else:
                derived_word = f"{root1}-{root2}"
            origin_note = f"Compound metaphor: '{comp1}' ({root1}) + '{comp2}' ({root2}) [{item['literal']}]"
        else:
            # Crea una raíz nueva y le pega un sufijo abstracto (-ism, -ness) si existen
            new_base = _get_unique_word(base_syllables)
            if abstract_affixes and morphology["typology"] != "Isolating":
                chosen_affix = random.choice(abstract_affixes)
                derived_word = inflect_word(new_base, [chosen_affix], morphology, phonology)
                origin_note = f"Abstract root '{new_base}' + derivational suffix '-{chosen_affix}'"
            else:
                derived_word = new_base
                origin_note = "Independent abstract root"

        entries[concept_id] = {
            "word": derived_word,
            "root": derived_word,
            "pos": item["pos"],
            "noun_class": entries[comp2].get("noun_class"),
            "origin": origin_note,
            "is_irregular": False,
            "irregular_form": None
        }

    # 3. Generar Sistema de Pronombres y Estratificación Social (Eje 12)
    pronouns = _build_pronoun_system(config, phonology, _get_unique_word)

    # División de vocabulario por casta (ej. un verbo "comer" para plebeyos y otro para nobles)
    caste_variants: Dict[str, Dict[str, str]] = {}
    if config.lexical_caste_split >= 0.35:
        for verb_id in ["eat", "speak", "walk", "see"]:
            if random.random() < config.lexical_caste_split:
                caste_variants[verb_id] = {
                    "commoner": entries[verb_id]["word"],
                    "high_caste_royal": _get_unique_word(base_syllables + 1)
                }

    # 4. Generar Palabras Funcionales / Partículas para la Sintaxis (Ejes 6 y 7)
    function_words = {
        "the": _get_unique_word(1) if config.helper_particle_density >= 0.4 else "",
        "over": _get_unique_word(1),
        "and": _get_unique_word(1),
        "not": _get_unique_word(1),
        "yesterday_particle": _get_unique_word(1) if config.standalone_time_adverbs >= 0.4 else "",
        "future_will_aux": _get_unique_word(1) if config.helper_particle_density >= 0.5 else ""
    }

    return {
        "dictionary": entries,
        "pronouns": pronouns,
        "caste_lexical_splits": caste_variants,
        "function_words": function_words,
        "stats": {
            "total_words": len(entries) + len(function_words),
            "metaphor_ratio_used": round(config.body_nature_metaphor_rate, 2),
            "has_caste_registers": len(caste_variants) > 0
        }
    }


def _match_noun_class(semantic_group: str, available_classes: List[str]) -> str:
    """Empareja el significado de la palabra con la clase nominal del idioma."""
    for c in available_classes:
        if c in semantic_group or semantic_group in c:
            return c
    # Si el sistema es binario/ternario (masculino/femenino/neutro), lo asigna de forma determinista o aleatoria
    return random.choice(available_classes)


def _build_pronoun_system(config: Any, phonology: Dict[str, Any], word_gen_func) -> Dict[str, Any]:
    """
    Construye la tabla de pronombres (1, 2 o 3 niveles de estatus social)
    según pronoun_set_multipliers (Eje 12).
    """
    base_pronouns = {
        "1sg (I)": word_gen_func(1),
        "2sg (You)": word_gen_func(1),
        "3sg (He/She/It)": word_gen_func(1),
        "1pl (We)": word_gen_func(1),
        "3pl (They)": word_gen_func(1)
    }

    if config.pronoun_set_multipliers < 0.40:
        return {"egalitarian_standard": base_pronouns}

    # Si hay jerarquía media o alta, agrega pronombres formales/superiores e inferiores
    system = {
        "neutral_equals": base_pronouns,
        "speaking_to_superior": {
            "1sg (Humble I)": word_gen_func(2),
            "2sg (Exalted You)": word_gen_func(2)
        }
    }
    if config.pronoun_set_multipliers >= 0.75:
        system["speaking_to_inferior"] = {
            "1sg (Dominant I)": word_gen_func(1),
            "2sg (Lowly You)": word_gen_func(1)
        }
    return system