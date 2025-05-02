#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Keypad.h>

// Configuración del Keypad
const byte FILAS = 4;
const byte COLUMNAS = 4;
byte pinesFilas[FILAS] = {A0, A1, A2, A3};
byte pinesColumnas[COLUMNAS] = {A4, A5, A6, A7};
LiquidCrystal_I2C lcd(0x27, 16, 2);
char teclas[FILAS][COLUMNAS] = {
  {'0','1','2','3'},
  {'4','5','6','7'},
  {'8','9','A','B'},
  {'C','D','E','F'}
};

Keypad customKeypad = Keypad(makeKeymap(teclas), pinesFilas, pinesColumnas, FILAS, COLUMNAS);

// Pines Flip-Flops
const int ffIN[16] = {
  22, 24, 26, 28, 30, 32, 34, 36,
  38, 40, 42, 44, 46, 48, 50, 52
};

const int ffRD[16] = {
  23, 25, 27, 29, 31, 33, 35, 37,
  39, 41, 43, 45, 47, 49, 51, 53
};

//pines de matriz de leds
const int ledJuego[16] = {
  3, 4, 5, 6, 7, 8, 9, 10,
  62, 63, 64, 65, 66, 67, 68, 69 // A8–A15
};


// Pines de control
#define CLK 2
#define LEDINGAME 13  
#define LEDGAMEOVER 12
#define LEDWIN 11

// Variables de estado
String input = "";
int puntajeMax = 16;
int puntaje = 0;
bool configurando = false;
bool leyendoJuego = false;
bool partyMode = false;
unsigned long previousMillis = 0;
const long interval = 200; // Intervalo para animación

void setup() {
  Serial.begin(9600);      // USB serial
  Serial1.begin(9600);     // Bluetooth por pines 18/19 (TX1/RX1)
  
  for(int i=0; i<16; i++){
    pinMode(ffIN[i], OUTPUT);
    digitalWrite(ffIN[i], LOW);
    pinMode(ffRD[i], INPUT);
  }
  lcd.init();
  lcd.backlight();
  lcd.clear();
  pinMode(CLK, OUTPUT);
  pinMode(LEDINGAME, OUTPUT);
  pinMode(LEDGAMEOVER, OUTPUT);
  pinMode(LEDWIN, OUTPUT);
  digitalWrite(CLK, LOW);
  digitalWrite(LEDINGAME, LOW);
  digitalWrite(LEDGAMEOVER, LOW);
  digitalWrite(LEDWIN, LOW);
//ciclo para recorrer la matriz de leds
  for (int i = 0; i < 16; i++) {
  pinMode(ledJuego[i], OUTPUT);
  digitalWrite(ledJuego[i], LOW); // Apagados al inicio
}


}

void loop() {
  procesarEntradas();
  procesarKeypad();
  animarLeds();
}

void procesarEntradas() {
  while(Serial.available()){
    char c = Serial.read();
    manejarCaracter(c);
  }
  while(Serial1.available()){
    char c = Serial1.read();
    manejarCaracter(c);
  }
}

void manejarCaracter(char c) {
  if(c == '\n' || c == '\r' || c == ' '){
    input.trim();
    if(input.length() > 0){
      procesarComando(input);
    }
    input = "";
  } else {
    input += c;
  }
}

void procesarKeypad() {
  char tecla = customKeypad.getKey();
  if(tecla){
    int num = convertirTeclaANumero(tecla);
    if(num != -1){
      if(configurando){
        actualizarConfiguracion(num);
        Serial.println("Activado FF" + String(num + 1));
        Serial1.println("Activado FF" + String(num + 1));
      } else if(leyendoJuego){
        leerFlipFlop(num);
      }
    }
  }
}

void procesarComando(String comando) {
  auto responder = [](const String& msg){
    Serial.println(msg);
    Serial1.println(msg);
  };

  int num = -1;
  if(comando.length() == 1){
    char c = comando.charAt(0);
    num = convertirTeclaANumero(c);
  } else {
    num = comando.toInt();
    if(num == 0 && comando != "0") num = -1; // prevenir falso positivo
  }

  if(configurando && num >= 0 && num <= 15){
    actualizarConfiguracion(num);
    responder("Activado FF" + String(num + 1));
    return;
  }

  if(leyendoJuego && num >= 0 && num <= 15){
    leerFlipFlop(num);
    return;
  }

  if(comando.equalsIgnoreCase("configuracion")){
    configurando = true;
    leyendoJuego = false;
    responder("Modo configuracion activado");
  }
  else if(comando.equalsIgnoreCase("finconfiguracion")){
    configurando = false;
    responder("Fin configuracion");
    pulsarCLK();
  }
  else if(comando.equalsIgnoreCase("initJuego")){
    iniciarJuego();
    responder("Modo juego activado");
  }
  else if(comando.equalsIgnoreCase("finJuego")){
    finalizarJuego();
    responder("Fin modo juego");
  }
  else if(comando.equalsIgnoreCase("reset")){
    resetSistema();
    responder("Sistema reiniciado");
  }
  else if(comando.equalsIgnoreCase("modoFiesta")){
    activarModoFiesta();
    responder("Modo fiesta activado!");
  }
}

