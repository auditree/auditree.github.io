---
layout: post
category: architecture
title: Goals & general architecture
author: Simon Metson
author_github: drsm79
---

When building Auditree we wanted to shift compliance problems into engineering problems. We have more people with knowledge and expertise around engineering, DevOps and automation than we do around compliance, so scaling the compliance skills we do have is essential. At the same time; tools & approaches that are familiar to our engineers is going to mean better engagement from them in addressing & supporting compliance activities.

![Clipboard to automation](/images/clipboard.png)

When designing Auditree, we deliberately constrained the architecture to only use tools that were already in our stack, and had a goal of not requiring any additional infrastructure be added or managed by the team. This makes sense not just from a familiarity & velocity point of view, but also from a repudiation point of view; if we're using systems managed as a service by other teams we have less access & ability to tamper with them.

## Framework is smart so fetchers & checks don't need to be

The reason for building Auditree is to improve the scaling of our compliance efforts. We wanted engineers to be able to dip in, write a `unittest` based check & go back to their normal activities. To enable this, we built the framework, with the aim of it holding the "smarts" and the fetchers/checks only containing the logic and sufficient intelligence required to collect & evaluate evidence.

We've exposed this functionality as decorators and context managers that can be used to [write][] and [read][] evidence, as well as [`Fetcher`][fetcher] and [`Check`][check] classes. Using these mean that people can write their code and not worry about evidence TTL (time to live), where files reside in [the Locker](#the-locker) or managing pushing data remotely as the framework takes care of these functions for you.

## The Locker

Auditree focuses on evidence. We wanted to use a long term store which:

- Met familiarity goals of the project as a whole
- Maintained record integrity & provided evidence of tampering
- Could deliver a change history via a defined API
- Had suitable access & permission controls
- Was able to support a range of data formats (text based or binary)
- Was able to meet the retention requirements associated with the durations of audits

While we run a [database-as-a-service](https://cloudant.com) we quickly realised another tool was actually a better fit: Git. Git meets all our requirements; its used daily by our team, we're well versed in managing access & integrity, it has a well documented interface (with a decent [python library](https://gitpython.readthedocs.io/en/stable/)) and it's pretty permissive with regards to data it holds.

What we didn't want was being tied to a single hosting platform (GitHub, GitLab...). This means the Locker is implemented as "pure git", and does not use proprietary vendor APIs. We do have notifiers and fetchers that talk to vendor APIs but the core framework does not.

## Runner agnostic

Initially we ran Auditree on Travis; we have a private instance which required some configuration but no new infrastructure had to be deployed. The environment & install is simple & portable between different runners, and we've ensured the framework is agnostic of its running environment - we've run it in Jenkins, from cron, in Tekton as well as in Travis. All that's required is the ability to verify that the runner has not been tampered with.

One thing we baked in early on is that each run is a new install. This means we can rectify issues in fetcher/check code or configuration and have the next run pick up the fix, without intervention. It also means that the only state shared between invocations is managed via the locker, preventing any "ghosts in the machine" from changing evidence.

[check]: https://complianceascode.github.io/auditree-framework/design-principles.html#compliance-checks
[write]: https://complianceascode.github.io/auditree-framework/design-principles.html#evidence-validation
[read]: https://complianceascode.github.io/auditree-framework/design-principles.html#id2
[fetcher]: https://complianceascode.github.io/auditree-framework/design-principles.html#compliance-fetchers
[locker]: https://complianceascode.github.io/auditree-framework/design-principles.html#evidence-locker
