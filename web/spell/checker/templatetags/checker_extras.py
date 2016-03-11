import datetime
from django import template

register = template.Library()


@register.simple_tag
def cur_time(fmt_str):
    return datetime.datetime.now().strftime(fmt_str)


side_pages = [(u'Spelling Checker', 'checker.index'),
              (u'Ngrams Stats', 'checker.stats'),
              #(u'Quick Search', 'checker.index'),
              ]


@register.inclusion_tag('sidebar.html')
def get_side_bar(page=None):
    return {'urls': side_pages, 'act_page': page}
