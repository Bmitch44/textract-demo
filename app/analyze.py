import json

def load_blocks_from_file(filename):
    with open(filename, 'r') as f:
        blocks = json.load(f)
    return blocks

def group_related_blocks(blocks):
    # First, create a dictionary mapping block IDs to blocks
    block_dict = {block['Id']: block for block in blocks}

    # Next, create a dictionary mapping each block ID to a list of related blocks
    related_blocks = {block['Id']: [] for block in blocks}

    # For each block, if it has relationships, add the related blocks to the related_blocks dictionary
    for block in blocks:
        if 'Relationships' in block:
            for relationship in block['Relationships']:
                related_block_ids = relationship['Ids']
                for related_block_id in related_block_ids:
                    related_block = block_dict.get(related_block_id)
                    if related_block is not None:
                        related_blocks[block['Id']].append(related_block)

    return related_blocks

# Load blocks from file
blocks = load_blocks_from_file('output.txt')

# Group related blocks
related_blocks = group_related_blocks(blocks)

with open('documents/analysis.txt', 'w') as f:
    json.dump(related_blocks, f, indent=4)
