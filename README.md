# Senior-Design-MiniProject

Design:
1. Authentication Page: This page displays a function called "google login" for user to click on to enter 3rd party login page.
2. Login Page: User can use their google username and password to login in or create a new google account to login in.
3. Home Page: Displays a welcome information and user's profile picture. Displays three buttons to click on to add sensor, display sensor or logout.
4. Add Sensor Page: User need to enter "sensor name" and "sensor type", which are humidity and temperature, then click submit to send the information of newly added sensor to user's database.
5. Display Sensor Data Page: Displays 2 graphs: one for humidity, the other for temperature, and then user can click "submit" to submit the user-defined sensor. After clicking "submit" button, the site re-direct the user to a new page that congratulates the user of his/her successful sensor adding.


API Documentation:
API                         Description

/                           - Google login option presented

/login                      - Google account login

/login/callback             - Google redirection: create user in the database, begin user session and send user back to homepage

/logout                     - Google account logout

/home                       - Displays user profile and buttons the direct users to other web pages

/entersensor                - Enter a new sensor information web-page

/addsensor                  - Add user defined sensor to the database

/displayssensors            - Displays the list of sensors that users defined and added

/list                       - Displays graphs for humidity and temperature sensors


Instructions on what need to be downloaded to run this web-app locally.
1. Install several packages:
1) "pip install -r requirements.txt"
2) "pip install numpy"
3) "pip install matplotlib"
2. Download the whole package
3. Run "python app.py"


Run on the hosted platform:
hrsun.pythonanywhere.com
(we coulndn't get the hosted platform to work fully)

