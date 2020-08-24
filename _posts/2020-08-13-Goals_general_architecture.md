---
layout: post
category: architecture
title: Goals & general architecture
---

When building Auditree we wanted to shift compliance problems into engineering problems. We have more people with knowledge and expertise around engineering, DevOps and automation than we do around compliance, so scaling the compliance skills we do have is essential. At the same time; tools & approaches that are familiar to our engineers is going to mean better engagement from them in addressing & supporting compliance activities.

![Clipboard to automation](/images/clipboard.png)

When designing Auditree, we deliberately constrained the architecture to only use tools that were already in our stack, and had a goal of not requiring any additional infrastructure be added or managed by the team. This makes sense not just from a familiarity & velocity point of view, but also from a repudiation point of view; if we're using systems managed as a service by other teams we have less access & ability to tamper with them.

## Framework is smart so fetchers & checks don't need to be

The reason for building Auditree is to improve the scaling of our compliance efforts. We wanted engineers to be able to dip in, write a `unittest` based check & go back to their normal activities. To enable this, we built the framework, with the aim of it holding the "smarts" and the fetchers/checks only containing the logic and sufficient intelligence required to collect & evaluate evidence.

We've exposed this functionality as [decorators and context managers][evidence], as well as [`Fetcher`][fetcher] and [`Check`][check] classes. Using these mean people can write their code and not worry about evidence TTL, where files reside in the locker or managing git as the framework takes care of these functions for you.

## Runner agnostic

Initially we ran Auditree on Travis; we have a private instance & it required config but no new infrastructure be deployed. The environment & install is simple & portable between different runners, and we've ensured the framework is agnostic of it's running environment - we've run it in Jenkins, from cron, in Tekton. All that's required is the ability to verify that the runner has not been tampered with.

One thing we baked in early on is that each run is a new install. This means we can rectify issues in fetcher/check code or configuration and have the next run pick up the fix, without intervention. It also means that the ony state shared between invocations is managed via the locker, preventing any "ghosts in the machine" from changing evidence.

[check]: https://github.com/ComplianceAsCode/auditree-framework/blob/main/compliance/check.py
[evidence]: https://github.com/ComplianceAsCode/auditree-framework/blob/main/compliance/evidence.py
[fetcher]: https://github.com/ComplianceAsCode/auditree-framework/blob/main/compliance/fetch.py