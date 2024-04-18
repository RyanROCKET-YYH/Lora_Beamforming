#!/usr/bin/env python3

import zmq
import time
import pmt
import matplotlib.pyplot as plt
import math
import numpy as np

send_context = zmq.Context()
pull_context = zmq.Context()
send_command_context = zmq.Context()

# create socket
send_sock = send_context.socket(zmq.PUSH)
send_command_sock = send_command_context.socket(zmq.PUSH)
pull_socket = pull_context.socket(zmq.PULL)

send_sock.bind("tcp://127.0.0.1:50122")
send_command_sock.bind("tcp://127.0.0.1:50123")
pull_socket.connect("tcp://127.0.0.1:50124")

phase_offset = 0
angle = -180
scan_degree_step = 4
phase_shift_list = []
db_list = []

def apply_phase_shift(phase_shift):
    send_sock.send(pmt.serialize_str(pmt.from_long(phase_shift + phase_offset)))

def request_signal_strength():
    time.sleep(0.1)
    send_command_sock.send(pmt.serialize_str(pmt.to_pmt("0")))
    return pmt.to_float(pmt.deserialize_str(pull_socket.recv()))

# while True:
#     apply_phase_shift(-180)
#     signal_strength = request_signal_strength()
#     print('-180 received signal db is ' + str(signal_strength))
#     apply_phase_shift(0)
#     signal_strength = request_signal_strength()
#     print('0 received signal db is ' + str(signal_strength))

def sweep_scan():
    # Initial 360 degree scaning
    global phase_shift_list, db_list
    phase_shift_list = []
    db_list = []
    for i in range(-180, 181, scan_degree_step):
        apply_phase_shift(i)
        print('sending phase shift command: ' + str(i))
        signal_strength = request_signal_strength()
        print('received signal db is ' + str(signal_strength))
        phase_shift_list.append(i)
        db_list.append(signal_strength)

    current_db = max(db_list)
    current_phase_shift = phase_shift_list[db_list.index(current_db)]

    print("Max phase shift is on " + str(current_phase_shift) + " degree")
    print("Object is at " + str(math.degrees(math.asin(math.radians(current_phase_shift)/math.pi))) + " degree")
    plt.figure(figsize=(8, 6))
    plt.plot(phase_shift_list, db_list, label='Object angle vs dB')
    plt.title('dB vs degree')
    plt.xlabel('degree')
    plt.ylabel('dB')
    plt.grid(True)
    plt.legend()
    plt.show()
    
    return current_phase_shift


def continunous_sweep():
    try:
        while True:
            for i in range(-180, 181, scan_degree_step):
                apply_phase_shift(i)
                # print('sending phase shift command: ' + str(i))
                signal_strength = request_signal_strength()
                # print('received signal db is ' + str(signal_strength))
                phase_shift_list.append(i)
                db_list.append(signal_strength)

            current_db = max(db_list)
            current_phase_shift = phase_shift_list[db_list.index(current_db)]
            db_list.clear()
            phase_shift_list.clear()

            print('device is at ' + str(math.degrees(math.asin(math.radians(current_phase_shift)/math.pi))) + ' degree')
            time.sleep(1)
    except KeyboardInterrupt:
        send_context.term()
        send_command_context.term()
        pull_context.term()


def initial_scan():
    phase_shift_list.clear()
    db_list.clear()
    for i in range(-180, 181,scan_degree_step):
        apply_phase_shift(i)
        signal_strength = request_signal_strength()
        phase_shift_list.append(i)
        db_list.append(signal_strength)

        max_index = np.argmax(db_list)

    return phase_shift_list[max_index], db_list[max_index]


def continuous_tracking():
    cycle = 20  # do the full sweep every 20 cycles of adaptive tracking
    count = 0
    width = 30

    while True:
        if count % cycle == 0:
            print("performing a 360 degree full sweep...")
            current_phase_shift, _ = initial_scan()

        start = max(-180, current_phase_shift - width)
        end = min (180, current_phase_shift + width)
        local_shifts = []
        local_dbs = []

        for i in range(start, end, scan_degree_step):
            apply_phase_shift(i)
            signal_strength = request_signal_strength()
            local_shifts.append(i)
            local_dbs.append(signal_strength)

        max_index = np.argmax(local_dbs)
        current_phase_shift = local_shifts[max_index]
        print('device is at ' + str(math.degrees(math.asin(math.radians(current_phase_shift)/math.pi))) + ' degree')
       
        count += 1
        time.sleep(1)


def sweep_scan1(): 
    global phase_shift_list, db_list 
    phase_shift_list = []
    db_list = [] 
    # Initial 360 degree scanning 
    for i in range(-180, 181, scan_degree_step):
        apply_phase_shift(i)
        signal_strength = request_signal_strength()
        phase_shift_list.append(math.radians(i)) # Convert degrees to radians for polar plot 
        db_list.append(signal_strength) # Convert lists to numpy arrays for easier manipulation 
    phase_shift_array = np.array(phase_shift_list) 
    db_array = np.array(db_list) # Normalize signal strengths 
    db_array = db_array - max(db_array) # Polar plot 
    plt.figure(figsize=(8, 6)) 
    ax = plt.subplot(111, polar=True) 
    ax.plot(phase_shift_array, db_array, label='Signal strength (dB)') 
    ax.set_theta_zero_location('N') # Set 0 degrees to the top 
    ax.set_theta_direction(-1) # Set the plot to go clockwise 
    ax.set_thetamin(-180) # Set the plot to go from -180 to 180 degrees 
    ax.set_thetamax(180) 
    ax.grid(True) 
    plt.title('Normalized Signal Strength vs. Phase Shift')
    plt.legend(loc='upper right')
    plt.show()
        

def main():
    try:
        # sweep_scan1()
        initial_phase_shift = sweep_scan()
        continuous_tracking()
        # # # continunous_sweep()
    except KeyboardInterrupt:
        send_context.term()
        send_command_context.term()
        pull_context.term()

if __name__ == '__main__':
    main()
