**💠TDMBOT Discord Bot💠** 
Made with Python and Discord.py  
ES🇪🇸

---

### ¿Qué es TDMBOT?  
TDMBOT es un bot de discord creado desde 0 con Python y con ayuda de la librería Discord.py, la opción por excelencia para desarrollar bots de discord con este maravilloso lenguaje🐍, esta potente librería Open Source ofrece una integración completa y funcional con la API de Discord permitiéndonos crear nuestros bots de manera sencilla, su sintaxis y sus clases nos servirán para interactuar con todo lo que tiene Discord para ofrecernos al crear nuestras aplicaciones, en mi caso he integrado todo esto con aún más librerías conocidas, usadas mucho en el ecosistema de Python con la finalidad de dotar al bot de funcionalidades interesantes, como mensajes generados por IA gracias a la API del modelo Gémini de Google🧠, a continuación explicaré todos los comandos que hasta ahora el bot tiene para ofrecer.  

---

## Comandos disponibles  

```bash
>help: Para visualizar todos los comandos e información general del bot
>ia(prompt): Consultar cualquier duda o interactuar con el modelo Gémini 1.5 flash de Google
>wiki(query): Búsqueda de algún artículo en Wikipedia
>img(query): Búsqueda de imágenes en Google
>yt(query): Búsqueda de videos en YouTube
>google(query): Búsqueda simple en Google
>meme/dankmeme/shitpost: Selecciona algún meme aleatorio de Reddit y lo envía al chat
>cat: Selecciona alguna imagen alearoria de gatitos y la envía al chat
>avatar(username): Muesra el avatar de un usuario
>spotify(username): Muestra lo que está escuchando un usuario en Spotify (el comando más inútil del bot)
>binary(int value): Convierte un número entero a binario
>convert(to_bin, to_text: text, bin): Convierte texto a binario y viceversa
>ocr(language code): Extrae texto de imágenes en distintos idiomas, especificados con su código de idioma
>translate(language: text): Traduce texto en distintos idiomas especificado el código de idioma a traducir
>dl(url): Descarga video de distintos sitios web y lo muestra en chat
```


---


## Limitaciones a considerar💡  
1: El comando ```bash>dl``` no puede descargar contenido de YouTube ya que el sitio detecta las solicitudes del bot como tráfico automatizado, estoy trabajando en arreglar esto  
2: Tienes que agregar todos los parámetros necesarios en ciertos comandos  
- En ```bash>translate``` tienes que agregar los códigos de idioma siguiendo el estandar [ISO 639-1](https://es.wikipedia.org/wiki/ISO_639-1)
- En ```bash>ocr``` tienes que agregar los códigos de idioma que se usan en los traineddata de [tesseract](https://github.com/tesseract-ocr/tessdata)
