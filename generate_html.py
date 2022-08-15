import os

dir = os.sys.argv[1]

dirs = os.listdir(dir)

dirs = sorted(dirs)

categories = []
for d in dirs:
    if os.path.isdir(dir + '/' + d):
        categories.append(d)

catgs = []

for cat in categories:
    fItems = os.listdir(dir + '/' + cat)
    fItems = sorted(fItems)
    items = []

    category_thumbnail = ""
    
    for file in fItems:
        if "p_" in file:
            category_thumbnail = cat + '/' + file
            
        if os.path.isdir(dir+'/'+cat+'/'+file):
            cdir = dir+'/'+cat+'/'+file
            cdir2 = cat+'/'+file

            item_thumbnail = ""
            variants = []
            for img in sorted(os.listdir(cdir)):
                if img.endswith("png"):
                    if img.startswith('ii_'):
                        item_thumbnail = cdir2 + '/' + img
                    else:
                        variants.append(cdir2 + '/' + img)
                
            items.append((item_thumbnail,variants,cdir,cdir2)) #cdir is the base path
            
            #print(item_thumbnail)        
    #f.write("<img src=\"" + category_thumbnail + "\"/>" )
    catgs.append((category_thumbnail,items, cat))


with open(dir+'/output.html', 'w') as f:
    f.write('''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
        }
        img.content{
            width: 200px;
        }
        .thumbnail{
            margin: 10px;
            width: 50px;
            height: 50px;
            border: 1px solid black;
            padding: 5px;
        }
        .thumbnail img{
            width: 50px;
        }
        .cat_wrapper{
            display: flex;
            flex-direction: row;
            flex-wrap: wrap;
        }
        .header{
            width:50px;
            height:50px;
        }
        .hdr {
            display: flex;
            align-items: center;
        }
        .hdr .title{
            margin:10px;
        }
    </style>
</head>
<body>
<ul>
    ''')

    counter = 0
    for cat in catgs:

        #counter = counter + 1
        if counter > 10:
            break
        f.write('<li>')
        f.write('<div class="hdr">')
        f.write('<img class="header" src="' + cat[0] + '" />')
        f.write('<h3 class="title">' + ''.join(cat[2].split('-')[1:]) + '</h3>')
        f.write('</div>')
        f.write('<div class="cat_wrapper">')

        for item in cat[1]:
            #f.write('<tr>')
            #f.write('<td class="thumbnail"><a href="' + item[2] + '/index.html"><img src="' + item[0] + '" /></a></td>')
            #for variant in item[1]:
            #    f.write('<td><img class="content" src="' + variant + '" /></td>')

            #f.write('</tr>')
            f.write('<div class="thumbnail"><a href="' + item[3] + '/index.html" target="_blank"><img src="' + item[0] + '" /></a></div>')

        f.write('</div>')
        f.write('</li>')
    

    f.write('''
    </ul>
    </body>
    </html>
    ''')

html_header = '''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
        }
        img.content{
            width: 200px;
        }
        td.thumbnail img{
            width: 50px;
        }
        .content{
            width:150px;
            border: 1px solid black;
        }
    </style>
</head>
<body>'''

html_footer = '''
    </body>
    </html>
    '''

for cat in catgs:
    for item in cat[1]:
        with open(item[2] + '/index.html','w') as f:
            f.write(html_header)
            f.write('<img class="thumbnail" src="' + item[0].split('/')[-1] + '" />')
            f.write('<div class="main">')

            for variant in item[1]:
                f.write('<img class="content" src="' + variant.split('/')[-1] + '" />')
            f.write('</div>')
            f.write(html_footer)
