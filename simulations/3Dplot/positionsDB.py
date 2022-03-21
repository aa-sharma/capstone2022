# Dictonaries of hand positions
# Each contains 21 keys (xyz for 5 fingers, palm and wrist) where the values are lists of coordinates
position1 = {
    'thumbA' : [3, 0, 0],
    'thumbB' : [3, 8, -1],
    'thumbC' : [3, 8, -1],

    'indexA' : [3, 8, 3],
    'indexB' : [3, 9, 0],
    'indexC' : [3, 8, -1],

    'middleA' : [2, 8, 3],
    'middleB' : [2, 10, 5],
    'middleC' : [2, 14, 8],

    'ringA' : [-1, 8, 3],
    'ringB' : [-1, 10, 5],
    'ringC' : [-1, 14, 8],

    'pinkyA' : [-3, 8, 3],
    'pinkyB' : [-3, 10, 5],
    'pinkyC' : [-3, 14, 8],

    'wristA' : [0, 0, 0],
    'wristB' : [-3, 0, 0],
    'wristC' : [3, 0, 0],
    'wristD' : [-3, -8, 0],
    'wristE' : [3, -8, 0]
}

horizontal_ok = {
    'x_thumb' : [0, 0, 0, 0],
    'y_thumb' : [6, 9, 5, 0],
    'z_thumb' : [3, -1, -2, -1],

    'x_index' : [-2, -2, -2],
    'y_index' : [5, 9, 11],
    'z_index' : [4, 8, 10],
    
    'x_middle' : [-4, -4, -4],
    'y_middle' : [5, 9, 11],
    'z_middle' : [4, 8, 10],

    'x_ring' : [-6, -6, -6],
    'y_ring' : [5, 9, 11],
    'z_ring' : [4, 8, 10],

    'x_pinky' : [],
    'y_pinky' : [],
    'z_pinky' : [],

    'x_palm' : [-6, -6, -4, -2, 0, 0],
    'y_palm' : [0, 5, 5, 5, 6, 0],
    'z_palm' : [-1, 4, 4, 4, 3, -1],

    'x_wrist' : [-6, 0, 0, -6, -6],    #order matters for connecting points properly
    'y_wrist' : [-5, -5, 0, 0, -5],
    'z_wrist' : [-1, -1, -1, -1, -1]
}

peace = {
    'x_thumb' : [],
    'y_thumb' : [],
    'z_thumb' : [],

    'x_index' : [],
    'y_index' : [],
    'z_index' : [],
    
    'x_middle' : [],
    'y_middle' : [],
    'z_middle' : [],

    'x_ring' : [],
    'y_ring' : [],
    'z_ring' : [],

    'x_pinky' : [],
    'y_pinky' : [],
    'z_pinky' : [],

    'x_palm' : [],
    'y_palm' : [],
    'z_palm' : [],

    'x_wrist' : [],    #order matters for connecting points properly
    'y_wrist' : [],
    'z_wrist' : []
}