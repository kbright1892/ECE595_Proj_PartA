features: dict[str, int] = {
    "outlook": 0,
    "temperature": 1,
    "humidity": 2,
    "wind": 3
}

data: dict[int, list] = {
    1: ["sunny", "hot", "high", "weak"],
    2: ["sunny", "hot", "high", "strong"],
    3: ["overcast", "hot", "high", "weak"],
    4: ["rain", "mild", "high", "weak"],
    5: ["rain", "cool", "normal", "weak"],
    6: ["rain", "cool", "normal", "strong"],
    7: ["overcast", "cool", "normal", "strong"],
    8: ["sunny", "mild", "high", "weak"],
    9: ["sunny", "cool", "normal", "weak"],
    10: ["rain", "mild", "normal", "weak"],
    11: ["sunny", "mild", "normal", "strong"],
    12: ["overcast", "mild", "high", "strong"],
    13: ["overcast", "hot", "normal", "weak"],
    14: ["rain", "mild", "high", "strong"]
}

outcomes: dict[int, str] = {
    1: "no",
    2: "no",
    3: "yes",
    4: "yes",
    5: "yes",
    6: "no",
    7: "yes",
    8: "no",
    9: "yes",
    10: "yes",
    11: "yes",
    12: "yes",
    13: "yes",
    14: "no"
}
