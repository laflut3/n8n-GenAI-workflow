from typing import Dict, List, Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
        name="internship",
        host="0.0.0.0",
        port=8000
    )

CITY_SENSITIVITY: Dict[str, float] = {
    "Zurich": 95.44,
    "Frankfurt": 100.00,
    "Munich": 85.34,
    "Edinburgh": 95.97,
    "Trondheim": 94.87,
    "Geneva": 94.63,
    "Vienna": 82.31,
    "Copenhagen": 97.23,
    "Stockholm": 85.43,
    "Berlin": 98.29,
    "Trieste": 89.47,
    "Glasgow": 89.47,
    "Helsinki": 95.76,
    "Amsterdam": 93.29,
    "Bristol": 84.21,
    "Hamburg": 87.14,
    "Oslo": 90.01,
    "Valencia": 92.98,
    "Gdansk": 98.25,
    "Tallinn": 92.65,
    "Ljubljana": 92.85,
    "Rome": 97.04,
    "Kiev": 98.12,
    "Moscow": 100.00,
    "Reykjavik": 85.42,
    "Timisoara": 93.75,
    "Novi Sad": 95.83,
    "Sarajevo": 95.83,
    "Skopje": 93.75,
    "Bergen": 97.40,
    "Belfast": 84.62,
    "Constanta": 91.10
}


def _min_max(values: List[float]) -> Dict[str, float]:
    min_val = min(values)
    max_val = max(values)
    return {"min": min_val, "max": max_val}


def _inverse_min_max_score(value: float, min_val: float, max_val: float) -> float:
    if max_val == min_val:
        return 100.0
    normalized = (value - min_val) / (max_val - min_val)
    return round((1.0 - normalized) * 100.0, 2)


@mcp.tool()
def find_city_score(city_name: str) -> Dict:
    """
    Get sensitivity analysis Sj (%) for a city.
    """
    key = next(
        (k for k in CITY_SENSITIVITY if k.lower() == city_name.lower()),
        None
    )

    if not key:
        raise ValueError(f"City '{city_name}' not found")

    stats = _min_max(list(CITY_SENSITIVITY.values()))
    raw = CITY_SENSITIVITY[key]
    return {
        "city": key,
        "sensitivity_percent": raw,
        "city_score": _inverse_min_max_score(raw, stats["min"], stats["max"]),
    }


@mcp.tool()
def list_cities(
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    sort_desc: bool = True
) -> List[Dict]:
    """
    List cities with sensitivity analysis values.
    """
    results = []
    stats = _min_max(list(CITY_SENSITIVITY.values()))

    for city, value in CITY_SENSITIVITY.items():
        if min_value is not None and value < min_value:
            continue
        if max_value is not None and value > max_value:
            continue

        results.append({
            "city": city,
            "sensitivity_percent": value,
            "city_score": _inverse_min_max_score(value, stats["min"], stats["max"]),
        })

    results.sort(
        key=lambda x: x["city_score"],
        reverse=sort_desc
    )

    return results


def main():
    mcp.run(transport="streamable-http", mount_path="/mcp")


if __name__ == "__main__":
    main()
