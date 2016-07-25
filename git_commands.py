from github import Github
from github import GithubException
import sys, json, getpass, base64
import urllib.request

class GitHubUser(object):
    def __init__(self,user,pswrd):
        self.try_write_auth(user,pswrd)
        self.username = user
        self.password = pswrd
    def try_write_auth(self,userr,pswrd):
        global wrong_pass
        wrong_pass = False
        try:
            global g
            g = Github(userr,pswrd)
            user = g.get_user()
            user.total_private_repos
        except GithubException:
            msg = sys.exc_info()
            if msg[1]._GithubException__data["message"] == "Bad credentials":
                wrong_pass = True
        if wrong_pass:
            raise Exception("Wrong password.")
        ###################################################
        #               save info now                     #
        ###################################################
        w = open("userData.json",'w')
        jsonObj = {
            "user" : userr,
            "pswrd" : pswrd
            }
        jstr = json.dumps(jsonObj, indent=4)
        w.write(jstr)
        w.close()
        pass
    def commit_file(self,path,msg,file,branch,commiter,repo_url,print_status=False):
        if print_status:
            print("retriving file sha...")
        if repo_url[-1] != "/":
            repo_url = repo_url + "/"
        #print(repo_url,path,branch)
        content_url = repo_url + "contents/" + path + "?ref=" + branch
        sha = urllib.request.urlopen(content_url).read()
        sha = json.loads(sha.decode('utf-8'))["sha"]
        #print(sha)
        jsonObj = {
            "message" : msg,
            "content" : file,
            "sha" : sha,
            "commiter" : commiter
            }
        jsonObj["file"] = base64.b64encode(file.encode('utf-8'))
        jsonObj["file"] = jsonObj["file"].decode('utf-8').replace("\n","\\n")
        strJson = json.dumps(jsonObj)
        if print_status:
            print("Making request to commit...")
        oauth_token = None
        headers = {
            'Authorization' : "token " + oauth_token
            }
        res = requests.put(content_url, headers=headers, data=strJson)
        pass
ps = getpass.getpass()
user = GitHubUser("CalderWhite",ps)
user.commit_file("Test.txt","commit from module","new test commit","master",{"CalderWhite","calderwhite1@gmail.com"},"https://api.github.com/repos/CalderWhite/Github_Api_Test")
#commit_file("/Test.txt","Test commit for api.",b'Testing123',"master")
