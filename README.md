# simon_tester
Using a wearable Metatracker device and supporting circuitry to test reaction time to stimuli.

## hardware
The user wears a MbientLab MetaTracker. GPIO 0-3 control pager motors attached to the subject's legs, GPIO 4 & 5 correspond to foot pedals to measure response time.

The test administrator must have a computer with bluetooth capabililtes.

## debian-based computer usage
Must have a  computer with Python 3 and the [MbientLab Python API](https://mbientlab.com/tutorials/PyLinux.html#metawear) installed. To run the script use

`sudo python3 reac_deb.py [mac_address] [# of samples] [file_name.csv]` 

where the mac_address is the one printed on the MetaTracker, the sample number is how many time the user must react, and file_name is where the data will be stored.

I recommend adding `export mtr=[mac_address]` to your .bashrc file to shortcut typing the MAC address to simple `$mtr`.

## windows 10 computer usage 

Must have a computer with Python 2.7 and the [MbientLab Python API](https://mbientlab.com/tutorials/PyWindows.html) installed. To run the script use

`python reac_win.py [mac_address] [# of samples] [file_name.csv]` 

where the mac_address is the one printed on the MetaTracker, the sample number is how many time the user must react, and file_name is where the data will be stored.

I recommend inputting `set mtr=[mac_address]` to shortcut typing the MAC address to simple `%mtr%`.

## output

Progam output is a CSV file with information about which motor was excited, if the subject's reaction was correct, and how long in seconds the reaction time was.
