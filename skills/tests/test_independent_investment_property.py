"""Independent AI adversarial review; never an authenticated human signoff.

Baseline fingerprints were captured before Investment dispatch edits, from
merged a2c1aa35 on the reconciled branch fc109694. Runtime challenges follow
when the Investment fixture contract is available. The old captures remain
below as immutable evidence; active preservation follows owner-integrated
Grants main e753, whose separately reviewed migration supersedes a2 identities.
"""
import unittest
from borrowing_costs_cases import case as borrowing_case
from production import case_fingerprint

BASELINE_BORROWING_FINGERPRINTS = {
 'IFRS':'eadf65c022bbfc082d15a587f7af7fafc0c9be40da61a91dbb9c2aa734994de3',
 'AASB':'e44e77bf56e0645489c8fa753de48a81330d685eb82fbab76a6e4c0907a79b88',
 'US_GAAP':'6a0f0aebeffe95a1bc7d6a3372d147b7b3b80a2dd4c2bebbf4214707d7e0a9c1',
 'UK_GAAP':'feeba3d1df4116c238ef415dfcb4fc1a1d3c0b813d08b14308299950bb9fb6fb',
}
MAIN_BORROWING_FINGERPRINTS = {
 'IFRS':'d50409cffccbecd1006bdd2d88cc0c336ed16b26519d886205ad9b64c8489537',
 'AASB':'5a8b36a12258e2ddc780e49bedf0ed6216db362a316595aade1c1c20a083f5fb',
 'US_GAAP':'ef709e949183a02efe02584ba90c07c3292f56f062d2607194821222fb3839fe',
 'UK_GAAP':'dc8ddeebd6f60b9da15123ec5d05dbc9a1cc5be18bcec7d6603c812500777625',
}

class IndependentHistoricalIntegrity(unittest.TestCase):
 def test_merged_borrowing_case_fingerprints_preserved(self):
  for framework, expected in MAIN_BORROWING_FINGERPRINTS.items():
   with self.subTest(framework=framework):
    self.assertEqual(expected, case_fingerprint(borrowing_case(framework)))

if __name__ == '__main__': unittest.main()
