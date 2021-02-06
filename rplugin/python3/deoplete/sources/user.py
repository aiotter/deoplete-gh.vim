from deoplete.source.base import Base

from pathlib import Path
import importlib.util
spec = importlib.util.spec_from_file_location('user', Path(__file__).parent.parent / 'libs/user.py')
user = importlib.util.module_from_spec(spec)
spec.loader.exec_module(user)


class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)
        self.name = 'github_user'
        self.mark = '[GitHub]'
        self.rank = 500
        self.is_debug_enabled = True
        self.input_pattern = r'@.*'
        self.filetypes = ['gitcommit']
        self.sorters = ['sorter_comments']

    def get_complete_position(self, context):
        pos = context['input'].rfind('@')
        return pos if pos < 0 else pos + 1

    def gather_candidates(self, context):
        return user.candidates_from_github_users()
