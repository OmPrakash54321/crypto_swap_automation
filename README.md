THis is an automation script(not generalised) written in python to automate the transactions between cryptos.
It runs for a certain number of iterations. This is a project for a very specific usecase and wont be useful for general audience.
The python script used 'PyAutoGUI' for automation.
Currently, the clicks are position based -> should change the dimensions in the scritp manually for different screen resolutions. Tried identifying the location based on the logo, but not working.

THe way the script works is:
1. Find the position of the 'amount enter' cell
2. enter the amount
3. Click 'swap'
4. Wait for wallet and approve
5. wait for 'swap again'
6. Reverse the cryptocoins
7. Repeat

Dirs and contents:
GPT --> conttains the scripts and images. The automate_with_error_sound_with_diff_swap.py is the latest one that works well.
requirements.txt --> has python requirements. Create a venv and install these using pip

TODOS:
1. Should make the position_finder_based_on_image so that it works well for different systems.
2. Clean up
