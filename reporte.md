# Reporte

## Ecobici

### 1. Horarios y estaciones de mayor afluencia

Agregando el numero de veces que los usuarios utilizaron ecobicis en periodos de tiempo de 30 minutos se obtuvo la siguiente gráfica:

[Demanda Bicicletas](https://www.dropbox.com/s/pgmis7r1jpoyokj/demanda_bicis.png?dl=0)

La distribución cuenta con tres medias ubicadas en los intervalos 08:00-09:00, 14:00-15:00 y 18:00-19:00. La demanda de bicicletas es mayor en estos horarios puesto que se trata de las horas en las que las personas entran a trabajar/estudiar, salen a comer y regresan del trabajo/escuela.

Las estaciones con mas afluencia son:

Estaciones | Numero de salidas
---- | -----
27   | 25074
271  | 19426
18   | 18624
1    | 17833
21   | 16721

El promedio de utilización de una bicicleta es de 14 minutos.

En total se identificaron 452 estaciones de bicicleta en los datos.

### 2. Tendencia de uso

Nuestro análisis consistió en contruir y caracterizar las series de tiempo de utilización de bicicletas por cada una de las estaciones. Para caracterizar cada serie utilizamos una regresión lineal.

Nuestro método para identificar estaciones con tendencia de uso a la alta consistió en ordenar las pendientes de los ajustes lineales de las series. Dentro de las estaciones con las pendientes positivas mas grandes se encuentran:

Estaciones | Pendiente
--- | ---
61 | 0.649626
69 | 0.314748
54 | 0.218777

Las graficas estan disponibles en los siguientes enlaces:

* [Estación 61](https://www.dropbox.com/s/ew4evrw8ubl7cyz/estacion_61.png?dl=0)
* [Estación 69](https://www.dropbox.com/s/re7bu2d87lren8g/estacion_69.png?dl=0)
* [Estación 54](https://www.dropbox.com/s/7w0db94uitbo8ya/estacion_54.png?dl=0)

Al analizar las gráficas observamos que la tendencia global a lo largo de los tres meses es a la alta, sin embargo, es posible observar que, para todos los casos, la serie cae drásticamente en los últimos días del mes de Diciembre. Este comportamiento es explicado por el hecho de que dichos días empatan con los periodos vacacionales de muchas personas; periodos en donde la movilidad en la ciudad disminuye drásticamente.

¿Podemos categorizar las estaciones con base en su tendencia de uso?

Si. Una opción sería clasificarlas en tendencia creciente, tendencia 'estable' y tendencia decreciente. De hecho con el método implimentado (explicado anteriormente) es muy sencillo hacer esto: sería necesario definir los umbrales de decisión para las tendecias creciente y decreciente y categorizar las estaciones según dichos umbrales.

Dicha categorización sería muy útil a la hora de distribuir bicicletas a las estaciones. Por ejemplo, mandar mas bicicletas a las estaciones con tendencia a la alta, quitarlas de las estaciones con tendencia a la baja.

### 3. Matriz de origen-destino

La matriz esta disponible en el siguiente link:

[Matriz origen destino](https://www.dropbox.com/s/kajimzstszctxhu/heatmap.png?dl=0)

### 4. Perfiles de uso

Los resultados del proceso de clusterización estan disponibles en el siguiente enlace:

[Modelo perfil estaciones](https://www.dropbox.com/s/h7587uma8hzlyrb/demanda_estaciones.png?dl=0)

Nuestro proceso identificó los siguientes cuatro grupos:
* Grupo rojo. Estaciones menos demandadas. Representan el 52% del total.
* Grupo verde. Estaciones con nivel de demanda regular. Representan el 33% del total.
* Grupo amarillo. Estaciones con alta demanda. Representan el 14% del total.
* Grupo azul. Estaciones de movilidad crítica.

Los resultados anteriores concuerdan con lo observado en la matriz de origen-destino, en donde la mayoría de las rutas estan dentro del promedio azul
mientras que una cantidad mucho menor se encuentra dentro del promedio azul-claro. Finalmente, si observamos detalladamente, es posible encontrar algunos puntos en amarillo o rojo.

Otra tendencia que es posible observar en la matriz es que los usuarios utilizan la bici para paseos redondos. Sería bueno investigar a que se debe esto. Algunas hipotesis incluye salidas a comer o cancelación de la ruta.

Para nuestro modelo de "perfiles de uso", caracterizamos cada estación con su número total de entradas y salidas, posteriormente utilizamos k-means. Dado que ambos features tienen las mismas dimensiones decidimos no utilizar ningún método de normalización o escalado de datos.

Para identificar el número apropiado de perfiles de uso (k en k-means) utilizamos el metodo 'elbow' de manera visual. El gráfico generado esta disponible en:

[Elbow plot](https://www.dropbox.com/s/x8jf9zlspnwtvz0/kmeans-elbow.png?dl=0)

K-means nos pareció buena elección puesto que se trata de un módelo sencillo de clusterización que ofrece grupos excluyentes.

### 5. Atributos geográficos

De la matriz de origen-destino, las tres rutas mas concurridas fueron:

Ruta | Ocasiones | Ubicación geográfica 
--- | --- | 
211-217 | 1727 | Polanco
18-1 | 1368 | Cuauhtemoc-Reforma
183-174 | 1118 | San Rafael

Los mapas con la ubicación de las rutas estan disponibles en:
* [211-217](https://www.dropbox.com/s/6xm4o1ki9xarvl5/route_211_217.png?dl=0)
* [18-1](https://www.dropbox.com/s/sr7v8q8c3suz9n1/route_18_1.png?dl=0)
* [183-174](https://www.dropbox.com/s/nofho6r3uvh2jwc/route_183_174.png?dl=0)

Adicionalmente, hemos creado un mapa con las ubicaciones del grupo azul (estaciones con el mayor uso):

[Estaciones mayor demanda](https://www.dropbox.com/s/2y8vwd4j6trm75z/estaciones.png?dl=0)

Las imagenes anteriores corroboran el comportamiento de las relaciones encontradas en las preguntas pasadas. Es posible observar que las rutas y estaciones con mayor demanda estan ubicadas en puntos a lo largo de reforma centro.
También es posible observar que hay dos estaciones con mucha demanda en Buenavista lo cual podría explicarse por el hecho de que en ese punto convergen diversos sistemas de transporte masivo (metro, metrobus, tren suburvano).

Los atributos geográficos para nuestro análisis de movivilidad del sistema Ecobici son esenciales por las siguientes razones:
* Nos permite ubicar las estaciones en una zona geográfica.
* Nos permite relacionar las estaciones con todas las demas entidades que comparten la misma ubicación geográfica i.e. estaciones de transporte, oficinas, escuelas, ...
* Nos permitiría realizar analísis de estaciones por zonas geográficas.

### 6. Notas

Utilicé el archivo de ecobici de Septiembre en lugar del de Octubre. La razón fue que en el archivo de Octubre las horas de retiro de bicis parecían estar incorrectas.

## Bebés



El archivo con las estimaciones se encuentra en el siguiente enlace:

[Estimaciones bebes 0 a meses](https://www.dropbox.com/s/dstpkuj6t3047zi/ageb.csv?dl=0)

Fuentes de datos:

[1](http://www.inegi.org.mx/sistemas/consulta_resultados/ageb_urb2010.aspx?c=28111&s=est)

