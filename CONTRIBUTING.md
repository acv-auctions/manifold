# Contributing to Manifold

👍 First off, thanks for taking the time to contribute! 👍

The following is a set of guidelines for contributing to Manifold, which are hosted in the [ACV Auctions Organization](https://github.com/acv-auctions) on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

#### Table Of Contents

* [How Can I Contribute?](#how-can-i-contribute)
  * [Reporting Bugs](#reporting-bugs)
  * [Suggesting Enhancements](#suggesting-enhancements)
  * [Your First Code Contribution](#your-first-code-contribution)
  * [Pull Requests](#pull-requests)

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for Manifold. Following these guidelines helps maintainers and the community understand your report 📝, reproduce the behavior 💻 💻, and find related reports 🔎.

Before creating bug reports, please check [this list](https://github.com/acv-auctions/manifold/issues) as you might find out that you don't need to create one. When you are creating a bug report, please [include as many details as possible](#how-do-i-submit-a-good-bug-report). [Fill out an issue](https://github.com/acv-auctions/manifold/issues) using the correct template, the information it asks for helps us resolve issues faster.

> **Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.

#### How Do I Submit A (Good) Bug Report?

Bugs are tracked as [GitHub issues](https://guides.github.com/features/issues/). Create an issue on that repository and provide the following information by filling in [the template](https://github.com/acv-auctions/manifold/issues/new).

Explain the problem and include additional details to help maintainers reproduce the problem:

* **Use a clear and descriptive title** for the issue to identify the problem.
* **Describe the exact steps which reproduce the problem** in as many details as possible.
* **Provide specific examples to demonstrate the steps**. Include links to files or GitHub projects, or copy/pasteable snippets, which you use in those examples. If you're providing snippets in the issue, use [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
* **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior.
* **Explain which behavior you expected to see instead and why.**
* **Include screenshots and animated GIFs** which show you following the described steps and clearly demonstrate the problem.
* **If the problem is related to performance or memory**, include some details about what exactly is happening.

Provide more context by answering these questions:

* **Did the problem start happening recently** (e.g. after updating to a new version of Manifold) or was this always a problem?
* If the problem started happening recently, **can you reproduce the problem in an older version of Manifold?** What's the most recent version in which the problem doesn't happen? You can download older versions of Manifold from [the releases page](https://github.com/acv-auctions/manifold/releases).
* **Can you reliably reproduce the issue?** If not, provide details about how often the problem happens and under which conditions it normally happens.

Include details about your configuration and environment:

* **Which version of Manifold are you using?** You can get the exact version by running the `manage.py runrpcserver` command, or by checking in `manifold.__init__.py`.
* **What's the name and version of the OS you're using**?
* **Are you running Manifold in a virtual machine?** If so, which VM software are you using and which operating systems and versions are used for the host and the guest?

#### How Do I Submit A (Good) Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues](https://guides.github.com/features/issues/). Provide the following information.

* **Use a clear and descriptive title** for the issue to identify the suggestion.
* **Provide a step-by-step description of the suggested enhancement** in as many details as possible.
* **Provide specific examples to demonstrate the steps**. Include copy/pasteable snippets which you use in those examples, as [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
* **Describe the current behavior** and **explain which behavior you expected to see instead** and why.
* **Include screenshots and animated GIFs** which help you demonstrate the steps or point out the part of Manifold which the suggestion is related to. You can use [this tool](https://www.cockos.com/licecap/) to record GIFs on macOS and Windows, and [this tool](https://github.com/colinkeenan/silentcast) or [this tool](https://github.com/GNOME/byzanz) on Linux.
* **Explain why this enhancement would be useful** to most Manifold developers.
* **Specify which version of Manifold you're using.** You can get the exact version by running the `manage.py runrpcserver` command, or by checking in `manifold.__init__.py`.
* **Specify the name and version of the OS you're using.**

#### Local Development

For local development, [clone the repository](https://github.com/acv-auctions/manifold). There exists the `manifold`
module, a `tests` directory for all local testing, and a `Makefile` to help complete basic commands.

### Pull Requests

* Fill in [the required template](PULL_REQUEST_TEMPLATE.md)
* Do not include issue numbers in the PR title
* Include screenshots and animated GIFs in your pull request whenever possible.
* Document new code based on the [Documentation Styleguide](#documentation-styleguide)
* End all files with a newline
* Avoid platform-dependent code
