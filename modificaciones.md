## 1) Coherencia y veracidad (lo que dices vs lo que haces)

### Problemas

* En la landing afirmas métricas concretas post-ataque (“72% del cluster unido”, “67% eficiencia”) , pero:

  * `attack_simulator.py` **solo elimina nodos al azar** y reporta **fragmentación = nº de componentes**. No calcula “cluster unido” ni “eficiencia”. Además exporta métricas “final_entropy=0.0, final_syntropy=1.0” **siempre**, incluso tras destruir la red .
  * El simulador web también mata nodos al azar y muestra un mensaje fijo (“Estructura mantiene integridad”), sin análisis real .
* `data_generator.py` dice “cristalización / convergencia” pero en realidad:

  * pone **todos** los nodos como `coherent` con `coherence_score=1.0` (no hay dinámica ni convergencia progresiva),
  * crea una malla conectando 3 vecinos cercanos (eso sí) .
* README promete “métricas de eficiencia global”  pero eso no existe en el código.

### Recomendación mínima antes de publicar

* O bien **bajas el marketing** y lo presentas como “visualización conceptual / toy model”, o bien implementas métricas reales (aunque sean simples).
* Si quieres mantener la narrativa “resiliencia”:

  * En Python calcula **tamaño del componente gigante** (GCC), **nº de componentes**, **densidad**, **grado medio**, y si quieres “eficiencia global” usa `networkx.global_efficiency(G)` (ojo: coste en grafos grandes).
  * En el JSON exporta esas métricas y muéstralas en la web.

---

## 2) Inconsistencias operativas (nombres, defaults, flujo)

### Problemas

* `data_generator.py` tiene `DEFAULT_NODES = 80` pero el archivo se llama `syntropy_100.json` por defecto . Eso es confuso y suena a descuido.
* `attack_simulator.py` asume `INPUT_FILE="syntropy_100.json"` y `OUTPUT_FILE="syntropy_attacked.json"` . Si el usuario genera 80 nodos, el nombre “100” ya miente.
* Los visores piden “pega tu JSON aquí” (UX frágil).  

### Recomendación mínima

* Renombra a algo neutro: `syntropy.json` y `syntropy_attacked.json`, o usa el nº real en el nombre (`syntropy_{nodes}.json`) y propágalo.
* En web: añade opción “Cargar archivo .json” (File input) además de textarea. Pegar JSON es una tortura.

---

## 3) Seguridad y robustez web (básico)

### Problemas

* Dependencias por CDN sin integridad (SRI) y sin control de versión real:

  * Tailwind CDN, three.js r128, chart.js, fontawesome…   
* Mucho JS inline: difícil de mantener, y si algún día pones CSP estricta, te lo rompe.

### Recomendación práctica

* Para un portfolio/demo está bien usar CDN, pero:

  * fija versiones (ya lo haces con r128, bien),
  * si es para “subir a web seria”, empaqueta (Vite/Parcel) o al menos añade SRI a los `<script>`/`<link>`.
* Separa JS a archivos `.js` y deja HTML limpio.

---

## 4) Rendimiento y experiencia (lo notarás en equipos modestos)

### Problemas

* En `index.html` creas una escena 3D de fondo a pantalla completa + animaciones constantes + blur/backdrop + sombras. Eso es precioso, pero puede freír GPU/batería .
* En los visores hay render loop constante aunque no cambie nada  .

### Recomendación mínima

* Pausa animación cuando la pestaña no está visible (`document.visibilitychange`).
* Limita FPS (requestAnimationFrame con throttle) o reduce geometría/efectos.
* Añade “reduce motion” si el usuario lo pide (CSS `prefers-reduced-motion`).

---

## 5) Documentación de cara a web (lo que un visitante entiende)

### Problemas

* README sirve para devs, pero para web te falta:

  * “qué es esto” en 3 líneas,
  * “qué es real y qué es conceptual” (importante para no vender humo),
  * instrucciones “1 click” (sin terminal) para probar visualizaciones .

### Recomendación mínima

* Añade en README (y/o en la web) una sección “Modelo”:

  * Qué simplificaciones hay (p.ej. “ataque aleatorio”, “coherencia forzada”).
  * Qué métricas son reales y cuáles son placeholders (ahora mismo varias son placeholders).

---

## Cambios concretos que yo haría antes de subir (lista corta y ejecutable)

1. **Arreglar la mentira “0/1 métricas”**: en ataque, no exportes `final_entropy=0` y `final_syntropy=1` siempre. O las calculas, o las eliminas. 
2. **Unificar naming y defaults**: `DEFAULT_NODES` y nombre de output coherentes. 
3. **Cambiar UX de “pega JSON”** por “sube archivo JSON” (+ mantener textarea opcional).  
4. **Ajustar la landing**: o quitas 72%/67% o lo haces medible y demostrado. 
5. **Empaquetar o endurecer dependencias** (mínimo: versiones + SRI si vas en serio).

---

Si quieres, en el siguiente paso puedo:

* proponerte una estructura de publicación (carpetas / build) para dejarlo “subible” en producción, y
* devolverte un README revisado (honesto, técnico y vendible sin humo) alineado con lo que realmente hace el proyecto ahora.

