# CITS5506: Internet of Things

# Project Proposal: Smart Entry System

## 1. Name of Project:

**Smart Entry System**

## 2. Group Number, Names and Student Numbers of team members:
Group Number: 41
| student id | name                                                     |
| ---------- | -------------------------------------------------------- |
|24323312   | Jingtong Peng                                            |
| 23891727   | Tang Fung Leung                                          |
| 24177876   | Ming Gao                                                 |
| 24162835   | Joaquin Cornejo Lema (may drop UWA at the end of August) |

## 3. Why do you want to do this project? What is the problem? What is the benefit of its solution? What is the impact of the solution?

**(1). Why Do You Want to Do This Project?**

Temperature has been recognized as a key indicator of COVID-19 and flu. The World Health Organization (WHO) has emphasized the importance of temperature screening as an effective method to detect potential cases early[1]. Additionally, WHO recommends using masks as one of the simplest and cheapest measures to prevent the transmission of viruses[2].

Many of our group members have working experience in Greater China.
During the COVID-19 pandemic, we all observed the inefficiencies and challenges in temperature screening and mask compliance checks. Manual temperature checks at entry points, especially in high-traffic areas like workplaces and airports, have proven to be slow and inefficient.Typically, only one staff is at an entrance gate, causing severe delays.

With the ongoing normalization of COVID-19[3], there is a critical need for an efficient and reliable solution that can detect abnormal temperature and protect public health.

**(2). What Is the Problem?**

- **_Individual Problems_**:

  a.  <u>Inefficiency During Peak Hours</u>: During peak hours, such as the start of the workday, it's difficult for a single staff to manage the screening process efficiently.

  b.  <u>Human Resource Misallocation</u>: Adding more staff during peak hour will be a waste of human resource, because the peak hour usually doesn't last long. 

  c.  <u>Human Error in Temperature Reading</u>: Staffs often need to be trained to use scanners, which could lead to human errors in reading values. As a result, individuals with higher temperatures could be allowed to entry.

- **_Social Problems_**:  

  a.  <u>Dependence on Staff Accountability</u>: The manual process is highly dependent on the presence and responsibility of the staff. If supervisors are not watching, the scanning process might be skipped. 

  b.  <u> Risk of Screening Bypass</u>: There are always people who try to avoid the checks. The manual approach can't prevent them from bypassing the screening process, which increases the potential for risky entry.

  c.  <u> Public Health Risks</u>: The inefficiency and unreliability of the current manual temperature screening process increase the risk of potential virus transmission, particularly in high-traffic areas, which could lead to serious consequences for public health.

**(3). What Is the Benefit of Its Solution?**

- **_Individual Benefits_**:

  a. <u>Enhanced Screening Accuracy</u>: Our smart entry system uses a contactless temperature sensor and a camera to monitor mask compliance. No manual conduct is involved in the process, which reduces the possibility of human mistakes.

  b. <u>Time Saving</u>: This automation ensures that each individual is screened quickly. By speeding up the screening process, waiting times can be reduced during peak hours.

  c. <u>Human Resource Efficiency</u>: By automating the temperature and mask compliance checks, the system frees staff from manual work, allowing them to focus on more meaningful tasks.

  d.  <u>Physical Entry Control</u>: By integrating the system with a gate system, it can also physically prevent entry for those who do not meet the necessary health conditions, such as having a high temperature or not wearing a mask.

- **_Social Benefits_**:  

  a. <u>Improved Public Health</u>: By ensuring that only individuals who meet the necessary health conditions are allowed to enter, the system reduces the spread of infectious diseases. This contributes to a safer environment in high-traffic areas like offices, airports and protects the community in the long run.

  b. <u>Real-time Health Monitoring</u>: Our system has the ability to transmit real-time data to a central server. Health departments can monitor situation, analyse data, and respond promptly to potential cases. This data-driven approach ultimately will contribute to a healthier and safer public environment.

**(4). What Is the Impact of the Solution?**

- **_Wide-reaching Impact Due to Large Population_**: The smart entry system is designed to be implemented in high-traffic public spaces. If used worldwide, millions of people will pass through these devices daily, significantly decreasing the spread of infectious virus. Public health will be ensured on a large scale.

