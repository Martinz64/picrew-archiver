# Picrew archiver

I made this simple python script to download all of the assets of a picrew (for archival reasons)

This will only download the png's, you will have to combine them on a photo editor like GIMP or Photoshop


How to use:

1. Get the picrew id:
   
```https://picrew.me/image_maker/[[ID]]```

2. Run `get_info.py` and pipe its output to `download-fast.sh`:

```python3 get_info.py [[ID]] | ./download-fast.sh```

1. Go into the newly created folder (name is the id) and run `generate_cf_img_json.py` to generate `cf.json` and `img.json` (required for using the picrew player):

```
cd [[ID]]
python3 ../generate_cf_img_json.py [[ID]]
```

4. (Optional) Generate a nice html page from the assets:

```python3 generate_html.py [directory created on the previous stage]```
