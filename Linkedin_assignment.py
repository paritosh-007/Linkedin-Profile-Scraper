from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd 
import os

# Creating a webdriver instance
driver = webdriver.Chrome()


def linkedin_creds():
	file1 = open("linkedin_creds.txt")
	creds=file1.readlines()
	email,password = creds[0].split('=')[1].strip(),creds[1].split('=')[1].strip()
	file1.close()
	return email,password

def profile_details(profile_url):
	
	driver.get(profile_url)  



	start = time.time()

	# will be used in the while loop
	initialScroll = 0
	finalScroll = 1000

	while True:
		driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
		# this command scrolls the window starting from
		# the pixel value stored in the initialScroll
		# variable to the pixel value stored at the
		# finalScroll variable
		initialScroll = finalScroll
		finalScroll += 1000

		# we will stop the script for 3 seconds so that
		# the data can load
		time.sleep(3)
		# You can change it as per your needs and internet speed

		end = time.time()

		# We will scroll for 20 seconds.
		# You can change it as per your needs and internet speed
		if round(end - start) > 20:
			break


	src = driver.page_source
	 
	# Now using beautiful soup
	soup = BeautifulSoup(src, 'lxml')


	# Extracting the HTML of the complete introduction box
	# that contains the name, company name, and the location
	intro = soup.find('div', {'class': 'pv-text-details__left-panel'})

	#print(intro)


	# In case of an error, try changing the tags used here.

	name_loc = intro.find("h1")

	# Extracting the Name
	name = name_loc.get_text().strip()
	# strip() is used to remove any extra blank spaces

	about_loc = intro.find("div", {'class': 'text-body-medium'})

	# this gives us the HTML of the tag in which the About section is present
	# Extracting About section
	about = about_loc.get_text().strip()
		
		
	# Getting the HTML of the Experience section in the profile
	experience = soup.find_all("li", {"class": "artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"})
	index,multiflag=0,0
	# these are special cases where the values are differently ordered due to multilevel experience section
	for i in experience:
		contents = i.getText().strip().splitlines()
		if 'You' in contents[0] or 'Workplace' in contents[0] or 'Government' in contents[0] or 'Ask' in contents[0]:
			index +=1
		else:
			break
	experience_details = []
	experience_sliced = experience[index].getText().strip().splitlines()
	
	for i in experience_sliced:
		j=i.replace('Full-time','').replace('·','').strip()
		if(len(j)>1):
			experience_details.append(j[0:len(j)//2])
	
	#print('experience_details',experience_details)
	
	try:
		len(experience_details[1].split())>1
	except:
		multiflag=0
	else:
		if len(experience_details[1].split())>1:
			if experience_details[1].split()[1]=='yrs' or experience_details[1].split()[1]=='yr':
				multiflag=1
	if multiflag==0:
		try:
			job_title = experience_details[0]
		except:
			job_title = ''
		else:
			job_title = experience_details[0]
		
		try:
			company_name = experience_details[1]
		except:
			company_name = ''
		else:
			company_name = experience_details[1]
		
		try:
			employment_duration = experience_details[2].split('-')[1].split(' ',3)[3]
		except:
			employment_duration = ''
		else:
			employment_duration = experience_details[2].split('-')[1].split(' ',3)[3]
		
		try:
			company_location = experience_details[3]
		except:
			company_location = ''
		else:
			company_location = experience_details[3]
	else:
		search_keyword = 'Present'
		locator,index = 0,0
		try:
			([idx for idx, s in enumerate(experience_details) if search_keyword in s][0])
		except:
			locator = -1
		else:
			index = ([idx for idx, s in enumerate(experience_details) if search_keyword in s][0])
		
		if locator ==-1 and index not in (3,4):
			job_title,company_name,employment_duration,company_location = '','','',''
		elif index == 3:
			try:
				job_title = experience_details[2]
			except:
				job_title = ''
			else:
				job_title = experience_details[2]
			
			try:
				company_name = experience_details[0]
			except:
				company_name = ''
			else:
				company_name = experience_details[0]

			try:
				employment_duration = experience_details[1]
			except:
				employment_duration = ''
			else:
				employment_duration = experience_details[1]
			
			try:
				company_location = experience_details[4]
			except:
				company_location = ''
			else:
				company_location = experience_details[4]
		else:
			try:
				job_title = experience_details[3]
			except:
				job_title = ''
			else:
				job_title = experience_details[3]
			
			try:
				company_name = experience_details[0]
			except:
				company_name = ''
			else:
				company_name = experience_details[0]

			try:
				employment_duration = experience_details[1]
			except:
				employment_duration = ''
			else:
				employment_duration = experience_details[1]
			
			try:
				company_location = experience_details[2]
			except:
				company_location = ''
			else:
				company_location = experience_details[2]
	
	return (name,about,job_title,company_name,employment_duration,company_location);


def write_csv(dataframe):
	file = "linkedin_profiles.csv"
	if os.stat(file).st_size == 0:
		dataframe.to_csv(file, index=False)
	else:
		dataframe.to_csv(file, header=False, mode='a', index=False)


def write_to_gsheet(dataframe):

	scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
	# Add your Service Account file
	#creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/json/file', scope)
	creds = ServiceAccountCredentials.from_json_keyfile_name('demo.json', scope)
	# Authorize the clientsheet 
	client = gspread.authorize(creds)

	# Get the instance of the Spreadsheet
	#sheet = client.open('name_of_the_spreadsheet')
	sheet = client.open("Linkedin Profile Scraper")
	# Get the first sheet of the Spreadsheet
	sheet_instance = sheet.get_worksheet(0)
	
	# Append DataFrame to Sheet
	sheet_instance.append_rows(dataframe.values.tolist())
	
	
def main():
	
	# This instance will be used to log into LinkedIn
	
	print("Reading the credentials from locally stored text file")
	email,password = linkedin_creds() 
	
	print("Opening LinkedIn\'s login page")
	driver.get("https://linkedin.com/uas/login")
	# waiting for the page to load
	time.sleep(5)

	# entering username
	username = driver.find_element(By.ID, "username")
	# In case of an error, try changing the element tag used here.
	username.send_keys(email)
	
	# entering password
	pword = driver.find_element(By.ID, "password")
	# In case of an error, try changing the element tag used here.
	pword.send_keys(password)	
	
	# Clicking on the log in button
	driver.find_element(By.XPATH, "//button[@type='submit']").click()
	# In case of an error, try changing the XPath used here.
	
	# entering name to search
	time.sleep(10)
	First_name = input("Enter First Name to Search:\n")
	Last_name = input("Enter Last Name to Search:\n")
	Name = First_name + ' ' + Last_name
	prefix = 'https://www.linkedin.com/search/results/people/?keywords='
	search_url = prefix + First_name + '%20' + Last_name
	
	driver.get(search_url)
	src = driver.page_source
	 
	# Now using beautiful soup
	soup = BeautifulSoup(src, 'lxml')  
	selectableEls = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "app-aware-link ")))
	links = []
	for el in selectableEls:
		temp_link = el.get_attribute('href')
		if 'miniProfileUrn' in temp_link and First_name.lower() in temp_link:
			links.append(temp_link.split('?',1)[0])
	links = list(set(links))
	data = []
	counter=0
	for link in links:
		name,about,job_title,company_name,employment_duration,company_location = profile_details(link)
		print('\n name=',name,'\n about=',about,'\n job_title=',job_title,'\n company_name=',company_name,'\n employment_duration=',employment_duration,'\n location=',company_location,'\n profile_link=',link)
		value = []
		value.extend((name,about,job_title,company_name,employment_duration,company_location,link))
		data.append(value)
		counter+=1
		if counter==10:
			break
	
	df = pd.DataFrame(data, columns =['Name', 'About', 'Job Title', 'Company Name', 'Employment Duration', 'Company Location', 'Profile Link'])
	print(df)
	write_csv(df)
	print("Dataframe appended to locally saved csv \n Closing the browser")
	
	response = input("Want to export this to Google Sheet? (Y/N)\n")
	if response.lower() == 'y':
		write_to_gsheet(df)
		print("DataFrame appended to G-sheet")
		
if __name__ == "__main__":
    main()
