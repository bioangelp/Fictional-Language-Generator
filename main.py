import json
import random
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

# Importar los 5 motores lingüísticos reales
from phonology import build_phonology
from morphology import build_morphology
from lexicon import build_lexicon
from syntax import build_syntax
from script_gen import build_script


# =====================================================================
# 1. Variables
# =====================================================================
@dataclass
class LanguageConfig:
    # Categoria 1: Textura Acústica (Ejes 1, 2, 3)
    voiceless_consonant_weight: float = 0.5
    voiced_plosives_weight: float = 0.5
    tonal_probability: float = 0.5
    vowel_to_consonant_ratio: float = 0.5
    glottal_and_click_freq: float = 0.5
    max_consonant_cluster: float = 0.5
    labial_dental_weight: float = 0.5
    velar_uvular_weight: float = 0.5
    back_vowel_bias: float = 0.5

    # Categoria 2: Arquitectura de Palabras (Ejes 4, 5)
    base_root_length: float = 0.5
    max_affixes_per_word: float = 0.5
    compound_word_prob: float = 0.5
    vowel_harmony_strictness: float = 0.5
    root_mutation_rate: float = 0.5
    irregular_exception_rate: float = 0.5

    # Categoria 3: Flujo de Pensamiento / Sintaxis (Ejes 6, 7)
    verb_slot_index: float = 0.5
    adposition_type: float = 0.5
    auxiliary_placement: float = 0.5
    case_marking_count: float = 0.5
    syntax_scramble_prob: float = 0.5
    helper_particle_density: float = 0.5

    # Categoria 4: Clasificación del Mundo / Semántica (Ejes 8, 9)
    noun_class_total: float = 0.5
    class_prefix_visibility: float = 0.5
    adjective_agreement_flag: float = 0.5
    body_nature_metaphor_rate: float = 0.5
    unique_root_generation_rate: float = 0.5
    abstract_derivational_affixes: float = 0.5

    # Categoria 5: Precisión y Tiempo / Verbos (Ejes 10, 11)
    tense_marker_count: float = 0.5
    aspect_affix_weight: float = 0.5
    standalone_time_adverbs: float = 0.5
    evidential_suffix_count: float = 0.5
    mood_marker_complexity: float = 0.5
    verb_string_length_modifier: float = 0.5

    # Categoria 6: Expresión Social y Material / Escritura (Ejes 12, 13, 14)
    pronoun_set_multipliers: float = 0.5
    honorific_affix_freq: float = 0.5
    lexical_caste_split: float = 0.5
    bezier_curve_ratio: float = 0.5
    sharp_vertex_angle_weight: float = 0.5
    continuous_stroke_length: float = 0.5
    total_unique_glyphs: float = 0.5
    strokes_per_glyph_limit: float = 0.5
    glyph_to_phoneme_mapping: float = 0.5

    def apply_effects(self, effects: Dict[str, float], learning_rate: float = 0.45):
        """
        Actualiza las variables según las respuestas del usuario (-1.0 a 1.0)
        manteniéndolas dentro del rango [0.0, 1.0].
        """
        for var_name, delta in effects.items():
            if hasattr(self, var_name):
                current_val = getattr(self, var_name)
                new_val = current_val + (delta * learning_rate)
                clamped_val = max(0.0, min(1.0, round(new_val, 4)))
                setattr(self, var_name, clamped_val)
            else:
                print(f"Advertencia: La variable '{var_name}' no existe en LanguageConfig.")


# =====================================================================
# 2. CARGADOR DE PREGUNTAS 
# =====================================================================

def load_questionnaire(filepath: str = "questions.json") -> List[Dict[str, Any]]:
    """Lee el archivo JSON de preguntas y selecciona 1 pregunta por pool_id."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    pools: Dict[str, List[Dict[str, Any]]] = {}
    for q in data.get("questions", []):
        pool_id = q.get("pool_id", q["question_id"])
        pools.setdefault(pool_id, []).append(q)

    # Elige 1 pregunta aleatoria por cada pool (escalable cuando agregues 5 por eje)
    selected_questions = [random.choice(q_list) for q_list in pools.values()]
    return selected_questions


def generate_language_pipeline(user_selected_options: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Ejecuta la tubería completa: aplica los pesos de las respuestas y corre
    los 5 módulos lingüísticos en orden estricto.
    """
    config = LanguageConfig()

    for option in user_selected_options:
        effects = option.get("effects", {})
        config.apply_effects(effects)

    # llama las funciones
    phonology_data = build_phonology(config)
    morphology_data = build_morphology(config, phonology_data)
    lexicon_data = build_lexicon(config, phonology_data, morphology_data)
    syntax_data = build_syntax(config, phonology_data, morphology_data, lexicon_data)
    script_data = build_script(config, phonology_data, lexicon_data)

    return {
        "config_variables": asdict(config),
        "phonology": phonology_data,
        "morphology": morphology_data,
        "lexicon": lexicon_data,
        "syntax": syntax_data,
        "script": script_data
    }


# =====================================================================
# 3. PRUEBA 
# =====================================================================
if __name__ == "__main__":
    questions = load_questionnaire("questions.json")
    simulated_answers = []

    print(f"Cargadas {len(questions)} preguntas del cuestionario. Simulando respuestas...\n")
    for q in questions:
        # Simulamos que el usuario elige una opción al azar en cada pregunta
        chosen_option = random.choice(q["options"])
        simulated_answers.append(chosen_option)
        print(f"[{q['axis_id']}] {q['question_text']}")
        print(f"  -> Respuesta elegida: {chosen_option['text']}\n")

    language = generate_language_pipeline(simulated_answers)

    print("=" * 65)
    print("RESUMEN DEL IDIOMA GENERADO")
    print("=" * 65)
    print(f"Tipología Morfológica : {language['morphology']['typology']}")
    print(f"Orden Sintáctico      : {language['syntax']['rules']['base_word_order']}")
    print(f"Es Tonal              : {language['phonology']['is_tonal']}")
    print(f"Armonía Vocálica      : {language['phonology']['uses_vowel_harmony']}")
    print(f"Sistema de Escritura  : {language['script']['script_type']} ({language['script']['writing_tool_style']})")
    print(f"Total de Glifos SVG   : {language['script']['total_glyphs_generated']}")

    print("\n--- MUESTRA DEL DICCIONARIO (Primeras 8 palabras) ---")
    for concept, info in list(language["lexicon"]["dictionary"].items())[:8]:
        print(f"  {concept.ljust(10)} = {info['word'].ljust(12)} | Origen: {info['origin']}")

    print("\n--- TRADUCCIÓN Y GLOSA DEL PANGRAMA ---")
    pangram = language["syntax"]["translated_corpus"][0]
    print(f"  Inglés   : {pangram['english_original']}")
    print(f"  Conlang  : {pangram['conlang_text']}")
    print(f"  Glosa    : {pangram['interlinear_gloss']}")