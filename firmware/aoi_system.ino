/*
 * Firmware AOI PCB System - ADAPTAT
 * Placa: NextLabTech A1 (ATmega328PB)
 * Senzor: HC-SR04 (Trig=7, Echo=3)
 * Motor: Servo GoBilda (Pin 9)
 */

#include <Servo.h>

// --- PINOUT CORECTAT CONFORM DEBUG-ULUI ---
const int PIN_TRIG = 7; 
const int PIN_ECHO = 3; 
const int PIN_SERVO = 9;

Servo conveyorServo;

// --- CONFIGURARE VITEZĂ ---
const int SPEED_STOP = 1500;
const int SPEED_RUN  = 1600; 

// --- VARIABILE SISTEM ---
bool isRunning = false;
bool obstacleDetected = false;
unsigned long lastSensorTime = 0;

void setup() {
  Serial.begin(9600);
  
  conveyorServo.attach(PIN_SERVO);
  conveyorServo.writeMicroseconds(SPEED_STOP);
  
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);
  
  // Mesaj de confirmare pentru debug-ul la pornire
  Serial.println("SYSTEM_READY");
}

void loop() {
  // 1. Ascultăm comenzi de la Python (PC)
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    if (cmd == 'S') { // START
      isRunning = true;
      obstacleDetected = false;
      Serial.println("ACK:STARTING");
    } 
    else if (cmd == 'O') { // STOP
      isRunning = false;
      conveyorServo.writeMicroseconds(SPEED_STOP);
      Serial.println("ACK:STOPPED");
    }
  }

  // 2. Verificăm Senzorul (la fiecare 100ms)
  if (millis() - lastSensorTime >= 100) {
    checkSensor();
    lastSensorTime = millis();
  }

  // 3. Control Motor (Logica prioritara: Obstacolul opreste motorul oricand)
  if (isRunning && !obstacleDetected) {
    conveyorServo.writeMicroseconds(SPEED_RUN);
  } else {
    conveyorServo.writeMicroseconds(SPEED_STOP);
  }
}

void checkSensor() {
  digitalWrite(PIN_TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(PIN_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);
  
  // Folosim un timeout de 25000us (~4 metri) pentru siguranta
  long duration = pulseIn(PIN_ECHO, HIGH, 25000); 
  
  if (duration == 0) return; // Daca nu primim raspuns, ignoram citirea

  float distance = duration * 0.034 / 2;

  // Logica detectie PCB (< 6 cm)
  if (distance > 0.1 && distance < 6.0) {
    if (!obstacleDetected) {
      obstacleDetected = true;
      Serial.println("OBSTACOL"); // Anuntam Python sa inceapa inspectia
    }
  } 
  // Histerezis: Repornim doar daca piesa a fost indepartata (distanta > 10cm)
  else if (distance > 10.0) {
    if (obstacleDetected) {
      obstacleDetected = false;
      Serial.println("CLEAR"); // Optional: anuntam ca banda e libera
    }
  }
}
