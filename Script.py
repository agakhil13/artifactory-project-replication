import requests
import json


def get_project_detail(token, baseurl):
    url = baseurl + "access/api/v1/projects"
    headers = {
        'Authorization': 'Bearer ' + token
    }

    response = requests.request("GET", url, headers=headers)
    result = json.loads(response.text)
    return result


def create_project(token, baseurl, data):

    url = baseurl + "access/api/v1/projects"

    payload = json.dumps(data)
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    output = json.loads(response.text)
    return output


def get_project_roles(token, baseurl, project_key):

    url = baseurl + "access/api/v1/projects/" + project_key + "/roles"

    headers = {
        'Authorization': 'Bearer ' + token
    }

    response = requests.request("GET", url, headers=headers)

    result = json.loads(response.text)
    return result


def set_project_roles(token, baseurl, data, project_key):
    url = baseurl + "access/api/v1/projects/" + project_key + "/roles"

    payload = json.dumps(data)
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    output = json.loads(response.text)
    return output


def update_project_roles(token, baseurl, data, project_key, role_name):
    url = baseurl + "access/api/v1/projects/" + project_key + "/roles/" + role_name

    payload = json.dumps(data)
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)
    output = json.loads(response.text)
    return output


def get_project_users(token, baseurl, project_key):

    url = baseurl + "access/api/v1/projects/" + project_key + "/users"

    headers = {
        'Authorization': 'Bearer ' + token
    }

    response = requests.request("GET", url, headers=headers)

    result = json.loads(response.text)
    return result


def set_project_users(token, baseurl, data, project_key, user_name):
    url = baseurl + "access/api/v1/projects/" + project_key + "/users/" + user_name

    payload = json.dumps(data)
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)
    output = json.loads(response.text)
    return output


def get_project_repositories(token, baseurl, project_key):

    url = baseurl + "repositories?project=" + project_key
    headers = {
        'Authorization': 'Bearer ' + token
    }

    response = requests.request("GET", url, headers=headers)

    output = json.loads(response.text)
    return output

def set_project_repositories(token,baseurl, project_key, repo):

    url = baseurl + "access/api/v1/projects/_/attach/repositories/" + repo + "/" + project_key + "?force=true"

    payload={}
    headers = {
    'Authorization': 'Bearer ' + token
    }

    response = requests.request("PUT", url, headers=headers, data=payload)
    if response.text:
        output = json.loads(response.text)
        return output

def share_project_repositories(token,baseurl, project_key, repo):

    url = baseurl + "access/api/v1/projects/_/share/repositories/" + repo + "/" + project_key

    payload={}
    headers = {
    'Authorization': 'Bearer ' + token
    }

    response = requests.request("PUT", url, headers=headers, data=payload)
    if response.text:
        output = json.loads(response.text)
        return output

def unshare_project_repositories(token,baseurl, project_key, repo):

    url = baseurl + "access/api/v1/projects/_/share/repositories/" + repo + "/" + project_key

    payload={}
    headers = {
    'Authorization': 'Bearer ' + token
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)
    if response.text:
        output = json.loads(response.text)
        return output
def delete_project_repositories(token,baseurl, repo):

    url = baseurl + "access/api/v1/projects/_/attach/repositories/" + repo 

    payload={}
    headers = {
    'Authorization': 'Bearer ' + token
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)
    if response.text:
        output = json.loads(response.text)
        return output


def delete_project(token, baseurl, project_key):
    url = baseurl + "access/api/v1/projects/" + project_key
    headers = {
        'Authorization': 'Bearer ' + token
    }

    response = requests.request("DELETE", url, headers=headers)
    if response.text:
        output = json.loads(response.text)
        return output

if __name__ == "__main__":
    PROD_TOKEN = "ADMIN_TOKEN"
    PROD_BASE_URL = "https://artifactory.com/artifactory/api/"
    STA_TOKEN = "ADMIN_TOKEN"
    STA_BASE_URL = "https://staging-artifactory.com/artifactory/api/"
    project_detail = get_project_detail(PROD_TOKEN, PROD_BASE_URL)
    # print(project_detail)
    for x in project_detail:
        if x["project_key"] in ["det-debian", "det"]:
            print("\n")
            project_key = x["project_key"]
            new_project = create_project(STA_TOKEN, STA_BASE_URL, x)
            if "errors" in new_project:
                print("Already exists project with Display Name: " +
                      x["display_name"])
                repos = get_project_repositories(STA_TOKEN, STA_BASE_URL, project_key)
                for repo in repos:
                    repo_name = repo["key"]
                    if repo["type"] == "LOCAL":
                        delete_project_repositories(STA_TOKEN,STA_BASE_URL, repo_name)
                    elif repo["type"] == "REMOTE":
                        unshare_project_repositories(STA_TOKEN, STA_BASE_URL, project_key, repo_name)
                result = delete_project(STA_TOKEN, STA_BASE_URL, project_key)
                print("Project deleted from staging " + x["display_name"])
                # continue
                print("Creating new project..")
                new_project = create_project(STA_TOKEN, STA_BASE_URL, x)
                if "display_name" in new_project:
                    print("Created project with Display Name: " + new_project["display_name"])
            elif "display_name" in new_project:
                print("Created project with Display Name: " + new_project["display_name"])
            roles = get_project_roles(PROD_TOKEN, PROD_BASE_URL, project_key)
            for role in roles:
                if role["type"] == "CUSTOM":
                    print("Creating Role.. "+ role["name"])
                    result = set_project_roles(STA_TOKEN, STA_BASE_URL, role, project_key)
                    if "errors" in result:
                        print("Error while creating role..")
                    #     print("Role already exists.. "+ role["name"])
                    #     role_name = role["name"]
                    #     print("Updating Role.. "+ role["name"])
                    #     update_project_roles(STA_TOKEN, STA_BASE_URL, role, project_key, role_name)
            users = get_project_users(PROD_TOKEN, PROD_BASE_URL, project_key)
            for user in users["members"]:
                username = user["name"]
                output = set_project_users(STA_TOKEN, STA_BASE_URL, user, project_key, username)
                if "name" in output:
                    print("User "+ output["name"] + " added into project..")
                else:
                    print("error while adding user " + username)
            repos = get_project_repositories(PROD_TOKEN, PROD_BASE_URL, project_key)
            print("Adding repositories to the project..")
            for repo in repos:
                repo_name = repo["key"]
                if repo["type"] == "REMOTE":
                    result = share_project_repositories(STA_TOKEN, STA_BASE_URL, project_key, repo_name)
                elif repo["type"] == "LOCAL":
                    result = set_project_repositories(STA_TOKEN, STA_BASE_URL, project_key, repo_name)
                if result:
                    print(result)
            print("[Done]")
