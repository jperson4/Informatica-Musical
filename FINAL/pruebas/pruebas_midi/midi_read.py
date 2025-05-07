import mido

# Automatically find MPK Mini input port
input_ports = mido.get_input_names()
mpk_port = next((port for port in input_ports if "MPK Mini" in port), None)

if not mpk_port:
    print("MPK Mini not found. Available ports:")
    for port in input_ports:
        print(f"  - {port}")
    exit()

# Open MIDI input
print(f"Listening on: {mpk_port}")
with mido.open_input(mpk_port) as inport:
    for msg in inport:
        print(msg)
