from pynvim import Nvim
from deoplete.base.filter import Base
from deoplete.util import UserContext, Candidates

from pathlib import Path
import importlib.util
spec = importlib.util.spec_from_file_location('issue', Path(__file__).parent.parent / 'libs/issue.py')
issue = importlib.util.module_from_spec(spec)
spec.loader.exec_module(issue)


class Filter(Base):
    def __init__(self, vim: Nvim) -> None:
        super().__init__(vim)

        self.name = 'sorter_number'
        self.description = 'sorts on number of issues or PRs'

    def filter(self, context: UserContext) -> Candidates:
        return sorted(context['candidates'], key=issue.get_number_from_candidate, reverse=True)
