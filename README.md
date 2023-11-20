
# Robotat GUI - Alpha

![](https://pandao.github.io/editor.md/images/logos/editormd-logo-180x180.png)

This project aims to set the starting point to develop a full desktop application to simulate robots on the robotics experimenting platform of Universidad del Valle de Guatemala, Robotat. This first version establishes a structure to simulate Pololu 3Pi+ mobile robots, program the ESP32 that controls various functions of the Pololu (as establishing connection with ``Robotat's`` server), and monitoring the Pololu's pose on the tests' table of the Robotat. In that way, the aim is to create a full experimentation flow with the Pololu 3Pi+.

**Table of Contents**

[TOCM]

[TOC]

### Features

- The repository is divided into 

### Repository structure
Here's an overview of the project's files structure:
- **`docs`**: This folder contains documentation related to the project, including video demos showcasing the GUI functionality. The content is organized into subfolders:

  - **`recordings`**: Video recordings demonstrating the usage and features of the GUI, Pololu's .
  - **`screenshots`**: Screenshots capturing different aspects of the GUI for reference.
  - *Other Files*: Additional documentation or files relevant to the project.

- **`microros`**: This directory holds all the source files required for working with ROS2 and micro-ROS on an ESP32. It's designed for development on the Ubuntu operating system.

- **`src`**: This directory is dedicated to the source code of the project, housing implementations for the three main features. Within this folder, you'll find the following subdirectories:

  - **`feature_1`**: Source code related to the first main feature.
  - **`feature_2`**: Source code related to the second main feature.
  - **`feature_3`**: Source code related to the third main feature.
  - *Other Files*: Additional source files, utilities, or configurations relevant to the main features.
