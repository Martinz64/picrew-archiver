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

id = argv[1]

main_page = requests.get("https://picrew.me/image_maker/"+id).text

key_pattern = re.compile("release_key:\"([A-Za-z0-9]+)\"")
key = key_pattern.findall(main_page)[0]

print("https://picrew.me/app/image_maker/" + id + "/" + key + "/cf.json")
cf_data = requests.get("https://picrew.me/app/image_maker/" + id + "/" + key + "/cf.json").text
cf = json.loads(cf_data)

img_data = requests.get("https://picrew.me/app/image_maker/" + id + "/" + key + "/img.json").text
img = json.loads(img_data)

#print(cf)
mkdir(id)

base_url = cf['baseUrl']
part_list = cf['pList']

for p in part_list:
    print(p['pId'],p['pNm'],base_url + p['thumbUrl'])
    path =id+"/"+str(p['pId'])+'-'+p['pNm']
    #mkdir(path)
    #download(base_url + p['thumbUrl'],dest_folder=path)
    print("DL: ["+base_url + p['thumbUrl']+"] -> [" + path + "]")

    for item in p['items']:
        item_path = path + "/" + str(item['itmId'])
        #download(base_url + item['thumbUrl'],dest_folder=item_path)
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
            

