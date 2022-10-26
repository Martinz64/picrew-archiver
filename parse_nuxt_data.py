import requests
import re
import json
import os
import js2py

#No hace nada (solo para pruebas)

main_page = requests.get("https://picrew.me/image_maker/1272810").text
nuxt_pattern = re.compile("<script>.+(__NUXT__.*\);)<\/script>")
nuxt_data = nuxt_pattern.findall(main_page)[0]

context = js2py.EvalJs({})
context.execute(nuxt_data)
parsed_nuxt_data = context.to_dict()['__NUXT__']

print(context.to_dict())

#parsed_nuxt_data = js2py.eval_js("function getData(){ "  + nuxt_data + "\n return __NUXT__}\n")


config_json = parsed_nuxt_data['state']['config']
img_json = {"baseUrl":"https:\/\/cdn.picrew.me","lst":parsed_nuxt_data['state']['commonImages']}

print(parsed_nuxt_data()['state']['commonImages'])
#print(res_2()['commonImages'])
#print(res_2['config'])

