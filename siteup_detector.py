import pyaudio
import time
import numpy as np
import requests
import datetime
import keyboard


# Inicializar PyAudio
p = pyaudio.PyAudio()

# Parámetros de configuración
FORMAT = pyaudio.paFloat32
CHANNELS = 2
RATE = 44100
CHUNK = 1024


url = "https://chatgpt.com/" #sitio a consultar

# Función para generar una onda sinusoidal
def generate_sine_wave(frequency, duration):
    t = np.linspace(0, duration, int(RATE * duration), False)
    return np.sin(frequency * t * 2 * np.pi)

def obtener_estado_sitio(url):
  """Obtiene el estado HTTP de un sitio web.
  Args:     url: La URL del sitio web.
  Returns:  El código de estado HTTP.
  """
  try:
    response = requests.get(url)
    return response.status_code
  except requests.exceptions.RequestException as e:
    print(f"/n Error al consultar {url}: {e}")
    return None

print(" Inicializando....")
continuo=True
pito=60

while continuo:
    time.sleep(30) #espera 30 segundos
    estado = obtener_estado_sitio(url)
    print(f"Se intentó el {datetime.datetime.now()} y se obtuvo la respuesta: {estado}")
    if estado == 200:
       print(f"Se intentó el {datetime.datetime.now()} y del sitio {url} finalmente se obtuvo la respuesta: {estado}")
       break

# Generar una onda sinusoidal de 440 Hz durante 1/2 segundo
samples = generate_sine_wave(440, 0.5).astype(np.float32).tobytes()

# Abrir un stream de salida
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True)


while True:
    # Escribir los datos en el stream (esta es la linea que emite el sonido)
    stream.write(samples)
    time.sleep(0.5)
    pito-=1
    #print(f"vuelta {pito}")
    if keyboard.is_pressed('q'):
        pito = 0
        break
    if pito < 1: break
    

stream.stop_stream()
stream.close()

# Terminar PyAudio
p.terminate()