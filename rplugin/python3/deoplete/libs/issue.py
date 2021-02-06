from deoplete.util import Candidate
import typing


def get_candidate_from_issue(issue: typing.Dict, width=4) -> Candidate:
    labels = ' '.join(f"[{label['name']}]" for label in issue['labels'])
    body = issue['body'].replace('\r', '')
    return {
        'word': str(issue['number']),
        'abbr': '#{0:<{width}} {1}'.format(issue['number'], issue['title'], width=width),
        'kind': 'PullReq' if issue.get('pull_request') else 'Issue',
        'info': f" {labels or ' == No Labels == '} \n{body}",
    }


def get_title_from_candidate(candidate: Candidate) -> str:
    return candidate['abbr'].split(' ', maxsplit=1)[-1]


def get_number_from_candidate(candidate: Candidate) -> str:
    return int(candidate['word'])
