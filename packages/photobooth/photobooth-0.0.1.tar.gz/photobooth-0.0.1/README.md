# Photobooth

> Photobooth application purely written in Python. Controlling a dslr camera and capturing photo.

![PyPI - Licence](https://img.shields.io/pypi/l/photobooth)
[![Current version on PyPI](https://img.shields.io/pypi/v/photobooth)](https://pypi.org/project/photobooth/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/photobooth.svg?color=dark-green)](https://pypi.org/project/photobooth/)

## Installation on RaspberryPi

### Installing the Photobooth package

```sh
$ sudo apt-get -y update && sudo apt-get -y upgrade && sudo apt-get -y autoremove
$ sudo apt-get -y install python3-pip python3-pyqt5 libgphoto2-dev
$ sudo pip install photobooth[dslr,rpi]
```

Start the photobooth with

```sh
$ photobooth -c <path/to/photobooth_config.ini>-d <path/to/dslr_config.ini>
```

### Installing the window manager, if using Raspbian Lite

1. Install Packages

   ```
   $ sudo apt-get install -y --no-install-recommends xserver-xorg x11-xserver-utils xinit openbox

   $ sudo apt-get install -y unclutter
   ```

   The package unclutter is optional. It will prevent showing the mouse curser.

1. Change the `.xinitrc` file by adding the following line

   ```
   exec openbox-session
   ```

1. Create the `autostart` file unter `~/.config/openbox/autostart`

   ```
   setxkbmap -option terminate:ctrl_alt_bksp

   xset s noblank
   xset s off
   xset -dpms

   unclutter -idle 0.5 -root &

   photobooth -c <path/to/photobooth_config.ini> -d <path/to/dslr_config.ini>
   ```

   Remarks:

   - If you like to show the mouse curser remove `unclutter -idle 0.5 -root &`
   - If you like to use the default configuration remove the options `-c` and `-d`.

1. Start the photobooth with

   ```sh
   $ startx
   ```

1. If you like to autostart the photobooth add the following line to `~/.bash_profile` and enable auto-login via `raspi-config`
   ```
   startx
   ```

## Configuration

The photobooth can be configured via a configuration file.

```
; Configuration of the application
[widget]

; Title of the application window
title = Photobooth

; Path to the background image
background_image = ./oak.jpg


; Configuration of the gallery screen
[widget.gallery]

; Label for the right button
right_button = Photo

; Position of the images [<x-position>, <y-position>, <angle>]
; - x- and y-position are in percent relative to the center of the page
; - angle is the degree of image rotation
positions = [[0.0, 0.0, 2], [-0.8, -0.6, -6], [0.7, -0.65, 10], [0.4, 0.8, -4], [-0.5, 0.8, 8], [-0.9, 0.6, -6], [0.05, -0.9, 4], [0.95, 0.95, 2], [0.85, -0.05, -4], [-0.95, -0.95, -4], [-0.1, -0.05, 12], [0.9, -0.95, -10], [0.0, 0.95, 2], [-0.65, 0.95, 4], [0.25, 0.05, 4], [-0.5, -0.5, -10]]


; Configuration of the liveview screen
[widget.liveview]

; Label for the left button
left_button = Back

; Label for the right button
right_button = Photo


; Configuration of the capture screen
[widget.capture]

; Countdown text comma separated
countdown = 3,2,Smile!
; Color of the message
countdown_color = "#333333"

; Messages after image is captured. Placeholder {number} is replaced with the photo number.
file_number_message = "This photo has the number: {number}"
; Color of the message
file_number_message_color = "#333333"


; Configuration of the preview screen
[widget.preview]

; Label for the left button
left_button = Delete

; Label for the right button
right_button = Next

; Time the preview is show in milliseconds
timeout = 5000


; Configuration of the hardware buttons
[hardwarebutton]

; GPIO Pin of the left button
left_button = 23

; GPIO Pin of the right button
right_button = 24

; Configuration of the camera
[camera]

; Image naming pattern to use for extraction as regex expression
file_number_pattern = P\d{2}_(\d{4}).JPG

; Time delay of the camera shutter from signal to actual capturing the photo (used to correct the countdown)
shutter_delay = 800
```

## Warranty

No guaranty or coverage of any kind to damages what so ever.
