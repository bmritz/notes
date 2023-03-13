"""Clean the HTML files output by singlefile."""

import bs4
import logging
from dataclasses import dataclass
from typing import Generator
import functools
import pathlib

logger = logging.getLogger(__name__)

def change_links(a):
    """Change links to relative links.
    
    Notes:
        The soup that is entered can be assumed to be an a tag.
    
    """
    domains = [
        "#/"
    ]
    assert a.name == "a"

    attrs = a.attrs
    href = attrs.pop('href', None)
    if href:
        for domain in domains:
            href = href.removeprefix(domain)

    dataref = attrs.pop('data-ref', None)
    if dataref: 
        href = dataref # + ".html"

    if href:
        a.attrs['href'] = href


# add in css

def add_css_stylesheet(soup, css_path: str):
    logger.info("Adding stylesheet.")
    style_tag = soup.new_tag('link', attrs=dict(href=css_path, rel="stylesheet", type="text/css"))
    head = soup.select_one('head')
    head.append(style_tag)

def add_css_stylesheets(soup):
    css_paths = ["static/css/export.css","static/css/custom.css", "static/css/style.css", "static/css/tabler-icons.min.css"]
    for css_path in css_paths:
        add_css_stylesheet(soup, css_path=css_path)

@dataclass
class Selector:
    name: str
    kwargs: dict[str, str]

@dataclass
class Action:
    name: str
    kwargs: dict[str, str]

@dataclass
class WorkPiece:
    selector: Selector
    action: Action

@dataclass
class Work:
    worklist: list[WorkPiece]

# add in css
ACTIONS = {
    "parent-extract": lambda el: el.parent.extract(),
    "extract": lambda el: el.extract(),
    "append-class": lambda el, class_: el.attrs['class'].append(class_),
    'change-links': change_links,
    'add-stylesheet-links': add_css_stylesheets,
}

FIND = 'find_all'
SELECT = 'select'
SELF = 'self'
SELECTORS = {
    # selector functions should return an iterable
    SELECT: lambda soup, selector: soup.select(selector),
    FIND: lambda soup, **kwargs: soup.find_all(**kwargs),
    SELF: lambda soup: [soup],
}


WORK = [
    {
        # remove the inline styles
        'selector': {'name': SELECT, 'kwargs': {'selector': 'style'}}, 
        'action': {'name': 'extract'}
    },
    {
        # remove the script tags
        'selector': {'name': FIND, 'kwargs': {'name': 'script'}}, 
        'action': {'name': 'extract'}
    },
    {
        # add links to css stylesheets
        'selector': {'name': SELF}, 
        'action': {'name': 'add-stylesheet-links'}
    },
    {
        # open the left menu
        'selector': {'name': SELECT, 'kwargs': {'selector': 'main'}}, 
        'action': {'name': 'append-class', 'kwargs': {'class_': 'ls-left-sidebar-open'}}
    },
    {
        # open the left menu
        'selector': {'name': SELECT, 'kwargs': {'selector': '#main-container'}}, 
        'action': {'name': 'append-class', 'kwargs': {'class_': 'ls-left-sidebar-open'}}
    },
    {
        # open the left menu
        'selector': {'name': SELECT, 'kwargs': {'selector': '#left-sidebar'}}, 
        'action': {'name': 'append-class', 'kwargs': {'class_': 'ls-open'}}
    },
    # {
    #     # delete the search icon
    #     'selector': {'name': SELECT, 'kwargs': {'selector': '#search-button'}}, 
    #     'action': {'name': 'parent-extract'}
    # },
    # {   
    #     # delete the navbar toggle icon
    #     'selector': {'name': SELECT, 'kwargs': {'selector': '#left-menu'}}, 
    #     'action': {'name': 'parent-extract'}
    # }, 
    # {
    #     # delete the graph button
    #     'selector': {'name': FIND, 'kwargs': {'name': 'a', 'string': 'Graph'}}, 
    #     'action': {'name': 'extract'}
    # },
    # {
    #     # delete the toolbar button
    #     'selector': {'name': FIND, 'kwargs': {'name': 'button', "attrs": {"class":'toolbar-dots-btn'}}}, 
    #     'action': {'name': 'extract'}
    # },
    # {
    #     # delete the right sidebar button
    #     'selector': {'name': FIND, 'kwargs': {'name': 'button', "attrs": {"class":'toggle-right-sidebar'}}}, 
    #     'action': {'name': 'extract'}
    # },
    # {
    #     # delete the home button
    #     'selector': {'name': FIND, 'kwargs': {'name': 'button', "attrs": {"class": 'icon', 'title': 'Home'}}}, 
    #     'action': {'name': 'extract'}
    # },
    # {
    #     # delete the unlinked references if they exist
    #     'selector': {'name': FIND, 'kwargs': {'name': 'div', "attrs": {"class":'page-unlinked'}}}, 
    #     'action': {'name': 'extract'}
    # },
    # {
    #     # delete the info button that is generated from comments
    #     'selector': {'name': FIND, 'kwargs': {'string': lambda t: isinstance(t, bs4.Comment) }}, 
    #     'action': {'name': 'extract'}
    # },
    # {
    #     # delete the info button that is generated from comments
    #     'selector': {'name': FIND, 'kwargs': {'name': 'a' }}, 
    #     'action': {'name': 'change-links'}
    # },
]


def get_selector(piece_of_work):
    selector_name = piece_of_work['selector']['name']
    selector_kwargs = piece_of_work['selector'].get('kwargs', {})
    return functools.partial(SELECTORS[selector_name], **selector_kwargs)

def get_action(piece_of_work):
    action_name = piece_of_work['action']['name']
    action_kwargs = piece_of_work['action'].get('kwargs', {})
    return functools.partial(ACTIONS[action_name], **action_kwargs)

@dataclass
class File:
    path: pathlib.Path
    soup: bs4.BeautifulSoup


    def get_save_path(self):
        """Return the path to save the file."""
        # split on the url fragment, and return the last part if it exists
        parts = str(self.path).split("#")
        if len(parts) == 1:
            return self.path
        path = parts[1]
        if path == '/':
            path = 'index.html'
        directory = self.path.parent
        return directory / path

    def save(self):
        save_path = self.get_save_path()

        with open(save_path, "w") as fil:
            fil.write(str(self.soup))
        logger.info(f"Saved to {self.path}")
            
            

def execute(work: Work, file: File):
    """Perform the `work` on `soup`, modifying in place
    
    Returns:
        A reference to the same `soup` input.
        
    """
    for piece_of_work in work.worklist:

        selector = get_selector(piece_of_work)
        action = get_action(piece_of_work)
        for el in selector(file.soup):
            if el:
                action(el)
    logger.info(f"processed {file.path}")
    return file


def read_files(directory: pathlib.Path) -> Generator[File, None, None]:
    """Yield the files from the directory, skipping subdirectories."""
    for path in directory.iterdir():
        if path.is_file():
            with open(path, 'rb') as fil:
                soup = bs4.BeautifulSoup(fil.read(), features="html.parser")
            yield File(path=path, soup=soup)

def process_directory(directory: str):

    for file in read_files(pathlib.Path(directory)):
        if not file.soup:
            logger.info(f"skipped {file.path}")
            continue
        logger.info(f"Beginning to process: {file.path}")
        # modifies the file "in place"
        execute(work=Work(worklist=WORK), file=file)
        
        file.save()


logging.basicConfig(level=logging.DEBUG)
process_directory('www3')