"""
This Pseudo Code module is meant to provide an overview of the integrity usage behind the algorithm


Pseudo Code:
    function algorithm(key, message):
        bits_key = encode_to_bits(key) #convert key to bits
        bits_message = encode_to_bits(message) #convert message to bits
        combined = combine(bits_key, bits_message)  # apply algorithm (call algorithm function)
        tag = hash(combined) # apply hash and return as "tag"
        return tag
"""