import sys
import os
from collections import defaultdict, deque

import sys
import os 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'onetjobsInf')))

# Import necessary modules
from OnetWebService import OnetWebService
from onet_credentials import get_credentials
from bfs_knowledge_search import get_knowledge, extract_knowledge_ids

def load_job_ids_from_file(file_path):
    """
    Load job IDs from the Occupation Data.txt file.
    
    Args:
        file_path (str): Path to the Occupation Data.txt file
        
    Returns:
        list: List of job IDs
    """
    job_ids = []
    try:
        with open(file_path, 'r') as file:
            # Skip header line
            next(file)
            for line in file:
                parts = line.strip().split('\t')
                if parts and len(parts) > 0:
                    job_id = parts[0].strip()
                    if job_id:
                        job_ids.append(job_id)
        print(f"Loaded {len(job_ids)} job IDs from {file_path}")
        return job_ids
    except Exception as e:
        print(f"Error loading job IDs from file: {str(e)}")
        return []

class JobKnowledgeNetwork:
    def __init__(self):
        # Get credentials and initialize the O*NET service
        username, password = get_credentials()
        self.onet_service = OnetWebService(username, password)
        
        # Initialize dictionaries to store job-knowledge and knowledge-job mappings
        self.job_to_knowledge = defaultdict(set)
        self.knowledge_to_jobs = defaultdict(set)
        
        # Cache for already queried jobs to avoid redundant API calls
        self.queried_jobs = set()
        
        # Load all available job IDs
        data_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                               'onetjobsInf/src_data/Occupation Data.txt')
        self.all_job_ids = load_job_ids_from_file(data_file)
    
    def get_job_knowledge(self, job_id):
        # Check if we've already queried this job
        if job_id in self.queried_jobs:
            return self.job_to_knowledge[job_id]
        
        # Get the knowledge data and extract knowledge IDs using the API
        try:
            knowledge_data = get_knowledge(self.onet_service, job_id)
            if not knowledge_data:
                self.queried_jobs.add(job_id)
                return set()
            
            knowledge_ids = extract_knowledge_ids(knowledge_data)
            
            # Update the mappings
            self.job_to_knowledge[job_id] = set(knowledge_ids)
            for knowledge_id in knowledge_ids:
                self.knowledge_to_jobs[knowledge_id].add(job_id)
            
            # Mark this job as queried
            self.queried_jobs.add(job_id)
            
            return set(knowledge_ids)
        except Exception as e:
            print(f"Error getting knowledge for job {job_id}: {str(e)}")
            self.queried_jobs.add(job_id)
            return set()
    
    def explore_job_knowledge_network(self, initial_job_id, similarity_threshold, max_jobs=None):
        # Get knowledge for the initial job
        try:
            current_knowledge_set = self.get_job_knowledge(initial_job_id)
            if not current_knowledge_set:
                print(f"Warning: No knowledge found for job {initial_job_id}")
                return set(), set()
        except Exception as e:
            print(f"Error retrieving knowledge for initial job {initial_job_id}: {str(e)}")
            return set(), set()
        
        # Print original job ID and knowledge
        print("\n" + "="*50)
        print(f"ORIGINAL JOB: {initial_job_id}")
        print(f"ORIGINAL KNOWLEDGE ({len(current_knowledge_set)}):")
        for knowledge in sorted(current_knowledge_set):
            print(f"  - {knowledge}")
        print("="*50 + "\n")
        
        # Initialize sets to track all found jobs and knowledge
        all_jobs = {initial_job_id}
        all_knowledge = set(current_knowledge_set)
        
        # Initialize BFS queue
        queue = deque([(initial_job_id, current_knowledge_set)])
        
        while queue:
            job_id, job_knowledge = queue.popleft()
            print(f"Exploring job {job_id} with {len(job_knowledge)} knowledge areas")
            
            # Stop if we've reached the maximum number of jobs (if specified)
            if max_jobs and len(all_jobs) >= max_jobs:
                print(f"Reached maximum number of jobs ({max_jobs}), stopping")
                break
            
            # Use ALL job IDs from the occupation data file as candidates
            candidate_jobs = [jid for jid in self.all_job_ids if jid not in all_jobs]
            print(f"Evaluating {len(candidate_jobs)} candidate jobs from occupation data")
            
            # Track jobs that meet the similarity threshold
            similar_jobs = []
            
            # Evaluate each candidate job for similarity
            for candidate_job_id in candidate_jobs:
                try:
                    # Get knowledge for this job
                    candidate_job_knowledge = self.get_job_knowledge(candidate_job_id)
                    
                    # Skip jobs with no knowledge data
                    if not candidate_job_knowledge:
                        continue
                    
                    # Calculate similarity based on knowledge overlap
                    overlap = len(candidate_job_knowledge.intersection(job_knowledge))
                    similarity = overlap / len(job_knowledge) if job_knowledge else 0
                    
                    if similarity >= similarity_threshold:
                        similar_jobs.append((candidate_job_id, similarity, candidate_job_knowledge))
                        print(f"Found similar job {candidate_job_id} with {similarity:.2f} similarity ({overlap}/{len(job_knowledge)} knowledge areas)")
                        
                        if max_jobs and len(all_jobs) + len(similar_jobs) >= max_jobs:
                            break
                except Exception as e:
                    print(f"Error processing job {candidate_job_id}: {str(e)}. Continuing with next job.")
                    continue
            
            similar_jobs.sort(key=lambda x: x[1], reverse=True)
            
            if not similar_jobs:
                print(f"No new similar jobs found for job {job_id}, moving to next job in queue")
                continue
            
            new_jobs_added = 0
            new_knowledge_added = 0
            
            for candidate_job_id, similarity, candidate_job_knowledge in similar_jobs:
                all_jobs.add(candidate_job_id)
                new_jobs_added += 1
                
                new_knowledge = candidate_job_knowledge - all_knowledge
                if new_knowledge:
                    all_knowledge.update(new_knowledge)
                    new_knowledge_added += len(new_knowledge)
                    print(f"  Added {len(new_knowledge)} new knowledge areas from job {candidate_job_id}")
                
                queue.append((candidate_job_id, candidate_job_knowledge))
                
                if max_jobs and len(all_jobs) >= max_jobs:
                    break
            
            print(f"Iteration complete: Added {new_jobs_added} jobs and {new_knowledge_added} knowledge areas")
            
            if new_knowledge_added == 0:
                print("No new knowledge areas found, stopping search")
                break
        
        print("\n" + "="*50)
        print(f"FINAL JOB LIST ({len(all_jobs)}):")
        for job in sorted(all_jobs):
            print(f"  - {job}")
        print(f"\nFINAL KNOWLEDGE LIST ({len(all_knowledge)}):")
        for knowledge in sorted(all_knowledge):
            print(f"  - {knowledge}")
        print("="*50 + "\n")
        
        return all_jobs, all_knowledge


if __name__ == "__main__":
    DEFAULT_JOB_ID = "29-2099.01"
    
    print(f"Initializing Job Knowledge Network...")
    network = JobKnowledgeNetwork()
    
    job_id = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_JOB_ID
    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 0.75
    max_jobs = int(sys.argv[3]) if len(sys.argv) > 3 else None
    
    try:
        print(f"Exploring job knowledge network for job ID: {job_id}, similarity threshold: {threshold}")
        related_jobs, all_knowledge = network.explore_job_knowledge_network(job_id, similarity_threshold=threshold, max_jobs=max_jobs)
        
        print(f"Exploration complete. Found {len(related_jobs)} related jobs and {len(all_knowledge)} knowledge areas.")
    except Exception as e:
        print(f"ERROR: {str(e)}")
        print("Script completed with errors, but did not crash.")
