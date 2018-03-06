
import click
from readingdb import get_items, get_trends, search_host, percentil, rank, mean


@click.command()
@click.option('--name', prompt='What host are you searching for?',help='Host to look for.')

def hosts(name):
    host_list = search_host(name)
    
    while host_list == []:
        #Check if the host exists
    	name =click.prompt("The host doesn't exists,select a new one")
        host_list = search_host(name)
    	
    hosts_ids = [e[0] for e in host_list]
    select = ''

    click.echo('Hostid\tHostname')
    for host in host_list:
        print('{}\t{}'.format(*host))
    while not select.isnumeric() or int(select) not in hosts_ids:
        select = click.prompt('\nSelect a hostid')

        if not select.isnumeric() or int(select) not in hosts_ids:
            click.echo('\nPlease use a number from the list')

    click.echo('You selected host: "{}" with hostid: {}'.format([e[1] for e in host_list if e[0] == int(select)].pop(), select))

    items_list = get_items(int(select))

    click.echo('Hostid\tItemid\tItemName')
    for item in items_list:
        click.echo('{}\t{}\t{}'.format(*item))
    select = ''
    items_ids = [e[1] for e in items_list]
    while not select.isnumeric() or int(select) not in items_ids:
        select = click.prompt('\nSelect an itemid')

        if not select.isnumeric() or int(select) not in items_ids:
            click.echo('\nPlease use a number from the list')
            print(items_ids)

    item = [e for e in items_list if e[1] == int(select)].pop()
    select = int(select)
    click.echo('You have selected the item: {}'.format(item[2]))

    # (trends.itemid, trends.value_min, trends.value_avg, trends.value_max)
    trends = get_trends(select)
    # print(select, type(select))
    if trends == []:
        click.echo('No trends in database for that item')
        exit()

    if click.confirm('Do you want to see it?'):
        click.echo('Itemid\tMin\t\tAvg\t\tMax')
        for trend in trends:
            click.echo('{}\t{}\t\t{}\t\t{}'.format(*trend))

    if click.confirm('Do you want to export it to a .csv file? \nThe file if exist will be deleted'):
        file = ''
        while file == '':
            file = click.prompt('Name the file')
            try:
                fd = open(file, 'w')

            except Exception as e:
                click.echo('Error opening the file')
                print(e)
                print('try again')
                file = ''
            pass

        click.echo('Itemid;Min;Avg;Max', file=fd)

        for trend in trends:
            click.echo('{};{};{};{}'.format(*trend), file=fd)

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

    print('\nAverage max', num_max)
    print('\n95 percentile max', ans_max)
    print('\nAverage avg', num_avg)
    print('\n95 percentile avg', ans_avg)
    print('\nAverage min', num_min)
    print('\n95 percentile min', ans_min)
    print('\n')


hosts()
