================
Django Blog Base
================

A Django application that provides a few utilities useful for implementing
basic blog functionality. The application is quite flexible and can be used to
implement a blog in a project or as a base for creating a blogging engine.

The application is pretty specialized and does not provide any functionality
to do comments, trackbacks, tags etc. There are applications and external
solutions out there that provide such functionality. Roll a reusable
application that includes and configures everything you need if you find
yourself creating a lot of blogs that share a set of common functionality.

Dependencies
============

Any markup module you wish to use (`markdown`, `textile` or `docutils`).

Installation
============

Settings
--------

Add the ``blog_base`` to your INSTALLED_APPS::

    INSTALLED_APPS = (
        ...
        'blog_base',
    )

Create an Entry Model
---------------------

Create a model that extends `blog_base.models.BaseEntry`::

    from blog_base.models import BaseEntry

    class DevelopmentEntry(BaseEntry):
        some_field = ...

Register your blog
------------------

Register the model you created in the previous step for use when creating
entries. Your project's `urls.py` might be a good place::

    from blog_base import blogs
    blogs.register('development', DevelopmentEntry)
    
(NOTE: You must register your model *before* running `admin.autodiscover()`)

URL directives
--------------

Get started by adding the following in your projects' `urls.py`::

    (r'^blogs/', include('blog_base.urls')),

And your blog should now be available at::

    /blogs/development/

Configuration
=============

`blogs.register()` takes a configuration class as an optional argument. A
configuration class works in a similar fashion to a `admin.ModelAdmin` class;
you extend a basic configuration and override any attributes to achieve
desired behaviour.

Example::

    from blog_base.blogs import BlogConfiguration

    class DevelopmentConfiguration(BlogConfiguration):
        entry_list_template_name = 'myblog/entry_list.html'
        feed_title = 'Feed for my blog'

And register as such::

    blogs.register('development', DevelopmentEntry, DevelopmentConfiguration)

See ``blog_base.blogs.BlogConfiguration`` for documentation of all available
attributes.

TODO
====

I'm not entirely satisfied with some implementation details. The application
will probably see quite a few changes when I have time to play with it.

* Add regression tests and work a little more on the example application.
* Consider alternative URL implementations. Prefixing all URLs with something
  like '^/blogs/' is far from ideal in many situations (especially not
  suitable for single-blog implementations). It's easy enough to write new
  routing based on the one provided by the application, or to simply use an
  empty pattern ('^'), but there are better solutions to this I am sure.
* Friendly error message when selecting a markup option that has not been
  installed.
* Better support for configuring the admin interface.
* Improve feed-configuration.
* Must configurations really be registered before running
  `admin.autodiscover()`? Is that really a problem? Look into it.
* Maybe not send the entire configuration instance in every view.
* Support for alternative content types might fall in the scope of this
  application (think pygments etc).
* Consider possible performance improvements, if just for a few seconds.
* Maybe split BaseEntry into a minimal core and a few special abstract models?
