def _draw_agent(self, img, agent):
    r, c = agent.position
    color = agent.color

    center_x = (1 + 1.5 * r) * SIZE_HEX

    center_y = math.sqrt(3) * c
    if r % 2 == 1:
        center_y += math.sqrt(3) / 2.
        center_y *= SIZE_HEX

    edge_angles = [
        math.pi / 2 - agent.angle * math.pi / 3 + 2 * math.pi / 3 *
        (edge_index) for edge_index in range(3)
    ]
    edges = [(SIZE_HEX / 2 * math.cos(angle),
              SIZE_HEX / 2 * math.sin(angle)) for angle in edge_angles]

    edges_r = [x + center_x for x, _ in edges]
    edges_c = [y + center_y for _, y in edges]

    rows, cols = polygon(edges_r, edges_c, img.shape)

    img[rows, cols, :] = 255 * color