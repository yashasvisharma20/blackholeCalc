from typing import Dict, Union

class BlackHoleClassifier:
    @staticmethod
    def identify(mass: float, spin: float = 0, charge: float = 0) -> Dict[str, Union[str, bool]]:
        """Identifies the metric type based on physical parameters."""
        # Validity Check
        is_stable = (spin**2 + charge**2) <= 1.0
        status = "Stable Event Horizon" if is_stable else "UNSTABLE (Naked Singularity)"
        
        # Classification Logic
        if spin == 0 and charge == 0:
            mtype = "Schwarzschild"
            desc = "Static, Neutral"
        elif spin != 0 and charge == 0:
            mtype = "Kerr"
            desc = "Rotating, Neutral"
        elif spin == 0 and charge != 0:
            mtype = "Reissner-Nordström"
            desc = "Static, Charged"
        else:
            mtype = "Kerr-Newman"
            desc = "Rotating, Charged"
            
        return {
            "Type": mtype,
            "Description": desc,
            "Status": status,
            "Is_Physical": is_stable
        }