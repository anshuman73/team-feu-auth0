# Main Backend service powering Face Factor Authentication.

## About

This folder hosts the code which powers the main backend that powers the Face Factor Authentication (FFA) project.

The idea is that we want to replace 2FA (Two Factor Authentication) techniques with something that's easier, and well faster. With increasingly every company protecting their data with 2FA during the Work From Home era, we wanted to introduce a way that is less annoying (well, texts and emails every time one wants to login can quickly grow on one if you have to do it everyday), and faster.

Hence, was born FFA :smile:

## How it works

We currently work on top of Auth0's authentication to get started in within minutes, and plan to expand much sooner to provide standalone SDKs.
Currently, the process is simple as these 3 steps for a developer - 


1. Sign up on Auth0 and setup their app
2. Copy paste a custom hook on their Auth0 project
3. Copy paste a custom rule on their Auth0 project

Voila!

That's pretty much it!

## Tech Stack

This is built upon the following technologies / frameworks - 

1. Flask Backend for routing and handling requests
2. Azure's Face API (For Face Data management and Recognition)
3. MongoDB to store metadata about users


## How to run it

* Rename .env-sample to .env and add all API credentials
* Setup MongoDB on your system
* Install the dependencies
* Simply run ```python3 app.py``` !
