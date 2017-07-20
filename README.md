# buscamedvenezuela

Nota: Este repo existe para el deploy en heroku, está configurado para tal fin y por funciona correctamente de forma local. Todos los PATHS aquí mencionados son relativos a la estructura de este repositorio.

Los archivos: nltk.txt, Procfile, runtime.txt y requirements.txt son usados por Heroku para la instalación e inicio de la app en el servidor de Heroku.

En app/models.py se encuentran los modelos del modelo MVC
En app/templates/app se encuentran todas las vistas del modelo MVC
En app/views.py se encuentran los controladores del modelo MVC

baseDatos-completa.csv es el archivo en csv con el formato usado por el comando creado "loaddb" ( encontrado en app/management/commands/loaddb.py) para popular la base de datos con los componentes activos, medicinas y presentaciones

train.py es el script usado para entrenar el modelo elegido (regresión lineal), aquí ocurre todo el pre-procesamiento del texto del tweet y se hace la división 70% para entrenamiento y 30% para evaluación de los tweets clasificados a mano. El modelo entrenado es guardado bajo el nombre de "logistic_regression" y el vector de palabras de bag of words con el nombre de "vectorizer"

classifier.py es el script usado para obtener tweets que contengan nombres de "medicinas" en ellas y clasificarlos haciendo uso del modelo guardado por train.py. De igual forma agrega a la base de datos aquellos tweets que son clasificados como "oferta" o "demanda".