Requirements:
	Anaconda2-5.3.0
		Scrapy==1.5.1
		selenium==3.14.1
	Firefox (updated)
	geckodriver (https://github.com/mozilla/geckodriver/releases)

01. get_raw_html

	This folder contains a python script that uses selenium webdriver to download raw html files from Google Scholar. The files are saved in the articles_html folder. 

	The geckodriver executable must be downloaded (see link above) and placed in this folder.

	Queries must be defined within a text file (see for example example_scholar_urls.txt). Each query must be placed in URL form within its own line in the text file.

	If the query returns results in several pages, the script will navigate through each page and download a html file for each of the pages of results.

	Be aware that if too many queries are carried out in a short period of time, Google Scholar will ask you to solve one or several CAPTCHAs, or will directly block you. The script will detect when Google Scholar requests a CAPTCHA, and will pause if this happens. The user must solve the CAPTCHA manually. When the browser resumes displaying search results, the user can resume the process by clicking enter in the terminal window. This script cannot resume automatically after Google Scholar has blocked you for making too many queries.

	The script can be executed using the following command in a terminal (adapt paths and filenames as needed): python gs_search.py scholar_urls.txt

02. process_html

	This folder contains code for a scrapy spider that can extract the relevant data from the raw html we have downloaded earlier.

	1. Create a scrapy project called "scholar_scraper" in this folder. You can use the command "scrapy startproject scholar_scraper"
	2. Substitute items.py and settings.py within the new scrapy project with the files in "02.process_html"
	3. Move scholar.py to the spiders folder within the scrapy project
	4. (optional) Move "generate local urls.exe" and run.bat to the scholar_scraper folder
	5. Generate a text file that contains the local path to the raw html that you downloaded earlier (see example_local_urls.txt as an example)
	6. Run the following command to run the data extraction process, and save the results as a csv file (adapt paths and filenames as needed): scrapy crawl scholar -o output_file.csv -t csv -a filename=example_local_urls.txt
