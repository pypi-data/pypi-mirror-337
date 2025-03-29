def payload_seeker(target_maze, target_value, _index_map=None):
    if _index_map is None:
        _index_map = []
    if target_maze == target_value:
        return _index_map
    if isinstance(target_maze, dict):
        for index, (key, value) in enumerate(target_maze.items()):
            _index_map.append(index)
            if target_value == key or target_value == value:
                return _index_map
            if result := payload_seeker(value, target_value, _index_map):
                return result
            _index_map.pop()
    if isinstance(target_maze, list):
        for index, value in enumerate(target_maze):
            _index_map.append(index)
            if target_value == value:
                return _index_map
            if result := payload_seeker(value, target_value, _index_map):
                return result
            _index_map.pop()

    return None


if __name__ == "__main__":
    ex = {
        "a": 1,
        "b": [1, 2, 3, 4, 5],
        "c": {"z": 10, "x": 20, "c": 30},
        "d": {"z": [100, 200, 300, 400, 500], "x": [11, 22, 33, 44, 55], "c": [101, 202, 303, 404, 505]},
    }
    x = payload_seeker(ex, 101)
