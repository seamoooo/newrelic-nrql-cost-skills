#!/usr/bin/env python3
"""Synthetic APM event/metric counterexamples; does not execute NRQL."""
import sqlite3
import unittest


class AgentSemantics(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        self.addCleanup(self.db.close)
        self.db.executescript("""
            CREATE TABLE transactions(id, app, seconds, error);
            INSERT INTO transactions VALUES ('a','prod',0.2,0), ('b','prod',0.8,1), ('c','staging',2.0,1);
            CREATE TABLE metric_points(observations, seconds_sum, errors);
            INSERT INTO metric_points VALUES (90,18.0,0), (10,8.0,10);
            CREATE TABLE error_events(transaction_id);
            INSERT INTO error_events VALUES ('b'), ('b');
        """)

    def test_events_and_metrics_are_different_populations(self):
        events = self.db.execute("SELECT COUNT(*),AVG(seconds) FROM transactions WHERE app='prod'").fetchone()
        metrics = self.db.execute('SELECT SUM(observations),SUM(seconds_sum)/SUM(observations) FROM metric_points').fetchone()
        self.assertEqual(events, (2,0.5))
        self.assertEqual(metrics, (100,0.26))

    def test_error_events_are_not_unique_error_transactions(self):
        records = self.db.execute('SELECT COUNT(*) FROM error_events').fetchone()[0]
        requests = self.db.execute("SELECT COUNT(*) FROM transactions WHERE app='prod' AND error=1").fetchone()[0]
        self.assertEqual((records,requests), (2,1))

    def test_metric_point_count_is_not_request_count(self):
        self.assertEqual(self.db.execute('SELECT COUNT(*),SUM(observations),SUM(errors)*100.0/SUM(observations) FROM metric_points').fetchone(), (2,100,10.0))


if __name__ == '__main__':
    unittest.main(verbosity=2)
