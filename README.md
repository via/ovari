# ovari - a simple rpm building service


## Configuration ==
/etc/ovari.conf
```
[paths]
# Where to store persistent data about environments
environments=/var/ovari/environments 

# Where to have the individual job chroots
workspaces=/var/ovari/workspaces

# Where to store the job database
jobdb=/var/ovari/jobs.db

# Where to store build results
results=/var/ovari/results
```

# API 

### GET /v1/jobs/ 
Collection that returns a JSON list of all job IDs

### GET /v1/jobs/:jobid
Returns information about a job:
{
  "status": "building",
  "started": "2015-06-23 11:23:49 EDT",
  "environment": "centos-6-x86_64",
  "log": "/v1/jobs/:jobid/log",
}
-or-
{
  "status": "success",
  "started": "2015-06-23 11:23:49 EDT",
  "finished": "2015-06-23 11:25:20 EDT",
  "environment": "centos-6-x86_64",
  "log": "/v1/jobs/:jobid/log",
  "rpms": [
    "/v1/jobs/:jobid/rpms/blah.rpm",
    "/v1/jobs/:jobid/rpms/blah-mysql.rpm"
  ],
  "srpm": "/v1/jobs/:jobid/rpms/blah.src.rpm"
}
-or-
{
  "status": "failed",
  "started": "2015-06-23 11:23:49 EDT",
  "finished": "2015-06-23 11:25:20 EDT",
  "environment": "centos-6-x86_64",
  "log": "/v1/jobs/:jobid/log",
  "srpm": "/v1/jobs/:jobid/rpms/blah.src.rpm"
}

### DELETE /v1/jobs/:jobid
Deletes the job and all associated files

### GET /v1/environments/
Returns a json list of all configured environments

### POST /v1/environments/:environment
### PATCH /v1/environments/:environment
### DELETE /v1/environments/:environment
Creates, updates, or deletes an environment

Pass in a json body containing the initial package list and macros:
{
  "packages": [
    "vim"
  ],
  "macros": [
    "_dist": "el5"
  ]
}

### POST /v1/environments/:environment/image
Pass in a tarball containing a root filesystem ready to be chrooted into

### GET /v1/environments/:environment/repos/
Returns a list of repo files associated with the environment

### GET /v1/environments/:environment/repos/:repo
Returns the repo file

### DELETE /v1/environments/:environment/repos/:repo
Deletes the repo file

### POST /v1/environments/:environment/repos/:repo
Pass in a yum repo file

### POST /v1/environments/:environment/jobs/
Start a new job, pass in an SRPM as the body.

Returns a json body:
{
  "jobid": "abcdefg",
  "joburl: "/v1/jobs/abcdefg"
}

### GET /v1/environments/:environment/jobs/
Returns a json list of all job IDs associated with this environment
