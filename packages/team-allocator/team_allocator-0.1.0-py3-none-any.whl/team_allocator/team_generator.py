import random
from typing import List, Dict, Optional, Any

class TeamAllocator:
    """
    A comprehensive team allocation library with multiple strategies 
    for creating balanced, random, and attribute-based diverse teams.
    """
    
    @staticmethod
    def random_teams(participants: List[str], 
                     team_size: Optional[int] = None, 
                     num_teams: Optional[int] = None) -> List[List[str]]:
        """
        Randomly distribute participants into teams.
        
        Args:
            participants (List[str]): List of participant names.
            team_size (Optional[int]): Desired size of each team.
            num_teams (Optional[int]): Number of teams to create.
        
        Returns:
            List[List[str]]: Randomly generated teams.
        
        Raises:
            ValueError: If neither `team_size` nor `num_teams` is specified.
        """
        if not participants:
            raise ValueError("Participants list cannot be empty.")
        
        # Shuffle participants
        shuffled = participants.copy()
        random.shuffle(shuffled)
        
        # Determine team creation strategy
        if team_size is not None:
            return [shuffled[i:i+team_size] for i in range(0, len(shuffled), team_size)]
        elif num_teams is not None:
            if num_teams <= 0:
                raise ValueError("Number of teams must be greater than 0.")
            
            base_team_size = len(shuffled) // num_teams
            remainder = len(shuffled) % num_teams
            
            teams = []
            start = 0
            for i in range(num_teams):
                end = start + base_team_size + (1 if i < remainder else 0)
                teams.append(shuffled[start:end])
                start = end
            
            return teams
        else:
            raise ValueError("Either `team_size` or `num_teams` must be specified.")
    
    @staticmethod
    def balanced_teams(participants: List[str], 
                       team_size: Optional[int] = None, 
                       num_teams: Optional[int] = None,
                       skill_weights: Optional[Dict[str, float]] = None) -> List[List[str]]:
        """
        Create teams with balanced distribution based on optional skill weights.
        
        Args:
            participants (List[str]): List of participant names.
            team_size (Optional[int]): Desired size of each team.
            num_teams (Optional[int]): Number of teams to create.
            skill_weights (Optional[Dict[str, float]]): Optional skill ratings for participants.
        
        Returns:
            List[List[str]]: Balanced teams.
        
        Raises:
            ValueError: If neither `team_size` nor `num_teams` is specified.
        """
        if not participants:
            raise ValueError("Participants list cannot be empty.")
        
        if skill_weights is None:
            # If no skill weights, fall back to random allocation
            return TeamAllocator.random_teams(participants, team_size, num_teams)
        
        # Sort participants by skill in descending order
        sorted_participants = sorted(
            participants, 
            key=lambda x: skill_weights.get(x, 0), 
            reverse=True
        )
        
        # Determine number of teams
        if num_teams is None:
            if team_size is None:
                raise ValueError("Either `team_size` or `num_teams` must be specified.")
            num_teams = max(1, len(participants) // team_size)
        
        # Create teams by distributing top participants
        teams = [[] for _ in range(num_teams)]
        
        for i, participant in enumerate(sorted_participants):
            teams[i % num_teams].append(participant)
        
        return teams
    
    @staticmethod
    def group_by_attribute(participants: List[Dict[str, Any]], 
                           attribute: str, 
                           num_teams: int) -> List[List[Dict[str, Any]]]:
        """
        Group participants based on a specific attribute to ensure diverse teams.
        
        Args:
            participants (List[Dict[str, Any]]): List of participant dictionaries.
            attribute (str): Attribute to use for grouping.
            num_teams (int): Number of teams to create.
        
        Returns:
            List[List[Dict[str, Any]]]: Teams with diverse attributes.
        
        Raises:
            ValueError: If `num_teams` is less than or equal to 0.
        """
        if num_teams <= 0:
            raise ValueError("Number of teams must be greater than 0.")
        
        if not participants:
            raise ValueError("Participants list cannot be empty.")
        
        # Group by specified attribute
        attribute_groups = {}
        for participant in participants:
            key = participant.get(attribute)
            if key not in attribute_groups:
                attribute_groups[key] = []
            attribute_groups[key].append(participant)
        
        # Distribute across teams
        teams = [[] for _ in range(num_teams)]
        group_order = sorted(attribute_groups.keys(), key=lambda k: len(attribute_groups[k]), reverse=True)
        
        for group in group_order:
            group_members = attribute_groups[group]
            for i, member in enumerate(group_members):
                teams[i % num_teams].append(member)
        
        return teams

# Convenience alias
team_allocator = TeamAllocator()