# CITS5506: Internet of Things

# Project Proposal: Smart Entry System

## 1. Name of Project:

**Smart Entry System**

## 2. Group Number, Names and Student Numbers of team members:

| student id | name                                                     |
| ---------- | -------------------------------------------------------- |
| 24323312   | Jingtong Peng                                            |
| 23891727   | Tang Fung Leung                                          |
| 24177876   | Ming Gao                                                 |
| 24162835   | Joaquin Cornejo Lema (may drop UWA at the end of August) |

## 3. Why do you want to do this project; What is the problem? What is the benefit of its solution? What is the impact of the solution?

**Why Do You Want to Do This Project?**<br>
Temperature has been recognized as a key indicator of COVID-19 and flu. The World Health Organization (WHO) has emphasized the importance of temperature screening as an effective method to detect potential cases early[1]. Additionally, WHO recommends using masks as one of the simplest and cheapest measures to prevent the transmission of viruses[2].

Many of our group members have working experience in Greater China.
During the COVID-19 pandemic, we all observed the inefficiencies and challenges in temperature screening and mask compliance checks. Manual temperature checks at entry points, especially in high-traffic areas like workplaces and airports, have proven to be slow and inefficient.Typically, only one staff is at an entrance gate, causing severe delays.

With the ongoing normalization of COVID-19[3], there is a critical need for an efficient and reliable solution that can detect abnormal temperature and protect public health.

**What Is the Problem?**<br>

The primary problem with the current manual temperature screening process is inefficiency and unreliability. During peak hours, such as the start of the workday, it's difficult for a single staff to manage the screening process efficiently. Adding more staff will be a waste of human resource, because the peak hour usually doesn't last long. Staffs often need to be trained to use scanners, which could lead to human errors in reading values. As a result, individuals with higher temperatures could be allowed to entry. Additionally, the manual process is highly dependent on the presence and responsibility of the staff. If supervisors are not watching, the scanning process might be skipped. Moreover, this manual approach can't prevent individuals from bypassing the screening process, which increases the risk to public health.

**What Is the Benefit of Its Solution?**<br>

Our smart entry system uses a contactless temperature sensor and a camera to monitor mask compliance, both connected to a Raspberry Pi, which controls the entire operation. This automation ensures that each individual is screened quickly and accurately without the risk of human error. By integrating the system with a gate system, it can also physically prevent entry for those who do not meet the necessary health conditions, such as having a high temperature or not wearing a mask. In this way, public health is ensured.

This automated system can be installed at multiple entry points, significantly increasing the speed and efficiency of the screening process, especially during peak hours. Moreover, the system frees staff from manual work, allowing them to focus on more meaningful tasks.

**What Is the Impact of the Solution?**<br>

In high-traffic environments such as offices, airports, and public spaces, the system increases the efficiency and reliability of temperature checks and mask compliance. As a result, the system can reduce the risk of COVID-19 transmission and other infectious diseases, which ensures public health.

Moreover, the integration of IoT capabilities allows the system to transmit real-time data to a central server. With this data, health department can monitor the situation and respond promptly if a potential case is detected and ultimately contributes to a healthier environment.

## 4. What are the existing solutions? (Literature Review)

## **5. Methodology**

**(1). Research and Assessment:**
Our research amis to address the need for automated influenza prevention measures at entry points. Furthermore, we will evaluate previous projects and research papers that are relevant to the algorithm we intend to employ for facical mask detection, infrared temperature mesuring and automatic gate control to assess the feasibility of our project goals.

**(2). Define Project Scope:**

- **_Project goals_**: Implement a non-contact entry system that ensures only individuals with normal body temperature and wearing face masks can gain access to a facility, enhancing health safety measures during pandemics like COVID-19. Automate the entry process to reduce the need for human intervention, speeding up entry procedures while maintaining high accuracy. Design an intuitive user interface that allows easy configuration and monitoring by facility managers.

- **_Deliverables_**: A working **_`prototype`_** of the Smart Entry System integrating temperature and mask detection with an automatic gate control. Full assembly of the system, including infrared temperature sensors, Raspberry Pi, DC motor or servo motor, and necessary power supply. Comprehensive documentation including system architecture, UML diagram, build instruction, debuggin. Detailed reports of testing phases, including functionality, reliability, and performance tests.

- **_Task_**: Identify the specific requirements for the system, including sensor accuracy, motor type, and software specifications. Choose suitable components like the infrared temperature sensor, Raspberry Pi, motorized gate system. Develop the algorithm for temperature and use CNN and OpenCV for mask detection. Implement the user interface for system configuration and monitoring. Integrate the software with hardware components (sensors and gate motor). Connect sensors and motorized gate system to the Raspberry Pi. Test the hardware integration with the software. Conduct unit tests on individual components. Perform system integration tests. Iterate based on feedback to ensure functionality and reliability. Install the system at the desired location.

