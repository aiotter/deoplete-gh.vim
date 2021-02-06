from pynvim import Nvim
from deoplete.base.filter import Base
from deoplete.util import UserContext, Candidates

from pathlib import Path
import importlib.util
spec = importlib.util.spec_from_file_location('matcher_number', Path(__file__).parent / 'matcher_number.py')
matcher_number = importlib.util.module_from_spec(spec)
spec.loader.exec_module(matcher_number)

spec = importlib.util.spec_from_file_location('matcher_title', Path(__file__).parent / 'matcher_title.py')
matcher_title = importlib.util.module_from_spec(spec)
spec.loader.exec_module(matcher_title)


class Filter(Base):
    def __init__(self, vim: Nvim) -> None:
        super().__init__(vim)

        self.name = 'matcher_number_title'
        self.description = 'matches if either number or title of issues or PRs matches'

    def filter(self, context: UserContext) -> Candidates:
        filtered_by_number = matcher_number.Filter.filter(self, context)
        filtered_by_title = matcher_title.Filter.filter(self, context)
        return filtered_by_number + filtered_by_title
