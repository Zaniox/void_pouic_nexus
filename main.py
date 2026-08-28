"""
==================================================================================
           ⚡ VOID POUIC NEXUS : TRANSCENDENCE EDITION ⚡
                      Architecture by @zanioxx_off
          Compatible Nativement : Python 3.10 à 3.14+ (0 Dépendance)
==================================================================================
"""

import tkinter as tk
import math
import random
import time
import threading
import struct
import io
import wave
import sys
import ctypes

# =====================================================================
# 1. MOTEUR AUDIO SPATIALISÉ ULTRA-FLUIDE (WinMM 44.1 kHz PCM)
# =====================================================================
class TranscendenceAudio:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.volume = 0.85
        self.sound_cache = {}
        self.viz_level = 0.0
        self.is_muted = False

        try:
            self.winmm = ctypes.windll.winmm
        except Exception:
            self.winmm = None

    def set_volume(self, val):
        self.volume = max(0.0, min(1.0, val))

    def change_volume(self, delta):
        self.set_volume(self.volume + delta)

    def toggle_mute(self):
        self.is_muted = not self.is_muted

    def _generate_stereo_wav(self, gen_func, duration, pan=0.0):
        total_samples = int(self.sample_rate * duration)
        raw_data = bytearray()
        
        # Balance stéréo trigonométrique
        left_vol = math.cos((pan + 1.0) * math.pi / 4.0)
        right_vol = math.sin((pan + 1.0) * math.pi / 4.0)
        fade_len = int(self.sample_rate * 0.015)

        for i in range(total_samples):
            t = i / self.sample_rate
            prog = i / total_samples

            # Enveloppe Hanning douce anti-clic
            fade = 1.0
            if i < fade_len:
                fade = 0.5 * (1.0 - math.cos(math.pi * i / fade_len))
            elif i > total_samples - fade_len:
                fade = 0.5 * (1.0 - math.cos(math.pi * (total_samples - i) / fade_len))

            s = gen_func(t, prog) * fade
            s_l = int(max(-1.0, min(1.0, s * left_vol * self.volume)) * 32767)
            s_r = int(max(-1.0, min(1.0, s * right_vol * self.volume)) * 32767)
            raw_data.extend(struct.pack('<hh', s_l, s_r))

        buf = io.BytesIO()
        with wave.open(buf, 'wb') as wav:
            wav.setnchannels(2)
            wav.setsampwidth(2)
            wav.setframerate(self.sample_rate)
            wav.writeframes(raw_data)
        
        return buf.getvalue()

    def bake_audio_library(self, progress_cb=None):
        """Pré-compilation des ondes audio en mémoire vive."""
        # 1. Pouic Élastique Haute Fidélité
        def pouic_sample(t, p):
            freq = 320.0 + 1180.0 * (p ** 1.65)
            env = math.sin(p * math.pi) ** 0.65
            return (0.84 * math.sin(2 * math.pi * freq * t) + 
                    0.16 * math.sin(4 * math.pi * freq * t)) * env
        self.sound_cache['pouic'] = self._generate_stereo_wav(pouic_sample, 0.15, pan=0.0)
        if progress_cb: progress_cb(0.20, "CALIBRATING ELASTIC POUIC HARMONICS...")

        # 2. Sub-Bass Slam Explosif
        def slam_sample(t, p):
            f = 240.0 * (1.0 - p) + 36.0
            env = math.exp(-4.5 * p)
            return (0.75 * math.sin(2 * math.pi * f * t) + 0.25 * math.sin(4 * math.pi * f * t)) * env
        self.sound_cache['slam'] = self._generate_stereo_wav(slam_sample, 0.34, pan=0.0)
        if progress_cb: progress_cb(0.40, "TUNING SUB-BASS SLAM RESONANCE...")

        # 3. Notes Stéréo P-O-U-I-C (Panoramique dynamique Gauche -> Droite)
        notes = [523.25, 587.33, 659.25, 783.99, 880.00]
        pans = [-0.80, -0.40, 0.0, 0.40, 0.80]
        for idx, (freq, pan) in enumerate(zip(notes, pans)):
            def note_sample(t, p, f=freq):
                decay = math.exp(-7.8 * p)
                return (0.75 * math.sin(2 * math.pi * f * t) + 
                        0.20 * math.sin(4 * math.pi * f * t) + 
                        0.05 * math.sin(6 * math.pi * f * t)) * decay
            self.sound_cache[f'note_{idx}'] = self._generate_stereo_wav(note_sample, 0.22, pan=pan)
            if progress_cb: progress_cb(0.40 + (idx + 1) * 0.09, f"SYNTHESIZING NODE [{idx+1}/5] (PAN {pan:+.2f})...")

        # 4. Perfect Timing Chime
        def chime_sample(t, p):
            decay = math.exp(-6.5 * p)
            return (0.6 * math.sin(2 * math.pi * 1046.5 * t) + 0.4 * math.sin(2 * math.pi * 2093.0 * t)) * decay
        self.sound_cache['perfect'] = self._generate_stereo_wav(chime_sample, 0.18, pan=0.0)

        # 5. UI Tick
        def click_sample(t, p):
            return math.sin(2 * math.pi * 1400 * t) * math.exp(-30.0 * p)
        self.sound_cache['ui_click'] = self._generate_stereo_wav(click_sample, 0.05, pan=0.0)

        # 6. Surchauffe Fail
        def fail_sample(t, p):
            f = 145.0 - (p * 65.0)
            return (0.5 * math.sin(2 * math.pi * f * t) + 0.5 * math.sin(2 * math.pi * (f * 1.35) * t)) * (1.0 - p)
        self.sound_cache['fail'] = self._generate_stereo_wav(fail_sample, 0.28, pan=0.0)
        if progress_cb: progress_cb(1.0, "SPATIAL PCM MATRIX READY.")

    def play(self, name):
        if self.is_muted or self.volume <= 0.001 or name not in self.sound_cache:
            return

        wav_bytes = self.sound_cache[name]
        self.viz_level = min(1.0, self.viz_level + 0.85)

        def _worker():
            try:
                if self.winmm:
                    self.winmm.PlaySoundW(wav_bytes, None, 0x0004 | 0x0000)
                else:
                    import winsound
                    winsound.PlaySound(wav_bytes, winsound.SND_MEMORY)
            except Exception:
                pass
        threading.Thread(target=_worker, daemon=True).start()


