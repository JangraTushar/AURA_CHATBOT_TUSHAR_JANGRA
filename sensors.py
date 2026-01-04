# sensors.py
import json
from typing import Dict, Any, List

from config import SAMPLE_FARM_DATA_FILE, DIAGNOSTIC_RULES_FILE


def load_farm_data() -> Dict[str, Any]:
    with open(SAMPLE_FARM_DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data  # {"farms": [...]}


def get_farm_by_id(farm_id: str) -> Dict[str, Any]:
    data = load_farm_data()
    for farm in data["farms"]:
        if farm["farmId"] == farm_id:
            return farm
    raise ValueError(f"Unknown farm_id: {farm_id}")


def load_diagnostic_rules() -> Dict[str, Any]:
    with open(DIAGNOSTIC_RULES_FILE, "r", encoding="utf-8") as f:
        rules = json.load(f)
    return rules  # {"diagnostic_rules": {...}}


def basic_rule_checks(sensors: Dict[str, float]) -> List[Dict[str, Any]]:
    """
    Simple 3+ rules as given in assignment (EC, temperature, PPFD, plus pH).
    """
    issues = []

    # EC rule
    if "ec" in sensors and sensors["ec"] < 1.2:
        issues.append(
            {
                "parameter": "EC",
                "current": sensors["ec"],
                "optimal": "1.2-1.6 mS/cm",
                "problem": "Nutrient deficiency (low EC).",
                "solution": "Increase nutrient concentration to raise EC into 1.2-1.6 range.",
            }
        )

    # Temperature rule
    if "temperature" in sensors and sensors["temperature"] < 18:
        issues.append(
            {
                "parameter": "Temperature",
                "current": sensors["temperature"],
                "optimal": "18-22°C",
                "problem": "Cold stress slowing growth.",
                "solution": "Increase room temperature and check heater operation.",
            }
        )

    # Light (PPFD) rule (too low). [file:6][file:5]
    if "ppfd" in sensors and sensors["ppfd"] < 200:
        issues.append(
            {
                "parameter": "Light (PPFD)",
                "current": sensors["ppfd"],
                "optimal": "200-300 µmol/m²/s",
                "problem": "Insufficient light for optimal photosynthesis.",
                "solution": "Increase light intensity or duration.",
            }
        )

    # Optional: pH rule
    if "ph" in sensors and (sensors["ph"] < 5.5 or sensors["ph"] > 6.5):
        issues.append(
            {
                "parameter": "pH",
                "current": sensors["ph"],
                "optimal": "5.5-6.5",
                "problem": "pH out of optimal range, affecting nutrient uptake.",
                "solution": "Adjust nutrient solution pH gradually toward ~6.0.",
            }
        )

    return issues


def level_2_answer(question: str, farm_id: str) -> str:
    """
    Sensor-driven diagnosis using farm data and simple rules.
    """
    farm = get_farm_by_id(farm_id)
    sensors = farm["sensors"]  # temperature, ec, ph, ppfd, etc. [file:4]

    issues = basic_rule_checks(sensors)

    if not issues:
        return (
            "All key parameters (EC, temperature, light, pH) are within their optimal "
            "ranges for lettuce. The problem might be related to pests, disease, or "
            "variety-specific behaviour."
        )

    main = issues[0]
    response = f"""
I analysed your farm sensors for {farm['currentCrop']} at {farm['location']}.

Parameter: {main['parameter']}
Current value: {main['current']}
Optimal range: {main['optimal']}

Problem: {main['problem']}
Recommended action: {main['solution']}
"""
    return response.strip()
