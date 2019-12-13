
with open("D8I.txt") as f:
    image_text = f.readline().rstrip()

image_size = (25, 6)
image_area = image_size[0] * image_size[1]

image = \
    [
        [
            int(n)
            for n in list(image_text[layer_idx * image_area : (layer_idx + 1) * image_area])
        ]
        for layer_idx in range(len(image_text) // image_area)
    ]

image_grid = \
[
    [
        [
            [
                int(n)
                for n in list(row)
            ]
            for row in layer[row_idx: row_idx + image_size[0]]
        ]
        for row_idx in range(0, image_area, image_size[0])
    ]
    for layer in
    [
        image_text[layer_idx * image_area : (layer_idx + 1) * image_area]
        for layer_idx in range(len(image_text) // image_area)
    ]
]

zero_digits = [layer.count(0) for layer in image]
fewest_layer_idx = zero_digits.index(min(zero_digits))
fewest_layer = image[fewest_layer_idx]
n = fewest_layer.count(1) * fewest_layer.count(2)
print(n)

