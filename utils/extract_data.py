import requests
from bs4 import BeautifulSoup
import json
import os
from tqdm import tqdm

# request_string = "https://en.wikipedia.org/w/api.php?action=query&titles=Reddit&prop=contributors|revisions&format=json"
# response = requests.get(request_string)
# data = json.loads(response.text)
# print(data)
# exit()
data = os.path.join('..', 'data')
to_read = os.path.join(data, 'enwiki-latest-all-titles')
count_read = os.path.join(data, 'count.json')
json_dump_path = os.path.join(data, 'json_dump')

if not os.path.exists(json_dump_path):
    os.mkdir(json_dump_path)

# Create new file to save the json data
filelist = os.listdir(json_dump_path)
savefile_path = os.path.join(json_dump_path, "dump_" + str(len(filelist)+1) + ".json")

# Open titles file
titles = open(to_read, 'r')
user_list = []

# Create a new file to save the read titles
if not os.path.exists(count_read):
    count = open(count_read, "w")
    count_json = {'male':0, 'female':0, 'unknown':0, 'titles_read':0}
    json.dump (count_json, count)
else:
    count = open(count_read, "r")
    count_json = json.load(count)
    count.close()

for i, title in tqdm(enumerate(titles)):
    if i < count_json['titles_read']:
        continue
    try:
        # Update titles read
        count_json['titles_read'] = i

        # Request Contributors list wikipedia API for the title
        request_string = "https://en.wikipedia.org/w/api.php?action=query&titles=" + title.split('\t')[1][:-1] +"&prop=contributors|revisions&format=json"
        response = requests.get(request_string)

        data = json.loads(response.text)

        try:
            timestamp = next(iter(data['query']['pages'].values()))['revisions'][0]['timestamp']
            date = timestamp.split('T')[0]
        except:
            continue

        # If the Article is edited after 2014, get the user info
        if int(date.split('-')[0]) > 2014:
            try:
                contributors = next(iter(data['query']['pages'].values()))['contributors']
            except:
                continue
            search_string = ""
            for user in contributors:
                search_string += user['name'] + '|'
            request_string = "https://en.wikipedia.org/w/api.php?action=query&list=users&ususers="+ search_string +"&usprop=gender&format=json"
            response = requests.get(request_string)
            data = json.loads(response.text)
            
            user_list.extend(data['query']['users'])

            # Get gender of user and keep track of count
            for user in data['query']['users']:
                try:
                    if user['gender'] == 'male':
                        count_json['male'] += 1
                    elif user['gender'] == 'female':
                        count_json['female'] += 1
                    else:
                        count_json['unknown'] += 1
                except:
                    continue


            # Dump data to new json file
            savefile = open(savefile_path, "w")
            json_dump = {'users':user_list}
            json.dump(json_dump, savefile)

            # Dump gender count
            count = open(count_read, "w")
            json.dump(count_json, count)
            count.close()

    except KeyboardInterrupt:
        titles.close()
        raise

