from config import parse_config

config = parse_config("config.txt")
print(f"{config.width}")
print("The height:", config.height)
print("The entry is:", config.entry)
# width: int
#     height: int
#     entry: Tuple[int, int]
#     exit: Tuple[int, int]
#     output_file: str
#     perfect: bool
#     seed: Optional[int] = None
