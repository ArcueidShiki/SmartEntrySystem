# SmartEntrySystem

CITS5506 Group Project Repo

## Project Title: IOT Temperature & Mask Scan Entry System

### Description:

This project addresses the need for automated influenza prevention measures at entry points by developing a system that checks both temperature and mask compliance. The system uses a contactless temperature sensor and camera to scan individuals and transmits the results to a mobile or web application for display. Controlled by a Raspberry Pi, the system allows for real-time monitoring without the need for physical barriers. This solution is ideal for high-traffic environments like airports, offices, and public spaces. In the future, this project could evolve to include an automatic gate system that integrates with barriers to automatically prevent entry if unsafe conditions are detected.

### Components: Raspberry Pi, Temperature Sensor, Camera, ESP8266 WiFi Module, etc.

Applications: Railways, Airports, Offices, Public Spaces
Advantages: Fully automated, real-time result display
Disadvantages: Requires power supply, needs a reliable internet connection

## Workflow

```bash
# download code repository
1. git clone https://github.com/ArcueidShiki/SmartEntrySystem.git

# select a branch for development
2. git checkout dev
   or # solving current issue branch
   git checkout -b [issue_branch_name] [issue_branch_name]

3. Coding / solve issue / bugfix / writing test

# publish your changes
4. git add .
   or
   git add [path-to-your-files]

5. git commit -m "commit message"

# keep updated with remote main branch to avoid conflict
6. git pull origin main 
   # or
   git merge origin main
   # if conflict with some files after running this command do following:
   1. git status # to see which files are conflict
   2. click [resolve] a blue button in vscode editor, compare and merges.
   3. git status # check all the conflicts are solved, if not, back to step2 until all the conflicts are solved.

7. git push origin [remote_branch_name]

8. New a pull request on GitHub, compare [main] to [branch_name]

9. Add reviewers, assignee, labels and development related to the issue need to be solved under this pull request.

10. If meet the requirements, merge pull request.
```
