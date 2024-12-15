def _reader(filename, part):
    walls = set()
    boxes = [] if part == 1 else {}
    counter = 0
    with open(filename, "r") as file:
        warehouse, movements = file.read().split("\n\n")
    for j, line in enumerate(warehouse.splitlines()):
        for i, char in enumerate(line):
            match char:
                case "#":
                    walls.update(((i, j),) if part == 1 else ((2 * i, j), (2 * i + 1, j)))
                case "O":
                    if part == 1:
                        boxes.append((i, j))
                    else:
                        boxes[(2 * i, j)] = counter
                        boxes[(2 * i + 1, j)] = counter
                        counter += 1
                case "@":
                    robot = (i, j) if part == 1 else (2 * i, j)
                case _:
                    continue
    movements = "".join(movements.splitlines())
    return walls, boxes, robot, movements

def _box_mover_1(ind, boxes, walls, move):
    new_box = tuple(b + m for b, m in zip(boxes[ind], move))
    if new_box in walls:
        return False, boxes
    elif new_box in boxes:
        new_ind = boxes.index(new_box)
        boxes[ind] = new_box
        return _box_mover_1(new_ind, boxes, walls, move)
    else:
        boxes[ind] = new_box
        return True, boxes

def _box_mover_2(key, boxes, walls, move):
    value = boxes[key]
    keys = [k for k, v in boxes.items() if v == value]
    new_boxes = tuple(tuple(k + m for k, m in zip(key, move)) for key in keys)
    for k in keys:
        del boxes[k]
    if any(box in walls for box in new_boxes):
        return False, boxes
    do_move = True
    if new_boxes[0] in boxes:
        do_move, boxes = _box_mover_2(new_boxes[0], boxes, walls, move) 
    if do_move and new_boxes[1] in boxes:
        do_move, boxes = _box_mover_2(new_boxes[1], boxes, walls, move)
    if do_move:
        for box in new_boxes:
            boxes[box] = value
        return True, boxes
    else:
        return False, boxes

def _mover(robot, move, walls, boxes, part):
    new_robot = tuple(r + d for r, d in zip(robot, move))
    if new_robot in walls:
        return robot, boxes
    if new_robot in boxes:
        new_boxes = boxes.copy()
        if part == 1:
            do_move, new_boxes = _box_mover_1(boxes.index(new_robot), new_boxes, walls, move)
        else:
            do_move, new_boxes = _box_mover_2(new_robot, new_boxes, walls, move)
        if do_move:
            return new_robot, new_boxes
        else:
            return robot, boxes
    return new_robot, boxes 

def solver(filename):
    dirs = {">": (1, 0), "v": (0, 1), "<": (-1, 0), "^": (0, -1)}
    for part in (1, 2):
        walls, boxes, robot, movements = _reader(filename, part)
        for movement in movements:
            move = dirs[movement]
            robot, boxes = _mover(robot, move, walls, boxes, part)
        if part == 1:
            print(f"Part {part}: {sum(100 * box[1] + box[0] for box in boxes)}")
        else:
            print(f"Part {part}: {sum(100 * box[1] + box[0] for box in tuple(boxes.keys())[::2])}")
    