# =====================================================================
# 2. THÈMES VISUELS CYBERPUNK
# =====================================================================
THEMES = [
    {
        "id": "amethyst",
        "name": "VOID AMETHYST",
        "primary": "#00f0ff",
        "accent": "#ff007f",
        "secondary": "#a855f7",
        "bg_glow": "#16022c",
        "stars": "#d8b4fe",
        "card": "#0c021b"
    },
    {
        "id": "cyber_ice",
        "name": "CYBER ICE",
        "primary": "#38bdf8",
        "accent": "#00f7ff",
        "secondary": "#818cf8",
        "bg_glow": "#02172b",
        "stars": "#bae6fd",
        "card": "#020f1e"
    },
    {
        "id": "solar_flare",
        "name": "SOLAR FLARE",
        "primary": "#fbbf24",
        "accent": "#ff0055",
        "secondary": "#f97316",
        "bg_glow": "#26040a",
        "stars": "#fef08a",
        "card": "#1d0408"
    },
    {
        "id": "matrix_neon",
        "name": "MATRIX NEON",
        "primary": "#22c55e",
        "accent": "#00ffcc",
        "secondary": "#4ade80",
        "bg_glow": "#021c0c",
        "stars": "#bbf7d0",
        "card": "#011509"
    }
]


# =====================================================================
# 3. SYSTÈME DE PARTICULES, COSMOS & TEXTES FLOTTANTS
# =====================================================================
class StarDust:
    def __init__(self, w, h):
        self.x = random.uniform(0, w)
        self.y = random.uniform(0, h)
        self.size = random.uniform(1.0, 2.5)
        self.speed = random.uniform(0.12, 0.45)
        self.twinkle = random.uniform(0, math.pi * 2)

    def update(self, w, h):
        self.y -= self.speed
        if self.y < 0:
            self.y = h
            self.x = random.uniform(0, w)
        self.twinkle += 0.038

class FloatingScore:
    def __init__(self, x, y, text, color, size=24):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.size = size
        self.life = 1.0
        self.vy = -3.2

    def update(self):
        self.y += self.vy
        self.vy *= 0.94
        self.life -= 0.032

class Spark:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        ang = random.uniform(0, math.pi * 2)
        spd = random.uniform(3, 12)
        self.vx = math.cos(ang) * spd
        self.vy = math.sin(ang) * spd
        self.life = 1.0
        self.decay = random.uniform(0.02, 0.045)
        self.color = color
        self.size = random.uniform(3, 8)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.93
        self.vy *= 0.93
        self.life -= self.decay
        self.size = max(0.5, self.size * 0.96)

class ShockRing:
    def __init__(self, x, y, color, max_r=220):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 12
        self.max_radius = max_r
        self.life = 1.0

    def update(self):
        self.radius += 14
        self.life = max(0.0, 1.0 - (self.radius / self.max_radius))


