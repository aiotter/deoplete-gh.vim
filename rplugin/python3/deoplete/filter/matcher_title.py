from pynvim import Nvim
from deoplete.base.filter import Base
from deoplete.util import UserContext, Candidates
from deoplete.util import fuzzy_escape
import re


class Filter(Base):
    def __init__(self, vim: Nvim) -> None:
        super().__init__(vim)

        self.name = 'matcher_title'
        self.description = 'matches on title of issues or PRs'

    def filter(self, context: UserContext) -> Candidates:
        complete_str = context['complete_str']
        if context['ignorecase']:
            complete_str = complete_str.lower()
        if not complete_str:
            return list(context['candidates'])

        results = []
        for candidate in context['candidates']:
            title = candidate['_data'].title
            p = re.compile(fuzzy_escape(complete_str, context['camelcase']))
            if context['ignorecase']:
                if p.search(title.lower()):
                    results.append(candidate)
            else:
                if p.search(title):
                    results.append(candidate)
        return results
