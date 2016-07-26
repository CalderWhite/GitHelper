from github import Github
from github import GithubException
import sys, json, getpass, base64, requests, random
import urllib.request
import urllib.error

class GitHubUser(object):
    def __init__(self,oauth_token):
        self.oauth_token = oauth_token
        res = urllib.request.urlopen("http://api.github.com/user?oauth_token=" + oauth_token).read()
        j = json.loads(res.decode('utf-8'))
        self.user_json = j
    """
    the PyGithun library was terrible, so I decided to just use the github v3 REST api
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
    """
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
        print(res.text)
        pass
if __name__ == '__main__':
    user = GitHubUser(getpass.getpass("Gimme dat hash:"))
    user.commit_file("Testey.txt","commit from module",str(random.random()),"master","Github_Api_Test",print_status=True)
