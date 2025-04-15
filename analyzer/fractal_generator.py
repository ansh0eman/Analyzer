import matplotlib.pyplot as plt
import numpy as np
import hashlib
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import hashlib
import os
from datetime import datetime

def generate_fractal_from_text(text, output_dir='analyzer/static', filename=None):
    # Convert input to a hash seed
    hash_object = hashlib.sha256(text.encode())
    hash_hex = hash_object.hexdigest()
    seed = int(hash_hex[:8], 16)
    np.random.seed(seed)

    # Derive axiom, rule, angle from hash
    axiom_options = ["F", "F+F+F+F", "F-F+F"]
    axiom = axiom_options[seed % len(axiom_options)]

    angle = [60, 90, 120, 45][int(hash_hex[10], 16) % 4]
    iterations = 2 + (int(hash_hex[5], 16) % 3)  # 2–4 iterations

    # Choose rule variations
    rule_variants = [
        {"F": "F+F--F+F"},
        {"F": "F+F-F-F+F"},
        {"F": "F+G", "G": "F-G"},
        {"F": "F-F++F-F"}
    ]
    rules = rule_variants[int(hash_hex[15], 16) % len(rule_variants)]

    # L-System builder
    def lsystem(axiom, rules, iterations):
        result = axiom
        for _ in range(iterations):
            result = ''.join([rules.get(c, c) for c in result])
        return result

    pattern = lsystem(axiom, rules, iterations)

    # Turtle-like drawing
    x, y = [0], [0]
    direction = 0  # degrees

    for command in pattern:
        if command in "FG":
            x.append(x[-1] + np.cos(np.radians(direction)))
            y.append(y[-1] + np.sin(np.radians(direction)))
        elif command == '+':
            direction += angle
        elif command == '-':
            direction -= angle

    # Plot
    plt.figure(figsize=(6, 6))
    plt.plot(x, y, color=np.random.rand(3,))
    plt.axis('off')

    if not filename:
        filename = f"fractal_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    output_path = os.path.join(output_dir, filename)
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close()

    return filename
