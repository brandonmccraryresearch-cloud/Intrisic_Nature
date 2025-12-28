import unittest
from irh.verification import theoretical_reference, get_transparency_engine, UncertaintyValue

class TestVerificationInfrastructure(unittest.TestCase):
    
    def test_theoretical_reference_decorator(self):
        @theoretical_reference("Test Manuscript", "Eq. 1.0", "Test Description")
        def dummy_function():
            return 42
            
        self.assertTrue(hasattr(dummy_function, '_theoretical_refs'))
        ref = dummy_function._theoretical_refs[0] # type: ignore
        self.assertEqual(ref['manuscript'], "Test Manuscript")
        self.assertEqual(ref['equation'], "Eq. 1.0")
        self.assertIn("Theoretical Reference: Test Manuscript, Eq. 1.0", dummy_function.__doc__)
        
    def test_transparency_engine(self):
        engine = get_transparency_engine()
        engine.logs.clear()
        
        engine.log_theoretical_step("TestAction", "Doc1", "Eq1", {"key": "value"})
        
        self.assertEqual(len(engine.logs), 1)
        self.assertEqual(engine.logs[0].message, "Computing TestAction per Doc1, Eq1")
        self.assertEqual(engine.logs[0].context['key'], "value")
        
    def test_uncertainty_propagation(self):
        u1 = UncertaintyValue(10.0, 1.0, "SourceA")
        u2 = UncertaintyValue(20.0, 2.0, "SourceB")
        
        # Addition
        u_sum = u1 + u2
        self.assertEqual(u_sum.value, 30.0)
        # sqrt(1^2 + 2^2) = sqrt(5) approx 2.236
        self.assertAlmostEqual(u_sum.uncertainty, 2.236, places=3)
        
        # Multiplication
        u_prod = u1 * u2
        self.assertEqual(u_prod.value, 200.0)
        # Rel uncertainties: 0.1 and 0.1 -> sqrt(0.01 + 0.01) = sqrt(0.02) approx 0.1414
        # Abs uncertainty: 200 * 0.1414 = 28.28
        self.assertAlmostEqual(u_prod.uncertainty, 28.28, places=1)

if __name__ == '__main__':
    unittest.main()
