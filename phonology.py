import random
from typing import Dict, List, Any

# =====================================================================
# BASE DE DATOS ESTÁTICA FONÉTICA (Pesos base e IPA)
# Clasificamos los sonidos por sus propiedades biomecánicas reales
# para que las 9 variables sepan exactamente a qué letras multiplicar.
# =====================================================================

CONSONANT_DATABASE = {
    # Sordas (sin vibración de cuerdas vocales) vs Sonoras (con vibración)
    # Frontales (labios/dientes) vs Profundas (velo/úvula/garganta)
    "p":  {"base": 2.0, "voiceless": True,  "plosive": True,  "place": "front", "ipa": "/p/",  "liquid": False},
    "b":  {"base": 1.5, "voiceless": False, "plosive": True,  "place": "front", "ipa": "/b/",  "liquid": False},
    "t":  {"base": 7.0, "voiceless": True,  "plosive": True,  "place": "front", "ipa": "/t/",  "liquid": False},
    "d":  {"base": 4.0, "voiceless": False, "plosive": True,  "place": "front", "ipa": "/d/",  "liquid": False},
    "k":  {"base": 3.0, "voiceless": True,  "plosive": True,  "place": "back",  "ipa": "/k/",  "liquid": False},
    "g":  {"base": 2.0, "voiceless": False, "plosive": True,  "place": "back",  "ipa": "/g/",  "liquid": False},
    "q":  {"base": 0.5, "voiceless": True,  "plosive": True,  "place": "back",  "ipa": "/q/",  "liquid": False},
    "f":  {"base": 2.2, "voiceless": True,  "plosive": False, "place": "front", "ipa": "/f/",  "liquid": False},
    "v":  {"base": 1.2, "voiceless": False, "plosive": False, "place": "front", "ipa": "/v/",  "liquid": False},
    "th": {"base": 1.8, "voiceless": True,  "plosive": False, "place": "front", "ipa": "/θ/",  "liquid": False},
    "s":  {"base": 6.5, "voiceless": True,  "plosive": False, "place": "front", "ipa": "/s/",  "liquid": False},
    "z":  {"base": 1.0, "voiceless": False, "plosive": False, "place": "front", "ipa": "/z/",  "liquid": False},
    "sh": {"base": 1.8, "voiceless": True,  "plosive": False, "place": "mid",   "ipa": "/ʃ/",  "liquid": False},
    "zh": {"base": 0.5, "voiceless": False, "plosive": False, "place": "mid",   "ipa": "/ʒ/",  "liquid": False},
    "kh": {"base": 0.8, "voiceless": True,  "plosive": False, "place": "back",  "ipa": "/x/",  "liquid": False},
    "gh": {"base": 0.6, "voiceless": False, "plosive": False, "place": "back",  "ipa": "/ɣ/",  "liquid": False},
    "h":  {"base": 3.5, "voiceless": True,  "plosive": False, "place": "back",  "ipa": "/h/",  "liquid": False},
    "m":  {"base": 3.0, "voiceless": False, "plosive": False, "place": "front", "ipa": "/m/",  "liquid": True},
    "n":  {"base": 6.8, "voiceless": False, "plosive": False, "place": "front", "ipa": "/n/",  "liquid": True},
    "l":  {"base": 4.5, "voiceless": False, "plosive": False, "place": "front", "ipa": "/l/",  "liquid": True},
    "r":  {"base": 5.5, "voiceless": False, "plosive": False, "place": "mid",   "ipa": "/r/",  "liquid": True},
    "w":  {"base": 2.0, "voiceless": False, "plosive": False, "place": "front", "ipa": "/w/",  "liquid": True},
    "y":  {"base": 2.0, "voiceless": False, "plosive": False, "place": "mid",   "ipa": "/j/",  "liquid": True},
}

# Sonidos especiales no pulmonares (cortes glotales, eyectivas y chasquidos)
GLOTTAL_CLICK_DATABASE = {
    "'":  {"base": 3.0, "ipa": "/ʔ/"},  # Corte de aire en la garganta
    "k'": {"base": 1.5, "ipa": "/kʼ/"}, # K eyectiva explosiva
    "t'": {"base": 1.5, "ipa": "/tʼ/"}, # T eyectiva explosiva
    "!":  {"base": 1.0, "ipa": "/ǃ/"},  # Chasquido alveolar
}

