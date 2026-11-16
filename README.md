# Inspector de tornillos: OK / DEFECTO

Prototipo de clasificación de imágenes, desarrollado como proyecto académico en la Tecnicatura Superior en Ciencia de Datos e IA (IFTS N.º 24), en la materia Laboratorio de Tecnologías de la Imagen Digital. Clasifica la foto de un tornillo como **OK** o **DEFECTO** y muestra el porcentaje de confianza de cada respuesta. Está hecho con fotos propias.

## Cómo usarla

Requiere Python 3.12.

```bash
pip install -r requirements.txt
python app.py
```

Después abrir en el navegador la dirección que aparece en la terminal (normalmente `http://127.0.0.1:7860`) y subir la foto de un tornillo.

El cuaderno `inspector.ipynb` tiene todo el proceso: carga de fotos, entrenamiento y evaluación. Se ejecuta de arriba hacia abajo, con la carpeta `datos/` al lado.

## Cómo funciona

- **Tarea:** clasificación de imágenes en dos clases (OK / DEFECTO).
- **Modelo:** MobileNetV2 preentrenada con ImageNet, con la base congelada. Solo entrené la parte final, que decide entre OK y DEFECTO. Así alcanzan pocas fotos.
- **Datos:** fotos sacadas por mí con el celular, sobre un mismo fondo.
  - `datos/ok`: 29 fotos de tornillos en buen estado.
  - `datos/defecto`: 32 fotos de tornillos doblados o con la rosca o la cabeza dañadas.
  - `datos/prueba_final`: 21 fotos (12 OK y 9 DEFECTO) que **no se usaron para entrenar**. Los DEFECTO son tornillos parecidos con otras curvaturas y los OK son, en su mayoría, de otro tipo.
  - `datos/limites`: 13 fotos de objetos que no son tornillos, para ver cómo responde el modelo.
- **Entrenamiento:** 80 % de las fotos de `ok` y `defecto` para entrenar y 20 % para validar, con el reparto fijado para poder repetirlo.
- **Interfaz:** Gradio.

## Resultados

Medidos en `prueba_final` (21 fotos), entrenando 5 veces con semillas distintas:

| | Resultado |
|---|---|
| Aciertos totales | 15 a 16 de 21 |
| Tornillos DEFECTO detectados | 9 de 9, en todas las corridas |
| Tornillos OK aceptados | 6 a 7 de 12 |

El modelo guardado (`modelo_inspector.keras`) corresponde a una de esas corridas: 16 de 21, con 7 de 12 OK y 9 de 9 DEFECTO.

Son pocas fotos, así que estos números son orientativos.

## Límites

- **Prefiere rechazar:** no dejó pasar ningún defectuoso en las pruebas, pero rechaza casi la mitad de los tornillos OK de un tipo que no estaba en el entrenamiento. Mi hipótesis, que no probé, es que faltan fotos de ese tipo de tornillo.
- **Solo conoce dos respuestas:** si se le muestra algo que no es un tornillo, igual responde OK o DEFECTO, porque no tiene una opción "esto no es un tornillo".
- **Pocos datos y un solo fondo:** 61 fotos de entrenamiento, todas con el mismo fondo.
- **Pruebas que no mejoraron:** probé aumento de datos (espejo, giro leve y cambio de brillo) y pasar las fotos a escala de grises. Ninguna mejoró el resultado, así que el modelo final no las usa.
- **Datos mal etiquetados:** encontré una foto mal etiquetada durante las pruebas y la corregí; el resultado mejoró.

## Qué seguiría explorando

- Sumar fotos de más tipos de tornillos, con otros fondos y luces.
- Agregar un aviso del tipo "no estoy seguro" cuando la confianza es baja.

## Estructura

```
app.py                   aplicación (Gradio)
inspector.ipynb          cuaderno con el proceso completo
modelo_inspector.keras   modelo entrenado
requirements.txt         librerías
datos/                   fotos
```

## Nota

Lo desarrollé con asistencia de IA (Claude) como apoyo para planificar, explicar conceptos y revisar el código. Las fotos, las pruebas y las decisiones son mías.
