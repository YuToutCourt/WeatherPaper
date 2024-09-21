def output_to_file(data):
    with open("weatherpaper.log", "a") as f:
        f.write(f"{data}\n")