# DWIN_T5UIC1_LCD

## Python class for the Ender 3 V2 LCD runing klipper3d with OctoPrint / Moonraker 

https://www.klipper3d.org

https://octoprint.org/

https://github.com/arksine/moonraker


## Setup:

### Enable UART GPIO on LePotato

```
git clone https://github.com/libre-computer-project/libretech-wiring-tool.git
cd libretech-wiring-tool
sudo make
sudo ldto enable uart-a
```

### [Enabling Klipper's API socket](https://www.klipper3d.org/API_Server.html)

By default, the Klipper's API socket is not enabled. In order to use the API server, adding `-a /tmp/klippy_uds` to the correct line in `systemd/system/klipper.service` [TODO]

### Library requirements 

  Thanks to [wolfstlkr](https://www.reddit.com/r/ender3v2/comments/mdtjvk/octoprint_klipper_v2_lcd/gspae7y)

  `sudo apt-get install python3-pip python3-gpiozero python3-serial git`

  `sudo pip3 install multitimer`

  `sudo pip3 install LePotatoPi.GPIO gpiod==1.5.3`

  `git clone https://github.com/Mickelbil84/DWIN_T5UIC1_LCD.git`


### Wire the display 
  * Display <-> LePotato GPIO BCM
  * Rx  =   GPIO12  (Tx)
  * Tx  =   GPIO13  (Rx)
  * Ent =   GPIO6
  * A   =   GPIO18
  * B   =   GPIO26
  * Vcc =   (5v)
  * Gnd =   (GND)

### Run The Code

Enter the downloaded DWIN_T5UIC1_LCD folder.
Make new file run.py and add
(you can also run `cp run.py.txt run.py` and insert the API_Key).

```python
#!/usr/bin/env python3
from dwinlcd import DWIN_LCD

encoder_Pins = (26, 18)
button_Pin = 6
LCD_COM_Port = '/dev/ttyAML6'
API_Key = 'XXXXXX'

DWINLCD = DWIN_LCD(
	LCD_COM_Port,
	encoder_Pins,
	button_Pin,
	API_Key
)
```

Run with `python3 ./run.py`

# Run at boot:

	Note: Delay of 30s after boot to allow webservices to settal.
	
	path of `run.py` is expected to be `/home/pi/DWIN_T5UIC1_LCD/run.py`

   `sudo chmod +x run.py`
   
   `sudo chmod +x simpleLCD.service`
   
   `sudo mv simpleLCD.service /lib/systemd/system/simpleLCD.service`
   
   `sudo chmod 644 /lib/systemd/system/simpleLCD.service`
   
   `sudo systemctl daemon-reload`
   
   `sudo systemctl enable simpleLCD.service`
   
   `sudo reboot`
   
   

# Status:

## Working:

 Print Menu:
 
    * List / Print jobs from OctoPrint / Moonraker
    * Auto swiching from to Print Menu on job start / end.
    * Display Print time, Progress, Temps, and Job name.
    * Pause / Resume / Cancle Job
    * Tune Menu: Print speed & Temps

 Perpare Menu:
 
    * Move / Jog toolhead
    * Disable stepper
    * Auto Home
    * Z offset (PROBE_CALIBRATE)
    * Preheat
    * cooldown
 
 Info Menu
 
    * Shows printer info.

## Notworking:
    * Save / Loding Preheat setting, hardcode on start can be changed in menu but will not retane on restart.
    * The Control: Motion Menu
