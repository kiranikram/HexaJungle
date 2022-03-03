def create_starting_positions(size, num_players):
    """
    Create the starting positions of the all players.
    """

    even_positions = []
    odd_positions = []
    side_step = 1
    for i in range(num_players):
        if i % 2 == 0:

            pos = int((size - side_step) / 2), int((size - side_step) / 2 - 1)
            side_step += 1
            even_positions.append(pos)

        elif i % 2 != 0:

            pos = int((size - side_step) / 2), int((size - side_step) / 2 + 1)
            side_step += 1
            odd_positions.append(pos)

    all_positions = even_positions + odd_positions

    return all_positions

# def create_starting_angles(num_players):
#
#     available_angles = [0,2,4,1,3,5,0,2,4,1,3,5]

