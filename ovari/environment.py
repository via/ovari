import os
import os.path
import shutil

def get_environments(env_path):
    dirs = os.listdir(env_path)
    return dirs

'''
On disk storage layout
/var/ovari/environments/centos-6-x86_64/
                                        image.tar.gz  -  Image file
                                        packages      -  Text list of packages
                                        macros        -  Rpmmacro file
                                        repos/
                                              centos-base
                                              epel
'''

class Environment:
    def __init__(self, env_path, name):
        self.name = name
        self.path = env_path

    def create(self):
        try:
            os.mkdir(os.path.join(self.path, self.name))
            os.mkdir(os.path.join(self.path, self.name, "repos"))
        except OSError:
            return False
        return True

    def delete(self):
        try:
            shutil.rmtree(os.path.join(self.path, self.name))
        except OSError:
            return False
        return True
 
    def get_image(self):
        try:
            with open(os.path.join(self.path, self.name, "image.tar.gz")) as f:
                image = f.read()
                return image
        except (OSError, IOError):
            return None

    def set_image(self, image):
        try:
            with open(os.path.join(self.path, self.name, "image.tar.gz"),
                      "w") as f:
                f.write(image)
                return True
        except (OSError, IOError):
            return False
 
    def get_macros(self):
        macros = {}
        try:
            with open(os.path.join(self.path, self.name, "macros")) as f:
                for macroline in f.readlines():
                    splits = macroline.split()
                    macros[splits[0]] = " ".join(splits[1:])
                return macros 
        except (OSError, IOError):
            return None

    def set_macros(self, macros):
        macrotext = "\n".join(["{0} {1}".format(k,v) for (k,v) in macros.items()])
        print macrotext
        try:
            with open(os.path.join(self.path, self.name, "macros"),
                      "w") as f:
                f.write(macrotext)
                return True
        except (OSError, IOError):
            return False

    def get_packages(self):
        try:
            with open(os.path.join(self.path, self.name, "packages")) as f:
                packages = [r.rstrip() for r in f.readlines()]
                return packages
        except (OSError, IOError):
            return None

    def set_packages(self, packages):
        try:
            with open(os.path.join(self.path, self.name, "packages"),
                      "w") as f:
                f.write("\n".join(packages))
                return True
        except (OSError, IOError):
            return False

    def list_repos(self):
        try:
            repos = os.listdir(os.path.join(self.path, self.name, "repos"))
            return repos
        except OSError:
            return None

    def set_repo(self, reponame, repocontents):
        try:
            with open(os.path.join(self.path, self.name, "repos",
                                   reponame), "w") as f:
                f.write(repocontents)
                return True
        except (OSError, IOError):
            return False

    def get_repo(self, reponame):
        try:
            with open(os.path.join(self.path, self.name, "repos",
                                   reponame)) as f:
                return f.read()
        except (OSError, IOError):
            return None

    def delete_repo(self, repo):
        try:
            os.remove(os.path.join(self.path, self.name, "repos", repo))
            return True
        except OSError:
            return False
    
