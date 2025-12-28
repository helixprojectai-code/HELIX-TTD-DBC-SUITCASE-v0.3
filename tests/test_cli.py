import unittest
import json
import os
import shutil
from pathlib import Path
from helix import HelixCLI

class TestHelixCore(unittest.TestCase):
    def setUp(self):
        self.cli = HelixCLI()
        self.test_dir = "test_output"
        self.custodian = "test_custodian_key"
        self.agent = "Unit_Test_Bot"
        # Clean start
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)

    def tearDown(self):
        # Cleanup
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_end_to_end_lifecycle(self):
        """Test the full lifecycle: Birth -> Verify -> Update"""
        
        # 1. Create
        result = self.cli.create_new_agent(self.custodian, self.agent, self.test_dir)
        self.assertIsNotNone(result, "Agent creation failed")
        
        paths = result['paths']
        self.assertTrue(os.path.exists(paths['dbc']), "DBC file not created")
        self.assertTrue(os.path.exists(paths['suitcase']), "Suitcase file not created")

        # 2. Verify
        verify_res = self.cli.verify_agent(str(paths['dbc']), str(paths['suitcase']))
        self.assertTrue(verify_res['dbc_valid'], "DBC verification failed")
        self.assertTrue(verify_res['chain_valid'], "Chain verification failed")

        # 3. Update State
        update_res = self.cli.update_agent_state(
            str(paths['dbc']), 
            str(paths['suitcase']), 
            "ACTIVE", 
            "Unit Test Activation"
        )
        self.assertIsNotNone(update_res, "State update failed")
        self.assertEqual(update_res['details']['to'], "ACTIVE")

if __name__ == '__main__':
    unittest.main()
