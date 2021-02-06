from pynvim import Nvim
from deoplete.base.filter import Base
from deoplete.util import UserContext, Candidates

from pathlib import Path
import importlib.util
spec = importlib.util.spec_from_file_location('user', Path(__file__).parent.parent / 'libs/user.py')
user = importlib.util.module_from_spec(spec)
spec.loader.exec_module(user)


class Filter(Base):
    def __init__(self, vim: Nvim) -> None:
        super().__init__(vim)

        self.name = 'sorter_comments'
        self.description = 'sorts based on number of comments they did on the repository'

    def filter(self, context: UserContext) -> Candidates:
        return sorted(context['candidates'], key=lambda dct: dct['_sort_key'], reverse=True)
