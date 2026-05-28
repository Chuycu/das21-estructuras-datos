COLORES = {
    "fondo":        "#F8F7F4",
    "superficie":   "#FFFFFF",
    "borde":        "#D3D1C7",
    "texto":        "#2C2C2A",
    "texto_sec":    "#5F5E5A",
    "acento":       "#185FA5",
    "acento_light": "#E6F1FB",
    "dep":          "#639922",
    "dep_light":    "#EAF3DE",
    "anx":          "#BA7517",
    "anx_light":    "#FAEEDA",
    "str":          "#993C1D",
    "str_light":    "#FAECE7",
    "normal":       "#5F5E5A",
    "normal_light": "#F1EFE8",
    "barra_dep":    "#97C459",
    "barra_anx":    "#EF9F27",
    "barra_str":    "#D85A30",
}

NIVEL_COLORES = {
    "Depresión":  (COLORES["dep"],  COLORES["dep_light"],  COLORES["barra_dep"]),
    "Ansiedad":   (COLORES["anx"],  COLORES["anx_light"],  COLORES["barra_anx"]),
    "Estrés":     (COLORES["str"],  COLORES["str_light"],  COLORES["barra_str"]),
}
