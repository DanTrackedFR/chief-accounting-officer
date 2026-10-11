# Build 4 deterministic proof and reproduction

From the frozen source tree, install intelligence/requirements.txt and reportlab,
then run Python3.12+ on POSIX:

```sh
PYTHONHASHSEED=283 python -m build4.prove_integrated > /tmp/build4-283.json
PYTHONHASHSEED=1709 python -m build4.prove_integrated > /tmp/build4-1709.json
cmp build4/release/integrated-proof.json /tmp/build4-283.json
cmp /tmp/build4-283.json /tmp/build4-1709.json
PYTHONHASHSEED=283 python -m build4.prove_memory > /tmp/memory-283.json
PYTHONHASHSEED=1709 python -m build4.prove_memory > /tmp/memory-1709.json
cmp build4/release/memory-proof.json /tmp/memory-283.json
cmp /tmp/memory-283.json /tmp/memory-1709.json
python -m build4.verify_release
```

Seeds283/1709 were independently selected by the accounting reviewer. Both modules
create new temporary databases and actual CLI subprocesses. Controlled interpretation
is not a live model. Review packs/governance remain explicitly synthetic.

Integrated proof retains original source bytes/identities/hashes, complete reviewed
inputs, expected/actual economics, Case/Scope/Period/owner identities, source snapshots,
exact result versions/receipts and correction/rework history. Boreal price42,000,
SSP30,000:20,000 and40% service satisfaction produce25,200+6,720=31,920; reviewed
price45,000 produces27,000+7,200=34,200. Original immutable versions survive.

Prepayment comparative3,000/current18,750 yield15,750 increase. The actual compliance
row discovers BC-20481 and preserves−100 unexplained residual. Invoice18,000/24months
cannot establish qualified allocation; final accounting legitimately BLOCKED.

Three actual repeated revenue owners use NL IFRS/EUR2026, US US_GAAP/USD2026 with
EUR presentation dimension, and NL2027. Separate Scope/Period/source/result identities
and typed Group conflict Cases are retained. No unsupported USD→EUR conversion or
Group receipt substitution is fabricated. This is bounded facade integration; existing
native full Group/multi-period flagships are separately required regression population.

The memory proof distinguishes native governance setup from client execution, retains
source-backed historical position/version/USE lineage, foreign-entity exclusion and
fresh CLI continuation before/after correction. New policy source/supersession tests
prove native policy reuse without replacing Revenue Recognition qualification.

Historical inventory contains1,848 baseline artifact files. All must remain byte
identical. No historical reference regenerated. Preliminary failed attempts and
old new-proof seed receipts remain preserved and are not final release claims.
Final hashes are authoritative in proof-seeds.json, artifact-inventory.json and
accepted-release.json; verify_release is read-only and never repairs a reference.
