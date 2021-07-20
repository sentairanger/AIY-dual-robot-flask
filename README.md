# AIY-dual-robot-flask

## Introduction

My inspiration for this project actually came from this project which is linked [here](https://hackaday.io/project/160052-voicebox). However I took a completely different approach from what this project was about. After several failed tries and restarts I was finally able to get the code running and now I will show you how I did it and how you can run it on your own.

## Getting Started

To get things started I gathered the following for hardware and software. You can use any hardware you wish as long as you change the code based on how the robots were constructed.

### Hardware

* My Raspberry Pi robots Linus and Torvalds (you can use any Raspberry Pi Robot you want)
* Google AIY voice kit V2 (You can use the V1 if you wish)
* A control PC (I used my Ubuntu PC for this but this can be run on Windows, Mac, Linux, Android and iOS assuming you have ssh) 

### Software
* The Google AIY Voice kit software. Click [here](https://github.com/google/aiyprojects-raspbian/releases) to download the latest image. Follow the instructions [here](https://aiyprojects.withgoogle.com/voice/) to follow the installation process.
* Raspberry Pi OS (Torvalds), Raspberry Pi OS Lite (Linus). 

Once you have everything set up, here are the next steps.

* After setting up the Voice kit, you can copy the code to the Voice kit with this command: `scp -r AIY-dual-robot-flask pi@ip-address:/home/pi`. The ip-address is the address assigned to the Voice kit. Provide the password and the files should be sent to the kit.
* On the robots make sure to ssh into both and then enable `pigpio` for remote GPIO access. Do this with `sudo pigpiod`.
* Then run the code with `python3 dual_robot_voice.py`. Go into a browser and then type `ip-address:5000`. ip-address is the address of the voice kit. Then move the sliders to see the servos move or to change the speed of the motors. Press the button and start saying commands like `turn left` or `go forward`. The robots should react accordingly.

## Code Explanation

* `dual_robot_voice.py`: Here there are three sections, the main button to control movement, the two sliders that control the servos and the two sliders that manage speed control. When pressing the button, speak into the Voice kit will initialize and then you just speak into it and give the robots commands.
* `dual_robot_voice.html`: This is the main template design for the app.

## Running on Different Platforms

This app can only be run on the voice kit and since all the available libraries such as `flask` and `gpiozero` are installed by default there is no need to run `pip install` at all. All you need to do is ssh into the Voice kit, cd into the directory and run the app. This can be run on Windows, Mac, Linux, Android and iOS. On Windows, use puTTy to ssh into the pi. Linux and Mac have ssh installed by default so there's no need for further installation. On Android and iOS you can use something like JuiceSSH and ssh into the pi. Then the app should be accessible on a browser. 

## Pictures
