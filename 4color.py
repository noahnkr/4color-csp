def is_valid(assignments, region, color, constraints):
    for neighbor in constraints[region]:
        if neighbor in assignments and assignments[neighbor] == color:
            return False
    return True

def forward_check(domains, region, color, constraints):
    updated_domains = {r: d[:] for r, d in domains.items()}
    for neighbor in constraints[region]:
        if color in updated_domains[neighbor]:
            updated_domains[neighbor].remove(color)
    return updated_domains

def get_mrv(assignments, regions, domains, constraints):
    # Degree Hueristic for choosing starting region
    if (len(assignments) == 0):
        return max(constraints, key=lambda k: len(constraints[k]))

    unassigned = [region for region in regions if region not in assignments]
    mrv = float('inf')

    # Find the unassigned region withthe minimum remaining values available.
    for u in unassigned:
        rv = len(domains[u])
        if rv < mrv:
            mrv = rv
            mrv_region = u
        

    return mrv_region

def count_solutions(assignments, regions, domains, constraints):
    # All regions assigned valid color. This is a solution.
    if len(assignments) == len(regions):
        return 1

    # Select the region with the least amount of choices.
    region = get_mrv(assignments, regions, domains, constraints)
    count = 0

    # Since we are counting solutions, we do not need to choose a 
    # least constraining value since we are checking for all colors.
    for color in domains[region]:
        if is_valid(assignments, region, color, constraints):
            assignments[region] = color
            # Perform forward checking by updating the domains
            new_domains = forward_check(domains, region, color, constraints)
            count += count_solutions(assignments, regions, new_domains, constraints)

            # Backtrack by deleting assignment
            del assignments[region]

    return count


regions = ['WA', 'NT', 'SA', 'Q', 'V', 'NSW', 'T']
colors = ['Red', 'Green', 'Blue', ]
domains = {region: colors[:] for region in regions}
constraints = {
    'WA': ['NT', 'SA'],
    'NT': ['WA', 'SA', 'Q'],
    'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
    'Q': ['NT', 'SA', 'NSW'],
    'V': ['SA', 'NSW'],
    'NSW': ['SA', 'Q', 'V'],
    'T': [],
}

print(count_solutions({}, regions, domains, constraints))