- **_Cost_**:

  | Items                        | Cost |
  | ---------------------------- | ---- |
  | Infrared Temperature Sensor: | $10  |
  | Raspberry Pi                 | $0   |
  | Camera                       | $0   |
  | DC Motor / Servo Motor       | $0   |
  | Camera                       | $0   |
  | Resistors                    | $0   |
  | LED                          | $0   |
  | Jumper Wires                 | $0   |
  | Total Cost                   | $10  |

- **_deadlines_**:

  | Tasks                                      |     Deadlines |
  | ------------------------------------------ | ------------: |
  | Initial Research and Requirement Gathering |         02/09 |
  | Hardware Selection and Procurement         |         02/09 |
  | Hardware Integration                       |         15/09 |
  | Software Development                       |         30/09 |
  | Testing and Iteration                      |         30/09 |
  | Documentation Completion                   |         01/10 |
  | Total Project Timeline:                    | 02/09 - 01/10 |

- **_functionalities_**:

| Functionalities             | Description                                                                                                                                 |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| _Temperature Measurement_   | Non-contact temperature measurement using an infrared sensor. Automatically restricts access if the temperature exceeds a preset threshold. |
| _Mask Detection_            | Uses computer vision algorithms to detect whether a person is wearing a mask. Only allows access to those with a mask.                      |
| _Automatic Gate Control_    | Controls the opening and closing of the gate based on temperature and mask detection results.                                               |
| _User Interface_            | Provides an intuitive interface for configuring system parameters, monitoring real-time data, and accessing logs.                           |
| _Remote Access: (Optional)_ | Remote access to the system for monitoring and control through a web or mobile interface.                                                   |
| _Data Logging(optional)_    | Records temperature readings, mask status, and entry attempts in a secure database for auditing and reporting.                              |

**(3). Hardware Selection:**

