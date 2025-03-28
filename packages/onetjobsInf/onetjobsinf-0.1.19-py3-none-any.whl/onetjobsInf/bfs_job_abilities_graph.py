import sys
import os
from collections import defaultdict, deque

# Add the Scaffolding directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'onetjobsInf')))

# Import necessary modules
from OnetWebService import OnetWebService
from onet_credentials import get_credentials
from bfs_abilities_search import get_abilities, extract_ability_ids

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

class JobAbilitiesNetwork:
    def __init__(self):
        # Get credentials and initialize the O*NET service
        username, password = get_credentials()
        self.onet_service = OnetWebService(username, password)
        
        # Initialize dictionaries to store job-abilities and abilities-job mappings
        self.job_to_abilities = defaultdict(set)
        self.ability_to_jobs = defaultdict(set)
        
        # Cache for already queried jobs to avoid redundant API calls
        self.queried_jobs = set()
        
        # Load all available job IDs
        data_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                               'onetjobsInf/src_data/Occupation Data.txt')
        self.all_job_ids = load_job_ids_from_file(data_file)
    
    def get_job_abilities(self, job_id):
        # Check if we've already queried this job
        if job_id in self.queried_jobs:
            return self.job_to_abilities[job_id]
        
        # Get the abilities data and extract ability IDs using the API
        try:
            abilities_data = get_abilities(self.onet_service, job_id)
            if not abilities_data:
                self.queried_jobs.add(job_id)
                return set()
            
            ability_ids = extract_ability_ids(abilities_data)
            
            # Update the mappings
            self.job_to_abilities[job_id] = set(ability_ids)
            for ability_id in ability_ids:
                self.ability_to_jobs[ability_id].add(job_id)
            
            # Mark this job as queried
            self.queried_jobs.add(job_id)
            
            return set(ability_ids)
        except Exception as e:
            print(f"Error getting abilities for job {job_id}: {str(e)}")
            self.queried_jobs.add(job_id)
            return set()
    
    def explore_job_abilities_network(self, initial_job_id, similarity_threshold, max_jobs=None):
        # Get abilities for the initial job
        print("RUNNING JOB ABILITIES NETWORK EXPLORATION")
        try:
            current_ability_set = self.get_job_abilities(initial_job_id)
            if not current_ability_set:
                print(f"Warning: No abilities found for job {initial_job_id}")
                return set(), set()
        except Exception as e:
            print(f"Error retrieving abilities for initial job {initial_job_id}: {str(e)}")
            return set(), set()
        
        # Print original job ID and abilities
        print("\n" + "="*50)
        print(f"ORIGINAL JOB: {initial_job_id}")
        print(f"ORIGINAL ABILITIES ({len(current_ability_set)}):")
        for ability in sorted(current_ability_set):
            print(f"  - {ability}")
        print("="*50 + "\n")
        
        # Initialize sets to track all found jobs and abilities
        all_jobs = {initial_job_id}
        all_abilities = set(current_ability_set)
        
        # Initialize BFS queue
        queue = deque([(initial_job_id, current_ability_set)])
        
        while queue:
            job_id, job_abilities = queue.popleft()
            print(f"Exploring job {job_id} with {len(job_abilities)} abilities")
            
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
                    # Get abilities for this job
                    candidate_job_abilities = self.get_job_abilities(candidate_job_id)
                    
                    # Skip jobs with no abilities data
                    if not candidate_job_abilities:
                        continue
                    
                    # Calculate similarity based on ability overlap
                    overlap = len(candidate_job_abilities.intersection(job_abilities))
                    similarity = overlap / len(job_abilities) if job_abilities else 0
                    
                    if similarity >= similarity_threshold:
                        similar_jobs.append((candidate_job_id, similarity, candidate_job_abilities))
                        print(f"Found similar job {candidate_job_id} with {similarity:.2f} similarity ({overlap}/{len(job_abilities)} abilities)")
                        
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
            new_abilities_added = 0
            
            for candidate_job_id, similarity, candidate_job_abilities in similar_jobs:
                all_jobs.add(candidate_job_id)
                new_jobs_added += 1
                
                new_abilities = candidate_job_abilities - all_abilities
                if new_abilities:
                    all_abilities.update(new_abilities)
                    new_abilities_added += len(new_abilities)
                    print(f"  Added {len(new_abilities)} new abilities from job {candidate_job_id}")
                
                queue.append((candidate_job_id, candidate_job_abilities))
                
                if max_jobs and len(all_jobs) >= max_jobs:
                    break
            
            print(f"Iteration complete: Added {new_jobs_added} jobs and {new_abilities_added} abilities")
            
            if new_abilities_added == 0:
                print("No new abilities found, stopping search")
                break
        
        print("\n" + "="*50)
        print(f"FINAL JOB LIST ({len(all_jobs)}):")
        for job in sorted(all_jobs):
            print(f"  - {job}")
        print(f"\nFINAL ABILITY LIST ({len(all_abilities)}):")
        for ability in sorted(all_abilities):
            print(f"  - {ability}")
        print("="*50 + "\n")
        
        return all_jobs, all_abilities


if __name__ == "__main__":
    DEFAULT_JOB_ID = "29-2099.01"
    
    print(f"Initializing Job Abilities Network...")
    network = JobAbilitiesNetwork()
    
    job_id = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_JOB_ID
    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 0.75
    max_jobs = int(sys.argv[3]) if len(sys.argv) > 3 else None
    
    try:
        print(f"Exploring job abilities network for job ID: {job_id}, similarity threshold: {threshold}")
        related_jobs, all_abilities = network.explore_job_abilities_network(job_id, 
                                                                            similarity_threshold=threshold, 
                                                                            max_jobs=max_jobs)
        
        print(f"Exploration complete. Found {len(related_jobs)} related jobs and {len(all_abilities)} abilities.")
    except Exception as e:
        print(f"ERROR: {str(e)}")
        print("Script completed with errors, but did not crash.")
