"""Node-addressed inputs and results. Package aliases resolve only when unique."""
from collections.abc import MutableMapping
from .scopes import execution_identity, scoped_context


class NodeTable(dict):
    def resolve(self, key):
        if dict.__contains__(self,key): return key
        matches=[n.id for n in self.values() if key==n.logical_id or (key==n.selected_skill and n.issue!='diagnostic accounting follow-up')]
        if len(matches)>1: raise ValueError('Ambiguous execution alias; exact node required')
        return matches[0] if matches else key
    def __getitem__(self,key): return dict.__getitem__(self,self.resolve(key))
    def get(self,key,default=None): return dict.get(self,self.resolve(key),default)
    def __contains__(self,key): return dict.__contains__(self,self.resolve(key))


class OwnerInputs(MutableMapping):
    def __init__(self, context): self.context=context; self.data={}; self.packages={}
    def add(self,owner,source):
        from .runtime import digest
        ctx=scoped_context(self.context,source)
        key=execution_identity(owner,ctx)
        if key in self.data and digest(self.data[key])!=digest(source): raise ValueError('Conflicting supplied owner cases for execution')
        self.data[key]=source;self.packages[key]=owner
        return key
    def key(self,owner,scope_id=None):
        matches=[id for id,pkg in self.packages.items() if pkg==owner and (scope_id is None or self.data[id].get('scope_id',self.data[id].get('entity'))==scope_id)]
        if len(matches)!=1:raise ValueError('Exact reviewed owner Scope required')
        return matches[0]
    def resolve(self,key):
        if key in self.data:return key
        matches=[id for id,owner in self.packages.items() if owner==key]
        if len(matches)>1:raise ValueError('Ambiguous package input; exact node required')
        return matches[0] if matches else key
    def __getitem__(self,key):return self.data[self.resolve(key)]
    def __setitem__(self,key,value):self.data[self.resolve(key)]=value
    def __delitem__(self,key):del self.data[self.resolve(key)]
    def __iter__(self):return iter(self.data)
    def __len__(self):return len(self.data)


def populations(facts):
    for family,value in facts.items():
        if family=='task_attributes':continue
        rows=value if isinstance(value,list) else [value]
        for source in rows:
            if not isinstance(source,dict):raise ValueError('Malformed supplied fact family: '+(family if family in __import__('orchestration.planning',fromlist=['FACT_ADAPTERS']).FACT_ADAPTERS else 'unregistered'))
            yield family,source
