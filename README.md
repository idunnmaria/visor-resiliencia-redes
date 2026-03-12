# **Proyecto Sintropía | Arquitectura del Orden**

Este proyecto es una visualización interactiva basada en la **Teoría de Sintropía Digital**. Demuestra cómo algoritmos de convergencia forzada pueden transformar ruido aleatorio (caos) en estructuras de malla cristalina altamente ordenadas y resilientes.

## **📂 Estructura del Proyecto**

El proyecto consta de dos partes:

1. **El Motor (Python):** Scripts que simulan la física de los nodos y generan los datos.  
2. **El Visor (Web):** Una interfaz Three.js que renderiza los resultados en 3D.

## **🚀 Guía de Inicio Rápido**

### **1\. Requisitos Previos**

Necesitas tener instalado Python 3.x y la librería networkx para los cálculos de topología.

pip install networkx

### **2\. Generar el Universo (Sintropía)**

Ejecuta el generador para crear una estructura de orden perfecto (0.0 de Entropía). Esto creará el archivo syntropy\_100.json.

python data\_generator.py \--nodes 100

### **3\. Simular un Ataque (Resiliencia)**

Pon a prueba tu red. Este script elimina aleatoriamente un porcentaje de nodos y calcula la integridad estructural restante. Generará syntropy\_attacked.json.

\# Simular un daño del 20%  
python attack\_simulator.py \--damage 0.2

### **4\. Visualización**

Simplemente abre index.html en tu navegador.

* **Ver Sintropía:** Carga los datos de la red perfecta.  
* **Simular Ataque:** Muestra visualmente los daños y la fragmentación.

## **🛠️ Detalles Técnicos**

### **Algoritmo de Convergencia**

El script data\_generator.py utiliza un modelo de atracción gravitacional donde los nodos con mayor coherencia actúan como "Hubs", atrayendo y realineando a los nodos caóticos cercanos hasta alcanzar un estado de equilibrio (Sintropía \= 1.0).

### **Métricas de Resiliencia**

El attack\_simulator.py no solo borra nodos; realiza un análisis de grafos para medir:

* **Fragmentación:** En cuántas "islas" desconectadas se ha roto la red.  
* **Eficiencia Global:** La capacidad restante de la red para transmitir información de un punto A a un punto B.

© 2025 Proyecto Sintropía. Open Source.