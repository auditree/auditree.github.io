---
layout: post
category: orchestration
title: Running Auditree in Tekton
---

[Tekton][] is a Kubernetes-native CI/CD tool. It provides the primatives of a build system as Kube resources, allowing a developer to chain together a pipeline in a way that feels natural to those familiar with Kube. More importantly, it's a good tool to run Auditree in, as it is easily deployed & managed, can be configured & extended through code and provides scheduled running. Tekton does move fast, so it's best to consult their documentation and treat what follows as a guide more than gospel. If you do find bugs, or places where their API has moved on, please file an [issue][] or [PR][]. Similarly, if you want to know how to deploy Tekton, there are a number of [tutorials](https://medium.com/01001101/tekton-pipeline-kubernetes-native-pipelines-296478f5c835) [out there](https://www.arthurkoziel.com/creating-ci-pipelines-with-tekton-part-1/), along side the projects documentation.

## Pipeline

Tekton assembles steps into tasks and tasks into pipelines. We're going to make a pipeline, with a single Auditree task which:

- pulls in your Auditree config
- installs the Auditree code
- verifies the install
- runs fetchers
- runs checks
- runs a [Harvest][] report

Each of these will be a separate step. Task steps can share storage (a `volumeMount`) between one another, and we'll use this to propagate state through the pipeline.

**TODO:**

### Auditree configuration

First we want to define a `pipelineResource` which is the configuration repository (where you store config for the fetchers/checks you run).

```
apiVersion: tekton.dev/v1alpha1
kind: PipelineResource
metadata:
  name: auditree-tekton-example
spec:
  type: git
  params:
    - name: url
      value: https://github.com/auditree/auditree-tekton-example
    - name: revision
      value: master
```

This will pull the repo in and make it available to our steps.

### Auditree installation

Auditree uses git for the locker, so we'll want to configure that in a step:

```yaml
    - name: git-config
      image: alpine
      imagePullPolicy: Always
      script: |
        #!/bin/sh
        apk add --no-cache bash git
        git config --global user.email "auditree-demo@contrived-example.com"
        git config --global user.name "Auditree"
      resources:
        inputs:
          - name: auditree-tekton-example
            type: git
```

We want every run of the pipeline to pull in the latest & greatest auditree code. This means each execution will have a clean environemnt & any issues that have been resolved since the last run will automatically be picked up. This means we can use a vanilla, minimal container, and install the code each invocation.

```yaml
    - name: build-venv
      image: python:3.7-alpine
      imagePullPolicy: Always
      script: |
        #!/bin/sh
        cd /workspace
        python3.7 -m venv venv
        . venv/bin/activate
        pip install -q --upgrade pip setuptools
        pip install -q . --upgrade --upgrade-strategy eager

```

Once built, we'll also want to confirm that the built environment is as we expect. If you use your own fetchers/checks, you may want to add a similar `python -c ...` to print out the version of your code.

```yaml
    -
      name: verify-built-env
      image: python:3.7-alpine
      imagePullPolicy: Always
      script: |
        #!/bin/sh
        apk add --no-cache bash git >> /dev/null
        cd /workspace
        . venv/bin/activate
        compliance -V
        python -c 'from arboretum import __version__; print(f"Auditree Arboretum: {__version__}")'
```

**TODO** credentials

### Collecting & validating evidence

We now have a configured installation of Auditree, and so can run it to collect & validate evidence. This is done in two steps:

```yaml
    - name: fetch
      image: python:3.7-alpine
      imagePullPolicy: Always
      env:
      -
        name: TMPDIR
        value: $(inputs.params.pathToTempDir)
      script: |
        #!/bin/sh
        apk add --no-cache bash git >> /dev/null
        . $(inputs.params.pathToCustomerEnv)/bin/activate
        cd $(inputs.params.pathToCustomerWorkspace)
        echo compliance --fetch --evidence full-remote --notify stdout -C auditree.json -v --creds-path=/home/credentials
        compliance --fetch --evidence full-remote --notify stdout -C auditree.json -v --creds-path=/home/credentials
        echo Fetching complete
      volumeMounts:
      - mountPath: /home
        name: internal-storage
    - name: check
      image: python:3.7-alpine
      imagePullPolicy: Always
      env:
      script: |
        #!/bin/sh
        apk add --no-cache bash git >> /dev/null
        . $(inputs.params.pathToCustomerEnv)/bin/activate
        cd $(inputs.params.pathToCustomerWorkspace)
        echo compliance --check $PROFILE_ID --evidence full-remote --notify stdout -C auditree.json -v -s --creds-path=/home/credentials
        compliance --check ${PROFILE_ID} --evidence full-remote --notify stdout -C auditree.json -v -s --creds-path=/home/credentials
        echo Checks complete
```

### Run reporting via Harvest

You may want to run a harvest report after you compliance run, or this may make sense to do as a separate pipeline (different frequencies for e.g.).

**TODO**

[Tekton]: https://github.com/tektoncd/pipeline
[issue]: https://github.com/auditree/auditree.github.io/issues
[pr]: https://github.com/auditree/auditree.github.io/pulls
[Harvest]: https://github.com/ComplianceAsCode/auditree-harvest