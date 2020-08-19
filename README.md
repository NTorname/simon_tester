# simon_tester
Using a wearable Metatracker device and supporting circuitry to test reaction time to stimuli

## hardware
The user wears a MbientLab MetaTracker. GPIO 0-3 control pager motors attached to the subject's legs, GPIO 4 & 5 correspond to foot pedals to measure response time.

## usage
Must have a computer with python3, bluetooth capabilities, and the MbientLab python API installed. To run the script run 'sudo python3 REACTION.py [mac address] [# of samples] [file_name.csv]' where the mac address is the one printed on the MetaTracker, the sample number is how many time the user must react, and file_name is where the data will be stored.
