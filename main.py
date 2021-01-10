import os
from datetime import datetime
import markdown2
# markdown2 helps to use metadata method.
import jinja2

# POST dict to store blog-posts in the folder posts
POSTS = {}
# Loop through all the markdown files in the posts folder
for markdown_post in os.listdir('posts'):
    file_path = os.path.join('posts', markdown_post)
    with open(file_path, 'r') as f:
        # extras=['metadata'] gives a dict of metadata
        # that we provided at the begining of the markdown file.
        POSTS[markdown_post] = \
           markdown2.markdown(f.read(), extras=['metadata'])
        # POSTS dict, key - markdown_post ie file name
        # value - content (string)
        # POSTs['markdown_post].metadata gives a dict of metadata

# Sort the markdown_posts w.r.t time
POSTS = {
    # key: value for key in sorted posts
    post: POSTS[post] for post in sorted(
        POSTS, key=lambda post: datetime.strptime(
            POSTS[post].metadata['date'], '%d-%m-%Y'),
        reverse=True)
    # strptime is used to convert string date to date format
}

# Extract variables from the parsed markdown and hand
# them over to jinja2
# Create an environment to show jinja2 where the templates folder is located.
env = jinja2.Environment(loader=jinja2.PackageLoader('main', 'templates'))
# PackageLoader - 1st arg is the name of the python file,
# and 2nd arg is the folder where template files are located.
home_template = env.get_template('home.html')
post_template = env.get_template('post.html')

# Pass metadata to home.html page
posts_metadata = [POSTS[post].metadata for post in POSTS]
# tags of each post in some kind of list to make each
# tag into a clickable link.
# Currently all the tags are being passed as a single string.
# tags = [post['tags'] for post in posts_metadata]

# After extracting data from our parsed file we hand
# it over to jinja2 while calling the render() function.

# home_html = home_template.render(posts=posts_metadata, tags=tags)
home_html = home_template.render(posts=posts_metadata)
# this will pass a list of metadata through the
# variable posts to our home page template
# Write this html to a file
with open('output/home.html', 'w') as g:
    g.write(home_html)

# To render individual post pages.
for post in POSTS:
    posts_metadata = POSTS[post].metadata
    post_data = {
        'content': POSTS[post],
        'title': posts_metadata['title'],
        'date': posts_metadata['date'],
    }
    post_html = post_template.render(post=post_data)
    post_file_path = 'output/posts/{slug}.html'.format(
        slug=posts_metadata['slug'])
    os.makedirs(os.path.dirname(post_file_path), exist_ok=True)
    with open(post_file_path, 'w') as h:
        h.write(post_html)
