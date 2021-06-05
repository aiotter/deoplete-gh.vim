from pynvim import Nvim
from deoplete.base.filter import Base
from deoplete.util import UserContext, Candidates


class Filter(Base):
    def __init__(self, vim: Nvim) -> None:
        super().__init__(vim)

        self.name = 'sorter_number'
        self.description = 'sorts on number of issues or PRs'

    def filter(self, context: UserContext) -> Candidates:
        return sorted(context['candidates'], key=lambda x: x['_data'].number, reverse=True)
