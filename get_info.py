import requests
import re
import json
import os
import js2py


def mkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    # be careful with file names
    filename = url.split('/')[-1].replace(" ", "_")
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

def get_release_key(pagedata):
    key_pattern = re.compile("release_key:\"([A-Za-z0-9]+)\"")
    key = key_pattern.findall(pagedata)[0]
    return key

'''def get_thumbnail_url(pagedata):
    thumbnail_pattern = re.compile("icon_url:\"(.*\.(?:png|jpg))\"")
    main_thumbnail_url = thumbnail_pattern.findall(pagedata)[0].replace("\\u002F","/")
    return main_thumbnail_url'''

def is_public_picrew(id):
    return not any(c.isalpha() for c in str(id))
# To avoid encoding error, this happens when OS is not using utf-8
#output = open("urls.txt", "w", encoding="utf-8")

id = os.sys.argv[1]
virtual_id = id
key = "" 
main_thumbnail_url = ""
if is_public_picrew(id):
    main_page = requests.get("https://picrew.me/image_maker/"+id).text
    key = get_release_key(main_page)
    #main_thumbnail_url = get_thumbnail_url(main_page)
else:
    main_page = requests.get("https://picrew.me/secret_image_maker/"+id).text
    key = get_release_key(main_page)
    #main_thumbnail_url = get_thumbnail_url(main_page)
    vid_pattern = re.compile("/app/image_maker/(.*)/icon.*.(png|jpg)")
    virtual_id = vid_pattern.findall(main_thumbnail_url)[0][0]
    print(virtual_id)



#======NO TOCAR======
#no me preguntes qu hace esto, no lo se ni yo 💀
#main_page = requests.get("https://picrew.me/image_maker/1272810").text
nuxt_pattern = re.compile("<script>.+(__NUXT__.*\);)<\/script>")
nuxt_data = nuxt_pattern.findall(main_page)[0]
parsed_nuxt_data = js2py.eval_js("function getData(){ "  + nuxt_data + "\n return __NUXT__}\n")

img = {"baseUrl":"https:\/\/cdn.picrew.me","lst":parsed_nuxt_data().to_dict()['state']['commonImages']}
cf = parsed_nuxt_data().to_dict()['state']['config']


# print(cf)


base_url = "https://picrew.me"
part_list = cf['pList']

thumbnail_url = parsed_nuxt_data().to_dict()['state']['imageMakerInfo']['icon_url']

print("DL: ["+ thumbnail_url + "] -> [" + id + "]")
#print("DL: [https://picrew.me/app/image_maker/" + virtual_id + "/" + key + "/cf.json] -> [" + id + "]")
#print("DL: [https://picrew.me/app/image_maker/" + virtual_id + "/" + key + "/img.json] -> [" + id + "]")


try:
    part_ctr = 0
    for p in part_list:
        part_ctr = part_ctr + 1
        path = id+"/"+ str(part_ctr).zfill(4) + '-' + str(p['pId'])+'-'+p['pNm']
        if p['thumbUrl']:  # Pass if thumbnail is null
            print(p['pId'], p['pNm'], base_url + p['thumbUrl'])
            #output.write(str(p['pId'])+' '+str(p['pNm'])+' ' +
            #             base_url + str(p['thumbUrl']) + '\n')
            # mkdir(path)
            #download(base_url + p['thumbUrl'],dest_folder=path)
            print("DL: ["+base_url + p['thumbUrl']+"] -> [" + path + "]")
            #output.write(
            #    "DL: ["+base_url + str(p['thumbUrl'])+"] -> [" + path + "]\n")

        item_ctr = 0
        for item in p['items']:
            item_ctr = item_ctr + 1
            item_path = path + "/" + str(item_ctr).zfill(4) + '-' + str(item['itmId'])
            if item['thumbUrl']:  # Pass if thumbnail is null
                item_path = path + "/" + str(item_ctr).zfill(4) + '-' + str(item['itmId'])
                #download(base_url + item['thumbUrl'],dest_folder=item_path)
                print("DL: ["+base_url + item['thumbUrl'] +
                      "] -> [" + item_path + "]")
                #output.write(
                #    "DL: ["+base_url + str(item['thumbUrl'])+"] -> [" + item_path + "]\n")
                print("-", item['itmId'], base_url + item['thumbUrl'])
                #output.write("-"+' '+str(item['itmId'])+' ' +
                #             base_url + str(item['thumbUrl']) + '\n')

            try:
                item_dict = img['lst'][str(item['itmId'])]
                for k1 in item_dict.keys():
                    for k2 in item_dict[k1].keys():
                        url = base_url + item_dict[k1][k2]['url']
                        # download(url,dest_folder=item_path)
                        print("DL: ["+url+"] -> [" + item_path + "]")
                        #output.write("DL: ["+url+"] -> [" + item_path + "]\n")
            except:
                print("parse error:", str(item['itmId']))

except:
    import traceback
    traceback.print_exc()

#output.close()
