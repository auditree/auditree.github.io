---
layout: post
category: architecture
title: Evidence locker overview
author: Al Finkelstein
author_github: alfinkel
---

At the core of the [Auditree framework][] is a [Git][] repository known as the
"evidence locker".  Each Auditree execution environment requires a dedicated
evidence locker in order to execute.  The Auditree framework can either clone
an evidence locker from a remote Git repository hosting service (GitHub,
GitLab, ...) or create a new local locker for you.  Serving as the Auditree
data store, the evidence locker houses evidence gathered by fetchers, evidence
generated by checks and/or evidence planted by the [Auditree Plant][] tool.

## Local vs. remote

The reasoning behind our choice of Git as the Auditree data store is
outlined nicely in our [previous post][] but in a nutshell, an evidence locker
uses Git as an efficient, reliable, tamper evident data store.  Although it is
possible to execute Auditree with only a local evidence locker, a typical
implementation of an Auditree execution environment will pull down a local
clone of a remote evidence locker, perform Auditree operations, store the
results of those operations as evidence in the cloned local locker and once
complete, push changes back to the remote evidence locker.

## Organization

Evidence locker content is namespaced into four top level folders within the
locker and manages that content on an ongoing basis.  The folders are:

- **raw**: All evidence retrieved by fetchers is stored here.
- **reports**: All report evidence generated by checks is stored here.
- **external**: All evidence gathered or generated outside of the Auditree
framework and planted by [Auditree Plant][] is stored here.
- **notifications**: All check notifications sent to the locker are stored
here.

## OK, but what makes it a locker?

...in a word, **metadata**.

As noted earlier, all files are organized according to their data type but
the Auditree framework still needs a way to treat these files as evidence and
that's where the metadata comes in.  The top level folders are purposefully
shallow. Each folder that contains evidence (`notifications` are a special
case, and not considered evidence) can be further organized with sub-folders
per category of evidence under `raw`, `reports` and `external`, for example by
tool or service provider.  Each evidence category sub-folder contains an
`index.json` file that stores all of the metadata for evidences within that
category.

Evidence metadata includes:

- Basic evidence metadata
   - An evidence last update date/time:  You may consider this as a duplication
   of Git file metadata but this last update date/time is updated as part of
   every execution of the Auditree framework whereas Git file metadata is only
   updated when the file content has changed.  This allows us to track the
   continued execution of fetchers and checks while still leveraging Git's
   efficient file storage methodology.
   - An evidence time to live duration
   - An evidence description
- Partitioned (raw) evidence metadata
   - Basic evidence metadata
   - Fields used to partition the evidence
   - A mapping of evidence partition to evidence file
- Report evidence metadata
   - Basic evidence metadata
   - Checks used to generate the report
   - A list of evidence used by the checks to produce the report
- External evidence metadata
   - Basic evidence metadata
   - Planter email
- Pruned evidence metadata
   - Basic/Partitioned/Report/External (whichever applies)
   - Pruner email
   - Evidence tombstone including an end of life date/time, last update
   date/time, and a reason for pruning.

In addition to all of the category `index.json` metadata files in the locker,
you will also find a `check_results.json` in the locker's root.  This file
contains all of the metadata from the most recent execution of Auditree checks.

Check results metadata is organized by check and contains:

- Accreditations tied a check
- Check results (successes/failures/warnings)
- A list of evidence used a check
- Report(s) generated a check

Finally, an evidence locker's `README.md` serves as an entry point into the
locker and contains a table of contents organized alphabetically by report
description.  For each report in the table of contents useful information such
as last execution date/time and evidence used to generate the report is included.

## Summary

An evidence locker is a namespaced Git repository with metadata.  It stores
files as evidence and allows the Auditree framework to manage that evidence
based on that evidence's metadata.


[Auditree framework]: https://github.com/ComplianceAsCode/auditree-framework
[Auditree Plant]: https://github.com/ComplianceAsCode/auditree-plant
[Git]: https://git-scm.com/
[previous post]: https://auditree.github.io/architecture/Goals_general_architecture.html#the-locker
