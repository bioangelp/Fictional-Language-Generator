import random
from typing import Dict, List, Any
from phonology import generate_phonetic_root

# =====================================================================
# CATÁLOGOS DE ETIQUETAS GRAMATICALES
# Listas ordenadas de conceptos gramaticales que el motor activará
# dependiendo de qué tan alto sea el valor de cada variable (0.0 a 1.0).
# =====================================================================

CASE_LABELS = [
    "nominative",  # Sujeto (Quién hace la acción)
    "accusative",  # Objeto directo (Quién recibe la acción)
    "genitive",    # Posesión (De quién es)
    "dative",      # Objeto indirecto (Para quién es)
    "locative",    # Lugar (En dónde)
    "instrumental",# Herramienta (Con qué se hizo)
    "ablative",    # Origen (Desde dónde)
    "vocative"     # Llamado directo
]

NOUN_CLASS_SYSTEMS = {
    2: ["masculine", "feminine"],
    3: ["masculine", "feminine", "neuter"],
    4: ["animate_human", "animate_animal", "inanimate_tool", "inanimate_nature"],
    6: ["human", "animal", "long_thin_object", "flat_object", "round_object", "liquid_abstract"]
}

TENSE_LABELS = ["present", "past", "future", "remote_past", "immediate_future", "mythic_timeless"]
ASPECT_LABELS = ["continuous", "completed", "habitual", "repetitive"]
EVIDENTIAL_LABELS = ["visual_witness", "hearsay_rumor", "inferred_clue", "assumed_memory"]
MOOD_LABELS = ["certain", "doubtful", "desired", "mandatory"]
ABSTRACT_AFFIX_LABELS = ["state_of_being (-ness)", "system_or_belief (-ism)", "tool_for (-er)", "study_of (-ology)"]


# =====================================================================
# MOTOR 2: CONSTRUCCIÓN DEL SISTEMA MORFOLÓGICO
# =====================================================================

def build_morphology(config: Any, phonology: Dict[str, Any]) -> Dict[str, Any]:
    """
    Lee las variables morfológicas de LanguageConfig y genera todas las reglas
    de formación de palabras, además de los prefijos y sufijos reales del idioma.
    """
    # 1. Definir el Arquetipo Tipológico según Densidad (Eje 4) y Fusión (Eje 5)
    max_affixes = int(round(config.max_affixes_per_word * 5))  # De 0 a 5 afijos por palabra
    base_syllables = 1 + int(round(config.base_root_length * 2))  # De 1 a 3 sílabas por raíz

    if max_affixes == 0:
        typology = "Isolating"  # Como mandarín o vietnamita (cero sufijos, palabras sueltas)
    elif config.root_mutation_rate >= 0.60:
        typology = "Fusional"   # Como latín, ruso o árabe (la raíz muta o el sufijo se funde)
    elif max_affixes >= 4:
        typology = "Polysynthetic" # Como náhuatl (palabras gigantescas con muchos afijos)
    else:
        typology = "Agglutinative" # Como turco, finés o suajili (bloques de Lego limpios)

    # Función interna rápida para crear afijos de 1 sílaba corta
    def _make_affix() -> str:
        raw = generate_phonetic_root(phonology, syllable_count=1)
        # Recortamos un poco si salió muy largo para que parezca sufijo real
        return raw[:3] if len(raw) > 3 else raw

    # 2. Generar Casos Gramaticales (Eje 7: Rigidez Estructural)
    num_cases = 0 if typology == "Isolating" else int(round(config.case_marking_count * 7))
    cases: Dict[str, str] = {}
    if num_cases > 0:
        cases["nominative"] = ""  # El sujeto suele ir sin marca extra
        for label in CASE_LABELS[1:num_cases + 1]:
            cases[label] = _make_affix()

    # 3. Generar Clases Nominales / Géneros (Eje 8: Clasificación del Mundo)
    raw_classes = int(round(config.noun_class_total * 6))
    noun_classes: Dict[str, str] = {}
    if raw_classes >= 2:
        # Buscar el sistema de clases más cercano (2, 3, 4 o 6 clases)
        chosen_key = min(NOUN_CLASS_SYSTEMS.keys(), key=lambda k: abs(k - raw_classes))
        for label in NOUN_CLASS_SYSTEMS[chosen_key]:
            # Si la visibilidad es alta, lleva prefijo/sufijo explícito
            noun_classes[label] = _make_affix() if config.class_prefix_visibility >= 0.4 else ""

    # 4. Generar Morfología Verbal: Tiempo, Aspecto y Evidencialidad (Ejes 10 y 11)
    num_tenses = int(round(config.tense_marker_count * len(TENSE_LABELS)))
    tenses = {label: _make_affix() for label in TENSE_LABELS[:num_tenses]}

    num_aspects = int(round(config.aspect_affix_weight * len(ASPECT_LABELS)))
    aspects = {label: _make_affix() for label in ASPECT_LABELS[:num_aspects]}

    num_evidentials = int(round(config.evidential_suffix_count * len(EVIDENTIAL_LABELS)))
    evidentials = {label: _make_affix() for label in EVIDENTIAL_LABELS[:num_evidentials]}

    num_moods = int(round(config.mood_marker_complexity * len(MOOD_LABELS)))
    moods = {label: _make_affix() for label in MOOD_LABELS[:num_moods]}

    # 5. Generar Afijos Derivativos Abstractos (Eje 9) y Honoríficos (Eje 12)
    num_abstract = int(round(config.abstract_derivational_affixes * len(ABSTRACT_AFFIX_LABELS)))
    abstract_affixes = {label: _make_affix() for label in ABSTRACT_AFFIX_LABELS[:num_abstract]}

    honorifics = {}
    if config.honorific_affix_freq >= 0.4:
        honorifics = {
            "high_status_prefix": _make_affix(),
            "low_status_prefix": _make_affix(),
            "formal_verb_suffix": _make_affix()
        }

    return {
        "typology": typology,
        "base_root_syllables": base_syllables,
        "max_affixes_per_word": max_affixes,
        "compound_word_prob": config.compound_word_prob,
        "uses_vowel_harmony": phonology["uses_vowel_harmony"],
        "root_mutation_rate": config.root_mutation_rate,
        "irregular_exception_rate": config.irregular_exception_rate,
        "adjective_agreement": config.adjective_agreement_flag >= 0.5,
        "plural_marker": _make_affix(),
        "cases": cases,
        "noun_classes": noun_classes,
        "verb_markers": {
            "tenses": tenses,
            "aspects": aspects,
            "evidentials": evidentials,
            "moods": moods
        },
        "abstract_affixes": abstract_affixes,
        "honorifics": honorifics
    }


