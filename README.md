
# Weapon Detection Surveillance Application

## Overview

The increasing frequency of gun violence and mass shootings across North America presents a growing threat to public safety. Such incidents are often unpredictable and can occur without prior warning, making them difficult to prevent. This project seeks to address this challenge by developing an intelligent surveillance application capable of detecting weapons in video footage. The application can be integrated into existing security systems to identify potential threats and alert authorities in real-time, thereby improving security and helping to prevent violent incidents.

## Dataset for the Model

For this project, we utilized the **Weapon Detection Dataset** provided by the Andalusian Research Institute in Data Science and Computational Intelligence (DaSCI Institute). The dataset contains 3,500 labeled images of various objects, such as knives, pistols, credit cards, smartphones, and wallets. The dataset does not require additional data cleaning. We used a separate validation set of 307 images to test the model's performance.

## Python Libraries Used

This project leverages several popular Python libraries to enable functionality:

- **YOLO**: "You Only Look Once" is a state-of-the-art, real-time object detection model. We employed the YOLOv5s variant due to its high efficiency, particularly for deployment on a CPU.
- **Tkinter**: A widely used GUI framework for creating the front-end user interface of the application.
- **smtplib**: This library is used for sending email alerts when a weapon is detected in the video feed.
- **pyaudio**: Enables the application to trigger audio alerts upon weapon detection.
- **OpenCV**: A powerful library for handling video capture from webcams and displaying live video feeds in real-time.

## Model Training and Evaluation

We trained and evaluated the model using different batch sizes and optimizers to assess performance, including training time and accuracy. The evaluation was based on **Mean Average Precision (mAP)** and **Intersection over Union (IoU)** metrics.

### Training Results

- **Case 1**: Batch size = 8, Optimizer = SGD
  - mAP @0.5: 0.98035
  - mAP @0.5:0.65: 0.85251

- **Case 2**: Batch size = 16, Optimizer = SGD
  - mAP @0.5: 0.98436
  - mAP @0.5:0.65: 0.86297

- **Case 3**: Batch size = 32, Optimizer = SGD
  - mAP @0.5: 0.98405
  - mAP @0.5:0.65: 0.86759

- **Case 4**: Batch size = 8, Optimizer = Adam
  - mAP @0.5: 0.813
  - mAP @0.5:0.65: 0.512

The best-performing configuration was **Case 2**, using a batch size of 16 and the **SGD optimizer**. The optimal configuration for deployment is:

- **Batch size**: 16
- **Image size**: 640x640
- **Epochs**: 30
- **Optimizer**: SGD

## Application Overview

The application integrates the YOLO object detection model with a Tkinter-based user interface to offer real-time surveillance capabilities. The application consists of two primary sections: **Surveillance** and **Configuration**.

### User Interface

- **Surveillance Section**: Displays the live video feed, with a reduced frame rate to accommodate image processing. The video feed is analyzed for weapon detection in real-time.
- **Configuration Section**: Provides users with options to adjust the settings of the application, such as enabling/disabling audio and email alerts, setting the email recipient, and adjusting the notification interval.

### Configuration Options

- **Audio Alert**: Toggle on/off for triggering sound notifications when a weapon is detected.
- **Email Alert**: Toggle on/off for sending email notifications when a weapon is detected.
- **Email ID**: Specify the recipient's email address.
- **Email ID Interval**: Set the interval between email notifications.
- **Save Button**: Saves the current configuration settings in a JSON file.
- **Test Button**: Tests the configuration settings by triggering both the audio and email alerts.

### Indication Labels

- **Green Label**: "Saved Successfully!!" (Displayed when configuration is saved).
- **Blue Label**: "Testing Completed!!" (Displayed after testing alert settings).
- **Red Label**: "Alert: Weapon Detected!!" (Displayed when a weapon is detected in the video feed).

## Weapon Detection and Alerting

When a weapon is detected in the video feed, the application enters "Alert Mode," where the window frame blinks red to capture the user's attention. Additionally, the application labels the identified weapon within the video feed and triggers both **audio** and **email** alerts, depending on the user's configuration. The email alert includes details of the detected weapon, along with an image of the potential threat.

## Conclusion

This project successfully creates an intelligent surveillance application that can detect weapons in video feeds. The system alerts authorities by sending timely notifications via email and audio, ensuring that security teams are immediately informed of potential threats. This application can be deployed in both public and private spaces to enhance security and help prevent gun violence incidents.

## Future Work

Future enhancements for the project include:

- Extending the dataset to include additional weapons and objects for more accurate detection.
- Integrating with external surveillance camera systems for broader deployment.
- Improving the application's efficiency and performance by experimenting with different model architectures.
