===========================
Django-Whoosh search engine
===========================

Djoosh is a very simple search engine for your Django projects.

WARNING: This is currently under heavy development, so use at your work risk!

Installation
============

#. Install with pip:

	``pip install djoosh``

#. Add `djoosh` to `INSTALLED_APPS` in your `settings.py`::

	INSTALLED_APPS = (
		'django.contrib.auth',
		'django.contrib.contenttypes',
		'django.contrib.sessions',
		'django.contrib.sites',
		...
		'djoosh',
	)

#. In your `models.py` add::

	from djoosh import SearchMixin
	
	...
	
	class BlogPost(models.Model, SearchMixin):
		...
		
   Note `SearchMixin` in the parents for `MyModel`. Just add it to any model
   that you want to search.
   

#. When you're done, run `python manage.py search rebuild`

#. That's it! You can now search your blog posts using
   ``BlogPost.search.query('some query')``,

   For example you can create a view like this::

	def search(request):
	
		query = request.GET.get('q', '')
		
		posts = BlogPost.search.query(query)
		
		return render_to_response('search_posts.html',
		                          {'posts': posts, 'query': query})

   ... and your template can be::
   
	<form action="/search" method="get">
		<input type="text" name="q" value="{{ query }}" />
		<input type="submit" value="Search Blogs" />
	</form>
	
	<h1>Search Results</h1>
	{% for post in posts %}
		<h2>{{ post.title }}</h2>
		<p>{{ post.content }}</p>
	{% endfor %}

Fine-Tuning
===========

Coming soon...

For the impatient::

	blog/search.py:

	from blog import BlogPost
	from djoosh import site, SearchModel
	
	class BlogPostSearch(SearchModel):
		model = BlogPost
		fields = ('title', 'tags')
		keywords = ('tags',)
		pk = 'id'
		
	site.register(BlogPost, BlogPostSearch)
	
You may also have a look at `djoosh.loading`, particularly `site` and `SearchModel`.
