import os
import unittest
from dotenv import load_dotenv
from agent import agent, build_graph

# Garante que o .env seja carregado antes de rodar os testes
load_dotenv()

class TestTravelAgent(unittest.TestCase):

    def setUp(self):
        if "GOOGLE_API_KEY" not in os.environ:
            self.skipTest("GOOGLE_API_KEY não está configurada no ambiente ou no arquivo .env.")

    def test_empty_request_returns_failure(self):
        """Spec: 'Se a entrada da solicitação estiver vazia, o status retornado deve ser failure'"""
        response = agent("")
        self.assertEqual(response["status"], "failure")
        self.assertIsNone(response["destination"])
        self.assertEqual(response["activities"], [])

    def test_build_graph_returns_compiled_graph(self):
        """Spec: 'OBRIGATORIAMENTE construir um StateGraph... retornando CompiledGraph'"""
        from langgraph.graph.state import CompiledStateGraph
        graph = build_graph()
        self.assertIsInstance(graph, CompiledStateGraph)

    def test_valid_request_execution(self):
        """Spec: Fluxo feliz validando esquema e restrições."""
        request = "Plan a 3-day trip to Rome focusing on history and gastronomy."
        response = agent(request)
        
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["destination"].lower(), "rome")
        self.assertEqual(response["duration_days"], 3)
        self.assertIsInstance(response["interests"], list)
        
        activities = response["activities"]
        self.assertGreaterEqual(len(activities), 3)
        
        days_present = [act["day"] for act in activities]
        self.assertIn(1, days_present)
        self.assertIn(2, days_present)
        self.assertIn(3, days_present)
        
        for act in activities:
            self.assertIsInstance(act["activity"], str)
            self.assertTrue(len(act["activity"].strip()) > 0)

if __name__ == "__main__":
    unittest.main()