eye_opening_threshold = 0.024
mouth_open_threshold = 0.035
squinting_threshold = 0.016
pucker_ratio_threshold = 0.28

erk_mouth_diff = 0.012
erk_eye_squint = 0.025

smile_teeth_width_ratio = 0.38
smile_teeth_gap = 0.015

# =========================
# Temporal Smoothing
# =========================

STABILITY_FRAMES = 5

expression_counters = {
    "erk": 0,
    "wow": 0,
    "tongue": 0,
    "shock": 0,
    "glare": 0,
    "smirk": 0
}

def update_expression(expression_name, detected):
    global expression_counters

    if detected:
        expression_counters[expression_name] += 1
    else:
        expression_counters[expression_name] = 0

    return expression_counters[expression_name] >= STABILITY_FRAMES

# =========================
# Expression Detection
# =========================

def cat_shock(face_points):
    l_top, l_bot = face_points[159], face_points[145]
    r_top, r_bot = face_points[386], face_points[374]

    eye_opening = (
        abs(l_top.y - l_bot.y) +
        abs(r_top.y - r_bot.y)
    ) / 2.0

    return eye_opening > eye_opening_threshold


def cat_tongue(face_points):
    mouth_open = abs(face_points[13].y - face_points[14].y)
    return mouth_open > mouth_open_threshold


def cat_glare(face_points):
    l_top, l_bot = face_points[159], face_points[145]
    r_top, r_bot = face_points[386], face_points[374]

    eye_squint = (
        abs(l_top.y - l_bot.y) +
        abs(r_top.y - r_bot.y)
    ) / 2.0

    mouth_lift = (
        (face_points[0].y - face_points[61].y) +
        (face_points[0].y - face_points[291].y)
    ) / 2.0

    return eye_squint < squinting_threshold and mouth_lift < 0.005


def cat_smirk(face_points):
    mouth_width = abs(face_points[61].x - face_points[291].x)
    face_width = abs(face_points[234].x - face_points[454].x)

    width_ratio = mouth_width / face_width
    mouth_gap = abs(face_points[13].y - face_points[14].y)

    mouth_diff = abs(
        (face_points[0].y - face_points[61].y) -
        (face_points[0].y - face_points[291].y)
    )

    return (
        width_ratio > smile_teeth_width_ratio and
        mouth_gap > smile_teeth_gap and
        mouth_diff < 0.010
    )


def cat_wow(face_points):
    mouth_width = abs(face_points[61].x - face_points[291].x)
    face_width = abs(face_points[234].x - face_points[454].x)

    current_ratio = mouth_width / face_width

    return current_ratio < pucker_ratio_threshold


def cat_erk(face_points):
    mouth_diff = abs(face_points[61].y - face_points[291].y)

    l_eye = abs(face_points[159].y - face_points[145].y)
    r_eye = abs(face_points[386].y - face_points[374].y)

    avg_eye = (l_eye + r_eye) / 2.0

    return (
        mouth_diff > erk_mouth_diff and
        avg_eye < erk_eye_squint
    )

# =========================
# Main Meme Decision
# =========================

def detect_meme(face_points):

    erk_active = update_expression(
        "erk",
        cat_erk(face_points)
    )

    wow_active = update_expression(
        "wow",
        cat_wow(face_points)
    )

    tongue_active = update_expression(
        "tongue",
        cat_tongue(face_points)
    )

    shock_active = update_expression(
        "shock",
        cat_shock(face_points)
    )

    glare_active = update_expression(
        "glare",
        cat_glare(face_points)
    )

    smirk_active = update_expression(
        "smirk",
        cat_smirk(face_points)
    )

    if erk_active:
        return "assets/cat-erk.jpg"

    elif wow_active:
        return "assets/cat-wow.jpg"

    elif tongue_active:
        return "assets/cat-tongue.jpeg"

    elif shock_active:
        return "assets/cat-shock.jpeg"

    elif glare_active:
        return "assets/cat-glare.jpeg"

    elif smirk_active:
        return "assets/cat-smirk.jpg"

    return "assets/larry.jpeg"

# Auto Caption System
def get_caption(cat_image_path):

    captions = {

        "assets/cat-shock.jpeg":
            "What!!! wait What!! ",

        "assets/cat-glare.jpeg":
            "judging silently...",

        "assets/cat-erk.jpg":
            "Hmm, I knew it.",

        "assets/cat-smirk.jpg":
            "ohhh~ girls",

        "assets/cat-wow.jpg":
            "Uoo Hooo",

        "assets/cat-tongue.jpeg":
            "blehhh"
    }

    return captions.get(cat_image_path, "")
