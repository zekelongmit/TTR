import ttr_classes as ttr
import ttr_info as info
from itertools import combinations
import time
import csv


game_map = ttr.Map(info.city_map,info.possible_tickets)
paths = set()

list_of_tickets = list(combinations(info.possible_tickets,3))
list_of_test_tickets = list(combinations(info.test_tickets,3))
# for i in list_of_tickets:
# 	min_path, min_cars, min_value = game_map.ticket_route(i)
# 	paths.add((str(min_path),i))


# for i in paths:
# 	print()
# 	print('path: ' + i[0])
# 	print('tickets for this path: ' + str(i[1]))
# 	print()

t = time.time()
with open('ticket_to_ride_paths.csv', 'w', newline='') as csvfile:
	spamwriter = csv.writer(csvfile)
	for i in list_of_tickets:
		min_path, min_cars, min_value = game_map.best_path_tickets(i)
		spamwriter.writerow([str(i)]+[str(min_path)] + [str(min_cars)] + [str(min_value)])

elapsed = time.time()-t

print(elapsed)