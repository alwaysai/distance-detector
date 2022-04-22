# Distance Detector
This app will display the distance between two hands in inches. This app uses a web camera as the video stream
and uses reference object metrics to approximate distance between two objects in an image.

## Requirements
* [alwaysAI account](https://alwaysai.co/auth?register=true)
* [alwaysAI Development Tools](https://alwaysai.co/docs/get_started/development_computer_setup.html)

## Usage
Once the alwaysAI tools are installed on your development machine (or edge device if developing directly on it) you can install and run the app with the following CLI commands:

To perform initial configuration of the app:
```
aai app configure
```

To prepare the runtime environment and install app dependencies:
```
aai app install
```

To start the app:
```
aai app start
```

### Configuration
The config.json file may be used to change the model that is used as well as define labels and metrics of objects
of interest. The default set up uses hands as objects of interest, and sets the width and height of the hand in inches.

## Support
* [Documentation](https://alwaysai.co/docs/)
* [Community Discord](https://discord.gg/alwaysai)
* Email: support@alwaysai.co

