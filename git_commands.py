print("Importing modules...")
from github import Github
from github import GithubException
import ghAuth
import sys, json, getpass, base64, requests, random
import urllib.request
import urllib.error

def check_oauth_token():
    global r
    global noFile
    global oauth_token
    noFile = False
    try:
        r = open("userData.json",'r')
    except:
        noFile = True
    if noFile:
        oauth_token = ghAuth.getAuth(useBrowser=True)
        w = open("userData.json",'w')
        w.write('"oauth_token" : "%s"}' % oauth_token)
        w.close()
    else:
        rf = r.read()
        j = json.loads(rf)
        r.close()
        try:
            oauth_token = j["oauth_token"]
        except KeyError:
            oauth_token = ghAuth.getAuth(useBrowser=True)
            w = open("userData.json",'w')
            w.write('{"oauth_token" : "%s"}' % oauth_token)
            w.close()
    #print(oauth_token)
    return oauth_token
        
class GitHubUser(object):
    def __init__(self,oauth_token):
        self.oauth_token = oauth_token
        res = urllib.request.urlopen("http://api.github.com/user?oauth_token=" + oauth_token).read()
        j = json.loads(res.decode('utf-8'))
        self.user_json = j
    def commit_file(self,path,msg,file,branch,name,print_status=False):
        if print_status:
            print("retriving file sha...")
        content_url = "http://api.github.com/repos/"+ self.user_json["login"] + "/" + name + "/contents/" + path + "?ref=" + branch + "&oauth_token=" + self.oauth_token
        global sha
        global no_sha
        no_sha = False
        try:
            sha = urllib.request.urlopen(content_url).read()
            sha = json.loads(sha.decode('utf-8'))["sha"]
        except urllib.error.HTTPError:
            e = sys.exc_info()[1]
            if e.code == 404:
                no_sha = True
        # now put all the needed data into 1 string
        # note: I didn't use .format or % () for the string since there were many Json parsing errors on the github end (400 errors)
        # when I did. but not when I used the old fashioned way of just stringing them together.
        email = self.user_json["email"]
        username = self.user_json["login"]
        file = base64.b64encode(file.encode('utf-8'))
        file = file.decode('utf-8').replace("\n","\\n")
        if no_sha:
            data = '{"commiter": {"email": "' + email + '", "name": "' + username + '"}, "content": "' + file + '", "message": "' + msg + '"}'
        else:
            data = '{"commiter": {"email": "' + email + '", "name": "' + username + '"}, "sha": "' + sha + '", "content": "' + file + '", "message": "' + msg + '"}'
        #print(data)
        if print_status:
            print("Making request to commit...")
        headers = {
            'Authorization' : "token " + self.oauth_token
            }
        new_url = "https://api.github.com/repos/"+ self.user_json["login"] + "/" + name + "/contents/" + path
        res = requests.put(new_url,data=data,headers=headers)
        return res.status_code
        pass
if __name__ == '__main__':
    oauth_token = check_oauth_token()
    user = GitHubUser(oauth_token)
    res = user.commit_file("Testey.txt","commit from module",str(random.random()),"master","Github_Api_Test",print_status=True)
    print("Got response " + str(res))
