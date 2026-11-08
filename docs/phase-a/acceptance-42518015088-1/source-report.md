# Frozen source, deterministic proof and preservation review

The genuine ZIP for artifact 13633904464 contains the source and input sidecars for run 42518015088 attempt 1. Its SHA-256 is `2d377c812a6df2c9bfb37bcdf9f2599937a6950852bc1bf8c59af3a933f14a61`. Both sidecars match the final manifest maps and the independent calculations below.

| Independent checkout | Commit | Git tree |
| --- | --- | --- |
| Tested | `6b36ae0d9bb942ec4eacc199e59c099c4cc01133` | `608963d0d7bc1028f2eeecdd11f2264ad0efd095` |
| Reviewed | `3c63a3a2b95df7907f547e8de64c7c68cf963910` | `0d96b2fc0b3a43b1664087fb6900c2808ff6d0ce` |

In each detached checkout, the production source and execution-input enumerators reproduced the same paths and bytes as the genuine artifact. `verify_source_binding` checked the mapped blobs against each respective Git tree. The complete 23-slot production gate plan matched the manifest for the hosted attempt. Six handoff files under `docs/phase-a/governance-remediation-42466932475/` account for the whole diff between the independent review and tested commits. Each lies outside both maps. The governance-remediation range from investigation commit 14c118c6 changes tests, fixture infrastructure, the proof selector, its governed successor contract and handoff evidence. It contains no accounting production implementation changes.

| Hosted sidecar | Paths | SHA-256 of original bytes |
| --- | ---: | --- |
| start-source-hashes.json | 464 | `ee95c7b3b25846fc1d3565071aa8f4ee3230c59607dd9ca1a5c4c7e01090ce3b` |
| start-input-hashes.json | 2,745 | `052556cede9067620fbd1e13049ca433feb22d28e18d083e3a00e93fecf5fd03` |

## Source-bound proof

The frozen workflow runs two real HTTP proofs with seeds 109 and 971, selects the governed successor and compares their output. Both seeds were executed again in a disposable frozen checkout. Both produced exactly the versioned `phase-a-v1/http-proof.json` bytes, SHA-256 `b973931977a198aced1c01ce2d3eb9013892a7f9c87114049e46714a488eef5d`. The selector validates the historical proof at `be06ab1a1ee247bc24159f7ad605eb30c1dc70fccb13c864b50a9da25e88bcb7`, the original Phase A contract and its pinned governance source amendment. The separate missing/stale/tampered proof and contract control passed in this checkout. Arithmetic agrees with 27 assets at cost 648,000, depreciation 64,800 and closing accumulated depreciation 64,800, and ten invoices totalling 1,550. Both packages had identical restart and idempotent-retry results. These are synthetic files.

## Preservation

Production `verify_historical()` passed on both trees under ordinary Python. Its 8,912 entries comprise 8,910 unchanged active originals and two archived originals with exact active successors for the orchestration workflow and hosted documentation. The governed accepted-main contract separately verified 7,963 original Git blob hashes, with 7,959 active originals and four archived originals with pinned successor hashes. These populations overlap and must not be added. The four accepted-main migrations govern the focused receipt issuer, release population, runner and verifier. The contract pins hashes and paths for these four entries. Historical receipts, proofs and releases covered by these contracts retain their original bytes. The failed-run investigation directory is the identical Git tree `c2d8d96c3ab14a0870b6916ccc7eb763efe08e80` at its publication commit 14c118c6 and at the frozen tested head.

## Bound workflow and release programs

| Path | SHA-256 |
| --- | --- |
| `.github/workflows/cao-presumed-sources.yml` | `09b7b7ede1545e74d055f6c3f117205fe60abd314226a08df3c79c1148a41fdc` |
| `skills/presumed-sources/execute_release.py` | `cb64d024015bdb5c97c4c128326b80ffa1d7eec68c8143ef0fc29872765dfbc0` |
| `skills/presumed-sources/run_release.py` | `f526ae84df74908e92ab8589d5f3fb8a7cb981c40cb06ba2711621ef3113fbe6` |
| `skills/presumed-sources/suite_runner.py` | `bf581a91aa3a5791d0bf2e61342e31944fd5154d6805038e57efa4c038aae63e` |
| `skills/presumed-sources/verify_release.py` | `f8dd854a490886c93db6cd82f74d339798a0c528deff3954bcea476f60a7f302` |
| `build4/verify_release.py` | `169b87306c6bfdeef8b5bc367464eb6e4ef7ad98b8c2dc825fc15fe02464f308` |
| `skills/presumed-sources/proof_selection.py` | `19dbe5411bdb03dd33d4247b38ee6d68732318229680c1d53fad1e59f14a9c5b` |
| `skills/presumed-sources/receipt_integrity.py` | `405edb2e8503f0dde57bfdea099ca96b5b084268900c166a630b5f4aa0b71acf` |

The source, proof and preservation checks support receipt review for this specific tested tree. This report does not itself issue or accept a receipt.
