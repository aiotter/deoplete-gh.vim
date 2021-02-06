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

        self.name = 'matcher_number'
        self.description = 'matches on number of issues or PRs'

    def filter(self, context: UserContext) -> Candidates:
        results = []
        for candidate in context['candidates']:
            number = issue.get_number_from_candidate(candidate)
            if str(number).startswith(context['complete_str']):
                results.append(candidate)
        return results
