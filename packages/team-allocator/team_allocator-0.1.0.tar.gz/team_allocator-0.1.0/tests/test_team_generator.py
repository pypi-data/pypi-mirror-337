import pytest
from team_allocator import TeamAllocator

def test_random_teams():
    participants = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank']
    
    # Test team size allocation
    teams = TeamAllocator.random_teams(participants, team_size=3)
    assert len(teams) == 2
    assert all(len(team) == 3 for team in teams)
    
    # Test number of teams allocation
    teams = TeamAllocator.random_teams(participants, num_teams=3)
    assert len(teams) == 3
    assert sum(len(team) for team in teams) == len(participants)

def test_balanced_teams():
    skill_weights = {
        'Alice': 9.0,
        'Bob': 7.5,
        'Charlie': 8.0,
        'David': 6.5,
        'Eve': 7.0,
        'Frank': 6.0
    }
    
    teams = TeamAllocator.balanced_teams(
        list(skill_weights.keys()), 
        num_teams=2, 
        skill_weights=skill_weights
    )
    
    assert len(teams) == 2
    # Ensure all participants are allocated
    all_participants = [participant for team in teams for participant in team]
    assert set(all_participants) == set(skill_weights.keys())
    
    # Check that the teams are balanced in terms of skill
    team_skills = [sum(skill_weights[participant] for participant in team) for team in teams]
    assert abs(team_skills[0] - team_skills[1]) <= max(skill_weights.values())

def test_group_by_attribute():
    participants = [
        {'name': 'Alice', 'role': 'Developer'},
        {'name': 'Bob', 'role': 'Designer'},
        {'name': 'Charlie', 'role': 'Developer'},
        {'name': 'David', 'role': 'Tester'},
        {'name': 'Eve', 'role': 'Designer'},
        {'name': 'Frank', 'role': 'Tester'}
    ]
    
    teams = TeamAllocator.group_by_attribute(participants, attribute='role', num_teams=2)
    
    assert len(teams) == 2
    # Ensure all participants are allocated
    all_participants = [participant['name'] for team in teams for participant in team]
    assert set(all_participants) == {p['name'] for p in participants}
    
    # Check that each team has diverse roles
    for team in teams:
        roles = {member['role'] for member in team}
        assert len(roles) > 1