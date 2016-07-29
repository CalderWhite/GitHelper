import os, sys, json, time
from tqdm import tqdm
git_files = []
bad_dirs = []
def process(filename,path):
    global git_files
    ft = filename.split(".")[-1]
    if ft == "gitpanion":
        git_files.append({
            "name" : filename,
            "path" : path
            })
def start_dir(path):
    global processed_files
    if path.find("$") < 0:
        global folders
        global err
        global bad_dirs
        err = False
        try:
            folders = next(os.walk(path))[1]
        except:
            #print("Error :" + path)
            bad_dirs.append(path)
            err = True
        if err == False:
            files = next(os.walk(path))[2]
            for folder in folders:
                start_dir(path + "/" + folder)
            for file in files:
                processed_files += 1
                #print(processed_files)
                #pbar.set_description(file + "\n")
                process(file,path)
                pbar.update(1)
    pass
def get_file_count(path,progress_prints=True):
    global processed_files
    global skipped_dirs
    processed_files = 0
    skipped_dirs = 0
    def count(path,prp=True):
        global processed_files
        global skipped_dirs
        if path.find("$") < 0:
            global folders
            global err
            global bad_dirs
            err = False
            try:
                folders = next(os.walk(path))[1]
            except:
                #print(path)
                skipped_dirs += 1
                bad_dirs.append(path)
                err = True
            if err == False:
                files = next(os.walk(path))[2]
                for folder in folders:
                    count(path + "/" + folder)
                for file in files:
                    processed_files += 1
                    if len(str(processed_files)) > 3:
                        if str(processed_files)[-4:] == "0000":
                            if prp:
                                print(str(processed_files) + " / ? counted.")
    count(path,progress_prints)
    return {"files" : processed_files, "skipped_dirs" : skipped_dirs}
def main():
    global git_files
    st = time.time()
    sys_files = get_file_count("C:/")
    global pbar
    pbar = tqdm(total=sys_files["files"])
    start_dir("C:/")
    et = time.time() - st
    print("Time elapsed: " + str(et))
    jstr = json.dumps(git_files,indent=4)
    dataPath = os.getenv("APPDATA") + "\\.gitpanion_api"
    try:
        w = open(dataPath + "search_data.json",'w')
        w.write(jstr)
        w.close()
    except FileNotFoundError:
        if os.path.exists(dataPath) == False:
            raise Exception("gitpanion_api not installed.")
    """
    start_dir("C:/Users/calder")
    w = open("sd.txt",'w')
    wstr = str(git_files).replace(",",",\n")
    w.write(wstr)
    """
if __name__ == '__main__':
    args = sys.argv[1:]
    os.system('title ' + args[0] + " file indexing")
    main()
