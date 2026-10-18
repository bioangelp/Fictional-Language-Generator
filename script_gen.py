import random
from typing import Dict, List, Tuple, Any

# =====================================================================
# CUADRÍCULA BASE DE 3x3 PUNTOS (Coordenadas en un lienzo de 100x100)
# Los 9 nodos invisibles por donde pueden viajar los trazos del alfabeto
# =====================================================================

GRID_POINTS: List[Tuple[int, int]] = [
    (20, 20), (50, 20), (80, 20),  # Fila superior (0, 1, 2)
    (20, 50), (50, 50), (80, 50),  # Fila central  (3, 4, 5)
    (20, 80), (50, 80), (80, 80)   # Fila inferior (6, 7, 8)
]

# Conexiones lógicas entre nodos para trazos rectos/angulares y curvos
ADJACENT_PAIRS = [
    (0, 1), (1, 2), (3, 4), (4, 5), (6, 7), (7, 8), # Horizontales
    (0, 3), (3, 6), (1, 4), (4, 7), (2, 5), (5, 8), # Verticales
    (0, 4), (4, 8), (2, 4), (4, 6), (1, 3), (1, 5), (3, 7), (5, 7) # Diagonales
]


# =====================================================================
# MOTOR 5: CONSTRUCCIÓN DEL SISTEMA DE ESCRITURA Y GLIFOS SVG
# =====================================================================

