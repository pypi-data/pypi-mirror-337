"""
PyDetex
https://github.com/ppizarror/PyDetex

FONTS
Configures font styles.
"""

__all__ = [
    'FONT_TAGS',
    'FONT_PROPERTIES',
    'TAGS_FONT'
]

from typing import Dict, Optional, Union

# Define properties
bg = 'background'
bold = 'bold'
fg = 'foreground'
italic = 'italic'
name = 'name'
overstrike = 'overstrike'
roman = 'roman'
slant = 'slant'
spacing3 = 'spacing3'
underline = 'underline'
weight = 'weight'
size = 'size'

# Configure fonts
FONT_PROPERTIES: Dict[str, Optional[Dict[str, Union[str, int]]]] = {
    'bold': {weight: bold},
    'bold_italic': {weight: bold, slant: italic},
    'bullet': None,
    'equation_char': {weight: bold, fg: '#19b70a'},
    'equation_inside': {slant: italic, fg: '#ffa450'},
    'error': {fg: '#ff6b68'},
    'h1': {size: 2, weight: bold, spacing3: 1},
    'highlight': {bg: '#fff200'},
    'italic': {slant: italic},
    'link': {weight: bold, fg: '#ff02a6'},
    'normal': {},
    'repeated_tag': {slant: italic, fg: '#ff002b'},
    'repeated_word': {weight: bold},
    'strike': {overstrike: True},
    'tex_argument': {fg: '#999999'},
    'tex_command': {fg: '#09accb'},
    'underlined': {underline: True, spacing3: 1}
}

# Configure the tags
FONT_TAGS: Dict[str, str] = {}
TAGS_FONT: Dict[str, str] = {}
for k in FONT_PROPERTIES.keys():
    FONT_TAGS[k] = f'⇱PYDETEX_FONT:{k.upper()}⇲'
    TAGS_FONT[FONT_TAGS[k]] = k
