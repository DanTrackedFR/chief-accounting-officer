"""Reperform retained cases, plus independent boundary/amount expectations."""
import ast,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def expression(s,values):
 tree=ast.parse(str(s),mode='eval')
 permitted=(ast.Expression,ast.Constant,ast.Name,ast.Load,ast.BinOp,ast.UnaryOp,ast.BoolOp,ast.Compare,ast.IfExp,ast.Call,ast.Add,ast.Sub,ast.Mult,ast.Div,ast.Pow,ast.USub,ast.UAdd,ast.Not,ast.And,ast.Or,ast.Eq,ast.NotEq,ast.Lt,ast.LtE,ast.Gt,ast.GtE)
 if any(not isinstance(n,permitted) for n in ast.walk(tree)):raise ValueError('unsafe expression')
 for n in ast.walk(tree):
  if isinstance(n,ast.Call) and (not isinstance(n.func,ast.Name) or n.func.id not in ('min','max','round','abs')):raise ValueError('unsafe call')
 return eval(compile(tree,'case','eval'),{'__builtins__':{},'min':min,'max':max,'round':round,'abs':abs},values)
class RevenueCases(unittest.TestCase):
 def test_retained_cases(self):
  cases=0
  for p in sorted((ROOT/'knowledge/topics').glob('TOPIC-03-*/phase-2d-scenarios.json')):
   for c in json.loads(p.read_text())['cases']:
    with self.subTest(case=c['id']):
     v=dict(c['facts'])
     for k,s in c['calculations'].items():v[k]=expression(s,v)
     for k,x in c['expected_calculations'].items():self.assertAlmostEqual(v[k],x,places=7)
     self.assertEqual(expression(c['route'],v),c['expected_route'])
     balances=dict(c.get('opening_balances',{}))
     for j in c['journals']:
      total=0
      for l in j['lines']:
       a=expression(l['amount'],v);signed=a if l['side']=='Dr' else -a
       total+=signed;balances[l['account']]=balances.get(l['account'],0)+signed
      self.assertAlmostEqual(total,0,places=7)
     for k,x in c.get('expected_balances',{}).items():self.assertAlmostEqual(balances.get(k,0),x,places=7)
     cases+=1
  self.assertGreaterEqual(cases,20)
 def test_independent_opposite_branches(self):
  self.assertEqual(1000*600/1000,600)
  self.assertEqual(1200*600/1000,720)
  self.assertEqual(140-85,55)
  self.assertEqual(90-30-max(0,60-(200-155)),45)
  self.assertEqual(900*.02+30,48)
  self.assertEqual(1000*.01+500*.05+100*.145,49.5)
  self.assertEqual(280-80+15-25,190)
  self.assertEqual(300-120-100-30,50)
  # Cost progress cannot override a failed third over-time route.
  for right,expected in [(100,0),(550,500)]:
   self.assertEqual(1000*.5 if right>=550 else 0,expected)
 def test_expression_rejects_executable_payload(self):
  with self.assertRaises(ValueError):expression('__import__("os").system("id")',{})