def build_script(
    config: Any,
    phonology: Dict[str, Any],
    lexicon: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Lee los Ejes 13 (Resistencia Material) y 14 (Densidad Gráfica) para determinar
    el tipo de escritura, crear la semilla de trazos tipográficos y generar un SVG
    único para cada letra, sílaba o palabra del idioma.
    """
    # 1. Determinar el Tipo de Sistema de Escritura según glyph_to_phoneme_mapping (Eje 14)
    if config.glyph_to_phoneme_mapping < 0.35:
        script_type = "Alphabet"     # 1 símbolo = 1 fonema (consonante o vocal)
    elif config.glyph_to_phoneme_mapping < 0.70:
        script_type = "Syllabary"    # 1 símbolo = 1 sílaba completa (Consonante + Vocal)
    else:
        script_type = "Logographic"  # 1 símbolo = 1 palabra raíz completa del diccionario

    # 2. Definir las Unidades Lingüísticas que recibirán un símbolo gráfico
    target_units = _select_script_units(script_type, config, phonology, lexicon)

    # 3. Calcular Parámetros Geométricos de la Herramienta (Eje 13 y Eje 14)
    # Cuántos trazos separados tiene cada glifo (de 2 en alfabetos simples a 7 en logogramas)
    min_strokes = 2 if script_type == "Alphabet" else 3
    max_strokes = min_strokes + int(round(config.strokes_per_glyph_limit * 4))

    # Cuántos nodos recorre un solo trazo sin levantar la mano (1 = cincel corto, 4 = pincel continuo)
    nodes_per_stroke = 1 + int(round(config.continuous_stroke_length * 3))

    # Estilo de las esquinas y terminaciones del trazo en SVG
    stroke_linecap = "round" if config.bezier_curve_ratio >= 0.5 else "square"
    stroke_linejoin = "round" if config.sharp_vertex_angle_weight < 0.5 else "miter"
    stroke_width = 7 if config.sharp_vertex_angle_weight > 0.6 else 5

    # 4. Generar la "Semilla Tipográfica" (Base Stroke Motifs)
    # Creamos entre 6 y 8 trazos madre que se combinarán para que todo el alfabeto tenga coherencia
    base_motifs = _generate_font_seed(
        curve_ratio=config.bezier_curve_ratio,
        sharp_weight=config.sharp_vertex_angle_weight,
        nodes_per_stroke=nodes_per_stroke,
        seed_size=8
    )

    # 5. Ensamblar los Glifos SVG únicos para cada unidad del idioma
    glyph_chart: List[Dict[str, str]] = []
    used_combinations = set()

    for unit in target_units:
        svg_code, path_data = _create_unique_glyph(
            base_motifs=base_motifs,
            min_strokes=min_strokes,
            max_strokes=max_strokes,
            stroke_width=stroke_width,
            linecap=stroke_linecap,
            linejoin=stroke_linejoin,
            used_set=used_combinations
        )
        glyph_chart.append({
            "unit": unit["symbol"],
            "meaning_or_ipa": unit["reference"],
            "svg": svg_code,
            "raw_path": path_data
        })

    return {
        "script_type": script_type,
        "writing_tool_style": _describe_material_style(config),
        "total_glyphs_generated": len(glyph_chart),
        "geometry_params": {
            "curve_ratio": round(config.bezier_curve_ratio, 2),
            "sharp_angle_weight": round(config.sharp_vertex_angle_weight, 2),
            "strokes_per_glyph_range": f"{min_strokes}-{max_strokes}",
            "continuous_stroke_nodes": nodes_per_stroke
        },
        "glyph_chart": glyph_chart
    }


# =====================================================================
# FUNCIONES AUXILIARES DE GENERACIÓN PROCEDIMENTAL EN CUADRÍCULA 3x3
# =====================================================================

def _select_script_units(
    script_type: str,
    config: Any,
    phonology: Dict[str, Any],
    lexicon: Dict[str, Any]
) -> List[Dict[str, str]]:
    """Elige qué elementos del idioma van a tener su propio símbolo en la tabla del PDF."""
    units = []

    if script_type == "Alphabet":
        # Un glifo por cada vocal y cada consonante activa
        for v in phonology["vowels"].keys():
            units.append({"symbol": v, "reference": phonology["ipa_guide"].get(v, f"/{v}/")})
        for c in phonology["consonants"].keys():
            units.append({"symbol": c, "reference": phonology["ipa_guide"].get(c, f"/{c}/")})

    elif script_type == "Syllabary":
        # Combina las consonantes y vocales más frecuentes para armar el silabario (ej. ka, ke, ko...)
        top_c = list(phonology["consonants"].keys())[:8]
        top_v = list(phonology["vowels"].keys())[:4]
        for c in top_c:
            for v in top_v:
                syl = c + v
                units.append({"symbol": syl, "reference": f"Syllable [{syl}]"})

    else:  # Logographic
        # Un glifo por cada palabra raíz del diccionario
        max_logos = int(15 + round(config.total_unique_glyphs * 25))
        for concept_id, data in list(lexicon["dictionary"].items())[:max_logos]:
            units.append({
                "symbol": data["word"],
                "reference": f" Meaning: '{concept_id.upper()}'"
            })

    return units


def _generate_font_seed(
    curve_ratio: float,
    sharp_weight: float,
    nodes_per_stroke: int,
    seed_size: int = 8
) -> List[str]:
    """
    Crea la lista de trazos base (en código SVG path 'M ... L ... Q ...')
    que definen la identidad estética de todo el sistema de escritura.
    """
    motifs = []
    for _ in range(seed_size):
        start_idx = random.randint(0, 8)
        current_idx = start_idx
        x0, y0 = GRID_POINTS[current_idx]
        path_cmds = [f"M {x0} {y0}"]

        for _ in range(nodes_per_stroke):
            # Buscar nodos vecinos o saltar a otro punto según si prefiere ángulos agudos
            candidates = [b for (a, b) in ADJACENT_PAIRS if a == current_idx] + \
                         [a for (a, b) in ADJACENT_PAIRS if b == current_idx]
            if not candidates or random.random() < sharp_weight * 0.4:
                next_idx = random.choice([i for i in range(9) if i != current_idx])
            else:
                next_idx = random.choice(candidates)

            x1, y1 = GRID_POINTS[next_idx]

            # Decidir si este segmento es una curva Bézier (Q) o una línea recta de cincel (L)
            if random.random() < curve_ratio:
                # Punto de control intermedio desplazado para curvar la línea
                ctrl_idx = random.choice([i for i in range(9) if i not in (current_idx, next_idx)])
                cx, cy = GRID_POINTS[ctrl_idx]
                path_cmds.append(f"Q {cx} {cy}, {x1} {y1}")
            else:
                path_cmds.append(f"L {x1} {y1}")

            current_idx = next_idx

        motifs.append(" ".join(path_cmds))

    return motifs


def _create_unique_glyph(
    base_motifs: List[str],
    min_strokes: int,
    max_strokes: int,
    stroke_width: int,
    linecap: str,
    linejoin: str,
    used_set: set
) -> Tuple[str, str]:
    """
    Combina de 2 a N trazos de la semilla (aplicando espejo horizontal o vertical
    ocasional) para armar un carácter único y devolver su bloque SVG listo para HTML/PDF.
    """
    for _ in range(50):
        num_strokes = random.randint(min_strokes, max_strokes)
        chosen = random.sample(base_motifs, k=min(num_strokes, len(base_motifs)))
        signature = "|".join(sorted(chosen))
        if signature not in used_set:
            used_set.add(signature)
            break

    combined_path = " ".join(chosen)

    svg_xml = (
        f'<svg viewBox="0 0 100 100" width="64" height="64" xmlns="http://www.w3.org/2000/svg">'
        f'<path d="{combined_path}" fill="none" stroke="currentColor" '
        f'stroke-width="{stroke_width}" stroke-linecap="{linecap}" stroke-linejoin="{linejoin}" />'
        f'</svg>'
    )
    return svg_xml, combined_path


def _describe_material_style(config: Any) -> str:
    """Devuelve una descripción legible para el PDF sobre el medio físico de escritura."""
    if config.bezier_curve_ratio < 0.30 and config.sharp_vertex_angle_weight > 0.60:
        return "Runic / Chiseled (Hard stone or wood-grain cuts with straight angular strokes)"
    elif config.bezier_curve_ratio > 0.70 and config.continuous_stroke_length > 0.60:
        return "Calligraphic / Flowing (Soft brush or reed pen on paper with continuous curves)"
    elif config.bezier_curve_ratio > 0.60 and config.sharp_vertex_angle_weight < 0.40:
        return "Rounded / Leaf-Inscribed (Curved stylus strokes avoiding straight horizontal tears)"
    else:
        return "Hybrid Standard Script (Balanced mix of geometric lines and curved loops)"