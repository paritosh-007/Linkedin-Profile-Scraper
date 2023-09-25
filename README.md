# Linkedin-Profile-Scraper
In this project, we are fetching some basic details of a linkedin member through user defined input :  
- FirstName
- LastName

The script **Linkedin_Assignment.py** reads the linkedin credentials from locally stored text file **linkedin_creds.txt** in which the email and password is to be specified in the format:
email=`<email-address>`
password=`<password>`

### Run the script

![image](https://github.com/paritosh-007/Linkedin-Profile-Scraper/assets/24694205/a05dd453-7e6e-4b16-bc92-0f637e3be896)


Web driver will trigger the automated Chrome browser
Click on `data;` tab to see the changes.

![image](https://github.com/paritosh-007/Linkedin-Profile-Scraper/assets/24694205/a83553be-6f11-4b02-af66-4a827a8cb549)

Sign In Page will be filled in with the details from credentials file.

![image](https://github.com/paritosh-007/Linkedin-Profile-Scraper/assets/24694205/a1ebb783-d240-4a8c-b2cd-88112ff1b954)


### Security Check
There might be cases when we have to navigate through **Security Verification** Page.

![image](https://github.com/paritosh-007/Linkedin-Profile-Scraper/assets/24694205/49ebf9d4-f467-4305-b41a-183111db4046)

Solve the PUZZLE to move forward in the flow.

![image](https://github.com/paritosh-007/Linkedin-Profile-Scraper/assets/24694205/339976b5-8f59-46e6-a840-422a21b6954a)

### Enter First Name and Last Name

The script will keep on displaying the details of the user in the iteration.


![image](https://github.com/paritosh-007/Linkedin-Profile-Scraper/assets/24694205/958591f6-ddf3-4bcb-b3af-3b58a4b30423)

### Saving data
At the end, it will display the dataframe to be inserted in the local csv file.
Further, it will ask whether the runner wants to save this dataframe to the specified Google Sheet.
Upon entering the character `Y` (case-insensitive) , it will add the data in the sheet as well and will close the browser.

[G-sheet](https://docs.google.com/spreadsheets/d/1a63m3d2mPAzi922LDsOjpcAIDj9Z6Ln4vkKKx0DaEpI/edit?usp=sharing)

![image](https://github.com/paritosh-007/Linkedin-Profile-Scraper/assets/24694205/746fac8e-c33b-4a52-87cd-6454221e4dd1)



![image](https://github.com/paritosh-007/Linkedin-Profile-Scraper/assets/24694205/2c20d62b-39db-4f3b-9982-a8bad8b6edcc)



![image](https://github.com/paritosh-007/Linkedin-Profile-Scraper/assets/24694205/f17ca46c-9072-4049-8364-69db4d6b2add)