VOWEL_DATABASE = {
    # Frontales/Claras vs Traseras/Profundas
    "i": {"base": 7.5, "group": "front", "ipa": "/i/", "tones": ["í", "ì", "î"]},
    "e": {"base": 11.0,"group": "front", "ipa": "/e/", "tones": ["é", "è", "ê"]},
    "a": {"base": 9.0, "group": "back",  "ipa": "/a/", "tones": ["á", "à", "â"]},
    "o": {"base": 7.0, "group": "back",  "ipa": "/o/", "tones": ["ó", "ò", "ô"]},
    "u": {"base": 4.0, "group": "back",  "ipa": "/u/", "tones": ["ú", "ù", "û"]},
}


# =====================================================================
# MOTOR 1: CONSTRUCCIÓN DEL PERFIL FONOLÓGICO
# =====================================================================

def build_phonology(config: Any) -> Dict[str, Any]:
    """
    Transforma las 9 variables acústicas (0.0 a 1.0) en el inventario de sonidos,
    pesos estadísticos y reglas de combinación silábica del idioma.
    """
    consonant_weights: Dict[str, float] = {}
    ipa_guide: Dict[str, str] = {}

    # 1. Calcular el peso de cada consonante según los Ejes 1, 2 y 3
    for symbol, props in CONSONANT_DATABASE.items():
        weight = props["base"]

        # Eje 1: Energía Vocal (Sordas vs Sonoras/Oclusivas)
        if props["voiceless"]:
            weight *= (0.3 + config.voiceless_consonant_weight * 1.7)
        if props["plosive"] and not props["voiceless"]:
            weight *= (0.2 + config.voiced_plosives_weight * 2.0)

        # Eje 2: Continuidad de Aire (Favorece líquidas/nasales si hay mucha vocal)
        if props["liquid"]:
            weight *= (0.4 + config.vowel_to_consonant_ratio * 1.6)

        # Eje 3: Profundidad Articulatoria (Labios/Dientes vs Garganta/Úvula)
        if props["place"] == "front":
            weight *= (0.2 + config.labial_dental_weight * 1.8)
        elif props["place"] == "back":
            weight *= (0.1 + config.velar_uvular_weight * 2.5)

        # Filtro de limpieza: si el peso cayó demasiado bajo, el sonido no existe en este idioma
        if weight >= 0.65:
            consonant_weights[symbol] = round(weight, 2)
            ipa_guide[symbol] = props["ipa"]

    # 2. Inyectar cortes glotales y chasquidos si la variable supera el umbral (Eje 2)
    if config.glottal_and_click_freq > 0.35:
        intensity = (config.glottal_and_click_freq - 0.35) * 2.5
        for symbol, props in GLOTTAL_CLICK_DATABASE.items():
            # Los chasquidos puros (!) solo aparecen en valores altos (> 0.65)
            if symbol == "!" and config.glottal_and_click_freq <= 0.65:
                continue
            w = round(props["base"] * intensity, 2)
            if w >= 0.5:
                consonant_weights[symbol] = w
                ipa_guide[symbol] = props["ipa"]

    # 3. Calcular el peso de cada vocal según el Eje 3 (Sesgo de vocales traseras/oscuras)
    vowel_weights: Dict[str, float] = {}
    front_vowels: List[str] = []
    back_vowels: List[str] = []

    for symbol, props in VOWEL_DATABASE.items():
        weight = props["base"]
        if props["group"] == "back":
            weight *= (0.3 + config.back_vowel_bias * 1.7)
            back_vowels.append(symbol)
        else:
            weight *= (0.3 + (1.0 - config.back_vowel_bias) * 1.7)
            front_vowels.append(symbol)

        vowel_weights[symbol] = round(weight, 2)
        ipa_guide[symbol] = props["ipa"]

    # 4. Definir Reglas de Tonos y Agrupación de Consonantes (Clusters)
    is_tonal = config.tonal_probability >= 0.65
    tonal_rate = round((config.tonal_probability - 0.5) * 1.2, 2) if is_tonal else 0.0

    # Escalar max_consonant_cluster (0.0 -> 1 sola consonante, 1.0 -> hasta 3 seguidas)
    max_cluster = 1 + int(round(config.max_consonant_cluster * 2))

    # Construir pares de consonantes permitidos (ej. "tr", "shk", "st")
    allowed_clusters = _generate_valid_clusters(consonant_weights, max_cluster)

    return {
        "consonants": consonant_weights,
        "vowels": vowel_weights,
        "vowel_groups": {"front": front_vowels, "back": back_vowels},
        "ipa_guide": ipa_guide,
        "is_tonal": is_tonal,
        "tonal_rate": tonal_rate,
        "max_consonant_cluster": max_cluster,
        "allowed_clusters": allowed_clusters,
        "vowel_ratio_target": round(0.30 + (config.vowel_to_consonant_ratio * 0.40), 2),
        "uses_vowel_harmony": config.vowel_harmony_strictness >= 0.60
    }


