import requests
import re
import json
import os
import js2py


def is_public_picrew(id):
    return not any(c.isalpha() for c in str(id))
# To avoid encoding error, this happens when OS is not using utf-8

id = os.sys.argv[1]
virtual_id = id
key = "" 
main_thumbnail_url = ""
if is_public_picrew(id):
    main_page = requests.get("https://picrew.me/image_maker/"+id).text
else:
    main_page = requests.get("https://picrew.me/secret_image_maker/"+id).text
    vid_pattern = re.compile("/app/image_maker/(.*)/icon.*.(png|jpg)")
    virtual_id = vid_pattern.findall(main_thumbnail_url)[0][0]
    print(virtual_id)

nuxt_pattern = re.compile("<script>.+(__NUXT__.*\);)<\/script>")
nuxt_data = nuxt_pattern.findall(main_page)[0]
parsed_nuxt_data = js2py.eval_js("function getData(){ "  + nuxt_data + "\n return __NUXT__}\n")


config_json = parsed_nuxt_data().to_dict()['state']['config']
with open('cf.json','w+') as f:
    f.write(json.dumps(config_json))

img_json = {"baseUrl":"https:\/\/cdn.picrew.me","lst":parsed_nuxt_data().to_dict()['state']['commonImages']}
with open('img.json','w+') as f:
    f.write(json.dumps(img_json))



#print(res_2()['commonImages'])
#print(res_2['config'])

