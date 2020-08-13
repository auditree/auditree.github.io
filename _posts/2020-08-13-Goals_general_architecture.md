---
layout: post
category: architecture
title: Goals & general architecture
---

When building Auditree we wanted to shift compliance problems into engineering problems. We have more people with knowledge and expertise around engineering, DevOps and automation than we do around compliance, so scaling the compliance skills we do have is essential. At the same time, tools & approaches that are familiar to our engineers is going to mean better engagement.

We deliberately constrained the architecture of Auditree to only use tools that were already in our stack, and had a goal of not requiring any additional infrastructure be added or managed by the team. This makes sense not just form a familiarity & speed point of view, but also from a repudiation point of view; if we're using systems managed as a service by other teams we have less access.

## Framework is smart so fetchers/checks don't need to be

The reason for building Auditree is scaling our compliance efforts. We wanted engineers to be able to dip in, write a `unittest` based check & go back to their normal activities. To enable this, we built the framework, with the aim of it holding the "smarts" and the fetchers/checks only containing the logic/intelligence required to collect & evaluate evidence.

We've exposed this functionality as [decorators and context managers][evidence], as well as [`Fetcher`][fetcher] and [`Check`][check] classes. Using these mean people can write their code and not worry about evidence TTL, where files reside in the locker or managing git as the framework takes care of these functions for you.



[check]: https://github.com/ComplianceAsCode/auditree-framework/blob/main/compliance/check.py
[evidence]: https://github.com/ComplianceAsCode/auditree-framework/blob/main/compliance/evidence.py
[fetcher]: https://github.com/ComplianceAsCode/auditree-framework/blob/main/compliance/fetch.py