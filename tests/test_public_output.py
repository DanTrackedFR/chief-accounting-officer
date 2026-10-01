import unittest
from interfaces.public_output import ROUTES, public_record, serialize_public

class PublicBoundaryTests(unittest.TestCase):
    def test_all_routes_both_note_formats_preserve_caveats(self):
        for route in ROUTES:
            for note in ('Source: FRC FRS 102', 'Source: ChatGPT training data'):
                with self.subTest(route=route, note=note):
                    payload = {'guidance': 'Assess the contract before measuring the liability.',
                               'effective_period': 'Periods beginning on or after 1 January 2026.',
                               'limitations': ['Historical periods require the earlier requirements.'],
                               'uncertainties': ['An unresolved legal judgment needs specialist review.'],
                               'source_note': note, 'evidence_status': 'MODEL_DERIVED_AUDIT_REQUIRED',
                               'audit_required': True, 'approval_track': 'TRAINING_DATA_CHECKED',
                               'approval_review': {'reviewer': 'internal reviewer'},
                               'claims': [{'proposition': note}], 'raw_markdown': note,
                               'citations': [{'title': 'FRS 102', 'url': 'https://www.frc.org.uk/',
                                              'source_note': note, 'reviewer': 'internal reviewer'}]}
                    output = serialize_public(payload, route=route)
                    for forbidden in (note, 'internal reviewer', 'audit_required', 'approval_track',
                                      'evidence_status', 'source_note', 'raw_markdown', 'claims'):
                        self.assertNotIn(forbidden, output)
                    self.assertIn('earlier requirements', output)
                    self.assertIn('unresolved legal judgment', output)
                    self.assertIn('1 January 2026', output)
    def test_embedded_notes_fail_closed_in_every_public_field(self):
        for route in ROUTES:
            for note in ('Source: FRC FRS 102', 'Source: ChatGPT training data'):
                for payload in ({'guidance': 'Accounting guidance. '+note},
                                {'limitations': [note]}, {'citations': [{'title': note}]}):
                    with self.subTest(route=route, payload=payload):
                        with self.assertRaises(ValueError):
                            public_record(payload, route=route)
    def test_unknown_routes_and_nested_content_fail_closed(self):
        for payload in ({'guidance': {'source_note': 'Source: private'}},
                        {'limitations': 'Not a list'}, {'citations': ['raw source']}):
            with self.assertRaises(ValueError):
                public_record(payload, route='answer')
        with self.assertRaises(ValueError):
            public_record({}, route='new_unreviewed_export')

if __name__ == '__main__':
    unittest.main()
