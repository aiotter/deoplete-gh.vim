from deoplete.util import Candidate
from typing import List, Dict


def get_candidates_from_issues(issues: List[Dict]) -> Candidate:
    width = bool(issues) and len(str(issues[0]['number']))
    candidates = []
    for issue in issues:
        labels = ' '.join(f"[{label['name']}]" for label in issue['labels'])
        body = issue['body'].replace('\r', '')
        candidates.append({
            'word': str(issue['number']),
            'abbr': '#{0:<{width}} {1}'.format(issue['number'], issue['title'], width=width),
            'kind': 'PullReq' if issue.get('pull_request') else 'Issue',
            'info': f" {labels or ' == No Labels == '} \n{body}",
        })
    return candidates


def get_title_from_candidate(candidate: Candidate) -> str:
    return candidate['abbr'].split(' ', maxsplit=1)[-1]


def get_number_from_candidate(candidate: Candidate) -> str:
    return int(candidate['word'])
