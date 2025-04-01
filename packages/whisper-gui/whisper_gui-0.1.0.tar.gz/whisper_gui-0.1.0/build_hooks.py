import subprocess
from pathlib import Path
from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class UICBuildHook(BuildHookInterface):
    """Build hook to regenerate ui_form.py when form.ui changes."""

    def initialize(self, version, build_data):
        """Initialize the build hook."""
        # Get the source directory
        src_dir = Path("src/whisper_gui")
        ui_file = src_dir / "form.ui"
        py_file = src_dir / "ui_form.py"
        
        # Check if form.ui exists and is newer than ui_form.py
        if ui_file.exists():
            if not py_file.exists() or (
                ui_file.stat().st_mtime > py_file.stat().st_mtime
            ):
                print("Regenerating ui_form.py from form.ui...")
                try:
                    subprocess.run(
                        ["pyside6-uic", str(ui_file), "-o", str(py_file)],
                        check=True,
                        capture_output=True,
                        text=True
                    )
                    print("Successfully regenerated ui_form.py")
                except subprocess.CalledProcessError as e:
                    print(f"Error regenerating ui_form.py: {e.stderr}")
                    raise 