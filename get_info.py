import requests
import re
import json
import os

def mkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir) 

def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_folder, filename)

    if os.path.exists(file_path):
        print("already saved", file_path)
        return

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))

id = os.sys.argv[1]

main_page = requests.get("https://picrew.me/image_maker/"+id).text

key_pattern = re.compile("release_key:\"([A-Za-z0-9]+)\"")
key = key_pattern.findall(main_page)[0]

thumbnail_pattern = re.compile("icon_url:\"(.*.[png]|[jpg])\"")
main_thumbnail_url = thumbnail_pattern.findall(main_page)[0].replace("\\u002F","/")
print(main_thumbnail_url)

print("https://picrew.me/app/image_maker/" + id + "/" + key + "/cf.json")
cf_data = requests.get("https://picrew.me/app/image_maker/" + id + "/" + key + "/cf.json").text
cf = json.loads(cf_data)

img_data = requests.get("https://picrew.me/app/image_maker/" + id + "/" + key + "/img.json").text
img = json.loads(img_data)

#print(cf)

base_url = "https://cdn.picrew.me"
try:
	base_url = cf['baseUrl']
except:
	#base_url = "https://picrew.me"
	""
part_list = cf['pList']

print("DL: ["+base_url + main_thumbnail_url + "] -> [" + id + "]")
print("DL: [https://picrew.me/app/image_maker/" + id + "/" + key + "/cf.json] -> [" + id + "]")
print("DL: [https://picrew.me/app/image_maker/" + id + "/" + key + "/img.json] -> [" + id + "]")

counter1 = 0
for p in part_list:
    counter1 = counter1 + 1
    path =id+"/"+ str(counter1).zfill(4) + "-" + str(p['pId'])+'-'+p['pNm']
    if p['thumbUrl']:
        print(p['pId'],p['pNm'],base_url + p['thumbUrl'])
        path =id+"/"+ str(counter1).zfill(4) + "-" + str(p['pId'])+'-'+p['pNm']
        #mkdir(path)
        #download(base_url + p['thumbUrl'],dest_folder=path)
        print("DL: ["+base_url + p['thumbUrl']+"] -> [" + path + "]")

    counter2 = 0
    for item in p['items']:
        item_path = path + "/" + str(counter2).zfill(4) + "-" + str(item['itmId'])
        counter2 = counter2 + 1
        #download(base_url + item['thumbUrl'],dest_folder=item_path)
        if item['thumbUrl']:
            print("DL: ["+base_url + item['thumbUrl']+"] -> [" + item_path + "]")
            print("-",item['itmId'], base_url + item['thumbUrl'])

        try:
            item_dict = img['lst'][str(item['itmId'])]
            for k1 in item_dict.keys():
                for k2 in item_dict[k1].keys():
                    url = base_url + item_dict[k1][k2]['url']
                    #download(url,dest_folder=item_path)
                    print("DL: ["+url+"] -> [" + item_path + "]")
        except:
            print("parse error:",str(item['itmId']))
                
