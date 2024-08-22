# CITS5506: Internet of Things
# Project Proposal: Smart Entry System
1. Name of Project: 

    **Smart Entry System**

2. Group Number, Names and Student Numbers of team members:
    
    Team 41<br>
    24162835 Joaquin Cornejo Lema (may drop UWA at the end of August)<br> 
    24323312 Jingtong Peng<br>
    23891727 Tang Fung Leung<br> 
    24177876  Ming Gao<br>

3. Why do you want to do this project; What is the problem? What is the benefit of its solution? What is the impact of the solution?

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

4. What are the existing solutions? (Literature Review)

5. How will you do it? Explain your methodology in a logical manner (step by step process). Draw a block diagram of the complete system. Explain design in terms of subsystems, their functionalities (software and Hardware) and their interdependence.

6. As sub teams are made, and project divided into tasks for sub teams then write initial distribution of work among students by mutual discussion (as per strengths of the members). You may change it during the project.

|Name of Student|Work Assigned|Reason for the Assignment|
|-----------------|---------------|---------------------------|
|Ming Gao| Documentation, Video Editing| Ming has years of working experience with paperwork and has used video editing software before|
|Jingtong Peng| Hardware researching and development, Design and Architecture| Jingtong has working experience in embedded system programming|
|Tang Fung Leung| User Interface Development & Testing | Tang has experience in agile web development

7. A well-defined timeline related to subsystems should be made. Tasks should be assigned to sub-teams (refer above 8) and Timeline should cater for interdependence (parallel or sequential) of the subsystems.
    # Smart Entry System Project Timeline

| Week  | Task                                                     | Details                                                                                                               |
|-------|----------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| **6** | Decide Necessary Hardware and Demonstration Method; Front-end and Back-end Design | Confirm the required hardware and order it online or obtain it from the university. Finalize the method to present the product, including its subsystems: Temperature subsystem, camera subsystem, LCD subsystem, autodoor subsystem, back-end subsystem, front-end subsystem. |
| **7** | Preliminary Design of Front-end/Back-end of Website/App | Develop a website that can display the temperature and mask-wearing information of the person in the browser.        |
| **8** | Assemble Hardware and Test It; Code Embedded in Hardware. Final Design of Front-end/Back-end of Website/App | Include components such as a contactless temperature sensor and a camera to detect whether a person entering is wearing a mask. Display pass/reject messages on the LCD device, red signal blink, and remind the person to wear a mask or advise them to go to a doctor. If the person is fine, allow entry. |
| **9** | Connect Hardware to Central Server and Test It          | Send temperature data and photo data to the central database, analyze it, and send the result back to the hardware. |
| **10**| Test the Project and Record Details                     | Record any errors encountered and continue testing.                                                                   |
| **11**| Test the Project and Record Details                     | Continue testing, recording errors, and refining the system.                                                           |
| **12**| Prepare Slides for Presentation and Rehearse            | Develop presentation slides and practice the presentation.                                                             |

8. Hardware required (Each group has $50 budget for the items (not including cost of items and sensors available at UWA)). Due to delivery time consideration, you should choose items from Jaycar and Altronics. Consult Andy our Lab Technician (Email andrew.burrell@uwa.edu.au), as there could be alternate items already at UWA, thus saving the delivery time.

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


9. References

    [1] World Health Organization. (2020). “Considerations for implementing and adjusting public health and social measures in the context of COVID-19.” WHO.
    
    [2] World Health Organization. (2020). “Advice on the use of masks in the context of COVID-19: Interim guidance.” WHO.

    [3] World Health Organization. (2022). “COVID-19: Endemic does not mean it’s harmless.” WHO.
