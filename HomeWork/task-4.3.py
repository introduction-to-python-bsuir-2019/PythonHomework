def get_top_performers(file_path,number_of_top_students):
	import csv
	from operator import itemgetter 
	with open( file_path,"r") as rf:
		ignore = rf.readline()
		list_one = []
		csv_reader = csv.reader(rf,delimiter=',')
		mydict =  {row[0]:row[2] for row in csv_reader}
		for key,val in sorted(mydict.items(), key = itemgetter(1) ,reverse = True):
			list_one.append(key)
	with open('E:/python/4Rth/student.csv','w') as wf:
		csv_writer = csv.writer(wf)
		csv_writer.writerow()	
			


			
			

	return list_one[0:number_of_top_students]	

print(get_top_performers("students.csv",8))





		
	

