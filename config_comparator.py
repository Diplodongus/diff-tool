import logging
from fuzzywuzzy import fuzz
from functools import lru_cache

@lru_cache(maxsize=1000)
def similar(a, b):
    return fuzz.ratio(a, b) / 100.0

def parse_config(config):
    lines = config.splitlines()
    parsed = []
    current_block = []
    
    for line in lines:
        if line.strip() and not line.startswith(' '):
            if current_block:
                parsed.append(tuple(current_block))
            current_block = [line]
        else:
            current_block.append(line)
    
    if current_block:
        parsed.append(tuple(current_block))
    
    return tuple(parsed)

def compare_blocks(golden_block, config_block, indent=''):
    diff = []
    i, j = 0, 0
    golden_set = set(line.strip() for line in golden_block)
    config_set = set(line.strip() for line in config_block)
    
    while i < len(golden_block) and j < len(config_block):
        golden_line = golden_block[i].strip()
        config_line = config_block[j].strip()
        
        if golden_block[i] == config_block[j]:
            diff.append(('unchanged', indent + golden_block[i]))
            i += 1
            j += 1
        else:
            # Check if the commands are the same but with different parameters
            golden_cmd = golden_line.split()[0] if golden_line.split() else ''
            config_cmd = config_line.split()[0] if config_line.split() else ''
            
            if golden_cmd == config_cmd:
                diff.append(('modified', f"{indent}{golden_block[i]} -> {config_block[j]}"))
                i += 1
                j += 1
            else:
                similarity = similar(golden_line, config_line)
                
                if similarity >= 0.8:
                    diff.append(('modified', f"{indent}{golden_block[i]} -> {config_block[j]}"))
                    i += 1
                    j += 1
                else:
                    # Look for best matches
                    best_golden_match = max(((line, similar(golden_line, line)) for line in config_set), key=lambda x: x[1], default=(None, 0))
                    best_config_match = max(((line, similar(config_line, line)) for line in golden_set), key=lambda x: x[1], default=(None, 0))
                    
                    if best_golden_match[1] > best_config_match[1] and best_golden_match[1] >= 0.8:
                        while j < len(config_block) and config_block[j].strip() != best_golden_match[0]:
                            diff.append(('extra', indent + config_block[j]))
                            j += 1
                        if j < len(config_block):
                            diff.append(('modified', f"{indent}{golden_block[i]} -> {config_block[j]}"))
                            i += 1
                            j += 1
                        else:
                            diff.append(('missing', indent + golden_block[i]))
                            i += 1
                    elif best_config_match[1] >= 0.8:
                        while i < len(golden_block) and golden_block[i].strip() != best_config_match[0]:
                            diff.append(('missing', indent + golden_block[i]))
                            i += 1
                        if i < len(golden_block):
                            diff.append(('modified', f"{indent}{golden_block[i]} -> {config_block[j]}"))
                            i += 1
                            j += 1
                        else:
                            diff.append(('extra', indent + config_block[j]))
                            j += 1
                    else:
                        diff.append(('missing', indent + golden_block[i]))
                        diff.append(('extra', indent + config_block[j]))
                        i += 1
                        j += 1
    
    # Add remaining golden lines as missing
    while i < len(golden_block):
        diff.append(('missing', indent + golden_block[i]))
        i += 1
    
    # Add remaining config lines as extra
    while j < len(config_block):
        diff.append(('extra', indent + config_block[j]))
        j += 1
    
    return diff

def compare_with_golden(config, golden_config):
    parsed_golden = parse_config(golden_config)
    parsed_config = parse_config(config)
    
    diff = []
    golden_top_level = {block[0].strip(): block for block in parsed_golden}
    config_top_level = {block[0].strip(): block for block in parsed_config}
    
    for golden_key, golden_block in golden_top_level.items():
        if golden_key in config_top_level:
            diff.extend(compare_blocks(golden_block, config_top_level[golden_key]))
        else:
            for line in golden_block:
                diff.append(('missing', line))
    
    # Check for extra top-level commands in config
    for config_key, config_block in config_top_level.items():
        if config_key not in golden_top_level:
            for line in config_block:
                diff.append(('extra', line))
    
    logging.debug(f"Comparison complete. Diff length: {len(diff)}")
    return diff