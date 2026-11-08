# Mandatory population verification

Reviewed frozen source `6b36ae0d9bb942ec4eacc199e59c099c4cc01133` and both genuine Actions archives. The current ZIP digest is `2d377c812a6df2c9bfb37bcdf9f2599937a6950852bc1bf8c59af3a933f14a61` (artifact 13633904464). The previous ZIP digest is `934a08ace3842f754b0ade43b9cee7a10083777a9e39c6ab8e3c79cf95e5d31f` (artifact 13613496888). Each matches GitHub metadata.

The reviewer matched each of 4,012 unique verbose unittest success lines to the exact qualified identity in its suite or orchestration shard. The 23 top-level sidecars, full manifest and discovery document agree by identity. No duplicates, skips, unexecuted methods, method errors, failures or suite setup/teardown errors appeared. All 23 suite outcomes report success.

| Population | Identities found executed and passed |
|---|---:|
| Previous discovery, from failed artifact | 4,011 / 4,011 |
| New governance control | 1 / 1 |
| Frozen historical remediation contract | 63 / 63 |
| Frozen Phase A corrections contract | 55 / 55 |
| Prior dedicated infrastructure suite | 16 / 16 |
| Earlier assertion failures | 4 / 4 |
| Earlier method error | 1 / 1 |
| Earlier setup-blocked methods | 28 / 28 |

The added identity is `tests::test_presumed_population_dispatch.ProductionPopulationDispatch.test_missing_outcome_dependency_refused_before_execution`. The 33 earlier affected identities match the frozen prior investigation TSV in identity and failure category. The earlier artifact recorded 4,011 discovered and scheduled, 3,983 actual executions and 3,978 passes. The recovery comparison preserves this distinction. Group membership and source hashes appear in mandatory.json. Each row describes coverage within the same 4,012-method population.
