=================================
django_js_utils - Django JS Utils
=================================

There have been many forks of this library tracing their source all back
to mlouro/django-js-utils. Each with the goal to eliminate the hard-coding
of django urls into javascript files. There are several different approaches:

- statically generating the javascript 'urls' file, client-side reverse
- a view that dynamically generates the full 'urls' file, client-side reverse
- an ajax handler that reverses the url, server-side reverse
- generate the full urls file upon first request and cache for subsequent, client-side reverse

They have their pros/cons and can be userful in different situations.

This fork is intended to combine all of the above approaches so that this library
can be used in any of the above scenerios. 


Installation
**********************
1. Install the application using pip (assuming you have a github acount[^non-github-install]):

    pip install git+git@github.com:ajmirsky/django-js-utils.git
    

Usage
********************

Method #1 :: statically generated (client-side)

Method #2 :: view generated (client-side)

Method #3 :: ajax url reverse (server-side)

Method #4 :: static and cache (client-side)


Footnotes
**********************
[^non-github-install]: For those who don't have a github account, you can install directly using:

pip install https://github.com/ajmirsky/django-js-utils.git
