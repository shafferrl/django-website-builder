# django-website-builder
Automated website builder for simple Django websites.

## Statement of Purpose ##

This simple website builder was created after having built my second website using the Django web development framework.  Finding much of the process tedious and a perfect candidate for automation, as well as to make the process of building a website as economically competitive as possible, this set of tools for building simple websites was created.

## Scope ##

The website builder was created with the intention of fully automating the process of building and deploying a website.  It was even desirable to have the process of creating accounts with a hosting provider on behalf of potential clients, but this part of the process was abandoned--at least temporarily--due to parts of the hosting provider's process requiring a human operator to approve new accounts, rendering streamlining relatively ineffective for this part of the process.  There also arose some legal concerns for purchasing services on behalf of clients with their payment credentials, and dealing with such matters was outside the scope of this project.

In addition to creating an automated process for building a website, this project was also undertaken to get better acquainted with Python, programming more generally, and the entire top-to-bottom process of building a website and deploying it to the internet.

## Limitations ##

The basic concept of this builder is relatively straightforward.  Whenever creating a website (in this case with Django), there are steps in the process that will involve no element of creativity or require no flexibility and can be readily automated.  If building websites for a living, it will also be desirable to let a script run in milliseconds what could take a developer seconds, minutes, or possibly hours to replicate, both because the developer will find it tedious to do the same thing over and over again and also to be competitive in the market where "time is money".

Given that this process is automated, it started with an extremely limited capability, which involved taking a pre-built template and replacing only the name on the banner with whatever name was entered at the start of the project.  This level of (in)flexibility was sufficient for a proof-of-concept, but for a real-world model, this would be unacceptable in most cases, as real clients would demand highly customizable options and would have a litany of choices in the open market for such tools.  Eventually, the scripts were improved to make the builder more flexible, but there were still fairly rigid requirements for a template to be able to work with the builder.  The project was eventually put "on ice" after it was decided that the only way to make it flexible enough for consumer demand would be to build an entire Content Management System or make the builder compatible with such solutions that are already established like WordPress.

## Use And Other Notes ##

There is currently no plan to make a detailed guide for how to use the website builder, as it is still limited in utility, there is a desire to keep a more flexible variant private, and some parts of the builder may run into terms of service violations if used in the wild.  For now, it is simply a portfolio project meant to demonstrate my experience with Python, Django, Linux, Bash, and various other services and tools used for full-stack web development.
