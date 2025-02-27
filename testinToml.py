import toml

try:
    with open('secrets.toml', 'r') as f:
        for line in f:
            print(line.strip())
        config = toml.load(f)
except Exception as e:
    print(f"Error leyendo el archivo TOML: {e}")