# Stage 2 intercompany provenance resolution

Status: verified implementation identity transition; no accounting correction.

The historical baseline commit `ea19ee62c938dba06f3faf758a75e17a7da27e15` reproduces all nine original published artifacts exactly. Complete worker archives bridge receipt and reclose evidence omitted by the original slim proof. The final review covers 28 authority records plus 11 subprocess exit witnesses, with ten complete worker archives and zero discrepancies.

## Concrete native owner anchor

Stable node: `exec:intercompany-accounting:GROUP-EUR:1cb88b781cbd7d2c092710cecc925084c419bee55dd11883b659093b16724b36`

| Identity | Historical | Current |
|---|---|---|
| version_id | `version:0676d4e2e6dffa6ad9f00e57f0196cd1d7ef045ab1b9ce85a5b2adafed382b6e` | `version:415d829120b07fe7cf1d273ee82f117507c4c2c7789533b003542614c0126e6a` |
| predecessor | `version:5806957c2cf1ab70ee93447b5e8e90a7047b5acfa15604143908a0ef654c961c` | `version:cd9fd1319e0ac50d2fbc7a034fdf8733c285c4fa69cfa83bcfa9f6e949d4a3a1` |
| result_id | `result:98857c1a0daafbf5c3aba01d65bfae1a99a3893d6bbb8dbc7cbbee5d76a72f05` | `result:98857c1a0daafbf5c3aba01d65bfae1a99a3893d6bbb8dbc7cbbee5d76a72f05` |
| source_fingerprint | `a184d681cc79ef2049c47a048a0a4915eec7ec1d4993b3365079681950b80a87` | `419239211d34e1d4d4ece04c2b3ea77a801c9b352562756d50452bfd2624bbaa` |
| exact_case_fingerprint | `f8c70266da3949cba7114faee4c2e2e8e082f759b09eb56fe490366568b35401` | `11c97a46a7e476839480ba01d158355fc433a2619ab8d32c9f41565998d3a433` |
| result_fingerprint | `eb639e9d8c4760e4f3cd543d2d2aebe48fa1670e66387d6604f0ba1030b2104c` | `3db0e35e2324ade3457b30aee3839d87f63d9935854f44c69958ea87c39da83f` |

The review anchors each version by the same native node and predecessor depth, then validates every source, result, receipt and dependency leaf through a single bijective identity map. Equal accounting amounts alone cannot authorize a producer substitution. Hash-sorted inventories retain exactly the same membership; ordered version, Case and operation histories remain ordered.

Classification: stale global implementation fingerprint coupling and incomplete slim provenance evidence. No historical error or accounting-governance regression was established. Current reference versions are separate, explicitly bound to original and current bytes. Original references and both full archive histories are preserved.

Independent checks: pre-existing independently authored Stage 2 recovery behavior suite (21 tests) passes. Adversarial qualification rejects wrong receipts, split/collapsed identities, money, population and status changes. The release regression also reexecutes authored and independently authored durable scenarios; its final status is recorded separately.


## Accounting anchor

The `fx` pair in the concrete GROUP-EUR owner result retains foreign principal `20`, A functional value `18.00`, B functional value `18.00`, A FX gain `0.00`, B FX loss `0.00` and recharges `0`. Its journal entity population and journal entry implications remain empty. Every other accounting leaf and owner/dependency binding is checked by the same expanded archive comparison; these amounts are not used to infer or authorize a replacement producer.

Direct historical compatibility check: the current runtime restores and exactly resnapshots the complete original Stage 2 worker checkpoints, including late reclose and repeat authorities. A separate check also restores 12 distinct untouched original published Stage 2/4 checkpoints. Transport hashes are checked before typed native decoding; current migrated references are not used for these checks. Logs: `original-stage2-worker-restoration.log` and `original-checkpoint-restoration.log`.
