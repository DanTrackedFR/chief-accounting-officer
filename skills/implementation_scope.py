"""Owner implementation closure for exact-case certification.

Unidentified legacy cases conservatively bind every owner. Reviewed canonical
document sets can identify legacy owners without guessing from amounts or IDs.
Ambiguous sets bind all matching owners. Supplied case bytes remain fingerprinted.
"""
import ast


def owners(case, packages):
    package = case.get('package')
    if package in packages:
        return [package]
    docs = case.get('knowledge_review', {}).get('documents', [])
    topics = {row.get('topic_id') for row in docs if isinstance(row, dict)} - {None}
    matches = [key for key, (_, expected) in packages.items() if topics and topics == set(expected)]
    return sorted(matches or packages)


def fingerprint_files(case, root, packages):
    common = ['skills/core_accounting.py', 'skills/production.py',
              'skills/implementation_scope.py', 'interfaces/public_output.py',
              'skills/REVIEWER-CONTROLS.md', 'skills/run_skill.py']
    files = {root / name for name in common}
    selected = owners(case, packages)
    queue = []
    for owner in selected:
        directory = root / 'skills' / owner
        queue.extend(directory.glob('*.py'))
        files.update(directory.glob('*.md'))
        files.update(directory.glob('*KNOWLEDGE-MAP.json'))
    visited = set()
    while queue:
        path = queue.pop()
        if path in visited:
            continue
        visited.add(path)
        files.add(path)
        for node in ast.walk(ast.parse(path.read_text())):
            names = []
            if isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            elif isinstance(node, ast.Import):
                names = [item.name for item in node.names]
            for name in names:
                candidate = root / 'skills' / (name + '.py')
                # production is the shared dispatch boundary, already bound;
                # scanning its routing imports would reintroduce all-owner coupling.
                if name != 'production' and candidate.is_file():
                    queue.append(candidate)
    supplements = {
        'government-grants': ('government-grants', 'grant_knowledge'),
        'borrowing-costs': ('borrowing-costs', 'borrowing_knowledge'),
        'insurance-contracts-accounting': ('insurance-contracts', 'insurance_knowledge'),
        'derivatives-hedge-accounting': ('derivatives-hedge', 'hedge_knowledge'),
        'inventory-cost': ('inventory-cost', None),
        'agriculture-biological-assets': ('agriculture', None),
        'income-taxes': ('income-taxes', None),
    }
    for owner in selected:
        if owner in supplements:
            folder, helper = supplements[owner]
            files.update((root / 'knowledge' / folder).glob('*.py'))
            if helper:
                files.add(root / 'skills' / (helper + '.py'))
    if root / 'skills/governance_accounting.py' in files:
        files.add(root / 'skills/GOVERNANCE-KNOWLEDGE-MAP.json')
    if root / 'skills/final_batch_accounting.py' in files:
        files.add(root / 'skills/FINAL-BATCH-KNOWLEDGE-MAP.json')
    return sorted(files)
