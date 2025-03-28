import sys
import os
import unittest

file_path = os.path.join(os.path.dirname(__file__), "..", "src_data", "Occupation Data.txt")
from onetjobsInf.bfs_job_abilities_graph import JobAbilitiesNetwork
from onetjobsInf.bfs_job_knowledge_graph import JobKnowledgeNetwork
from onetjobsInf.bfs_job_skills_graph import JobSkillsNetwork

class TestJobAbilitiesNetwork(unittest.TestCase):
    def setUp(self):
        self.network = JobAbilitiesNetwork()
    
    def test_get_job_abilities(self):
        job_id = "29-2099.01"
        abilities = self.network.get_job_abilities(job_id)
        self.assertIsInstance(abilities, set)
    
    def test_explore_job_abilities_network(self):
        job_id = "29-2099.01"
        jobs, abilities = self.network.explore_job_abilities_network(job_id, 
                                                                     similarity_threshold=0.75, 
                                                                     max_jobs=None)
        self.assertIsInstance(jobs, set)
        self.assertIsInstance(abilities, set)

class TestJobKnowledgeNetwork(unittest.TestCase):
    def setUp(self):
        self.network = JobKnowledgeNetwork()
    
    def test_get_job_knowledge(self):
        job_id = "29-2099.01"
        knowledge = self.network.get_job_knowledge(job_id)
        self.assertIsInstance(knowledge, set)
    
    def test_explore_job_knowledge_network(self):
        job_id = "29-2099.01"
        jobs, knowledge = self.network.explore_job_knowledge_network(job_id, 
                                                                     similarity_threshold=0.75, 
                                                                     max_jobs=None)
        self.assertIsInstance(jobs, set)
        self.assertIsInstance(knowledge, set)

class TestJobSkillsNetwork(unittest.TestCase):
    def setUp(self):
        self.network = JobSkillsNetwork()
    
    def test_get_job_skills(self):
        job_id = "29-2099.01"
        skills = self.network.get_job_skills(job_id)
        self.assertIsInstance(skills, set)
    
    def test_explore_job_skills_network(self):
        job_id = "29-2099.01"
        jobs, skills = self.network.explore_job_skills_network(job_id, 
                                                               similarity_threshold=0.75, 
                                                               max_jobs=None)
        self.assertIsInstance(jobs, set)
        self.assertIsInstance(skills, set)

if __name__ == '__main__':
    unittest.main()
