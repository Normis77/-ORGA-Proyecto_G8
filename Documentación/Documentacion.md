# UNIVERSIDAD DE SAN CARLOS DE GUATEMALA  
## FACULTAD DE INGENIERÍA  
### ESCUELA DE CIENCIAS Y SISTEMAS  
#### ORGANIZACIÓN COMPUTACIONAL  

---

<p align="center">
  <img src="Imagenes/image.png" alt="Logo Facultad de Ingeniería" width="250"/>
</p>

<h1 align="center">BUSCAMINAS</h1>
<h2 align="center">PROYECTO #1</h2>

---
### Integrantes del Grupo


| Nombre |Carnet|Trabajado|  
|--|--|--|
| **201900532** | Juan José Gerardi Hernández | *25%*
| **202300848** | Brayan Emanuel García | *25%*
| **202300824** | Alexander Samuel Us Upún | *25%*
| **202300768** | Norma Elizabeth Canú Xico | *25%*

---

##  Introducción

Este proyecto forma parte del curso de Organización Computacional y tiene como objetivo principal desarrollar un prototipo funcional del clásico juego "Buscaminas" utilizando circuitos digitales. Se integra la lógica combinacional y secuencial, memoria RAM creada con flip-flops, y comunicación serial para la interacción entre el hardware y una interfaz digital.

---

##  Descripción del Problema

Microsoft Windows ha solicitado el desarrollo de un juego interactivo para su nuevo sistema operativo. Se requiere un prototipo funcional del juego *Buscaminas*, que pueda ser controlado tanto desde una computadora como desde un circuito físico. El sistema debe incluir:

- Configuración de bombas en un tablero 4x4 usando memoria RAM.
- Control mediante interfaz web y módulo Bluetooth.
- Representación visual del estado del juego con LEDs y una pantalla LCD.
- Interacción a través de una arquitectura cliente-servidor.

---

##  Objetivos

### Objetivo General

Aplicar los conocimientos adquiridos en el curso para desarrollar un sistema basado en lógica combinacional y secuencial, utilizando flip-flops, módulos de comunicación y estructuras de control.

### Objetivos Específicos

- Diseñar circuitos combinacionales y secuenciales.  
- Implementar comunicación serial Arduino-PC vía Bluetooth.  
- Construir una memoria RAM con flip-flops.  
- Representar visualmente el estado del juego.

---

##  Lógica del Sistema

El sistema consta de dos fases:

### 1. Configuración

- Se cargan las posiciones de las bombas mediante una interfaz gráfica o archivo `.org`.
- La configuración se transmite vía serial al Arduino, que almacena los datos en una RAM de 4x4 hecha con flip-flops.
- Se usa una matriz de LEDs para representar las bombas.

### 2. Juego

- El jugador selecciona posiciones del tablero usando comandos Bluetooth.
- Si acierta, se incrementa su puntaje y se actualiza la LCD.
- Si falla (cae en una bomba), se muestra *Game Over* y se enciende un LED rojo.
- Si descubre todas las posiciones seguras, gana y se enciende un LED verde.
- Un LED azul indica el estado de “jugando”.

---

##  Arquitectura del Juego

![RAM](/Documentación/Imagenes/1.jpeg)
![Tablero](/Documentación/Imagenes/2.jpeg)
![Pantala LED](/Documentación/Imagenes/3.jpeg)
![Indicadores de Juego](/Documentación/Imagenes/4.jpeg)
![Conexión Arduino](/Documentación/Imagenes/5.jpeg)


- **Cliente:** Interfaz web + comunicación con Arduino  
- **Servidor:** Circuito físico + lógica de juego  
- **Memoria RAM:** Flip-flops (74174/74374)  
- **Visualización:** LEDs y pantalla LCD 16x2  
- **Interacción:** Teclado matricial, comandos Bluetooth

---

##  Equipo Utilizado

- Flip-flops D 74174 / 74374  
- Módulo Bluetooth HC-06  
- Puertas Lógicas: AND (7408), OR (7432), NOT (7404), XOR (7486)  
- Multiplexor 74153  
- Demultiplexor 74138  
- Pantalla LCD 16x2  
- Arduino Mega  
- Teclado matricial  
- LEDs  

---

##  Presupuesto

| Componente              | Cantidad | Costo Unitario | Costo Total |
|-------------------------|----------|----------------|-------------|
| Módulo Bluetooth HC-06  | 1        | Q70            | Q70         |
| Flip-flops 74174/74374  | 3        | Q6             | Q18         |
| Pantalla LCD 16x2       | 1        | Q50            | Q50         |
| Arduino Mega            | 1        | Q400           | Q400        |
| Teclado Matricial       | 1        | Q16            | Q16         |
| LEDs                    | 19       | Q1             | Q19         |
| **Total**               |          |                | **Q573**    |

---

##  Configuración del Módulo Bluetooth

1. Conectar el módulo HC-06 al Arduino (TX-RX, VCC, GND).  
2. Configurar la velocidad de comunicación a **9600 baudios**.  
3. Sincronizar el módulo con el front-end mediante comandos AT si es necesario.  
4. Utilizar una terminal Bluetooth para enviar comandos de juego (`1` al `16`, `reinicio`, etc.).  

---

##  Consideraciones Técnicas

- El proyecto debe cumplir con la arquitectura **cliente-servidor**.  
- La RAM debe ser implementada con flip-flops reales.  
- Se requiere comunicación serial efectiva para calificación.  
- Cada integrante debe tener al menos una rama *feature* con commits en el repositorio.  
- El coordinador del grupo debe realizar y aprobar los *merges*.  

---

##  Conclusiones

- Se logró implementar un sistema interactivo integrando hardware digital con software de comunicación.  
- El uso de comunicación serial permitió una experiencia de juego fluida entre la interfaz web y el circuito físico.  
- La simulación y prototipado permitieron aplicar la teoría de organización computacional en un entorno práctico.

---

##  Recomendaciones

- Mejorar la eficiencia del diseño reduciendo componentes redundantes.  
- Ampliar el juego para incluir pistas visuales o niveles de dificultad.  
- Usar PCB personalizada para una integración más limpia y profesional del circuito.

---