- Raspberry Pi
- DC Motor / Servo Motor
- [MLX90614 Infrared contactless temeperature sensor](https://www.aliexpress.com/item/1005005796792057.html?src=google&src=google&albch=shopping&acnt=708-803-3821&isdl=y&slnk=&plac=&mtctp=&albbt=Google_7_shopping&aff_platform=google&aff_short_key=UneMJZVf&gclsrc=aw.ds&&albagn=888888&&ds_e_adid=&ds_e_matchtype=&ds_e_device=c&ds_e_network=x&ds_e_product_group_id=&ds_e_product_id=en1005005796792057&ds_e_product_merchant_id=758212040&ds_e_product_country=AU&ds_e_product_language=en&ds_e_product_channel=online&ds_e_product_store_id=&ds_url_v=2&albcp=19373854259&albag=&isSmbAutoCall=false&needSmbHouyi=false&gad_source=1&gclid=Cj0KCQjww5u2BhDeARIsALBuLnObucoDOEMwFGbDHOxcD0_AX_ql3qjFJ_BcMI-25OMw-b-N0VzMzbsaAs6NEALw_wcB)
- Camera
- [ESP8266 Wifi Module](https://core-electronics.com.au/wifi-module-esp8266-4mb.html?gad_source=1&gclid=Cj0KCQjww5u2BhDeARIsALBuLnNhEuA19CzafMPlHxN2YyHtDuQzXu0ILG-6-zSYhU-_Q4LTA3dFxXEaAiQDEALw_wcB)
- Resistors
- LED(red, green)
- Jumper Wires

**(4). Software Development:**

- **a. Unit Testing**: will be conducted in this stage to verify the functionality of each sub-system individually.
- **b. Face Mask Detection**: Facial Mask Detection System will be built with OpenCV, TensorFlow using Deeping Learning and Computer Vision concepts in order to detect face masks in static images as well as in real-time video streams[4].
- **c. Temeperature Detection**: Develop software to monitor temperature and mask data in real-time, providing instant feedback to users and logging data for analysis. Implement communication protocols for transmitting data to a central server or cloud.
- **d. Gate Control**: Create an intuitive interface for security personnel or system administrators to monitor entry points. The interface should display temperature readings, mask compliance status, and allow for system configurations.
- **e. User Interface**: Create an intuitive interface for security personnel or system administrators to monitor entry points. The interface should display temperature readings, mask compliance status, and allow for system configurations.

**(5). Testing and Iteration:**

- **Continuous Integration and Delivery (CI/CD)**: Set up a CI/CD pipeline to ensure that new updates and features are integrated smoothly into the system without disrupting functionality. This also allows for regular updates based on user feedback and evolving requirements.
- **User Testing**: Conduct real-world testing in various environments (e.g., offices, schools, railways, airport, museums) to gather data on system performance. Use this feedback to make necessary adjustments and improvements.

**(6). System UML diagram:**

 - Usercases:

![](docs/diagrams/Usercases.drawio.svg)

- Sequence

![](docs/diagrams/Sequence.drawio.svg)

- Components

![](docs/diagrams/Components.drawio.svg)

- Status

![](docs/diagrams/Status.drawio.svg)

## 6 Functionality.

As sub teams are made, and project divided into tasks for sub teams then write initial distribution of work among students by mutual discussion (as per strengths of the members). You may change it during the project.

|Name of Student|Work Assigned|Reason for the Assignment|
|-----------------|---------------|---------------------------|
|Ming Gao| Documentation, Video Editing| Ming has years of working experience with paperwork and has used video editing software before|
|Jingtong Peng| Hardware researching and development, Design and Architecture| Jingtong has working experience in embedded system programming|
|Tang Fung Leung| User Interface Development & Testing | Tang has experience in agile web development

## 7. A well-defined timeline related to subsystems should be made. Tasks should be assigned to sub-teams (refer above 8) and Timeline should cater for interdependence (parallel or sequential) of the subsystems.
    ## Smart Entry System Project Timeline

| Week  | Task                                                     | Details                                                                                                               |
|-------|----------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| **6** | Decide Necessary Hardware and Demonstration Method; Front-end and Back-end Design | Confirm the required hardware and order it online or obtain it from the university. Finalize the method to present the product, including its subsystems: Temperature subsystem, camera subsystem, LCD subsystem, autodoor subsystem, back-end subsystem, front-end subsystem. |
| **7** | Preliminary Design of Front-end/Back-end of Website/App | Develop a website that can display the temperature and mask-wearing information of the person in the browser.        |
| **8** | Assemble Hardware and Test It; Code Embedded in Hardware. Final Design of Front-end/Back-end of Website/App | Include components such as a contactless temperature sensor and a camera to detect whether a person entering is wearing a mask. Display pass/reject messages on the LCD device, red signal blink, and remind the person to wear a mask or advise them to go to a doctor. If the person is fine, allow entry. |
| **9** | Connect Hardware to Central Server and Test It          | Send temperature data and photo data to the central database, analyze it, and send the result back to the hardware. |
| **10**| Test the Project and Record Details                     | Record any errors encountered and continue testing.                                                                   |
| **11**| Test the Project and Record Details                     | Continue testing, recording errors, and refining the system.                                                           |
| **12**| Prepare Slides for Presentation and Rehearse            | Develop presentation slides and practice the presentation.                                                             |

## 8. Hardware

required (Each group has $50 budget for the items (not including cost of items and sensors available at UWA)). Due to delivery time consideration, you should choose items from Jaycar and Altronics. Consult Andy our Lab Technician (Email andrew.burrell@uwa.edu.au), as there could be alternate items already at UWA, thus saving the delivery time.

| No. | Items Description                          | Available at UWA (Yes/No) | Cost  | Web address                                                                                                            | Delivery Time |
|-----|--------------------------------------------|---------------------------|-------|------------------------------------------------------------------------------------------------------------------------|---------------|
| 1   | Raspberry Pi                               | Yes                       | $61.95 | [Raspberry Pi 3 Model B+](https://core-electronics.com.au/raspberry-pi-3-model-b-plus.html)                         | 1 day         |
| 2   | Camera                                     | Yes                       | $36.65 | [Raspberry Pi Camera Board V2 8 Megapixels](https://core-electronics.com.au/raspberry-pi-camera-board-v2-8-megapixels-38552.html) | 1 day         |
| 3   | Contact-less Infrared Temperature Sensor   | No                        | $50   | [Contact-less Infrared Temperature Sensor](https://core-electronics.com.au/contact-less-infrared-temperature-sensor.html) | 2 weeks       |
| 4   | Servo Motor                                | Yes                       | $5.45 | [Feetech FS90 1.5kg/cm Micro Servo 9g](https://core-electronics.com.au/feetech-fs90-1-5kgcm-micro-servo-9g.html)     | 2 days        |
| 5   | LCD Display                                | Yes                       | $23.90 | [Assembled Standard LCD 16x2 Extras White on Blue](https://core-electronics.com.au/assembled-standard-lcd-16x2-extras-white-on-blue.html) | 1 day         |
| 6   | Jumper Wire                                | Yes                       | $3.20 | [Male to Female Dupont Line 40 Pin 10cm 24AWG](https://core-electronics.com.au/male-to-female-dupont-line-40-pin-10cm-24awg.html) | 1 day         |
| 7   | HDMI Cable                                 | Yes                       | $5.95 | [HDMI Cable 2m](https://core-electronics.com.au/hdmi-cable-2m.html)                                                   | 1 day         |
| 8   | Resistor                                   | Yes                       | $     |                                                                                                                        | 1 day         |

## 9. References

> [1] World Health Organization. (2020). “Considerations for implementing and adjusting public health and social measures in the context of COVID-19.” WHO.
>
> [2] World Health Organization. (2020). “Advice on the use of masks in the context of COVID-19: Interim guidance.” WHO.
>
> [3] World Health Organization. (2022). “COVID-19: Endemic does not mean it’s harmless.” WHO.
>
> [4] P. Mittal, K. Pandey, P. Tawani and R. Rohilla, "CNN-based Person Recognition System for Masked Faces in a post-pandemic world," 2021 2nd International Conference for Emerging Technology (INCET), Belagavi, India, 2021, pp. 1-6, doi: 10.1109/INCET51464.2021.9456416.
