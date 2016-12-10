import urllib.request
import json
import csv

job_categories = {1:'Accounting/Finance', 2:'Administrative', 3:'Analyst',4:'Architecture/Drafting', 5:'Art/Design/Entertainment',6:'Banking/Loan/Insurance',7:'Beauty/Wellness',8:'Business Development/Consulting',9:'Education',10:'Engineering (Non-software)',11:'Facilities/General Labor',12:'Hospitality',13:'Human Resources',14:'Installation/Maintenance/Repair',15:'Legal',16:'Manufacturing/Production/Construction',17:'Marketing/Advertising/PR',18:'Medical/Healthcare',19:'Non-profit/Volunteering',20:'Product/Project Management',21:'Real Estate',22:'Restaurant/Food Services',23:'Retail',24:'Sales/Customer Care',25:'Science/Research',26:'Security/Law Enforcement',27:'Senior Management',28:'Skilled Trade',29:'Software Development/IT',31:'Travel/Transportation',30:'Sports/Fitness',32:'Writing/Editing/Publishing',33:'Other'}

with open('top_cities.csv','w') as csvfile:
	fieldnames = ['job_category','city1','city2','city3','city4','city5','city6','city7','city8','city9','city10']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()

	for i in range(1,34):
		job_category = str(i)
		num_cities = 10 #Top 10 cities by default

		url = 'http://api.glassdoor.com/api/api.htm?t.p=103609&t.k=Isz9qpobHs&userip=155.41.75.92&useragent=&format=json&v=1&action=jobs-stats&jobType=fulltime&returnCities=true&jc=' + job_category
		req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		response = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
		cities = response['response']['cities']

		row = {'job_category': job_categories[i]}
		for j in range(0, num_cities):
			row['city'+str(j+1)] = cities[j]['name']
		writer.writerow(row)