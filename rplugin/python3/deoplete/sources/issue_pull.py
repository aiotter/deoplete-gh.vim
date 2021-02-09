from deoplete.source.base import Base

from pathlib import Path
import importlib.util
spec = importlib.util.spec_from_file_location('gql', Path(__file__).parent.parent / 'libs/gql.py')
gql = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gql)


class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)
        self.name = 'github_issue_pull'
        self.mark = '[GitHub]'
        self.rank = 500
        self.input_pattern = r'#.*'
        self.filetypes = ['gitcommit']
        self.matchers = ['matcher_number_title', 'matcher_opened']
        self.sorters = ['sorter_number']
        self.converters = ['converter_remove_overlap', 'converter_truncate_abbr',
                           'converter_truncate_kind',  # 'converter_truncate_info',
                           'converter_truncate_menu']

        self.handler = gql.GqlHandler(vim)

    def get_complete_position(self, context):
        pos = context['input'].rfind('#')
        return pos if pos < 0 else pos + 1

    def gather_candidates(self, context):
        return self.handler.issue_candidates + self.handler.pull_candidates