"""
run_manager.py

PURPOSE:
    Manages the lifecycle of a 'Run'. Ensures scientific reproducibility 
    by coupling inputs, outputs, and DEEP metadata into immutable records.

SCOPE:
    - UUID generation.
    - JSON serialization.
    - Capturing environment (Version, OS) for debugging.

ENTITIES:
    - Library Developer: Enforces schema.
    - Researcher: Relies on this for "auditable" results.
"""

import os
import json
import uuid
import datetime
import platform
import sys

# Dynamic version import to avoid circular dependency
# In a real install, this would be: from blackholecalc import __version__
PACKAGE_VERSION = "0.1.0-alpha" 

RUNS_DIR = "runs"

class RunContext:
    def __init__(self, run_name=None, description="", model_class_name="Unknown"):
        self.run_id = str(uuid.uuid4())[:8]
        self.timestamp = datetime.datetime.utcnow().isoformat() + "Z"
        self.run_name = run_name if run_name else f"run_{self.run_id}"
        self.description = description
        
        # Provenance Data
        self.model_class_name = model_class_name
        self.software_version = PACKAGE_VERSION
        self.python_version = sys.version.split()[0]
        self.platform = platform.platform()
        
        self.inputs = {}
        self.outputs = {}
        self.assumptions = []

    def log_input(self, key, value, unit=None):
        """Logs an input parameter. WARNING: Ensure units are explicit."""
        self.inputs[key] = {"value": value, "unit": unit}

    def log_output(self, key, value, unit=None):
        """Logs a computed result."""
        self.outputs[key] = {"value": value, "unit": unit}

    def add_assumption(self, text):
        self.assumptions.append(text)

    def save(self, base_path=RUNS_DIR):
        """Persists the run to disk with full provenance."""
        run_path = os.path.join(base_path, self.run_name)
        os.makedirs(run_path, exist_ok=True)

        # 1. Inputs
        with open(os.path.join(run_path, "inputs.json"), 'w') as f:
            json.dump(self.inputs, f, indent=4)

        # 2. Outputs
        with open(os.path.join(run_path, "outputs.json"), 'w') as f:
            json.dump(self.outputs, f, indent=4)

        # 3. Deep Metadata (The "Audit Trail")
        metadata = {
            "id": self.run_id,
            "timestamp": self.timestamp,
            "description": self.description,
            "provenance": {
                "library_version": self.software_version,
                "model_class": self.model_class_name,
                "python_version": self.python_version,
                "platform": self.platform
            },
            "assumptions": self.assumptions
        }
        with open(os.path.join(run_path, "metadata.json"), 'w') as f:
            json.dump(metadata, f, indent=4)

        print(f"[RunManager] Run saved to: {run_path} (ID: {self.run_id})")