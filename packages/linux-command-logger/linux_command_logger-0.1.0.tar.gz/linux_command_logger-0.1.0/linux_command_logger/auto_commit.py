import os

def auto_commit():
    """Automatically commit and push commands.md to GitHub."""
    os.system("git add commands.md")
    os.system("git commit -m 'Updated command documentation'")
    os.system("git push origin main")
    print("✅ Commands uploaded to GitHub!")

if __name__ == "__main__":
    auto_commit()
