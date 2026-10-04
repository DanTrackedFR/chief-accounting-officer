"""Governed work modes, orthogonal to accounting skill identity.

The bounded deterministic interpreter is a CI adapter. Semantic planners may
implement interpret(), but the runtime validates their proposal before routing.
"""
from dataclasses import dataclass, field, asdict
from enum import Enum

class WorkMode(str, Enum):
    DIAGNOSTIC_ANALYTICS = 'DIAGNOSTIC_ANALYTICS'
    ACCOUNTING_DETERMINATION = 'ACCOUNTING_DETERMINATION'
    CLOSE_REVIEW = 'CLOSE_REVIEW'
    RECONCILIATION_INVESTIGATION = 'RECONCILIATION_INVESTIGATION'
    REPORTING = 'REPORTING'
    PROCESS_CONTROL_REVIEW = 'PROCESS_CONTROL_REVIEW'
    AUDIT_SUPPORT = 'AUDIT_SUPPORT'
    DOCUMENTATION = 'DOCUMENTATION'
    TRANSACTION_ACCOUNTING = 'TRANSACTION_ACCOUNTING'

@dataclass
class Intent:
    primary: str
    secondary: list = field(default_factory=list)
    supporting: list = field(default_factory=list)
    bounded_owner: object = None
    interpretation: str = 'Structured accounting objective'
    def validate(self):
        modes = [self.primary] + self.secondary + [r['mode'] for r in self.supporting]
        if any(m not in {x.value for x in WorkMode} for m in modes) or len(modes)!=len(set(modes)):
            raise ValueError('Invalid or duplicate governed work modes')
        if any(not isinstance(r.get('reason'), str) or not r['reason'] for r in self.supporting):
            raise ValueError('Supporting intent requires reason')
        if self.bounded_owner and (self.secondary or self.supporting):
            raise ValueError('Simple inquiry cannot create artificial work modes')
        return self
    def record(self): return asdict(self.validate())


def interpret(objective):
    o=objective.lower().strip()
    # Bounded inquiries are selected before substantive classification.
    broad=any(w in o for w in ('review','investigate','why','explain','memo','process','account for'))
    if not broad and ('closing' in o or 'balance' in o):
        if 'inventory' in o:return Intent('REPORTING', bounded_owner='inventory-cost', interpretation='Closing inventory inquiry')
        if 'ap' in o.split():return Intent('REPORTING', bounded_owner='accounts-payable', interpretation='Closing AP inquiry')
    if 'memo' in o or 'document' in o:
        return Intent('DOCUMENTATION', ['ACCOUNTING_DETERMINATION'])
    if 'process' in o or 'too manual' in o or 'control' in o:
        return Intent('PROCESS_CONTROL_REVIEW', supporting=[dict(mode='CLOSE_REVIEW',reason='Recurring close process')])
    if 'how' in o and ('account' in o or 'recognise' in o or 'recognize' in o):
        return Intent('ACCOUNTING_DETERMINATION')
    if o.startswith('review') and 'close' in o:
        return Intent('CLOSE_REVIEW', ['DIAGNOSTIC_ANALYTICS'] if 'explain' in o or 'movement' in o else [],
            [dict(mode='ACCOUNTING_DETERMINATION',reason='Review accounting integrity')])
    if any(w in o for w in ('why','what’s going on',"what's going on",'figure out','explain','terrible')):
        return Intent('DIAGNOSTIC_ANALYTICS', supporting=[dict(mode='RECONCILIATION_INVESTIGATION',reason='Validate accounting movement'),
            *([dict(mode='CLOSE_REVIEW',reason='Requested close integrity review')] if 'close' in o else [])])
    if 'close' in o:return Intent('CLOSE_REVIEW')
    if 'reconcil' in o or 'investigat' in o:return Intent('RECONCILIATION_INVESTIGATION')
    if 'audit' in o:return Intent('AUDIT_SUPPORT')
    if 'statement' in o or 'report' in o:return Intent('REPORTING')
    if 'transaction' in o:return Intent('TRANSACTION_ACCOUNTING')
    return Intent('ACCOUNTING_DETERMINATION')
