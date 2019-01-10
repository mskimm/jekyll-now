import re
import os

import markdown

class Render:
  def __init__(self):
    with open('templates/header.html') as f:
      self.header = f.read()
    with open('templates/footer.md') as f:
      self.footer = '\n<footer>\n%s\n</footer>\n' % markdown.markdown(f.read())
    with open('templates/footer.html') as f:
      self.footer += f.read()
    with open('templates/disqus.html') as f:
      self.disqus = f.read()
    self.datepat = re.compile(r'([0-9]{4})(?:.?)([0-9]{2})(?:.?)([0-9]{2})')

  def __call__(self, src, to, replace={}, disqus=True):
    page = {}
    match = self.datepat.search(src)
    if match:
      page['date'] = '-'.join(match.groups())
    with open(src) as f:
      content = f.read()
    firstline = content.splitlines()[0].strip()
    page['title'] = 'no title'
    if firstline[0] == '#':
        page['title'] = firstline[1:]
    for old, new in replace.items():
      content = content.replace(old, new)
    with open(to, 'w') as f:
      f.write(self.header)
      f.write(markdown.markdown(content))
      if disqus:
          f.write(self.disqus)
      f.write(self.footer)
    return page

source = 'index.md'
target = 'index.html'

render = Render()
pages = []
for (path, _, files) in os.walk('.'):
  if path != '.' and source in files:
    page = render(os.path.join(path, source), os.path.join(path, target))
    if 'title' in page and 'date' in page:
        pages.append('* [{date}: {title}]({path})'.format(**page, path=os.path.normpath(path)))

# root pages
pages = '\n'.join(pages)
render('templates/index.md', 'index.html', {'{{pages}}': pages}, disqus=False)
render('templates/404.md', '404.html', disqus=False)

import http.server
http.server.test(http.server.SimpleHTTPRequestHandler)

