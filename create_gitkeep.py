from pathlib import Path

base = Path(r"C:\RIPC_NEW")

for folder in base.rglob("*"):

    if folder.is_dir():

        gitkeep = folder / ".gitkeep"

        if not gitkeep.exists():
            gitkeep.touch()

print("تم إنشاء .gitkeep داخل جميع المجلدات")