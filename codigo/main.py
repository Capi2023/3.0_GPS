################################################################################
# Nombre del Archivo: main.py
# Autor:             Equipo Dinamita
# Fecha:             14/11/2023
# Institución:       Tecnológico Nacional de México (TECNM) - Campus ITT
# Curso:             Sistemas Programables 
#
# Objetivo:
# Crear, programar y desiñar un gps usando raspberry en wokwi
#
# Historial de Revisiones:
# 14/11/2023        Equipo Dinamita - Creado
#
# Enlace a GitHub Repository ó GIST:
# https://github.com/Capi2023/3.0_GPS
#
# Enlace a Wokwi :
# https://wokwi.com/projects/381411706635128833
#
# Licencia:
# Este programa es software libre y puede ser redistribuido y/o modificado bajo los términos de la Licencia Pública General GNU
# como está publicado por la Free Software Foundation, ya sea la versión 3 de la Licencia, o (a tu elección) cualquier versión posterior.
#
# Este programa se distribuye con la esperanza de que sea útil, pero SIN GARANTÍA ALGUNA; incluso sin la garantía implícita de
# COMERCIALIZACIÓN o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la Licencia Pública General GNU para obtener más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.
#
################################################################################
# Importación de módulos necesarios
# from machine import Pin, I2C
# from ssd1306 import SSD1306_I2C
# import framebuf, sys
# import utime
# import random
# from machine import UART

# Definición de funciones
# def init_i2c
# def display_speed
# def get_direction
# def convert_coordinates
#

# Código principal


from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf, sys
import utime
import random
from machine import UART


pix_res_x = 128
pix_res_y = 64


# Initialize GPS module

def init_i2c(scl_pin, sda_pin):
    # Initialize I2C device
    i2c_dev = I2C(1, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=200000)
    i2c_addr = [hex(ii) for ii in i2c_dev.scan()]
    
    if not i2c_addr:
    raise RuntimeError("No se encontró ningún dispositivo I2C.")
    else:
        print("I2C Address      : {}".format(i2c_addr[0]))
        print("I2C Configuration: {}".format(i2c_dev))
    
    return i2c_dev

##se inicializa el oled
i2c_dev = init_i2c(scl_pin=27, sda_pin=26)

oled = SSD1306_I2C(pix_res_x, pix_res_y, i2c_dev)

plain_bytes = [
 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x03, 0xff, 0xfe, 0x01, 0xff, 0xfc, 
0x78, 0xff, 0xfc, 0xfc, 0xff, 0xf8, 0xfc, 0x7f, 0xf8, 0xfc, 0x7f, 0xf8, 0xfc, 0x7f, 0xfc, 0x78, 
0x7f, 0xfc, 0x30, 0xff, 0xfc, 0x01, 0xff, 0xf8, 0x00, 0xff, 0xf3, 0x01, 0x7f, 0xf3, 0x06, 0x3f, 
0xf6, 0x87, 0x9f, 0xee, 0xc7, 0x5f, 0xe7, 0xfe, 0x8f, 0xec, 0xff, 0xf7, 0xc0, 0x00, 0x03, 0xff, 
0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff
]
# Crea un objeto framebuf para la pantalla OLED
fb = framebuf.FrameBuffer(bytearray(plain_bytes), 24, 24, framebuf.MONO_HLSB)


##limpia la pantalla
oled.fill(0)

oled.show()
oled.fill(0)
   
##se muestra un texto en pantalla
oled.text("Iniciando", 5, 5)
oled.fill(0)
oled.show()


##------------------------------------------------------------------------------
# Función para mostrar la barra de velocidad en la pantalla OLED
def display_speed(speed, lat, lon, sat, direction, time):
    ##se carga el logo en pantalla
    oled.fill(0)
    oled.blit(fb, 0, 0)

    oled.text("{}".format(sat), 0, 28)


    ind = ">"
    if speed > 0.5 and speed < 0.7:
        ind = ">>"
    elif speed > 0.7:
        ind = ">>>"

    altura_barra = 20
    oled.text("{}{}".format(round(speed/100, 3), ind),32,0)

    oled.text("{}".format(lat[:5]), 0,45)
    oled.text("{}".format(lon[:5]), 0,56)

    oled.text("{}".format(time), 85,56)

    oled.text("{}".format(direction), 110,0)

    oled.text("SPEED", 32, 10)
    oled.text("km/h", 63, 38)
    max_speed = 10.0  # Velocidad máxima en m/s (ajusta según tus necesidades)
    bar_width = int(speed / max_speed * 120)
    oled.rect(32, altura_barra, 64, 16, 1)
    oled.fill_rect(32, altura_barra, bar_width, 16, 1)
    oled.show()

def get_direction(latitude, longitude):
    if latitude >= 0:
        lat_direction = 'N'
    else:
        lat_direction = 'S'
    
   if longitude >= 0:
    lon_direction = 'E'
else:
    lon_direction = 'W'

    return lat_direction + lon_direction

def convert_coordinates(sections):
    if sections[0] == 0:
        return None

    data = sections[0] + (sections[1] / 60.0)

    if sections[2] == 'S':
        data = -data
    if sections[2] == 'W':
        data = -data

    data = '{0:.6f}'.format(data)
    return str(data)


while True:
    # Simulaciones y operaciones
    utime.sleep(1) 

    # Simula los datos del GPS Neo-6M
    latitude_simulated = random.uniform(40.0, 41.0)
    longitude_simulated = random.uniform(-74.0, -73.0)
    
    latitude_simulated = round(latitude_simulated,2)
    longitude_simulated = round(longitude_simulated,2)

    current_time = "11:24"
    satellites_connected = random.randint(4, 12)  # Cantidad de satélites conectados
    direction = get_direction(latitude_simulated, longitude_simulated)  # Dirección
    speed_kph = random.uniform(0, 0.05)  # Velocidad en km/h

    latitude_sections = [int(latitude_simulated), (latitude_simulated - int(latitude_simulated)) * 60, 'N']
    longitude_sections = [int(longitude_simulated), (longitude_simulated - int(longitude_simulated)) * 60, 'W']

    latitude = convert_coordinates(latitude_sections)
    longitude = convert_coordinates(longitude_sections)

    if latitude is None or longitude is None or current_time is None:
        continue

    print('Latitud: ' + latitude)
    print('Longitud: ' + longitude)
    print('Satelites conectados:', satellites_connected)
    print('Punto cardinal:', direction)
    print('Velocidad (km/h):', speed_kph)
    print('Hora:', current_time)


    speed = random.uniform(0, 100)

    display_speed(speed, latitude, longitude, satellites_connected, direction, current_time)
