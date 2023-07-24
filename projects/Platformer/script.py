import UniPy as up
import math, random

player = up.GetObj("player")
btJ = up.GetObj("btJ")
tx = up.GetObj("tx!")
controller = None

speed = 5
force = 100

up.SetCamera("player")

factor = min(up.wWidth / up.pWidth, up.wWidth / up.wHeight) if up.wWidth > up.pWidth and up.wHeight > up.pHeight else min(up.wWidth / up.pWidth, up.wHeight / up.pHeight)

CHUNK_SIZE = 16
BLOCK_SIZE = (128 * factor, 128 * factor)

blocks = {
    1: "grass",
    2: "dirt",
    3: "plant",
    4: "stone",
    5: "sand"
}

p = {}

def init_p(seed):
    global p

    random.seed(seed)
    p[seed] = [random.randint(0, 255) for _ in range(256)]

def fade(t):
    return 6 * t**5 - 15 * t**4 + 10 * t**3

def lerp(t, a, b):
    return a + t * (b - a)

def grad(hash, x, y):
    h = hash & 15
    u = x if h < 8 else y
    v = y if h < 4 else (x if h == 12 or h == 14 else 0)
    return (u if (h & 1) == 0 else -u) + (v if (h & 2) == 0 else -v)

def noise(x, y, seed):
    X = math.floor(x) & 255
    Y = math.floor(y) & 255
    x -= math.floor(x)
    y -= math.floor(y)
    u = fade(x)
    v = fade(y)
    A = p[seed][X] + Y
    B = p[seed][X + 1] + Y
    AA = p[seed][A]
    AB = p[seed][A + 1]
    BA = p[seed][B]
    BB = p[seed][B + 1]
    return lerp(v, lerp(u, grad(p[seed][AA], x, y), grad(p[seed][BA], x - 1, y)), lerp(u, grad(p[seed][AB], x, y - 1), grad(p[seed][BB], x - 1, y - 1)))

def generate_chunk(chunk_x, chunk_y, seed):
    random.seed(seed)
    trailBlock = random.choice([1, 5])
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = chunk_x * CHUNK_SIZE + x_pos
            target_y = chunk_y * CHUNK_SIZE + y_pos
            tile_type = 0 # nothing
            height = int(noise(target_x * 0.1, target_y * 0.1, seed) * controller.height)
            
            if target_y > 10 - height:
                tile_type = random.choice([2, 4, 4]) if target_y == 10 else 4
            elif target_y == 9 - height:
                if random.randint(1, 2) == 1 and trailBlock == 5 and target_y > 6:
                    tile_type = 5
                else: tile_type = 2
            elif target_y > 8 - height:
                tile_type = 2 # dirt
            elif target_y == 8 - height:
                tile_type = trailBlock if target_y > 6 else 1
            elif target_y == 8 - height - 1:
                if random.randint(1, 4) == 1:
                    tile_type = 3 # plant
            if tile_type != 0:
                up.CloneObject(blocks[tile_type])
                up.objects[-1].rect.topleft = (target_x * BLOCK_SIZE[0], target_y * BLOCK_SIZE[1])

def Start():
    global controller
    
    controller = up.GetObj("landscape_controller").GetModule("landscape_controller")

    seed = random.randint(-999999, 999999)  # Замените на желаемый сид
        
    init_p(seed)
    
    generate_chunk(0, 0, seed)  # Генерация первого чанка с начальными координатами (0, 0)
    
def jump():
    if player.bottomCollided:
        player.addForce(force)

def Update():
    
    tx.text = f"x: $(0, 0, 255){player.rect.x}$(0,0,0), y: $(255, 0, 0){player.rect.y}"

btJ.onPressed = jump