def _generate_valid_clusters(consonant_weights: Dict[str, float], max_cluster: int) -> List[str]:
    """
    Crea una lista coherente de grupos consonánticos permitidos al inicio de sílaba
    combinando consonantes activas con sonidos líquidos o sibilantes del propio idioma.
    """
    if max_cluster <= 1:
        return []

    active_consonants = list(consonant_weights.keys())
    liquids = [c for c in ["r", "l", "w", "y", "n", "m"] if c in active_consonants]
    sibilants = [c for c in ["s", "sh", "z", "f", "kh"] if c in active_consonants]
    stops = [c for c in ["p", "t", "k", "b", "d", "g", "q"] if c in active_consonants]

    clusters = []
    # Pares tipo Oclusiva + Líquida (tr, kr, pl, kw)
    for s in stops:
        for l in liquids:
            if s != l:
                clusters.append(s + l)

    # Pares tipo Sibilante + Oclusiva (st, sp, shk, khp)
    for sib in sibilants:
        for st in stops:
            clusters.append(sib + st)
            # Si permite hasta 3 consonantes seguidas, arma grupos como "str" o "shkr"
            if max_cluster >= 3:
                for l in liquids:
                    clusters.append(sib + st + l)

    return clusters


# =====================================================================
# MOTOR AUXILIAR: GENERADOR DE SÍLABAS Y RAÍCES FONÉTICAS
# Esta función es la que llamarán Morfología y Léxico para crear palabras.
# =====================================================================

def generate_phonetic_root(phonology: Dict[str, Any], syllable_count: int = 2) -> str:
    """
    Genera una palabra raíz o un afijo respetando estrictamente los pesos,
    la armonía vocálica, los tonos y los grupos de consonantes del idioma.
    """
    c_symbols = list(phonology["consonants"].keys())
    c_weights = list(phonology["consonants"].values())

    # Si la armonía vocálica está activa, toda la palabra debe usar vocales del mismo grupo
    if phonology["uses_vowel_harmony"]:
        chosen_group = "back" if random.random() < 0.5 else "front"
        allowed_v = phonology["vowel_groups"][chosen_group]
        v_symbols = [v for v in allowed_v if v in phonology["vowels"]]
        v_weights = [phonology["vowels"][v] for v in v_symbols]
    else:
        v_symbols = list(phonology["vowels"].keys())
        v_weights = list(phonology["vowels"].values())

    word = ""
    v_ratio = phonology["vowel_ratio_target"]

    for i in range(syllable_count):
        # 1. Ataque de la sílaba (Consonante inicial o grupo de consonantes)
        # Si el idioma tiene muchas vocales (v_ratio alto), la sílaba puede empezar directo con vocal
        if i == 0 and random.random() < (v_ratio - 0.25):
            onset = ""
        else:
            if phonology["allowed_clusters"] and random.random() < 0.25:
                onset = random.choice(phonology["allowed_clusters"])
            else:
                onset = random.choices(c_symbols, weights=c_weights, k=1)[0]

        # 2. Núcleo de la sílaba (Vocal o Tono)
        base_vowel = random.choices(v_symbols, weights=v_weights, k=1)[0]
        if phonology["is_tonal"] and random.random() < phonology["tonal_rate"]:
            nucleus = random.choice(VOWEL_DATABASE[base_vowel]["tones"])
        else:
            nucleus = base_vowel

        # 3. Coda de la sílaba (Consonante final opcional, menos probable si el idioma es muy fluido)
        coda = ""
        if random.random() > v_ratio:
            coda_candidate = random.choices(c_symbols, weights=c_weights, k=1)[0]
            # Evitar que los chasquidos o eyectivas queden al final de una sílaba si es difícil de leer
            if coda_candidate not in ["!", "k'", "t'"]:
                coda = coda_candidate

        word += onset + nucleus + coda

    return word