## How to autorun a program:
First, make a copy of the program you want to run and rename it as main.py.

- Step 1: Install rshell (pip3 install rshell)
- Step 2: Connect to your Pico ( rshell --buffer-size=30 -p /dev/tty.usbmodem0000000000001 -a ) # NOTE: Your /dev/ naming may differ)
- Step 3: Copy your main.py code to the Pico ( cp main.py /pyboard )
- Step 4: Confirm your code is on the Pico ( ls /pyboard )
- Step 5: Disconnect ( Control-D)
- Step 6: Disconnect your Pico / Reconnect your Pico. Your code is now running.