- **_Impact on Workforce Efficiency_**: By automating temperature checks and mask compliance monitoring, the system doesn't require staff to work manually at each entry point. Those staff can devote their time and intelligence to more critical tasks, enhancing overall workplace productivity.

- **_Generating Employment Opportunities_**: The development, manufacturing, installation and maintenance of the Smart Entry System will create new employment opportunities across the world. 

- **_Impact on Global Health Expenditure_**: According to Cutler et al. (2020), the global cost of the COVID-19 pandemic was around $11 trillion as of 2020. There will be $10 trillion more in the following years due to healthcare costs and economic losses. By preventing the spread of infectious virus, the Smart Entry System can reduce the need for medical treatments and therefore save billions in healthcare expenditures worldwide.

- **_Enhancing Societal Well-being and Harmony_**: After the outbreak of COVID-19, people began to suspect their neighbors and coworkers of carrying virus. There were also many debates online, depicting conspiracy theories that certain institutions had created the virus on purpose. The high infection rate led to widespread fear and irrational thinking. By reducing the speed of transmission, the system helps the community to recover trust and foster social harmony.

## 4. What are the existing solutions? (Literature Review)

We break down some of the key ares to provide a literature review on existing solutions for smart entry system.

**(1). Contactless Temperature Screening Systems:**
- **_Infrared Thermal Camera_**: These systems have been in use for years. During past epidemics like SARS, Ng et al. (2004) highlighted the effectiveness of thermal cameras, emphasizing their importance in identifying fevered individuals in large crowds. Research by Sun et al. (2020) highlighted the effectiveness of thermal imaging cameras in detecting body temperatures as an early indicator of infection, particularly during pandemics like COVID-19.

- **_Handheld Infrared Thermometers_**: Handheld devices are convenient to use for temperature checks at entry points. However, these devices have been criticized for possible human errors and inefficiency in high-traffic environments. Chan et al. (2013) discussed the challenges of using handheld devices in mass screening. They pointed out the need for standardized training to improve accuracy. Ahn et al. (2020) also mentioned the limitations and lack of accuracy of handheld infrared thermometers.

**(2). Automated Mask Compliance Systems:**
- **_Computer Vision-Based Systems_**: Machine learning algorithms can be used to detect whether individuals are wearing masks. Cameras capture real-time video feeds, and the system flags individuals not wearing masks. Viola and Jones (2001) laid the groundwork for face detection algorithms, which have since been adapted for mask detection later. 

- **_AI-Powered Mask Detection_**: The application of AI in public health surveillance has been evolving. The algorithms have been trained on datasets that have thousands of images of people with and without masks. These systems have been implemented in public to ensure compliance with mask.Wang et al. (2020) outlined the development and deployment of AI systems for mask detection in smart surveillance networks. The work by Loey et al. (2021) demonstrates how convolutional neural networks (CNNs) can effectively detect masks in real-time video streams.  

**(3). Smart Entry Gates:**
- There are integrated systems that combines temperature and mask checks together in a single device eg Hikvision’s product. These devices are installed at entry gates, and they automate the process of checking. Pavlidis et al. (2007) did research on intergrated biometric and thermal smart systems. The data highlighted the potential in reducing the spread of infectious diseases. Research by Rahman et al. (2021) explores the effectiveness of these integrated systems in reducing the spread of COVID-19 by automating entry control. 

**(4). IoT-Enabled Solutions:**
- **_Real-Time Data Transmission_**: IoT-enabled systems connect temperature and mask compliance devices to central servers. Health departments can monitor and analyzed the data in real time. Responding actions can be taken if needed. A paper by Atzori et al. (2010) discussed the early development of IoT systems and their application in healthcare. Kumar et al. (2021) discussed how IoT technology has been used to create smarter, more responsive health monitoring systems, particularly in public spaces.

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
|Jingtong Peng| Hardware researching and development, Design and Architecture| Jingtong has working experience in system programming|
|Tang Fung Leung| User Interface Development & Testing | Tang Fung has experience in agile web development|

## 7. A well-defined timeline related to subsystems should be made. Tasks should be assigned to sub-teams (refer above 8) and Timeline should cater for interdependence (parallel or sequential) of the subsystems.
**Smart Entry System Project Timeline**

