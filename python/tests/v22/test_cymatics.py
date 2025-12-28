import unittest
import numpy as np
from irh.core.v22.cymatics import CymaticResonanceNetwork, ResonantNode

class TestCymatics(unittest.TestCase):
    
    def test_resonant_node_phase_update(self):
        node = ResonantNode(id=0, frequency=1.0, phase=0.0)
        dt = 0.1
        node.update_phase(dt)
        
        expected_phase = 0.1
        self.assertAlmostEqual(node.phase, expected_phase)
        self.assertAlmostEqual(node.state, np.exp(1j * expected_phase))
        
    def test_network_initialization(self):
        net = CymaticResonanceNetwork(num_nodes=50)
        self.assertEqual(len(net.nodes), 50)
        self.assertEqual(net.coupling_matrix.shape, (50, 50))
        
    def test_collective_wavefunction(self):
        net = CymaticResonanceNetwork(num_nodes=10)
        psi = net.get_collective_wavefunction()
        
        self.assertEqual(len(psi), 10)
        self.assertTrue(np.iscomplexobj(psi))
        
    def test_spectral_stability_check(self):
        net = CymaticResonanceNetwork(num_nodes=10)
        # Should return boolean, result depends on random init but must run
        result = net.check_spectral_stability()
        self.assertIsInstance(result, bool)

if __name__ == '__main__':
    unittest.main()
