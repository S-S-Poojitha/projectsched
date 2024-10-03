## Google Calendar Events Viewer & Scheduler
This agent schedules events based on the availability of user and organization. After identifying a free slot it schedules an event and sends a mail to the user with details regarding date,timmings,meeting link of the event scheduled. Now user has to respond through his calendar by either selecting "Yes"/"No" , here there is no observable change when pressed "Yes" but in case of "No" the event will be deleted from organization calendar thus rendering that particular slot free and this process takes place on running the script del.py.
## Requsites
Organization should two factor authentication enabled and their password and mail has to replaced in the placeholders of app.py and try.py
From Google Cloud Project host a project and download credentials as "credentials.json" and push it into your repository for this functionality to work
## Usage
If you don't have access to gitpod, make sure to run the following command in the terminal ( eg : VS Code terminal ,Codespaces terminal) before running the application :

command:

pip install streamlit google-auth google-auth-oauthlib google-api-python-client

## Run the Streamlit app:
streamlit run app.py

## Authenticate with your Google account:
Enter your email address
NOTE
User has to respond by yes or no through his google calendar . While responding "yes" might not be necessary responding "no" is important To remove slots that have been responded with "no" we have to run this python script in the terminal as follows python del.py On doing this the details of the user who responded no will be stored in a csv file. The event will be deleted from organization's calendar
