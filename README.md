# Weapon Detection Surveillance Application

## Introduction

In recent times, the number of gun violence incidents and mass shootings in parts of North America has increased at an alarming rate. Unlike earlier times, these shootings can be linked not only to terrorism but also to internal political/religious differences and mental health issues. Such attacks are hard to track and prevent early, as they can happen quickly and without organizational involvement.

This project aims to design a surveillance application that can detect weapons/arms from video footage. The application can be integrated into security surveillance units, helping to identify potential dangers within the monitored perimeter and alert the concerned authorities of any potential threats.

## Dataset for the Model

For this project, we are using the "Weapon detection dataset" provided by the Andalusian Research Institute in Data Science and Computational Intelligence (DaSCI Institute). The training dataset consists of 3,500 images of different items: knife, pistol, credit card, smartphone, and wallet. The dataset is labeled correctly, and no data cleaning processes were necessary. For validation, we will use 307 images of various labels.

## Python Libraries

In this project, we used several Python libraries:

- **YOLO:** "You Only Look Once" is a real-time object detection library in Python. We used the YOLOv5s model for its efficiency on a CPU.
- **Tkinter:** A widely used GUI framework in Python for creating the application's front-end.
- **smtplib:** Used to send email alerts.
- **pyaudio:** Used to handle audio files.
- **OpenCV:** Used to access the webcam and take live video feeds for the application.

## Model Training and Validation

We tested the model's performance with various batch sizes and optimizers to compare training time and accuracy. The accuracy was measured using Mean Average Precision (mAP) and Intersection over Union (IoU).

### Case Studies

- **Case 1:** Batch size = 8, Optimizer = SGD
  - mAP @0.5: 0.98035
  - mAP @0.5:0.65: 0.85251
- **Case 2:** Batch size = 16, Optimizer = SGD
  - mAP @0.5: 0.98436
  - mAP @0.5:0.65: 0.86297
- **Case 3:** Batch size = 32, Optimizer = SGD
  - mAP @0.5: 0.98405
  - mAP @0.5:0.65: 0.86759
- **Case 4:** Batch size = 8, Optimizer = Adam
  - mAP @0.5: 0.813
  - mAP @0.5:0.65: 0.512

The best performing model was Case 2 with batch size 16. Therefore, we will use the weights of this model configuration in our application:

- Batch size: 16
- Image size: 640x640
- Epochs: 30
- Optimizer: SGD

## Application and Functionalities

The YOLO model integrated with the Tkinter user interface enabled the development of a fully functional application. The application has two main sections: the surveillance part and the configuration part.

### User Interface

- **Surveillance Part:** Displays the video feed for monitoring purposes with a reduced frame rate to handle image processing.
- **Configuration Part:** Allows users to configure settings for the application's operation.

#### Configuration Options

- Audio Alert: Toggle on/off
- Email Alert: Toggle on/off
- Email ID: Enter email address
- Email ID Interval: Set interval for email notifications
- Save Button: Stores the configurations in a JSON file
- Test Button: Tests the configuration settings by running the audio and email alerts

### Indication Labels

- Green label: "Saved Successfully!!"
- Blue label: "Testing Completed!!"
- Red label: "Alert: Weapon Detected!!"

### Weapon/Arms Detection and Alerting

Upon detecting a weapon/arm, the application initiates alert mode, making the window blink red to grab attention. It labels the identified potential weapon within the video feed and triggers audio and email alerts based on user configurations.

## Conclusion

This project successfully developed an application for security surveillance in public and private spaces. It alerts higher authorities and sends an email with details (including a picture) of the possible assailant upon detecting a weapon or arms in its video footage.