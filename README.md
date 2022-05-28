# Picrew archiver

I made this simple python script to download all of the assets of a picrew (for archival reasons)

This will only download the png's, you will have to combine them on a photo editor like GIMP or Photoshop


How to use:

1. Get the picrew id:

```https://picrew.me/image_maker/[[ID]]```

2. Run `get_info.py` and pipe its output to a text file:

```python3 get_info.py [[ID]] > urls.txt```

3. Run `download.py` to download all assets (This will take a long time):

```python3 download.py urls.txt```

4. (Optional) Generate a nice html page from the assets:

```python3 generate_html.py [directory created on the previous stage]```


