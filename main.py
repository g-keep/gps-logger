import json

import datetime
import pynmea2
import time

import serial


def write_in_json_file(field, data):
    data = {}
    data['frame'] = json.encoder()


def parse_nmea_frame(frame):
    nmeaobj = pynmea2.parse(frame)
    data = dict()
    for i in range(len(nmeaobj.fields)):
        data[nmeaobj.fields[i][0]] = nmeaobj.data[i]

    print(json.dumps(data))
    with open('gps.json', '+a') as json_file:
        json.dump(data, json_file)
        json_file.write(',')
    if nmeaobj.fields[1][0] == 'A':
        return 0
    else:
        return 1


def logfilename():
    now = datetime.datetime.now()
    return 'NMEA_%0.4d-%0.2d-%0.2d_%0.2d-%0.2d-%0.2d.nmea' % \
           (now.year, now.month, now.day,
            now.hour, now.minute, now.second)




def read_data_from_serial_port(port):
    ser = serial.Serial(port, baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE, xonxoff=False)
    error_frame_cpt = 0
    cpt_frame = 0
    line = ser.readline()

    while line:
        line = ser.readline()
        input_data = line.decode()
        if input_data.startswith('GPS:'):
            frame = input_data.split(':')
            error_frame_cpt += parse_nmea_frame(frame[1])
            cpt_frame += 1
        print('Number of Errored Frames is : %d' + error_frame_cpt + ' of %d' + cpt_frame)
        ser.reset_input_buffer()


def main():
    parse_nmea_frame('$GPRMC,202200.200,A,4751.5685,N,00205.1080,E,0.66,353.68,111219,,,A*69')


if __name__ == "__main__":
    main()