| Week  | Task                                                     | Details                                                                                                               |
|-------|----------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| **6** | Decide Necessary Hardware and Demonstration Method; Front-end and Back-end Design | Confirm the required hardware and order it online or obtain it from the university. Finalize the method to present the product, including its subsystems: Temperature subsystem, camera subsystem, LCD subsystem, autodoor subsystem, back-end subsystem, front-end subsystem. |
| **7** | Preliminary Design of Front-end/Back-end of Website/App | Develop a website that can display the temperature and mask-wearing information of the person in the browser.        |
| **8** | Assemble Hardware and Test It; Code Embedded in Hardware. Final Design of Front-end/Back-end of Website/App | Include components such as a contactless temperature sensor and a camera to detect whether a person entering is wearing a mask. Display pass/reject messages on the LCD device, red signal blink, and remind the person to wear a mask or advise them to go to a doctor. If the person is fine, allow entry. |
| **9** | Connect Hardware to Different Components and Test It          | Send temperature data and photo data to the database in the Raspberry Pi, analyze it, and send the result back to the LCD and the UI in browser. |
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
| 8   | Resistor                                   | Yes                       | $NA     |                                                                                                                        | 1 day         |

## 9. References

> [1] World Health Organization. (2020). “Considerations for implementing and adjusting public health and social measures in the context of COVID-19.” WHO.
>
> [2] World Health Organization. (2020). “Advice on the use of masks in the context of COVID-19: Interim guidance.” WHO.
>
> [3] World Health Organization. (2022). “COVID-19: Endemic does not mean it’s harmless.” WHO.
>
> [4] P. Mittal, K. Pandey, P. Tawani and R. Rohilla (2021), "CNN-based Person Recognition System for Masked Faces in a post-pandemic world," 2021 2nd International Conference for Emerging Technology (INCET), Belagavi, India, pp. 1-6.
>
> [5] Ng, E. Y. K., Kaw, G. J. L., & Chang, W. M. (2004). “Analysis of IR Thermal Imager for Mass Blind Fever Screening.” Microvascular Research, 68(2), 104-109.
>
> [6] Sun, Z., et al. (2020). “Applications of Infrared Thermography for COVID-19 Pandemic Containment.” Journal of Medical Imaging and Health Informatics, 10(5), 1081-1087.
>
> [7] Chan, L. S., Cheung, G. T. Y., & Lauder, I. J. (2013). “Infrared Thermometry for Mass Fever Screening: Is it Safe and Effective?” American Journal of Infection Control, 41(7), 637-643.
>
> [8] Ahn, A. C., et al. (2020). “Limitations of Infrared Thermometers in Mass Screening for Fever.” American Journal of Infection Control, 48(10), 1234-1235.
>
> [9] Viola, P., & Jones, M. (2001). “Rapid Object Detection Using a Boosted Cascade of Simple Features.” Proceedings of the 2001 IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR 2001), 1, I-511-I-518.
>
> [10] Wang, S., et al. (2020). “A Deep Learning Algorithm Using Convolutional Neural Network for Mask Detection in Surveillance Video.” IEEE Access, 8, 192676-192686.
>
> [11] Loey, M., et al. (2021). “A Deep Transfer Learning Model with Classical Data Augmentation and CGAN to Detect Masked Face in the Era of COVID-19.” Journal of Ambient Intelligence and Humanized Computing, 12(3), 1123-1136.
>
> [12] Pavlidis, I., Symosek, P., Puri, C., & Fechtelkotter, P. (2007). “Biometrics: Face Recognition in the Thermal Infrared Spectrum.” IEEE Transactions on Biomedical Engineering, 54(12), 2147-2153.
>
> [13] Rahman, M. S., et al. (2021). “Smart Entry Gate System Using IoT: Temperature and Mask Detection.” Sensors, 21(9), 3031.
>
> [14] Atzori, L., Iera, A., & Morabito, G. (2010). “The Internet of Things: A Survey.” Computer Networks, 54(15), 2787-2805.
>
> [15] Kumar, R., et al. (2021). “IoT-Based Smart Health Monitoring System for COVID-19 Patients.” Journal of Healthcare Engineering, 2021, 8841912.
>
> [16] Cutler, D. M., & Summers, L. H. (2020). ‘The COVID-19 Pandemic and the $16 Trillion Virus.’ JAMA, 324(15), 1495–1496.
