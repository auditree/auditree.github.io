---
layout: index
title:
---

## Key concepts

> Auditree aims to be opinionated in how you work, but flexible in what work
> you do.

Everything revolves around *evidence*. Simple programs called *fetchers*
retrieve evidence from sources (API's, URL's, command line invocations) and
store that evidence in a *locker*. This is a git repository (so efficient,
tamper evident and versioned for storing evidence) with some additional
controls & metadata inserted by the supporting framework. Evidence can then be
verified by *checks*; simple unit tests against your evidence.

Your checks can be use to assert an operational posture, implement secondary
controls or be a primary control in your compliance posture.

Notification of check status can be sent to issues in a tracker, Slack,
PagerDuty, or even stored alongside evidence. Playbooks for how to respond to
check warnings or failures can be linked to from these notificiations.

## The tools

The Auditree system is designed to be extensible by those using it. It
provides a framework in which to build & run fetchers & checks, defines an
operational model for approaching compliance activities and supplies ancillary
tools to facilitate a workflow around that operational model.

- [Auditree framework][framework] - the core of the system, responsible for managing evidence in the locker, running fetchers & checks, notification and reporting. You can also read the [documentation][framework-docs] site.
- [Arboretum][arboretum] - a library of open fetchers & checks for you to use & contribute to.
- [Harvest][harvest] - collate evidence over time, run reports & analysis over the contents of the locker.
- [Plant][plant] - place manually gathered evidence into the locker.
- [Prune][prune] - correctly manage the retirement of evidence.

The framework, fetchers & checks and associated tools are all Apache licensed,
and open source for you and your auditors to review.

[framework]: https://github.com/ComplianceAsCode/auditree-framework
[framework-docs]: https://complianceascode.github.io/auditree-framework/
[arboretum]: https://github.com/complianceascode/auditree-arboretum
[harvest]: https://github.com/complianceascode/auditree-harvest
[plant]: https://github.com/complianceascode/auditree-plant
[prune]: https://github.com/complianceascode/auditree-prune
