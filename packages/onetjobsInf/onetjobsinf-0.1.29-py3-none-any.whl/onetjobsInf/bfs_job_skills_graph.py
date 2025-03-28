import sys
import os
from collections import defaultdict, deque

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'onetjobsInf')))

# Import necessary modules
from OnetWebService import OnetWebService
from onet_credentials import get_credentials
from bfs_skills_search import get_skills, extract_skill_ids

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

class JobSkillsNetwork:
    def __init__(self):
        # Get credentials and initialize the O*NET service
        username, password = get_credentials()
        self.onet_service = OnetWebService(username, password)
        
        # Initialize dictionaries to store job-skills and skills-job mappings
        self.job_to_skills = defaultdict(set)
        self.skill_to_jobs = defaultdict(set)
        
        # Cache for already queried jobs to avoid redundant API calls
        self.queried_jobs = set()
        
        # Load all available job IDs
        data_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                               'onetjobsInf/src_data/Occupation Data.txt')
        self.all_job_ids = load_job_ids_from_file(data_file)
    
    def get_job_skills(self, job_id):
        """
        Get skills for a job using the O*NET API and update the mappings.
        
        Args:
            job_id (str): The O*NET job code
            
        Returns:
            set: Set of skill IDs for the job
        """
        # Check if we've already queried this job
        if job_id in self.queried_jobs:
            return self.job_to_skills[job_id]
        
        # Get the skills data and extract skill IDs using the API
        try:
            # print(f"Querying API for job: {job_id}")
            skills_data = get_skills(self.onet_service, job_id)
            if not skills_data:
                # print(f"No skills data available for job {job_id}, skipping")
                # Still mark as queried to avoid repeated attempts
                self.queried_jobs.add(job_id)
                return set()
            
            skill_ids = extract_skill_ids(skills_data)
            
            # Update the mappings
            self.job_to_skills[job_id] = set(skill_ids)
            for skill_id in skill_ids:
                self.skill_to_jobs[skill_id].add(job_id)
            
            # Mark this job as queried
            self.queried_jobs.add(job_id)
            
            return set(skill_ids)
        except Exception as e:
            print(f"Error getting skills for job {job_id}: {str(e)}")
            # Mark as queried to avoid repeated attempts that will fail
            self.queried_jobs.add(job_id)
            return set()
    
    def explore_job_skills_network(self, initial_job_id, similarity_threshold, max_jobs=None):
        """
        Dynamically explore the job-skills network using a BFS algorithm:
        1. Get initial job skills
        2. Find similar jobs (>= similarity_threshold % shared skills)
        3. Add non-shared skills to skill list
        4. Repeat with expanded skill list until no new jobs/skills are found
        
        Args:
            initial_job_id (str): The starting job ID
            similarity_threshold (float): Minimum percentage of shared skills (0.0-1.0)
            max_jobs (int, optional): Maximum number of jobs to find (None for unlimited)
            
        Returns:
            tuple: (jobs_set, skills_set) containing all discovered jobs and skills
        """
        # Get skills for the initial job
        try:
            current_skill_set = self.get_job_skills(initial_job_id)
            if not current_skill_set:
                print(f"Warning: No skills found for job {initial_job_id}")
                return set(), set()
        except Exception as e:
            print(f"Error retrieving skills for initial job {initial_job_id}: {str(e)}")
            return set(), set()
        
        # Print original job ID and skills
        print("\n" + "="*50)
        print(f"ORIGINAL JOB: {initial_job_id}")
        print(f"ORIGINAL SKILLS ({len(current_skill_set)}):")
        for skill in sorted(current_skill_set):
            print(f"  - {skill}")
        print("="*50 + "\n")
        
        # Initialize sets to track all found jobs and skills
        all_jobs = {initial_job_id}
        all_skills = set(current_skill_set)
        
        # Initialize BFS queue
        queue = deque([(initial_job_id, current_skill_set)])
        
        while queue:
            job_id, job_skills = queue.popleft()
            print(f"Exploring job {job_id} with {len(job_skills)} skills")
            
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
                    # Get skills for this job
                    candidate_job_skills = self.get_job_skills(candidate_job_id)
                    
                    # Skip jobs with no skills data
                    if not candidate_job_skills:
                        continue
                    
                    # Calculate similarity based on skill overlap
                    overlap = len(candidate_job_skills.intersection(job_skills))
                    #PRINT STATEMENT HERE 
                    # print(len(job_skills) if job_skills else 0)
                    similarity = overlap / len(job_skills) if job_skills else 0
                    
                    if similarity >= similarity_threshold:
                        similar_jobs.append((candidate_job_id, similarity, candidate_job_skills))
                        print(f"Found similar job {candidate_job_id} with {similarity:.2f} similarity ({overlap}/{len(job_skills)} skills)")
                        
                        # Stop if we've reached the maximum number of jobs (if specified)
                        if max_jobs and len(all_jobs) + len(similar_jobs) >= max_jobs:
                            break
                except Exception as e:
                    # If there's an error with this job, log it and continue with the next job
                    print(f"Error processing job {candidate_job_id}: {str(e)}. Continuing with next job.")
                    continue
            
            # Sort similar jobs by similarity (highest first)
            similar_jobs.sort(key=lambda x: x[1], reverse=True)
            
            # If no new similar jobs were found, we're done
            if not similar_jobs:
                print(f"No new similar jobs found for job {job_id}, moving to next job in queue")
                continue
            
            # Add new jobs and their skills to our collections
            new_jobs_added = 0
            new_skills_added = 0
            
            for candidate_job_id, similarity, candidate_job_skills in similar_jobs:
                # Add job
                print("ADD JOB TO QUEUE")
                all_jobs.add(candidate_job_id)
                print(candidate_job_id)
                print(candidate_job_skills)
                new_jobs_added += 1
                
                # Add any new skills from this job
                new_skills = candidate_job_skills - all_skills
                if new_skills:
                    all_skills.update(new_skills)
                    new_skills_added += len(new_skills)
                    print(f"  Added {len(new_skills)} new skills from job {candidate_job_id}")
                
                # Add to BFS queue
                queue.append((candidate_job_id, candidate_job_skills))
                
                # Stop if we've reached the maximum number of jobs (if specified)
                if max_jobs and len(all_jobs) >= max_jobs:
                    break
            
            print(f"Iteration complete: Added {new_jobs_added} jobs and {new_skills_added} skills")
            
            # If no new skills were added, we can stop since the next iteration would yield the same results
            if new_skills_added == 0:
                print("No new skills found, stopping search")
                break
        
        # Print final results
        print("\n" + "="*50)
        print(f"FINAL JOB LIST ({len(all_jobs)}):")
        for job in sorted(all_jobs):
            print(f"  - {job}")
        print(f"\nFINAL SKILL LIST ({len(all_skills)}):")
        for skill in sorted(all_skills):
            print(f"  - {skill}")
        print("="*50 + "\n")
        
        return all_jobs, all_skills


if __name__ == "__main__":
    DEFAULT_JOB_ID = "29-2099.01"
    
    print(f"Initializing Job Skills Network...")
    network = JobSkillsNetwork()
    
    # Get job ID from command line if provided, otherwise use default
    job_id = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_JOB_ID
    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 0.75
    max_jobs = int(sys.argv[3]) if len(sys.argv) > 3 else None
    
    try:
        print(f"Exploring job skills network for job ID: {job_id}, similarity threshold: {threshold}")
        related_jobs, all_skills = network.explore_job_skills_network(job_id, similarity_threshold=threshold, max_jobs=max_jobs)
        
        print(f"Exploration complete. Found {len(related_jobs)} related jobs and {len(all_skills)} skills.")
    except Exception as e:
        print(f"ERROR: {str(e)}")
        print("Script completed with errors, but did not crash.")