# =====================================================================
# 4. APPLICATION PRINCIPALE : VOID POUIC NEXUS TRANSCENDENCE
# =====================================================================
class VoidPouicNexusTranscendence:
    def __init__(self, root):
        self.root = root
        self.root.title("VOID POUIC NEXUS : TRANSCENDENCE — by @zanioxx_off")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="#03010b")

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="#03010b", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.audio = TranscendenceAudio()

        # Thèmes & Paramètres
        self.theme_idx = 0
        self.difficulty = "STANDARD"  # STANDARD, HYPER, VOID_GOD
        self.particles_enabled = True
        self.shake_enabled = True

        # États du jeu : 'BOOT', 'MENU', 'SETTINGS', 'STATS', 'COUNTDOWN', 'PLAYING_LETTERS', 'POUIC_SLAM', 'GAMEOVER'
        self.state = "BOOT"
        self.load_progress = 0.0
        self.load_log = "STARTING QUANTUM BOOT SEQUENCE..."

        self.sequence = ['P', 'O', 'U', 'I', 'C']
        self.current_step = 0
        self.round_num = 1
        self.score = 0
        self.high_score = 0
        self.total_games = 0
        self.combo = 0
        self.max_combo = 0
        self.perfect_count = 0
        self.total_pouics = 0

        # Overdrive Fever
        self.fever_gauge = 0.0
        self.is_fever = False

        # Chrono & Télémétrie
        self.time_limit = 2.4
        self.time_remaining = 2.4
        self.last_tick = time.time()
        self.step_start_time = time.time()
        self.reaction_times = []
        self.clicks_history = []
        self.countdown_timer = 3

        # Éléments graphiques
        self.phase = 0.0
        self.shake_amount = 0
        self.stars = [StarDust(self.width, self.height) for _ in range(95)]
        self.sparks = []
        self.shock_rings = []
        self.floating_scores = []
        self.buttons = {}
        self.menu_buttons = {}
        self.mouse_pos = (self.width // 2, self.height // 2)
        self.mouse_trail = []

        # Raccourcis
        self.root.bind("<Escape>", self.handle_escape)
        self.root.bind("<F11>", lambda e: self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen")))
        self.root.bind("<plus>", lambda e: self.audio.change_volume(0.1))
        self.root.bind("<KP_Add>", lambda e: self.audio.change_volume(0.1))
        self.root.bind("<minus>", lambda e: self.audio.change_volume(-0.1))
        self.root.bind("<KP_Subtract>", lambda e: self.audio.change_volume(-0.1))
        self.root.bind("<m>", lambda e: self.audio.toggle_mute())
        self.root.bind("<M>", lambda e: self.audio.toggle_mute())
        self.root.bind("<t>", lambda e: self.cycle_theme())
        self.root.bind("<T>", lambda e: self.cycle_theme())
        self.root.bind("<Key>", self.handle_keypress)
        self.canvas.bind("<Motion>", self.handle_mouse_move)
        self.canvas.bind("<Button-1>", self.handle_click)

        # Synthèse audio asynchrone
        threading.Thread(target=self.init_audio_async, daemon=True).start()

        # Boucle 60 FPS
        self.game_loop()

    def get_theme(self):
        return THEMES[self.theme_idx]

    def cycle_theme(self):
        self.theme_idx = (self.theme_idx + 1) % len(THEMES)
        self.audio.play('ui_click')

    def init_audio_async(self):
        def cb(pct, msg):
            self.load_progress = pct
            self.load_log = msg
            time.sleep(0.10)
        self.audio.bake_audio_library(cb)
        time.sleep(0.15)
        self.load_progress = 1.0

    def trigger_shake(self, amount):
        if self.shake_enabled:
            self.shake_amount = amount

    def spawn_burst(self, x, y, color, count=30, is_slam=False):
        if not self.particles_enabled:
            return
        for _ in range(count):
            self.sparks.append(Spark(x, y, color))
        self.shock_rings.append(ShockRing(x, y, color, max_r=320 if is_slam else 200))

    def add_floating_text(self, x, y, text, color, size=24):
        self.floating_scores.append(FloatingScore(x, y, text, color, size))

    def handle_mouse_move(self, event):
        self.mouse_pos = (event.x, event.y)
        self.mouse_trail.append({'x': event.x, 'y': event.y, 'life': 1.0})

    def handle_escape(self, event=None):
        if self.state in ["SETTINGS", "STATS"]:
            self.state = "MENU"
            self.audio.play('ui_click')
        elif self.state == "MENU":
            self.root.destroy()
        elif self.state in ["PLAYING_LETTERS", "POUIC_SLAM", "GAMEOVER"]:
            self.state = "MENU"
            self.audio.play('ui_click')

    # -----------------------------------------------------------------
    # GESTION DES CLAVIERS ET CLICS
    # -----------------------------------------------------------------
    def handle_keypress(self, event):
        now = time.time()
        self.clicks_history.append(now)

        if self.state == "PLAYING_LETTERS":
            char = event.char.upper()
            if char in self.sequence:
                self.validate_step(char)

        elif self.state == "POUIC_SLAM":
            if event.keysym in ["space", "Return"] or event.char.upper() == 'P':
                self.trigger_pouic_slam()

        elif self.state == "MENU":
            if event.keysym == "Return":
                self.start_countdown()
            elif event.char.lower() == 's':
                self.state = "SETTINGS"
                self.audio.play('ui_click')

        elif self.state == "GAMEOVER":
            if event.keysym in ["Return", "space"]:
                self.start_countdown()

    def handle_click(self, event):
        mx, my = event.x, event.y
        cx, cy = self.width / 2, self.height / 2
        now = time.time()
        self.clicks_history.append(now)

        if self.state == "MENU":
            for name, btn in self.menu_buttons.items():
                if (btn['x1'] <= mx <= btn['x2']) and (btn['y1'] <= my <= btn['y2']):
                    self.audio.play('ui_click')
                    if name == "PLAY":
                        self.start_countdown()
                    elif name == "SETTINGS":
                        self.state = "SETTINGS"
                    elif name == "STATS":
                        self.state = "STATS"
                    elif name == "QUIT":
                        self.root.destroy()
                    return

        elif self.state == "SETTINGS":
            if (cx - 110 <= mx <= cx + 110) and (cy + 225 <= my <= cy + 275):
                self.audio.play('ui_click')
                self.state = "MENU"
                return
            if (cx - 190 <= mx <= cx + 190) and (cy - 120 <= my <= cy - 65):
                self.cycle_theme()
                return
            if (cx - 190 <= mx <= cx + 190) and (cy - 40 <= my <= cy + 15):
                diffs = ["STANDARD", "HYPER", "VOID_GOD"]
                idx = (diffs.index(self.difficulty) + 1) % len(diffs)
                self.difficulty = diffs[idx]
                self.audio.play('ui_click')
                return
            if (cx - 190 <= mx <= cx + 190) and (cy + 40 <= my <= cy + 95):
                self.particles_enabled = not self.particles_enabled
                self.audio.play('ui_click')
                return
            if (cx - 190 <= mx <= cx + 190) and (cy + 120 <= my <= cy + 175):
                self.shake_enabled = not self.shake_enabled
                self.audio.play('ui_click')
                return

        elif self.state == "STATS":
            if (cx - 110 <= mx <= cx + 110) and (cy + 225 <= my <= cy + 275):
                self.audio.play('ui_click')
                self.state = "MENU"
                return

        elif self.state == "PLAYING_LETTERS":
            for char, orb in self.buttons.items():
                if math.hypot(mx - orb['x'], my - orb['y']) <= orb['r'] + 15:
                    self.validate_step(char)
                    break

        elif self.state == "POUIC_SLAM":
            if math.hypot(mx - cx, my - cy) <= 120:
                self.trigger_pouic_slam()

        elif self.state == "GAMEOVER":
            if (cx - 160 <= mx <= cx + 160) and (cy + 110 <= my <= cy + 185):
                self.audio.play('ui_click')
                self.start_countdown()
            elif (cx - 160 <= mx <= cx + 160) and (cy + 200 <= my <= cy + 250):
                self.audio.play('ui_click')
                self.state = "MENU"

    # -----------------------------------------------------------------
    # LOGIQUE DE JEU & CYCLES TRANSCENDENCE
    # -----------------------------------------------------------------
    def start_countdown(self):
        self.state = "COUNTDOWN"
        self.countdown_timer = 3
        self.audio.play('note_2')
        self.step_start_time = time.time()

    def start_game(self):
        self.state = "PLAYING_LETTERS"
        self.current_step = 0
        self.round_num = 1
        self.score = 0
        self.combo = 0
        self.total_games += 1
        self.fever_gauge = 0.0
        self.is_fever = False
        
        base_limits = {"STANDARD": 2.4, "HYPER": 1.7, "VOID_GOD": 1.2}
        self.time_limit = base_limits.get(self.difficulty, 2.4)
        self.time_remaining = self.time_limit

        self.step_start_time = time.time()
        self.audio.play('slam')
        self.audio.play('pouic')
        self.trigger_shake(14)
        th = self.get_theme()
        self.spawn_burst(self.width / 2, self.height / 2, th["accent"], 50)
        self.add_floating_text(self.width / 2, self.height / 2 - 110, "⚡ LINK ESTABLISHED ⚡", th["primary"], 34)

    def validate_step(self, char):
        target = self.sequence[self.current_step]
        if char == target:
            elapsed_ms = int((time.time() - self.step_start_time) * 1000)
            self.reaction_times.append(elapsed_ms)
            self.step_start_time = time.time()
            th = self.get_theme()

            # Système de Précision de Frappe
            if elapsed_ms < 200:
                rating = "PERFECT!"
                r_col = "#ffe600"
                mult = 3.0
                self.perfect_count += 1
                self.fever_gauge = min(1.0, self.fever_gauge + 0.25)
                self.audio.play('perfect')
            elif elapsed_ms < 380:
                rating = "GREAT!"
                r_col = th["primary"]
                mult = 2.0
                self.fever_gauge = min(1.0, self.fever_gauge + 0.15)
                self.audio.play(f'note_{self.current_step}')
            else:
                rating = "GOOD"
                r_col = "#ffffff"
                mult = 1.0
                self.fever_gauge = min(1.0, self.fever_gauge + 0.08)
                self.audio.play(f'note_{self.current_step}')

            self.combo += 1
            if self.combo > self.max_combo:
                self.max_combo = self.combo

            fever_mult = 2.0 if self.is_fever else 1.0
            pts = int(100 * self.round_num * mult * fever_mult)
            self.score += pts

            orb = self.buttons[char]
            self.spawn_burst(orb['x'], orb['y'], th["primary"] if not self.is_fever else "#ffe600", 22)
            self.add_floating_text(orb['x'], orb['y'] - 38, f"{rating} +{pts}", r_col, 20)

            self.current_step += 1

            if self.current_step >= len(self.sequence):
                self.state = "POUIC_SLAM"
                self.time_remaining = max(0.65, self.time_limit * 0.6)
            else:
                self.time_remaining = self.time_limit
        else:
            self.game_over()

    def trigger_pouic_slam(self):
        self.audio.play('pouic')
        self.audio.play('slam')
        self.trigger_shake(22)
        cx, cy = self.width / 2, self.height / 2
        th = self.get_theme()
        self.total_pouics += 1

        slam_pts = 600 * self.combo * (2 if self.is_fever else 1)
        self.score += slam_pts
        self.spawn_burst(cx, cy, th["accent"] if not self.is_fever else "#ffe600", 80, is_slam=True)
        self.add_floating_text(cx, cy - 80, f"💥 POUIC SLAM ! +{slam_pts}", "#ffe600", 36)

        self.round_num += 1
        accel_factors = {"STANDARD": 0.88, "HYPER": 0.84, "VOID_GOD": 0.80}
        factor = accel_factors.get(self.difficulty, 0.88)
        base_limits = {"STANDARD": 2.4, "HYPER": 1.7, "VOID_GOD": 1.2}
        base = base_limits.get(self.difficulty, 2.4)

        self.time_limit = max(0.38, base * (factor ** (self.round_num - 1)))
        self.time_remaining = self.time_limit
        self.current_step = 0
        self.step_start_time = time.time()
        self.state = "PLAYING_LETTERS"

    def game_over(self):
        self.audio.play('fail')
        self.trigger_shake(26)
        self.state = "GAMEOVER"
        self.is_fever = False
        if self.score > self.high_score:
            self.high_score = self.score
        self.spawn_burst(self.width / 2, self.height / 2, "#ff0055", 85)

    def calculate_cps(self):
        now = time.time()
        self.clicks_history = [t for t in self.clicks_history if now - t <= 2.0]
        return len(self.clicks_history) / 2.0

    # -----------------------------------------------------------------
    # COMPOSANTS VISUELS & PANNEAUX GLASSMORPHISM
    # -----------------------------------------------------------------
    def draw_glass_card(self, x, y, w, h, border_color, fill_color=None):
        th = self.get_theme()
        fill_col = fill_color if fill_color else th["card"]
        for g in [14, 6]:
            self.canvas.create_rectangle(x - w/2 - g, y - h/2 - g, x + w/2 + g, y + h/2 + g, outline=border_color, width=1)
        self.canvas.create_rectangle(x - w/2, y - h/2, x + w/2, y + h/2, fill=fill_col, outline="#ffffff", width=2)

    def draw_interactive_btn(self, tag, x, y, w, h, title, subtitle="", border_col="#00f0ff"):
        mx, my = self.mouse_pos
        is_hover = (x - w/2 <= mx <= x + w/2) and (y - h/2 <= my <= y + h/2)
        th = self.get_theme()

        self.menu_buttons[tag] = {'x1': x - w/2, 'y1': y - h/2, 'x2': x + w/2, 'y2': y + h/2}
        col = th["accent"] if is_hover else border_col

        if is_hover:
            self.canvas.create_rectangle(x - w/2 - 4, y - h/2 - 4, x + w/2 + 4, y + h/2 + 4, outline=col, width=2)
            fill_c = "#1e0438"
        else:
            fill_c = th["card"]

        self.canvas.create_rectangle(x - w/2, y - h/2, x + w/2, y + h/2, fill=fill_c, outline=col, width=2)

        if subtitle:
            self.canvas.create_text(x, y - 12, text=title, fill="#ffffff", font=("Impact", 20, "bold"))
            self.canvas.create_text(x, y + 16, text=subtitle, fill=th["primary"], font=("Consolas", 11, "bold"))
        else:
            self.canvas.create_text(x, y, text=title, fill="#ffffff", font=("Impact", 22, "bold"))

    # -----------------------------------------------------------------
    # BOUCLE PRINCIPALE 60 FPS
    # -----------------------------------------------------------------
    def game_loop(self):
        now = time.time()
        dt = now - self.last_tick
        self.last_tick = now
        self.phase += 0.08
        th = self.get_theme()

        # Gestion Overdrive
        if self.fever_gauge >= 1.0 and not self.is_fever:
            self.is_fever = True
            self.add_floating_text(self.width / 2, 120, "⚡ OVERDRIVE ACTIVE (x2 POINTS) ⚡", "#ffe600", 26)
        if self.is_fever:
            self.fever_gauge = max(0.0, self.fever_gauge - dt * 0.15)
            if self.fever_gauge <= 0.0:
                self.is_fever = False

        self.canvas.delete("all")
        self.menu_buttons.clear()

        # Screen Shake
        off_x, off_y = 0, 0
        if self.shake_amount > 0:
            off_x = random.uniform(-self.shake_amount, self.shake_amount)
            off_y = random.uniform(-self.shake_amount, self.shake_amount)
            self.shake_amount *= 0.85

        cx, cy = self.width / 2 + off_x, self.height / 2 + off_y

        # 1. Cosmos de fond & Nébuleuse vivante
        pulse = (math.sin(self.phase * 0.5) + 1.0) * 0.5
        r_glow = 390 + pulse * 55
        self.canvas.create_oval(cx - r_glow, cy - r_glow, cx + r_glow, cy + r_glow, fill=th["bg_glow"], outline="")

        for s in self.stars:
            s.update(self.width, self.height)
            alpha = (math.sin(s.twinkle) + 1.0) * 0.5
            if alpha > 0.15:
                self.canvas.create_oval(s.x - s.size, s.y - s.size, s.x + s.size, s.y + s.size, fill=th["stars"], outline="")

        # 2. Visualiseur Audio Réactif
        self.audio.viz_level *= 0.91
        num_bars = 36
        bw = self.width / num_bars
        for i in range(num_bars):
            wave_h = (math.sin(self.phase * 2.5 + i * 0.35) + 1.0) * 0.5
            bh = 4 + (self.audio.viz_level * 75.0 * wave_h)
            bx = i * bw
            bar_col = "#ffe600" if self.is_fever else (th["primary"] if i % 2 == 0 else th["accent"])
            self.canvas.create_rectangle(bx + 3, self.height - bh, bx + bw - 3, self.height, fill=bar_col, outline="")

        # 3. Particules & Ondes de Choc
        for w in self.shock_rings[:]:
            w.update()
            if w.life <= 0:
                self.shock_rings.remove(w)
            else:
                self.canvas.create_oval(w.x - w.radius, w.y - w.radius, w.x + w.radius, w.y + w.radius, outline=w.color, width=max(1, int(4 * w.life)))

        for p in self.sparks[:]:
            p.update()
            if p.life <= 0:
                self.sparks.remove(p)
            else:
                self.canvas.create_oval(p.x - p.size, p.y - p.size, p.x + p.size, p.y + p.size, fill=p.color, outline="")

        for ft in self.floating_scores[:]:
            ft.update()
            if ft.life <= 0:
                self.floating_scores.remove(ft)
            else:
                self.canvas.create_text(ft.x, ft.y, text=ft.text, fill=ft.color, font=("Impact", int(ft.size * ft.life), "bold"))

        # 4. HUD Supérieur
        self.canvas.create_text(140, 30, text="VOID POUIC NEXUS", fill=th["primary"], font=("Impact", 16))
        self.canvas.create_text(140, 48, text="by @zanioxx_off", fill=th["accent"], font=("Consolas", 11, "bold"))

        vol_pct = int(self.audio.volume * 100) if not self.audio.is_muted else 0
        vol_txt = f"🔊 {vol_pct}%" if not self.audio.is_muted else "🔇 MUTE"
        self.canvas.create_text(self.width - 100, 38, text=vol_txt, fill=th["primary"], font=("Consolas", 13, "bold"))

        # =============================================================
        # 5. MACHINE D'ÉTATS
        # =============================================================

        # --- A. BOOT CINÉMATIQUE ---
        if self.state == "BOOT":
            ring_r = 80
            self.canvas.create_arc(cx - ring_r, cy - 70 - ring_r, cx + ring_r, cy - 70 + ring_r, start=self.phase * 50, extent=130, outline=th["primary"], width=5, style="arc")
            self.canvas.create_arc(cx - ring_r + 12, cy - 70 - ring_r + 12, cx + ring_r - 12, cy - 70 + ring_r - 12, start=-self.phase * 40, extent=170, outline=th["accent"], width=3, style="arc")

            bar_w = 440
            self.canvas.create_rectangle(cx - bar_w/2, cy + 60, cx + bar_w/2, cy + 74, outline=th["secondary"], width=2)
            self.canvas.create_rectangle(cx - bar_w/2, cy + 60, cx - bar_w/2 + bar_w * self.load_progress, cy + 74, fill=th["primary"], outline="")
            self.canvas.create_text(cx, cy + 105, text=f"// {self.load_log} [{int(self.load_progress * 100)}%]", fill="#ffffff", font=("Consolas", 12))

            if self.load_progress >= 1.0:
                self.audio.play('pouic')
                self.state = "MENU"

        # --- B. MENU PRINCIPAL INTERACTIF ---
        elif self.state == "MENU":
            self.canvas.create_text(cx, cy - 170, text="VOID POUIC NEXUS", fill=th["primary"], font=("Impact", 68, "bold"))
            self.canvas.create_text(cx, cy - 105, text="⚡ TRANSCENDENCE // BY @ZANIOXX_OFF ⚡", fill=th["accent"], font=("Consolas", 18, "bold"))
            self.canvas.create_text(cx, cy - 65, text=f"MODE : {self.difficulty}  |  THÈME : {th['name']}", fill="#94a3b8", font=("Consolas", 12, "bold"))

            self.draw_interactive_btn("PLAY", cx, cy + 5, 340, 75, "🎮 JOUER", "[CLIQUE OU APPUIS SUR ENTRÉE]", border_col=th["primary"])
            self.draw_interactive_btn("SETTINGS", cx, cy + 95, 340, 60, "⚙️ PARAMÈTRES", "[THÈMES, AUDIO, DIFFICULTÉ]", border_col=th["secondary"])
            self.draw_interactive_btn("STATS", cx, cy + 170, 340, 60, "📊 STATISTIQUES", "[RECORDS ET TÉLÉMÉTRIE]", border_col=th["secondary"])
            self.draw_interactive_btn("QUIT", cx, cy + 245, 340, 50, "❌ QUITTER", "", border_col="#ff0055")

        # --- C. PANNEAU DE PARAMÈTRES ---
        elif self.state == "SETTINGS":
            self.draw_glass_card(cx, cy, 540, 560, th["primary"])
            self.canvas.create_text(cx, cy - 230, text="⚙️ PARAMÈTRES DU NEXUS", fill=th["primary"], font=("Impact", 32))

            self.draw_interactive_btn("THEME_TOGGLE", cx, cy - 95, 380, 55, f"🎨 THÈME : {th['name']}", "[CLIQUE POUR CHANGER]", th["secondary"])
            self.draw_interactive_btn("DIFF_TOGGLE", cx, cy - 15, 380, 55, f"⚡ DIFFICULTÉ : {self.difficulty}", "[CLIQUE POUR CHANGER]", th["secondary"])
            
            p_txt = "ACTIVÉES" if self.particles_enabled else "DÉSACTIVÉES"
            self.draw_interactive_btn("PARTICLES_TOGGLE", cx, cy + 65, 380, 55, f"✨ PARTICULES : {p_txt}", "[CLIQUE POUR ACTIVER/DÉSACTIVER]", th["secondary"])

            s_txt = "ACTIVÉES" if self.shake_enabled else "DÉSACTIVÉES"
            self.draw_interactive_btn("SHAKE_TOGGLE", cx, cy + 145, 380, 55, f"📳 SECOUSSES D'ÉCRAN : {s_txt}", "[CLIQUE POUR ACTIVER/DÉSACTIVER]", th["secondary"])

            self.draw_interactive_btn("BACK_MENU", cx, cy + 245, 220, 48, "RETOUR", "[OU ÉCHAP]", "#ff0055")

        # --- D. PANNEAU DE STATISTIQUES & TÉLÉMÉTRIE ---
        elif self.state == "STATS":
            self.draw_glass_card(cx, cy, 560, 560, th["accent"])
            self.canvas.create_text(cx, cy - 230, text="📊 TÉLÉMÉTRIE & RECORDS", fill=th["accent"], font=("Impact", 32))

            avg_react = int(sum(self.reaction_times[-20:]) / max(1, len(self.reaction_times[-20:]))) if self.reaction_times else 0

            stats_lines = [
                f"MEILLEUR SCORE : {self.high_score:,} PTS",
                f"PARTIES JOUÉES : {self.total_games}",
                f"MAX COMBO ATTEINT : x{self.max_combo}",
                f"TEMPS DE RÉACTION MOYEN : {avg_react} ms",
                f"PERFECT TIMINGS : {self.perfect_count}",
                f"POUIC SLAMS RÉUSSIS : {self.total_pouics}"
            ]

            for idx, line in enumerate(stats_lines):
                self.canvas.create_text(cx, cy - 150 + idx * 42, text=line, fill="#ffffff", font=("Consolas", 14, "bold"))

            # Mini-Graphique de Télémétrie en temps réel
            self.canvas.create_text(cx, cy + 120, text="// HISTORIQUE RÉACTION (MS)", fill=th["primary"], font=("Consolas", 11, "bold"))
            gw = 360
            gh = 40
            gx = cx - gw / 2
            gy = cy + 140
            self.canvas.create_rectangle(gx, gy, gx + gw, gy + gh, outline=th["secondary"], width=1)
            
            recent_times = self.reaction_times[-12:]
            if recent_times:
                step_w = gw / 12
                for i, rtime in enumerate(recent_times):
                    bar_h = min(gh, int((rtime / 600.0) * gh))
                    bx = gx + i * step_w
                    self.canvas.create_rectangle(bx + 2, gy + gh - bar_h, bx + step_w - 2, gy + gh, fill=th["primary"], outline="")

            self.draw_interactive_btn("BACK_MENU", cx, cy + 240, 220, 48, "RETOUR", "[OU ÉCHAP]", th["primary"])

        # --- E. COMPTE À REBOURS AVANT MATCH ---
        elif self.state == "COUNTDOWN":
            elapsed = time.time() - self.step_start_time
            count = 3 - int(elapsed)
            if count > 0:
                self.canvas.create_text(cx, cy - 40, text=str(count), fill=th["primary"], font=("Impact", 120, "bold"))
                self.canvas.create_text(cx, cy + 60, text="PREPARE YOUR REFLEXES...", fill="#ffffff", font=("Consolas", 18, "bold"))
            else:
                self.start_game()

        # --- F. JEU EN COURS (LETTRES P-O-U-I-C & POUIC SLAM) ---
        elif self.state in ["PLAYING_LETTERS", "POUIC_SLAM"]:
            self.time_remaining -= dt
            if self.time_remaining <= 0:
                self.game_over()

            cps = self.calculate_cps()
            avg_react = int(sum(self.reaction_times[-5:]) / max(1, len(self.reaction_times[-5:]))) if self.reaction_times else 0

            # HUD Live
            self.canvas.create_text(cx - 250, 80, text=f"SCORE: {self.score:,}", fill=th["primary"] if not self.is_fever else "#ffe600", font=("Impact", 26))
            self.canvas.create_text(cx + 250, 80, text=f"CYCLE: x{self.round_num}", fill=th["accent"], font=("Impact", 26))
            self.canvas.create_text(cx, 80, text=f"COMBO: x{self.combo}  |  {cps:.1f} CPS  |  {avg_react} ms", fill="#ffffff", font=("Consolas", 13, "bold"))

            # Jauge Overdrive
            fg_w = 280
            self.canvas.create_rectangle(cx - fg_w/2, 105, cx + fg_w/2, 113, outline=th["secondary"], width=1)
            self.canvas.create_rectangle(cx - fg_w/2, 105, cx - fg_w/2 + fg_w * self.fever_gauge, 113, fill="#ffe600" if self.is_fever else th["primary"], outline="")

            # Timer Circulaire
            timer_r = 195
            ratio = max(0.0, self.time_remaining / self.time_limit)
            gauge_col = th["primary"] if ratio > 0.4 else ("#ffe600" if ratio > 0.2 else "#ff0055")
            self.canvas.create_arc(cx - timer_r, cy - timer_r, cx + timer_r, cy + timer_r, start=90, extent=-360 * ratio, outline=gauge_col, width=6, style="arc")

            # Disposition des Orbes
            self.buttons.clear()
            n = len(self.sequence)
            radius_layout = 245
            start_ang = -math.pi * 0.82
            end_ang = -math.pi * 0.18
            coords = []

            for i, char in enumerate(self.sequence):
                ang = start_ang + i * (end_ang - start_ang) / (n - 1)
                bx = cx + math.cos(ang) * radius_layout
                by = cy + math.sin(ang) * (radius_layout * 0.72) + 30
                coords.append((bx, by))
                self.buttons[char] = {'x': bx, 'y': by, 'r': 44}

            # Faisceaux Lasers d'interconnexion & Électrons voyageurs
            for i in range(len(coords) - 1):
                laser_col = "#ffe600" if self.is_fever else ("#3a0f66" if i >= self.current_step else th["primary"])
                self.canvas.create_line(coords[i][0], coords[i][1], coords[i+1][0], coords[i+1][1], fill=laser_col, width=3)
                
                # Électron en mouvement
                spark_t = (self.phase * 2.0 + i * 0.5) % 1.0
                ex = coords[i][0] + (coords[i+1][0] - coords[i][0]) * spark_t
                ey = coords[i][1] + (coords[i+1][1] - coords[i][1]) * spark_t
                self.canvas.create_oval(ex - 3, ey - 3, ex + 3, ey + 3, fill="#ffffff", outline="")

            for i, char in enumerate(self.sequence):
                bx, by = coords[i]
                r = 44
                is_target = (i == self.current_step) and (self.state == "PLAYING_LETTERS")
                is_done = (i < self.current_step)

                if is_target:
                    pulse_target = math.sin(self.phase * 2.2) * 5
                    self.canvas.create_oval(bx - r - 12 - pulse_target, by - r - 12 - pulse_target, bx + r + 12 + pulse_target, by + r + 12 + pulse_target, outline=th["accent"], width=2)

                fill_col = th["primary"] if is_done else (th["card"] if is_target else "#06010d")
                border_col = "#ffffff" if is_target else (th["primary"] if is_done else th["secondary"])

                self.canvas.create_oval(bx - r, by - r, bx + r, by + r, fill=fill_col, outline=border_col, width=2)
                self.canvas.create_text(bx, by, text=char, fill="#000000" if is_done else "#ffffff", font=("Impact", 30, "bold"))

            # Affichage Central dynamique
            if self.state == "PLAYING_LETTERS":
                target_char = self.sequence[self.current_step]
                self.canvas.create_text(cx, cy, text=f"FRAPPE : {target_char}", fill="#ffffff", font=("Impact", 32))
            elif self.state == "POUIC_SLAM":
                pulse_slam = math.sin(self.phase * 3.0) * 9
                self.canvas.create_oval(cx - 75 - pulse_slam, cy - 75 - pulse_slam, cx + 75 + pulse_slam, cy + 75 + pulse_slam, fill=th["accent"], outline="#ffe600", width=3)
                self.canvas.create_text(cx, cy, text="POUIC\nSLAM!", fill="#ffffff", font=("Impact", 26, "bold"), justify="center")

        # --- G. SURCHAUFFE / GAME OVER ---
        elif self.state == "GAMEOVER":
            self.canvas.create_text(cx, cy - 140, text="SURCHAUFFE DU SYSTÈME", fill="#ff0055", font=("Impact", 52, "bold"))
            self.canvas.create_text(cx, cy - 70, text=f"SCORE FINAL : {self.score:,}   |   RECORD : {self.high_score:,}", fill=th["primary"], font=("Consolas", 20, "bold"))

            rank_str = "SSS VOID EMPEROR" if self.round_num >= 14 else ("S NEXUS MASTER" if self.round_num >= 9 else ("A SPEED RUNNER" if self.round_num >= 5 else "B NOVICE"))
            self.canvas.create_text(cx, cy - 20, text=f"RANG ÉVALUÉ : {rank_str} (MAX COMBO: x{self.max_combo})", fill="#ffe600", font=("Consolas", 14, "bold"))

            self.draw_interactive_btn("RETRY", cx, cy + 145, 300, 75, "🔄 REJOUER", "[CLIQUE OU ENTRÉE]", border_col=th["primary"])
            self.draw_interactive_btn("MENU_BTN", cx, cy + 225, 300, 50, "🏠 MENU PRINCIPAL", "", border_col=th["secondary"])

        # 6. Traînée de Souris & Viseur Cybernétique
        for pt in self.mouse_trail:
            pt['life'] -= 0.08
            r = int(6 * pt['life'])
            if r > 0:
                self.canvas.create_oval(pt['x'] - r, pt['y'] - r, pt['x'] + r, pt['y'] + r, fill=th["primary"], outline="")
        self.mouse_trail = [pt for pt in self.mouse_trail if pt['life'] > 0]

        mx, my = self.mouse_pos
        self.canvas.create_arc(mx - 12, my - 12, mx + 12, my + 12, start=self.phase * 60, extent=100, outline=th["primary"], width=2, style="arc")
        self.canvas.create_arc(mx - 12, my - 12, mx + 12, my + 12, start=self.phase * 60 + 180, extent=100, outline=th["accent"], width=2, style="arc")
        self.canvas.create_oval(mx - 2, my - 2, mx + 2, my + 2, fill="#ffffff", outline="")

        # 7. Barre d'Aide Inférieure
        self.canvas.create_text(
            self.width / 2, self.height - 20,
            text="[P][O][U][I][C] Clavier/Souris  |  [ESPACE] Pouic Slam  |  [T] Thèmes  |  [M] Muet  |  [Échap] Retour  •  by @zanioxx_off",
            fill="#64748b", font=("Consolas", 11)
        )

        self.root.after(16, self.game_loop)


if __name__ == "__main__":
    root = tk.Tk()
    app = VoidPouicNexusTranscendence(root)
    root.mainloop()
