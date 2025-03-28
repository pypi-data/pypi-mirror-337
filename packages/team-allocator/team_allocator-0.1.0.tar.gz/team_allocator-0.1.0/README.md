# Team Allocator

A flexible Python library for creating random, balanced, and attribute-based team assignments.

## Installation

```bash
pip install team_allocator
```

## Features

* Random team generation
* Balanced team allocation with skill weighting
* Attribute-based team grouping

## Usage Examples

### Random Team Allocation

```python
from team_allocator import TeamAllocator

# List of participants
participants = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank']

# Create teams of 3
random_teams = TeamAllocator.random_teams(participants, team_size=3)

# Create 2 teams
random_teams = TeamAllocator.random_teams(participants, num_teams=2)
```

### Balanced Team Allocation

```python
# Create balanced teams using skill weights
skill_weights = {
    'Alice': 9.0,
    'Bob': 7.5,
    'Charlie': 8.0,
    'David': 6.5,
    'Eve': 7.0,
    'Frank': 6.0
}

balanced_teams = TeamAllocator.balanced_teams(
    list(skill_weights.keys()), 
    num_teams=2, 
    skill_weights=skill_weights
)
```

### Attribute-Based Team Grouping

```python
# Participants with different attributes
participants = [
    {'name': 'Alice', 'role': 'Developer'},
    {'name': 'Bob', 'role': 'Designer'},
    {'name': 'Charlie', 'role': 'Developer'},
    {'name': 'David', 'role': 'Tester'},
    {'name': 'Eve', 'role': 'Designer'},
    {'name': 'Frank', 'role': 'Tester'}
]

# Create teams with diverse roles
diverse_teams = TeamAllocator.group_by_attribute(
    participants, 
    attribute='role', 
    num_teams=2
)
```

## Methods

### `random_teams(participants, team_size=None, num_teams=None)`

* Randomly distribute participants into teams
* Can specify either team size or number of teams

### `balanced_teams(participants, team_size=None, num_teams=None, skill_weights=None)`

* Create teams with balanced distribution
* Optional skill weights for more strategic allocation

### `group_by_attribute(participants, attribute, num_teams)`

* Group participants based on a specific attribute
* Ensures diverse teams across different characteristics

## Error Handling

* Raises `ValueError` for invalid inputs
* Handles empty participant lists
* Supports flexible team creation strategies

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

MIT License

## Contact

Vineet Kumar
Email: whyvineet@outlook.com
