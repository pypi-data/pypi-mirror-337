import sys
import json
import os
import requests
#temp list of packages
url = ''
metapath = os.path.join(os.path.expanduser('~'), '.agpm', 'localmetadata.json')
settingspath = os.path.join(os.path.expanduser('~'), '.agpm', 'sources.escnf')

def fetchsource():
    print("fetching source list...")
    try:
      with open(settingspath, 'r') as file:
        source = file.readline()
        print("Source url: " + source)
        return source
    except Exception:
        return "https://eyescary-development.github.io/CDN/agpm_packages/"

def setsource(srcurl):
    with open(settingspath, 'w') as file:
        file.write(srcurl)

def fetchlist():
    print("fetching cloud metadata...")
    response = requests.get(url+"packagelist.json")
    response.raise_for_status()
    return response.json()

def fetchlocalmet():
    print("fetch local metadata...")
    try:
      with open(metapath, 'r') as f:
        localmetadata = json.load(f)
        return localmetadata
    except Exception:
        print("local metadata file doesn't exist, returning empty metadata...")
        return {}

def checkpackagelist(item):
    pkglist = fetchlist()
    print("checking package list...")
    try:
        temp=pkglist[item]
        return True
    except Exception:
        return False

def lookup(item):
    metadata=fetchlist()
    print("package name: " + str(item))
    print("description: " + str(metadata[item]["description"]))
    print("latest release notes: " + str(metadata[item]["releaseNotes"]))

def metawrite(metadata, path):
    with open(path, 'w') as f:
        json.dump(metadata, f, indent=2)

def install(item):
    os.system("curl -O "+url+item+"/protocols/install.sh && bash install.sh && rm install.sh")
    localmetadata=fetchlocalmet()
    cloudmetadata=fetchlist()
    localmetadata[item]=cloudmetadata[item]
    metawrite(localmetadata, metapath)

def uninstall(item):
    os.system("curl -O "+url+item+"/protocols/uninstall.sh && bash uninstall.sh && rm uninstall.sh")
    localmetadata = fetchlocalmet()
    localmetadata.pop(item, None)
    metawrite(localmetadata, metapath)

def update(item):
    metadata=fetchlist()
    cloudver = metadata[item]["version"]
    localmetadata = fetchlocalmet()
    localver = localmetadata[item]["version"]
    if localver != cloudver:
        os.system("curl -O "+url+item+"/protocols/update.sh && bash update.sh && rm update.sh")
        localmetadata[item]=metadata[item]
        metawrite(localmetadata, metapath)
    else:
        print("Package already up to date, command already satisfied")

def operate(task, app):
    if checkpackagelist(app):
        match task:
            case "install":
                install(app)
            case "uninstall":
                uninstall(app)
            case "update":
                update(app)
            case "search":
                lookup(app)
            case 'srcset':
                setsource(app)

    else:
        print("package doesn't exist, terminating...")

def main():
    global url
    url=fetchsource()
    if len(sys.argv) != 3:
        print("Usage: agpm-pyp <task> <app>")
        sys.exit(1)

    _, task, app = sys.argv
    operate(task, app)

if __name__ == "__main__":
    main()

