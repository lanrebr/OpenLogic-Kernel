import os
import json

def load_kernel():
    """Scans the concepts directory and loads all UCID mappings."""
    kernel = []
    base_path = 'concepts'
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith('.json'):
                with open(os.path.join(root, file), 'r') as f:
                    kernel.append(json.load(f))
    return kernel

def translate_to_logic(text, domain_hint):
    """
    Translates messy natural language into precise logic based on domain.
    """
    kernel = load_kernel()
    words = text.lower().split()
    translated_text = text
    
    for concept in kernel:
        # Check if the requested domain matches the concept's domains
        if domain_hint.upper() in concept['domains']:
            for alias in concept['legacy_aliases']:
                # Case-insensitive replacement for whole words
                if alias.lower() in words:
                    ucid = concept['ucid']
                    logic = concept['logic_definition']
                    replacement = f"[{ucid}: {logic}]"
                    translated_text = translated_text.replace(alias, replacement)
                    
    return translated_text

# --- Example Usage ---
if __name__ == "__main__":
    sentence_1 = "Check the proof of the sourdough."
    print(f"Baking Context: {translate_to_logic(sentence_1, 'CULINARY')}")

    sentence_2 = "The proof of the theorem is solid."
    print(f"Math Context: {translate_to_logic(sentence_2, 'MATHEMATICS')}")
