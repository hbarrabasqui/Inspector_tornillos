from pathlib import Path

import gradio as gr
import numpy as np
import tensorflow as tf
from PIL import Image

# 1. Cargar el modelo ya entrenado (el archivo está al lado de este script)
RUTA_MODELO = Path(__file__).parent / "modelo_inspector.keras"
modelo = tf.keras.models.load_model(RUTA_MODELO)


# 2. La función: recibe una foto y devuelve la respuesta
def inspeccionar(foto):
    if foto is None:
        return None
    img = foto.convert("RGB").resize((224, 224))
    x = np.array(img, dtype="float32")[np.newaxis, ...]   # (1, 224, 224, 3)
    p_defecto = float(modelo.predict(x, verbose=0)[0][0])
    return {"DEFECTO": p_defecto, "OK": 1 - p_defecto}


# 3. La ventana de Gradio
app = gr.Interface(
    fn=inspeccionar,
    inputs=gr.Image(type="pil", label="Foto del tornillo"),
    outputs=gr.Label(num_top_classes=2, label="Resultado"),
    title="Inspector de tornillos: OK / DEFECTO",
    description=(
        "Subí una foto de un tornillo. El modelo responde OK o DEFECTO con su "
        "porcentaje de confianza. Solo conoce estas dos respuestas: si le "
        "mostrás otra cosa, igual va a elegir una de las dos."
    ),
)

if __name__ == "__main__":
    app.launch()
