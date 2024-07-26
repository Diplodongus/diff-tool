# Legacy - Might add back in the future

def generate_remediation(diff, missing_golden):
    remediation = []
    for diff_type, line in diff:
        if diff_type == 'removed':
            remediation.append(f"no {line}")
        elif diff_type == 'added':
            remediation.append(line)
    
    for line in missing_golden:
        remediation.append(line)
    
    return remediation