# =====================================================================
# MOTOR AUXILIAR: ENSAMBLADOR DE PALABRAS (Armonía Vocálica y Fusión)
# Esta función la usarán el Léxico y la Sintaxis para pegar sufijos a las raíces.
# =====================================================================

def inflect_word(
    root: str,
    affixes: List[str],
    morphology: Dict[str, Any],
    phonology: Dict[str, Any],
    as_prefix: bool = False
) -> str:
    """
    Toma una palabra raíz y le pega una lista de afijos respetando el límite máximo,
    la tipología (aislante vs sintética), la armonía vocálica y la mutación fusional.
    """
    if not affixes:
        return root

    # Respetar el límite de afijos del idioma
    valid_affixes = [a for a in affixes if a][:morphology["max_affixes_per_word"]]
    if not valid_affixes:
        return root

    # Si el idioma es puramente Aislante (0 afijos pegados), devuelve partículas separadas por espacio
    if morphology["typology"] == "Isolating":
        joined_particles = " ".join(valid_affixes)
        return f"{joined_particles} {root}" if as_prefix else f"{root} {joined_particles}"

    processed_root = root

    # Si el idioma es Fusional, la vocal interna de la raíz puede mutar al conjugarse (como sing -> sang)
    if morphology["typology"] == "Fusional" and random.random() < morphology["root_mutation_rate"]:
        processed_root = _mutate_root_vowel(processed_root, phonology)

    # Detectar el grupo vocálico de la raíz (frontal vs trasera) para aplicar armonía vocálica
    front_v = phonology["vowel_groups"]["front"]
    back_v = phonology["vowel_groups"]["back"]
    is_front_root = any(v in processed_root for v in front_v)

    final_word = processed_root
    for affix in valid_affixes:
        adapted_affix = affix
        if morphology["uses_vowel_harmony"]:
            adapted_affix = _harmonize_affix(affix, is_front_root, front_v, back_v)

        if as_prefix:
            final_word = adapted_affix + final_word
        else:
            # Si chocan dos vocales iguales o dos consonantes iguales en la unión, las fusiona
            if final_word and adapted_affix and final_word[-1] == adapted_affix[0]:
                final_word = final_word + adapted_affix[1:]
            else:
                final_word = final_word + adapted_affix

    return final_word


def _harmonize_affix(affix: str, to_front: bool, front_vowels: List[str], back_vowels: List[str]) -> str:
    """Cambia las vocales de un sufijo para que coincidan con la familia vocálica de la raíz."""
    if not front_vowels or not back_vowels:
        return affix
    result = list(affix)
    for i, char in enumerate(result):
        if to_front and char in back_vowels:
            result[i] = front_vowels[0]
        elif not to_front and char in front_vowels:
            result[i] = back_vowels[0]
    return "".join(result)


def _mutate_root_vowel(root: str, phonology: Dict[str, Any]) -> str:
    """Simula la apofonía/ablaut fusional cambiando una vocal interna de la raíz."""
    all_vowels = list(phonology["vowels"].keys())
    if len(all_vowels) < 2:
        return root
    chars = list(root)
    for i in range(len(chars) - 1, -1, -1):
        if chars[i] in all_vowels:
            alternatives = [v for v in all_vowels if v != chars[i]]
            chars[i] = random.choice(alternatives)
            break
    return "".join(chars)