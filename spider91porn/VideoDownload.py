import json
import requests

with open("../1.json", 'r') as f:
    item = json.loads(f.read())
    f.close()
    for i in item:
        if i['yesdown'] == 1:
            file_name = i['title']
            print("Downloading file:%s.mp4" % file_name)
            r = requests.get(i['downurl'], stream=True)
            with open('VideoDownload/' + file_name + '.mp4', 'wb') as f:
                for chunk in r.iter_content():
                    if chunk:
                        f.write(chunk)

        else:
            pass
