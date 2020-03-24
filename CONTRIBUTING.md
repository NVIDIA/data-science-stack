# Contributing to Data Science Stack

Contributions are always welcome!

Your contributions will have the best chance of being addressed and accepted
smoothly if you understand and follow our guidelines.

## General Guidelines

#### File Issue First

Any suggestions or bug reports should start with issue for tracking and
discussion. We want to know about bugs as soon as possible.
Features or changes should have discussion before you get started, so we can
be sure they fit the overall goals and scope of the project
(maintaining software stacks for data science).

#### Versioning

Versioning follows [Semantic Versioning](https://semver.org/).

#### Releace Cycle and Flow

The `master` branch will alwys have the latest code.
Standard fork and pull request workflow.

Version bumps will have seperate commits and tags. So please do not include
a version change in your pull request.
Not every change will get a PATCH version bump and GitHub release.

MINOR version releases, where we reconsider what packages are in the default
stacks and do some housecleaning, follow a bit after releases of
[RAPIDS](https://rapids.ai/) stabilize, since those are the core
libraries in the stack.

MAJOR version releases - aiming to never break backward compatability.

#### Commit Messages

All commit messages should follow
[Conventional Commits](https://www.conventionalcommits.org/).

#### Pull Request Scope & Method

Each pull request should address a single overall feature or bug if possible.
If the change requires documentation updates those should be in the SAME
pull request.
This makes reviews easier, rollbacks manageable, and the history clearer.

Merges will be done as "Squash and Merge" in most cases, so do not worry
about having multiple commits.

#### Formatting

Try to follow the existing formats of files you modify.
* Clarity over brevity.
* Less than 80 columns whenever reasonable.

## Sign your work

The sign-off is a simple line at the end of the explanation for the patch.
Your signature certifies that you wrote the patch or otherwise have the right
to pass it on as an open-source patch. The rules are pretty simple: if you
can certify the below 
(from [developercertificate.org](http://developercertificate.org/)):

```
Developer Certificate of Origin
Version 1.1

Copyright (C) 2004, 2006 The Linux Foundation and its contributors.
1 Letterman Drive
Suite D4700
San Francisco, CA, 94129

Everyone is permitted to copy and distribute verbatim copies of this
license document, but changing it is not allowed.

Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the best
    of my knowledge, is covered under an appropriate open source
    license and I have the right under that license to submit that
    work with modifications, whether created in whole or in part
    by me, under the same open source license (unless I am
    permitted to submit under a different license), as indicated
    in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including all
    personal information I submit with it, including my sign-off) is
    maintained indefinitely and may be redistributed consistent with
    this project or the open source license(s) involved.
```

Then you just add a line to every git commit message:

    Signed-off-by: Joe Smith <joe.smith@email.com>

Use your real name (sorry, no pseudonyms or anonymous contributions.)

If you set your `user.name` and `user.email` git configs, you can sign your
commit automatically with `git commit -s`.
