import unittest
import numpy as np
from irh.core.v22.cancellation import SymplecticCancellation

class TestSymplecticCancellation(unittest.TestCase):
    
    def test_cancellation_planar_vs_nonplanar(self):
        verifier = SymplecticCancellation()
        
        # Genus 0 (Planar) should NOT cancel
        is_cancelled_planar = verifier.verify_cancellation(genus=0)
        self.assertFalse(is_cancelled_planar)
        
        # Genus 1 (Non-planar) should cancel (statistically)
        # Using enough samples to be reliable
        is_cancelled_nonplanar = verifier.verify_cancellation(genus=1, num_samples=10000)
        self.assertTrue(is_cancelled_nonplanar)
        
    def test_beta_function_logging(self):
        verifier = SymplecticCancellation()
        # Just ensure it runs and logs
        verifier.verify_exact_beta_functions(lambda_tilde=17.55)
        
        # Check logs via transparency engine
        from irh.verification import get_transparency_engine
        engine = get_transparency_engine()
        
        found_log = False
        for log in engine.logs:
            if "Verify Exact Beta Function" in log.message:
                found_log = True
                self.assertIn("beta_lambda", log.context)
                break
        self.assertTrue(found_log)

if __name__ == '__main__':
    unittest.main()
