from flask import Flask, request
from ConfigParser import ConfigParser
import json
from environment import Environment
from environment import get_environments as get_envs

app = Flask(__name__)
config = ConfigParser()
config.read("/etc/ovari.conf")

@app.route("/v1/environments/")
def get_environments():
    envs = get_envs(config.get("paths", "environments"))
    return (json.dumps(envs), 200)

@app.route("/v1/environments/<environment>", methods=["POST", "PATCH"])
def create_environment(environment):
    env = Environment(config.get("paths", "environments"), environment)
    payload = request.json
    if request.method == "POST":
        if not env.create():
            return ("Environment already exists!", 409)
    if "packages" in payload:
        env.set_packages(payload['packages'])
    if "macros" in payload:
        env.set_macros(payload['macros'])
    if request.method == "POST":
        return ("Environment created", 204)
    else:
        return ("Environment updated", 200)

@app.route("/v1/environments/<environment>", methods=["GET"])
def get_environment(environment):
    env = Environment(config.get("paths", "environments"), environment)
    macros = env.get_macros()
    packages = env.get_packages()
    res = {
      "name": environment,
      "macros": macros,
      "packages": packages
    }
    return (json.dumps(res), 200)
    

@app.route("/v1/environments/<environment>/image", methods=["GET", "PUT"])
def environment_image(environment):
    env = Environment(config.get("paths", "environments"), environment)
    if request.method == "GET":
        image = env.get_image()
        if image is None:
            return ("No image stored", 404)
        return (image, 200)
    if request.method == "PUT":
        if env.set_image(request.data):
            return ("Image saved", 200)
        else:
            return ("Image saving error", 500)

@app.route("/v1/environments/<environment>/repos/")
def get_environment_repos(environment):
    env = Environment(config.get("paths", "environments"), environment)
    repos = env.list_repos()
    if repos is None:
        return ("Error listing repositories", 500)
    return (json.dumps(repos), 200)

@app.route("/v1/environments/<environment>/repos/<repo>")
def get_environment_repo(environment, repo):
    env = Environment(config.get("paths", "environments"), environment)
    repo = env.get_repo(repo)
    if repo is None:
        return ("Repository not found", 404)
    return (repo, 200)

@app.route("/v1/environments/<environment>/repos/<repo>", methods=["DELETE"])
def delete_environment_repo(environment, repo):
    env = Environment(config.get("paths", "environments"), environment)
    if env.delete_repo(repo):
        return ("Successfully deleted", 200)
    else:
        return ("Unable to delete repository file", 500)

@app.route("/v1/environments/<environment>/repos/<repo>", methods=["PUT"])
def put_environment_repo(environment, repo):
    env = Environment(config.get("paths", "environments"), environment)
    if env.set_repo(repo, request.data):
        return ("Successfully created repository", 204)
    else:
        return ("Unable to create repository", 500)

app.run(debug=True)
