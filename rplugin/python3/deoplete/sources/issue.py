from deoplete.source.base import Base
import json
import subprocess

from pathlib import Path
import importlib.util
spec = importlib.util.spec_from_file_location('issue', Path(__file__).parent.parent / 'libs/issue.py')
issue = importlib.util.module_from_spec(spec)
spec.loader.exec_module(issue)
get_candidates_from_issues = issue.get_candidates_from_issues


class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)
        self.name = 'github_issue'
        self.mark = '[GitHub]'
        self.rank = 500
        self.is_debug_enabled = True
        self.input_pattern = r'#.*'
        self.filetypes = ['gitcommit']
        self.matchers = ['matcher_number_title']
        self.sorters = ['sorter_number']
        self.converters = ['converter_remove_overlap', 'converter_truncate_abbr',
                           'converter_truncate_kind',  # 'converter_truncate_info',
                           'converter_truncate_menu']

        process = subprocess.run(
            ['gh', 'api', '/repos/:owner/:repo/issues?per_page=100'], capture_output=True)
        self._issues = json.loads(process.stdout) if process.stdout else []

    def get_complete_position(self, context):
        pos = context['input'].rfind('#')
        return pos if pos < 0 else pos + 1

    # def on_post_filter(self, context):
    #     completion_start = context['complete_position']
    #     sharp_position = completion_start - 1
    #     if len(context['input']) <= sharp_position or context['input'][sharp_position] == '#':
    #         return context['candidates']
    #     else:
    #         return []

    def gather_candidates(self, context):
        return get_candidates_from_issues(self._issues)
