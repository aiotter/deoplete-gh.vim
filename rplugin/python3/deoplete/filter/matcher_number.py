from pynvim import Nvim
from deoplete.base.filter import Base
from deoplete.util import UserContext, Candidates


class Filter(Base):
    def __init__(self, vim: Nvim) -> None:
        super().__init__(vim)

        self.name = 'matcher_number'
        self.description = 'matches on number of issues or PRs'

    def filter(self, context: UserContext) -> Candidates:
        results = []
        for candidate in context['candidates']:
            number = candidate['_data'].number
            if str(number).startswith(context['complete_str']):
                results.append(candidate)
        return results
