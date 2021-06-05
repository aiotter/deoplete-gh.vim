from pynvim import Nvim
from deoplete.base.filter import Base
from deoplete.util import UserContext, Candidates


class Filter(Base):
    def __init__(self, vim: Nvim) -> None:
        super().__init__(vim)

        self.name = 'matcher_opened'
        self.description = 'matches only opened issues and PRs'

    def filter(self, context: UserContext) -> Candidates:
        return [c for c in context['candidates'] if not c['_data'].closed]