void leerFlipFlop(int num) {
  int estado = digitalRead(ffRD[num]);
  
  String mensaje = "FF" + String(num+1) + ": " + estado;
  Serial.println(mensaje);
  Serial1.println(mensaje);
  
  if(estado == HIGH){
    gameOver();
    return;
  }

  // Casilla correcta: encender el LED correspondiente
  digitalWrite(ledJuego[num], HIGH);
  
  actualizarPuntaje();
}

void actualizarPuntaje() {
  puntaje++;
  actualizarPantalla("Jugando", puntaje, puntajeMax);
  String puntajeMsg = "Puntaje: " + String(puntaje);
  Serial.println(puntajeMsg);
  Serial1.println(puntajeMsg);
  
  if(puntaje >= puntajeMax){
    actualizarPantalla("Ganaste :)", puntaje, puntajeMax);
    activarModoFiesta();
  }
  
}

void gameOver() {
  Serial.println("GAMEOVER");
  Serial1.println("GAMEOVER");
  digitalWrite(LEDINGAME, LOW);
  digitalWrite(LEDGAMEOVER, HIGH);
  actualizarPantalla("Game Over :(", puntaje, puntajeMax);
  leyendoJuego = false;
}

void activarModoFiesta() {
  partyMode = true;
  previousMillis = millis();
  Serial.println("GANASTE! Modo fiesta activado");
  Serial1.println("GANASTE! Modo fiesta activado");
}

void iniciarJuego() {
  leyendoJuego = true;
  configurando = false;
  digitalWrite(LEDINGAME, HIGH);
  digitalWrite(LEDGAMEOVER, LOW);
  digitalWrite(LEDWIN, LOW);
  actualizarPantalla("Jugando", puntaje, puntajeMax);
}


void finalizarJuego() {
  leyendoJuego = false;
  digitalWrite(LEDINGAME, LOW);
  puntaje = 0;
  actualizarPantalla("Finalizando Juego", puntaje, puntajeMax);
}

void resetSistema() {
  for(int i=0; i<16; i++) digitalWrite(ffIN[i], LOW);
  pulsarCLK();
  digitalWrite(LEDINGAME, LOW);
  digitalWrite(LEDGAMEOVER, LOW);
  digitalWrite(LEDWIN, LOW);
  leyendoJuego = false;
  configurando = false;
  puntaje = 0;
  puntajeMax = 16;
  partyMode = false;
  actualizarPantalla("Reset", puntaje, puntajeMax);  // <- Agregado
  Serial.println("Reseteado");
  Serial1.println("Reseteado");
  
  //Para apagar los leds al resetear
  for (int i = 0; i < 16; i++) {
  digitalWrite(ledJuego[i], LOW);
  }
}

void actualizarConfiguracion(int num) {
  puntajeMax--;
  digitalWrite(ffIN[num], HIGH);
  actualizarPantalla("Configurando", puntaje, puntajeMax);
}


int convertirTeclaANumero(char tecla) {
  tecla = toupper(tecla);
  if(tecla >= '0' && tecla <= '9') return tecla - '0';
  if(tecla >= 'A' && tecla <= 'F') return 10 + (tecla - 'A');
  return -1;
}

void pulsarCLK() {
  digitalWrite(CLK, LOW);
  delay(10);
  digitalWrite(CLK, HIGH);
  delay(10);
  digitalWrite(CLK, LOW);
}

void animarLeds() {
  if(partyMode){
    unsigned long currentMillis = millis();
    if(currentMillis - previousMillis >= interval) {
      previousMillis = currentMillis;
      
      static byte ledState = 0;
      const byte patterns[4] = {
        B111, // Todos encendidos
        B101, // LED INGAME y WIN
        B010, // Solo GAMEOVER
        B001  // Solo WIN
      };
      
      digitalWrite(LEDINGAME,   (patterns[ledState] & B100) >> 2);
      digitalWrite(LEDGAMEOVER, (patterns[ledState] & B010) >> 1);
      digitalWrite(LEDWIN,       patterns[ledState] & B001);
      
      if(++ledState >= 4){
        partyMode = false;
        digitalWrite(LEDINGAME, LOW);
        digitalWrite(LEDGAMEOVER, LOW);
        digitalWrite(LEDWIN, HIGH);
      }
    }
  }
}

void actualizarPantalla(String mensaje, int punteo, int punteoMax) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(mensaje);
  Serial.println("actualizando pantalla");
  Serial1.println("actualizando pantalla");

  lcd.setCursor(0, 1);
  lcd.print("Punteo ");
  lcd.print(punteo);
  lcd.print("/");
  lcd.print(punteoMax);
}