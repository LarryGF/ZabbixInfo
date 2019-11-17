import click
#to work with timestamps
import datetime,time
from readingdb import get_items, get_trends, search_host, percentil, rank, mean,filter_time,db_connect

@click.command()
@click.option('--name', prompt='\nWhat host are you searching for?',help='Host to look for.')

def hosts(name):
	host_list = search_host(name)
	
	while host_list == []:
		name =click.prompt("The host doesn't exists,select a new one")
		host_list = search_host(name)
		
	hosts_ids = [e[0] for e in host_list]
	select = ''

	click.echo("\nHostid\tHostname")
	for host in host_list:
		print('{}\t{}'.format(*host))
	while not select.isnumeric() or int(select) not in hosts_ids:
		select = click.prompt('\nSelect a hostid')

		if not select.isnumeric() or int(select) not in hosts_ids:
			click.echo('\nPlease use a number from the list:')

	click.echo('\nYou selected host: "{}" with hostid: {}'.format([e[1] for e in host_list if e[0] == int(select)].pop(), select))

	items_list = get_items(int(select))

	click.echo('\nHostid\tItemid\tItemName')
	for item in items_list:
		click.echo('{}\t{}\t{}'.format(*item))
	select = ''
	items_ids = [e[1] for e in items_list]
	
	while not select.isnumeric() or int(select) not in items_ids:
		select = click.prompt('\nSelect an itemid')

		if not select.isnumeric() or int(select) not in items_ids:
			click.echo('\nPlease use a number from the list:')
			items_ids.sort()
			print(items_ids)

	item = [e for e in items_list if e[1] == int(select)].pop()
	select = int(select)
	itemid = select
	click.echo('\nYou have selected the item: {}'.format(item[2]))

	# (trends.itemid, trends.value_min, trends.value_avg, trends.value_max)
	trends = get_trends(select)
	# print(select, type(select))
	if trends == []:
		click.echo('No trends in database for that item')
		exit()

	if click.confirm('\nDo you want to see it?'):
		click.echo('\nItemid\tMin\t\tAvg\t\tMax\t\tClock')
		for trend in trends:
			#to convert the timestamp into a human readable format
			clock = trend[4]
			date=datetime.datetime.fromtimestamp(int(clock)).strftime('%Y-%m-%d %H:%M:%S')
			click.echo('{}\t{}\t\t{}\t\t{}\t\t{}'.format(trend[0],trend[1],trend[2],trend[3],date))

	#Tells the rest of the program if the results will be filtered or not (is needed later)
	isfiltered=False

	if click.confirm('\nDo you want to filter by date and time?'):
		date = click.prompt('\nInsert the date and time to start with\nIt must be in the format YYYYMMDDHHMMSS (all together for now)')
		#fetchs the date from the 'date' string, so it can generate a Unix timestamp from it
		datetuple = (int(date[0:4]),int(date[4:6]),int(date[6:8]),int(date[8:10]),int(date[10:12]),int(date[12:14]),0,0,0)
		timestamp1 = int(time.mktime(datetuple))
		date = click.prompt('\nInsert the date and time to finish the search\nIt must be in the format YYYYMMDDHHMMSS (all together for now)')        
		datetuple = (int(date[0:4]),int(date[4:6]),int(date[6:8]),int(date[8:10]),int(date[10:12]),int(date[12:14]),0,0,0)
		timestamp2 = int(time.mktime(datetuple))
		filtered = filter_time(timestamp1,timestamp2,itemid)
		#Sets the variable to True so the rest of the programs knows that it's working with filtered values
		isfiltered = True

		if click.confirm('\nDo you want to see it?'):
			click.echo('\nItemid\tMin\t\tAvg\t\tMax\t\tClock')
			for sample in filtered:
				clock = sample[4]
				date=datetime.datetime.fromtimestamp(int(clock)).strftime('%Y-%m-%d %H:%M:%S')
				click.echo('{}\t{}\t\t{}\t\t{}\t\t{}'.format(sample[0],sample[1],sample[2],sample[3],date))

	
	if click.confirm('\nDo you want to export it to a .csv file? \nThe file if exist will be deleted'):
		file = ''
		while file == '':
			userinput = click.prompt('Name the file')
			import os
			csvdir = os.path.join(os.path.abspath('.'),'csv')
			fd = os.path.join(csvdir, userinput + '.csv')
			
			try:
				with open(fd, 'w') as f:
					file = f
					if isfiltered == False:
						click.echo('Itemid;Min;Avg;Max', file=f)
						for trend in trends:
							click.echo('{};{};{};{}'.format(*trend), file=f)
					else:
						click.echo('Itemid;Min;Avg;Max;Clock', file=f)
						for sample in filtered:
							clock = sample[4]
							date=datetime.datetime.fromtimestamp(int(clock)).strftime('%Y-%m-%d %H:%M:%S')
							click.echo('{};{};{};{};{}'.format(sample[0],sample[1],sample[2],sample[3],date), file=f)

			except Exception as e:
				click.echo('Error opening the file')
				print(e)
				print('try again')
				file = ''
			pass

		
	if isfiltered == False:
		numbers_max = [e[3] for e in trends]
		num_max = mean(numbers_max)

		numbers_avg = [e[2] for e in trends]
		num_avg = mean(numbers_avg)

		numbers_min = [e[1] for e in trends]
		num_min = mean(numbers_min)

		score_max = [e[3] for e in trends]
		score_max.sort()
		p_max = percentil(score_max)
		ans_max = rank(score_max, p_max, 0.95)

		score_avg = [e[2] for e in trends]
		score_avg.sort()
		p_avg = percentil(score_avg)
		ans_avg = rank(score_avg, p_avg, 0.95)

		score_min = [e[1] for e in trends]
		score_min.sort()
		p_min = percentil(score_min)
		ans_min = rank(score_min, p_min, 0.95)

	else:
		numbers_max = [sample[3] for sample in filtered]
		num_max = mean(numbers_max)

		numbers_avg = [sample[2] for sample in filtered]
		num_avg = mean(numbers_avg)

		numbers_min = [sample[1] for sample in filtered]
		num_min = mean(numbers_min)

		score_max = [sample[3] for sample in filtered]
		score_max.sort()
		p_max = percentil(score_max)
		ans_max = rank(score_max, p_max, 0.95)

		score_avg = [sample[2] for sample in filtered]
		score_avg.sort()
		p_avg = percentil(score_avg)
		ans_avg = rank(score_avg, p_avg, 0.95)

		score_min = [sample[1] for sample in filtered]
		score_min.sort()
		p_min = percentil(score_min)
		ans_min = rank(score_min, p_min, 0.95)


	print('\nAverage max', num_max)
	print('\n95 percentile max', ans_max)
	print('\nAverage avg', num_avg)
	print('\n95 percentile avg', ans_avg)
	print('\nAverage min', num_min)
	print('\n95 percentile min', ans_min)
	print('\n')

db_connect()
hosts()
