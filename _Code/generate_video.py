#!/usr/bin/env python3
"""
M3 Internal Assessment - Animation Video Generator
Topic: Eigenvalues and Eigenvectors: Visualizing Invariant Directions & Matrix Scaling
Target: 1080p 16:9 Landscape MP4 (1920x1080, 24 fps, Exactly 5:00 minutes = 7200 frames)
"""

import sys
import os
import subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, ArrowStyle, FancyArrowPatch, Circle, Polygon
import matplotlib.gridspec as gridspec

# Path setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
OUTPUT_VIDEO = os.path.join(PROJECT_DIR, "_Video.mp4")

# Locate ffmpeg
FFMPEG_CANDIDATES = [
    os.path.join(PROJECT_DIR, "../venv/bin/ffmpeg"),
    os.path.join(BASE_DIR, "ffmpeg"),
    "ffmpeg"
]
FFMPEG_BIN = None
for cand in FFMPEG_CANDIDATES:
    if os.path.exists(cand) and os.access(cand, os.X_OK):
        FFMPEG_BIN = cand
        break
    # Check if in PATH
    try:
        res = subprocess.run(["which", cand], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0:
            FFMPEG_BIN = res.stdout.strip()
            break
    except Exception:
        pass

if not FFMPEG_BIN:
    try:
        import imageio_ffmpeg
        FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        FFMPEG_BIN = "ffmpeg"

print(f"[+] Using ffmpeg binary: {FFMPEG_BIN}")
print(f"[+] Target output video: {OUTPUT_VIDEO}")

# Constants
WIDTH = 1920
HEIGHT = 1080
DPI = 120
FPS = 24
TOTAL_DURATION = 300  # seconds (5 minutes)
TOTAL_FRAMES = TOTAL_DURATION * FPS

# Colors
C_BG = "#0b0f19"
C_PANEL = "#111827"
C_BORDER = "#1f2937"
C_GRID = "#1e293b"
C_AXIS = "#475569"
C_TEXT = "#f8fafc"
C_MUTED = "#94a3b8"
C_CYAN = "#38bdf8"
C_GOLD = "#fbbf24"
C_ROSE = "#f43f5e"
C_EMERALD = "#34d399"
C_PURPLE = "#a855f7"

def init_figure():
    fig = plt.figure(figsize=(WIDTH / DPI, HEIGHT / DPI), dpi=DPI, facecolor=C_BG)
    return fig

def add_header_footer(ax_bg, scene_num, scene_title, current_time_str, progress_frac):
    ax_bg.set_xlim(0, 1)
    ax_bg.set_ylim(0, 1)
    ax_bg.axis('off')
    
    # Header bar
    ax_bg.fill_between([0, 1], [0.93, 0.93], [1, 1], color="#0f172a", zorder=1)
    ax_bg.plot([0, 1], [0.93, 0.93], color="#334155", lw=1.5, zorder=2)
    
    ax_bg.text(0.025, 0.965, "M3 Internal Assessment", 
               color=C_CYAN, fontsize=12, weight='bold', va='center', zorder=3)
    ax_bg.text(0.52, 0.965, f"Scene {scene_num}/6: {scene_title}", 
               color=C_TEXT, fontsize=13, weight='bold', ha='center', va='center', zorder=3)
    ax_bg.text(0.975, 0.965, current_time_str, 
               color=C_GOLD, fontsize=12, weight='bold', ha='right', va='center', zorder=3)
    
    # Bottom progress bar
    ax_bg.fill_between([0, 1], [0, 0], [0.015, 0.015], color="#1e293b", zorder=1)
    ax_bg.fill_between([0, progress_frac], [0, 0], [0.015, 0.015], color=C_CYAN, zorder=2)

def draw_grid_and_axes(ax, xlim=(-4.5, 4.5), ylim=(-4.5, 4.5), matrix=None, grid_step=1.0, alpha=0.3):
    ax.set_facecolor(C_BG)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect('equal')
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color(C_BORDER)
        spine.set_linewidth(1.2)
    
    # Base grid lines
    xs = np.arange(xlim[0] - 2, xlim[1] + 3, grid_step)
    ys = np.arange(ylim[0] - 2, ylim[1] + 3, grid_step)
    
    if matrix is None:
        for x in xs:
            ax.plot([x, x], [ylim[0] - 2, ylim[1] + 2], color=C_GRID, lw=1.0, alpha=alpha, zorder=1)
        for y in ys:
            ax.plot([xlim[0] - 2, xlim[1] + 2], [y, y], color=C_GRID, lw=1.0, alpha=alpha, zorder=1)
        # Main Axes
        ax.axhline(0, color=C_AXIS, lw=1.8, zorder=2)
        ax.axvline(0, color=C_AXIS, lw=1.8, zorder=2)
    else:
        # Transformed grid lines
        M = np.array(matrix)
        for x in xs:
            p1 = M @ np.array([x, ylim[0] - 4])
            p2 = M @ np.array([x, ylim[1] + 4])
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=C_GRID, lw=1.0, alpha=alpha, zorder=1)
        for y in ys:
            p1 = M @ np.array([xlim[0] - 4, y])
            p2 = M @ np.array([xlim[1] + 4, y])
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=C_GRID, lw=1.0, alpha=alpha, zorder=1)
        # Transformed axes
        ox1 = M @ np.array([xlim[0] - 4, 0])
        ox2 = M @ np.array([xlim[1] + 4, 0])
        ax.plot([ox1[0], ox2[0]], [ox1[1], ox2[1]], color=C_AXIS, lw=1.8, zorder=2, ls='--')
        oy1 = M @ np.array([0, ylim[0] - 4])
        oy2 = M @ np.array([0, ylim[1] + 4])
        ax.plot([oy1[0], oy2[0]], [oy1[1], oy2[1]], color=C_AXIS, lw=1.8, zorder=2, ls='--')
    
    # Tick marks
    for x in range(int(xlim[0]) + 1, int(xlim[1])):
        if x != 0:
            ax.text(x, -0.35, f"{x}", color=C_MUTED, fontsize=9, ha='center', va='top')
    for y in range(int(ylim[0]) + 1, int(ylim[1])):
        if y != 0:
            ax.text(-0.35, y, f"{y}", color=C_MUTED, fontsize=9, ha='right', va='center')
    ax.text(-0.3, -0.3, "O", color=C_MUTED, fontsize=10, ha='right', va='top')

def draw_vector(ax, v, color=C_CYAN, label=None, lw=3, zorder=5, text_offset=(0.2, 0.2)):
    vx, vy = v[0], v[1]
    ax.annotate('', xy=(vx, vy), xytext=(0, 0),
                arrowprops=dict(facecolor=color, edgecolor=color, width=lw, headwidth=lw*3.2, headlength=lw*3.5, shrink=0),
                zorder=zorder)
    if label:
        ax.text(vx + text_offset[0], vy + text_offset[1], label, 
                color=color, fontsize=12, weight='bold', zorder=zorder+1)

def add_info_card(ax, xy, width, height, title, lines, border_color=C_CYAN, title_color=None):
    rect = FancyBboxPatch(xy, width, height,
                          boxstyle="round,pad=0.02,rounding_size=0.03",
                          fc=C_PANEL, ec=border_color, lw=1.5, zorder=3)
    ax.add_patch(rect)
    t_color = title_color if title_color else (C_CYAN if border_color == C_BORDER else border_color)
    ax.text(xy[0] + 0.03, xy[1] + height - 0.045, title, 
            color=t_color, fontsize=13, weight='bold', va='top', zorder=4)
    avail = max(height - 0.11, 0.05)
    step = min(0.045, avail / max(len(lines), 1))
    y_cursor = xy[1] + height - 0.10
    for line in lines:
        ax.text(xy[0] + 0.03, y_cursor, line, color=C_TEXT, fontsize=11, va='top', zorder=4)
        y_cursor -= step

def render_frame_to_bytes(fig):
    fig.canvas.draw()
    return fig.canvas.buffer_rgba().tobytes()

def main():
    print("[*] Starting Video Generation Pipeline...")
    
    # FFmpeg command
    cmd = [
        FFMPEG_BIN, '-y',
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-s', f'{WIDTH}x{HEIGHT}',
        '-pix_fmt', 'rgba',
        '-r', str(FPS),
        '-i', '-',
        '-an',
        '-vcodec', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-preset', 'medium',
        '-crf', '18',
        OUTPUT_VIDEO
    ]
    
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    
    frame_idx = 0
    
    def write_frame(fig, count=1):
        nonlocal frame_idx
        raw = render_frame_to_bytes(fig)
        for _ in range(count):
            proc.stdin.write(raw)
            frame_idx += 1
            if frame_idx % 240 == 0:
                sec = frame_idx // FPS
                pct = (frame_idx / TOTAL_FRAMES) * 100
                print(f"    --> Rendered {sec//60:02d}:{sec%60:02d} / 05:00 ({pct:.1f}%) | Frames: {frame_idx}/{TOTAL_FRAMES}")

    # =========================================================================
    # SCENE 1: HOOK / CONTEXT (0:00 - 0:45 = 45 sec = 1080 frames)
    # =========================================================================
    print("[+] Rendering Scene 1: Hook / Context (0:00 - 0:45)...")
    
    # 1.1 Opening Title Frame (0:00 - 0:10 = 10s = 240 frames)
    fig = init_figure()
    ax_bg = fig.add_axes([0, 0, 1, 1])
    ax_bg.set_xlim(0, 1)
    ax_bg.set_ylim(0, 1)
    ax_bg.axis('off')
    
    # Elegant dark gradient & card
    rect = FancyBboxPatch((0.08, 0.12), 0.84, 0.76, boxstyle="round,pad=0.03,rounding_size=0.04",
                          fc="#0f172a", ec=C_CYAN, lw=2.5, zorder=2)
    ax_bg.add_patch(rect)
    
    ax_bg.text(0.5, 0.78, "M3 INTERNAL ASSESSMENT: PROJECT OPTION 1", 
               color=C_MUTED, fontsize=15, weight='bold', ha='center', va='center')
    ax_bg.text(0.5, 0.68, "EIGENVALUES & EIGENVECTORS", 
               color=C_CYAN, fontsize=32, weight='bold', ha='center', va='center')
    ax_bg.text(0.5, 0.60, "Visualizing Invariant Directions & Matrix Scaling in Linear Transformations", 
               color=C_GOLD, fontsize=18, weight='bold', ha='center', va='center')
    
    ax_bg.plot([0.2, 0.8], [0.53, 0.53], color="#334155", lw=2)
    
    ax_bg.text(0.5, 0.45, "Course: Mathematics III (Linear Algebra & Multivariable Calculus)", 
               color=C_TEXT, fontsize=15, ha='center', va='center')
    ax_bg.text(0.5, 0.38, "Candidate: Harsh | Candidate ID: M3-STUDENT", 
               color=C_EMERALD, fontsize=16, weight='bold', ha='center', va='center')
    ax_bg.text(0.5, 0.31, "Format: 1080p 16:9 | Visual Framework: Custom Python / Matplotlib Engine", 
               color=C_MUTED, fontsize=13, ha='center', va='center')
    ax_bg.text(0.5, 0.22, "Learning Objective: Understand how matrices transform space and why invariant directions matter.", 
               color=C_TEXT, fontsize=13, style='italic', ha='center', va='center')
    
    add_header_footer(ax_bg, 1, "Hook & Context", "0:00 - 0:10", 0.02)
    write_frame(fig, 240)
    plt.close(fig)

    # 1.2 Mystery of Matrix Transformation: Random vectors tilt (0:10 - 0:25 = 15s = 360 frames)
    # 72 animated frames (3s) + 288 hold frames (12s)
    anim_steps = 72
    for s in range(anim_steps):
        t = s / (anim_steps - 1)
        # Interpolate matrix from Identity to random shear/rotation
        # A_target = [[2.5, 1.0], [0.5, 1.8]]
        M = (1 - t) * np.eye(2) + t * np.array([[2.2, 0.8], [0.5, 1.5]])
        
        fig = init_figure()
        ax_bg = fig.add_axes([0, 0, 1, 1])
        add_header_footer(ax_bg, 1, "Hook: What Happens When Space Warps?", "0:10 - 0:25", 0.05 + 0.05 * t)
        
        # Left Text Panel
        add_info_card(ax_bg, (0.05, 0.15), 0.38, 0.72, "The Mystery of Matrix Transformations", [
            "• Every square matrix A represents a transformation of space.",
            "• It stretches, squashes, and rotates coordinate grids.",
            "",
            "• Take almost any random vector x:",
            "  Applying A usually rotates x into a completely new line!",
            "",
            "• Notice the pink vector u and orange vector w:",
            "  Both swing away from their original directional spans.",
            "",
            "• Guiding Question:",
            "  Does ANY non-zero vector maintain its original direction?"
        ], border_color=C_ROSE)
        
        # Right Plot Area
        ax_plot = fig.add_axes([0.48, 0.12, 0.48, 0.76])
        draw_grid_and_axes(ax_plot, xlim=(-4, 4), ylim=(-4, 4), matrix=M, alpha=0.35)
        
        # Test vectors
        u_init = np.array([2.0, 0.5])
        w_init = np.array([-1.0, 2.0])
        u_curr = M @ u_init
        w_curr = M @ w_init
        
        # Show original spans as dotted lines
        ax_plot.plot([-u_init[0]*2, u_init[0]*2], [-u_init[1]*2, u_init[1]*2], color=C_ROSE, ls=':', lw=1.5, alpha=0.6)
        ax_plot.plot([-w_init[0]*2, w_init[0]*2], [-w_init[1]*2, w_init[1]*2], color=C_GOLD, ls=':', lw=1.5, alpha=0.6)
        
        draw_vector(ax_plot, u_curr, color=C_ROSE, label=r"$\mathbf{u} \to A\mathbf{u}$ (Rotated!)", lw=3.5)
        draw_vector(ax_plot, w_curr, color=C_GOLD, label=r"$\mathbf{w} \to A\mathbf{w}$ (Deflected!)", lw=3.5)
        
        write_frame(fig, 1)
        if s == anim_steps - 1:
            write_frame(fig, 288)  # Hold final state
        plt.close(fig)

    # 1.3 The Invariant Direction Revealed & Real World Impact (0:25 - 0:45 = 20s = 480 frames)
    # Matrix A = [[3, 1], [1, 3]], eigenvector v1 = [1, 1], eigenvalue = 4
    anim_steps = 72
    for s in range(anim_steps):
        t = s / (anim_steps - 1)
        M = (1 - t) * np.eye(2) + t * np.array([[3.0, 1.0], [1.0, 3.0]])
        
        fig = init_figure()
        ax_bg = fig.add_axes([0, 0, 1, 1])
        add_header_footer(ax_bg, 1, "Hook: The Special Invariant Direction", "0:25 - 0:45", 0.10 + 0.05 * t)
        
        add_info_card(ax_bg, (0.05, 0.15), 0.38, 0.72, "The Invariant Direction Discovered!", [
            "• Look at the glowing cyan vector along the diagonal y = x:",
            "  As space warps, this vector does NOT rotate at all!",
            "",
            "• It remains exactly along its original span line.",
            "  It simply gets stretched by a pure scaling factor!",
            "",
            "• These invariant directions are called EIGENVECTORS.",
            "  The stretch factor is called the EIGENVALUE.",
            "",
            "• Why does this matter in real life?",
            "  - Google PageRank: Dominant eigenvector of web link graph.",
            "  - Civil Engineering: Bridge & skyscraper resonant frequencies.",
            "  - Machine Learning: Principal Component Analysis (PCA)."
        ], border_color=C_CYAN)
        
        ax_plot = fig.add_axes([0.48, 0.12, 0.48, 0.76])
        draw_grid_and_axes(ax_plot, xlim=(-4.5, 4.5), ylim=(-4.5, 4.5), matrix=M, alpha=0.35)
        
        # Invariant line y = x
        ax_plot.plot([-5, 5], [-5, 5], color=C_CYAN, ls='--', lw=2, alpha=0.7, zorder=3)
        ax_plot.text(3.2, 3.5, "Span Line: y = x (Invariant!)", color=C_CYAN, fontsize=11, weight='bold')
        
        v_eig = np.array([0.9, 0.9])
        v_transformed = M @ v_eig
        draw_vector(ax_plot, v_transformed, color=C_CYAN, label=r"$\mathbf{v} \to A\mathbf{v} = \lambda \mathbf{v}$", lw=4)
        
        # General vector that tilts
        u_rand = np.array([1.5, 0.0])
        u_trans = M @ u_rand
        draw_vector(ax_plot, u_trans, color=C_ROSE, label=r"$\mathbf{u} \to A\mathbf{u}$", lw=2.5)
        
        write_frame(fig, 1)
        if s == anim_steps - 1:
            write_frame(fig, 408)
        plt.close(fig)

    # =========================================================================
    # SCENE 2: CONCEPT INTRODUCTION (0:45 - 1:30 = 45 sec = 1080 frames)
    # =========================================================================
    print("[+] Rendering Scene 2: Concept Introduction (0:45 - 1:30)...")
    
    # 2.1 The Fundamental Equation Av = λv (0:45 - 1:05 = 20s = 480 frames)
    fig = init_figure()
    ax_bg = fig.add_axes([0, 0, 1, 1])
    add_header_footer(ax_bg, 2, "Concept Introduction: The Master Equation", "0:45 - 1:05", 0.18)
    
    # Main prominent equation card
    rect_eq = FancyBboxPatch((0.15, 0.60), 0.70, 0.26, boxstyle="round,pad=0.03,rounding_size=0.04",
                             fc="#0f172a", ec=C_CYAN, lw=3, zorder=2)
    ax_bg.add_patch(rect_eq)
    
    ax_bg.text(0.5, 0.78, "THE FUNDAMENTAL EIGEN-EQUATION", color=C_GOLD, fontsize=18, weight='bold', ha='center')
    ax_bg.text(0.5, 0.68, r"$A \mathbf{v} = \lambda \mathbf{v}$", color=C_TEXT, fontsize=38, weight='bold', ha='center')
    ax_bg.text(0.5, 0.62, "Matrix Multiplication = Simple Scalar Scaling", color=C_CYAN, fontsize=14, weight='bold', ha='center')
    
    # 3 Column Component Breakdown
    c_w = 0.26
    # Col 1: A
    add_info_card(ax_bg, (0.08, 0.14), c_w, 0.40, "Matrix A (Transformation)", [
        "• Size: n x n square matrix.",
        "• Represents a linear map T(v) = Av.",
        "• Warps the coordinate grid,",
        "  stretching and rotating space.",
        "• Given as the system operator."
    ], border_color=C_CYAN)
    
    # Col 2: v
    add_info_card(ax_bg, (0.37, 0.14), c_w, 0.40, "Eigenvector v (Direction)", [
        "• Non-zero column vector (v ≠ 0).",
        "• Defines an invariant 1D line (span).",
        "• Does NOT change direction",
        "  when transformed by matrix A.",
        "• 'Eigen' = German for 'own/peculiar'."
    ], border_color=C_EMERALD)
    
    # Col 3: λ
    add_info_card(ax_bg, (0.66, 0.14), c_w, 0.40, "Eigenvalue λ (Scale Factor)", [
        "• Scalar constant (real or complex).",
        "• Magnitude |λ|: stretch or shrink factor.",
        "• Sign of λ:",
        "    λ > 0 : same direction",
        "    λ < 0 : flips 180° reversed",
        "    λ = 0 : collapses into nullspace!"
    ], border_color=C_GOLD)
    
    write_frame(fig, 480)
    plt.close(fig)

    # 2.2 Deriving the Characteristic Equation: (A - λI)v = 0 (1:05 - 1:30 = 25s = 600 frames)
    fig = init_figure()
    ax_bg = fig.add_axes([0, 0, 1, 1])
    add_header_footer(ax_bg, 2, "Concept Introduction: The Characteristic Condition", "1:05 - 1:30", 0.25)
    
    add_info_card(ax_bg, (0.06, 0.12), 0.42, 0.75, "Step-by-Step Algebraic Derivation", [
        "1. Start with the definition:",
        "     A v = λ v",
        "",
        "2. Bring all terms to one side:",
        "     A v - λ v = 0",
        "",
        "3. Insert Identity Matrix I (since λ is scalar, A is matrix):",
        "     A v - λ I v = 0",
        "",
        "4. Factor out the vector v to the right:",
        "     (A - λ I) v = 0",
        "",
        "5. The Crucial Condition:",
        "   We seek non-trivial solutions (v ≠ 0).",
        "   Therefore, the matrix (A - λI) MUST be singular!",
        "   Its nullspace must contain more than just the zero vector."
    ], border_color=C_CYAN)
    
    add_info_card(ax_bg, (0.52, 0.12), 0.42, 0.75, "The Geometric Meaning of det(A - λI) = 0", [
        "• What does the determinant det(M) measure?",
        "  It measures the AREA SCALING factor of space!",
        "",
        "• If det(A - λI) ≠ 0:",
        "  The matrix (A - λI) is invertible.",
        "  The ONLY solution to (A - λI)v = 0 would be v = 0.",
        "  (Trivial solution - gives no direction!)",
        "",
        "• Therefore, for a true invariant direction to exist:",
        "  Space MUST be compressed into a lower dimension!",
        "",
        "★ THE CHARACTERISTIC EQUATION:",
        "        det( A - λ I ) = 0",
        "",
        "• Solving this polynomial gives the eigenvalues λ!"
    ], border_color=C_GOLD)
    
    write_frame(fig, 600)
    plt.close(fig)

    # =========================================================================
    # SCENE 3: VISUAL INTUITION (1:30 - 2:30 = 60 sec = 1440 frames)
    # =========================================================================
    print("[+] Rendering Scene 3: Visual Intuition (1:30 - 2:30)...")
    
    # 3.1 2D Grid Deformation under Matrix A = [[3, 1], [1, 3]] (1:30 - 1:55 = 25s = 600 frames)
    anim_steps = 96
    A_mat = np.array([[3.0, 1.0], [1.0, 3.0]])
    for s in range(anim_steps):
        t = s / (anim_steps - 1)
        # Smooth ease-in-out
        alpha = t * t * (3 - 2 * t)
        M_curr = (1 - alpha) * np.eye(2) + alpha * A_mat
        
        fig = init_figure()
        ax_bg = fig.add_axes([0, 0, 1, 1])
        add_header_footer(ax_bg, 3, "Visual Intuition: Grid Transformation", "1:30 - 1:55", 0.30 + 0.08 * t)
        
        add_info_card(ax_bg, (0.05, 0.14), 0.38, 0.73, "Transforming the Cartesian Grid", [
            "• Consider the symmetric matrix:",
            "     A = [ [3, 1],",
            "           [1, 3] ]",
            "",
            "• Watch how standard basis vectors transform:",
            "  - i-hat = [1, 0]ᵀ  maps to [3, 1]ᵀ (rotated!)",
            "  - j-hat = [0, 1]ᵀ  maps to [1, 3]ᵀ (rotated!)",
            "",
            "• The entire square grid is sheared into diamonds.",
            "• But notice the symmetry across the diagonal lines:",
            "  y = x   and   y = -x",
            "",
            "• The transformation has natural principal axes!"
        ], border_color=C_CYAN)
        
        ax_plot = fig.add_axes([0.48, 0.12, 0.48, 0.76])
        draw_grid_and_axes(ax_plot, xlim=(-4.5, 4.5), ylim=(-4.5, 4.5), matrix=M_curr, alpha=0.35)
        
        # Standard basis transformed
        i_curr = M_curr @ np.array([1.0, 0.0])
        j_curr = M_curr @ np.array([0.0, 1.0])
        draw_vector(ax_plot, i_curr, color=C_ROSE, label=r"$T(\hat{i})$", lw=3.2)
        draw_vector(ax_plot, j_curr, color=C_EMERALD, label=r"$T(\hat{j})$", lw=3.2)
        
        write_frame(fig, 1)
        if s == anim_steps - 1:
            write_frame(fig, 600 - anim_steps)
        plt.close(fig)

    # 3.2 360-degree Vector Sweep: The Angular Deflection Test (1:55 - 2:30 = 35s = 840 frames)
    # Sweep angle from 0 to 180 deg, plotting vector v and Av, plus deflection angle
    anim_steps = 144
    angles = np.linspace(0, np.pi, anim_steps)
    for s, theta in enumerate(angles):
        t = s / (anim_steps - 1)
        v_test = np.array([np.cos(theta), np.sin(theta)])
        Av_test = A_mat @ v_test
        
        # Compute angle between v and Av
        dot_val = np.dot(v_test, Av_test)
        norm_prod = np.linalg.norm(v_test) * np.linalg.norm(Av_test)
        cos_deflect = np.clip(dot_val / norm_prod, -1.0, 1.0)
        deflect_deg = np.degrees(np.arccos(cos_deflect))
        
        fig = init_figure()
        ax_bg = fig.add_axes([0, 0, 1, 1])
        add_header_footer(ax_bg, 3, "Visual Intuition: Angular Deflection Sweep", "1:55 - 2:30", 0.38 + 0.12 * t)
        
        # Left: Interactive Deflection Graph
        ax_graph = fig.add_axes([0.07, 0.10, 0.38, 0.38])
        ax_graph.set_facecolor("#0f172a")
        all_thetas = np.linspace(0, np.pi, 200)
        all_deflects = []
        for th in all_thetas:
            vt = np.array([np.cos(th), np.sin(th)])
            At = A_mat @ vt
            dp = np.clip(np.dot(vt, At) / (np.linalg.norm(vt)*np.linalg.norm(At)), -1, 1)
            all_deflects.append(np.degrees(np.arccos(dp)))
        
        ax_graph.plot(np.degrees(all_thetas), all_deflects, color=C_MUTED, lw=1.8, label="Deflection Angle")
        ax_graph.axvline(45, color=C_CYAN, ls='--', lw=2, label="θ = 45° (λ₁ = 4)")
        ax_graph.axvline(135, color=C_GOLD, ls='--', lw=2, label="θ = 135° (λ₂ = 2)")
        ax_graph.scatter([np.degrees(theta)], [deflect_deg], color=C_ROSE, s=90, zorder=5)
        
        ax_graph.set_xlim(0, 180)
        ax_graph.set_ylim(-2, 40)
        ax_graph.set_xlabel("Input Vector Angle θ (degrees)", color=C_TEXT, fontsize=10)
        ax_graph.set_ylabel("Deflection Angle |θ(Av) - θ(v)|", color=C_TEXT, fontsize=10)
        ax_graph.tick_params(colors=C_MUTED, labelsize=9)
        ax_graph.grid(True, color="#1e293b", ls=':')
        ax_graph.legend(facecolor="#111827", edgecolor="#334155", fontsize=8.5, labelcolor=C_TEXT)
        
        # Left Top Card
        add_info_card(ax_bg, (0.07, 0.54), 0.38, 0.34, "The 360° Sweep Experiment", [
            f"• Current input angle θ: {np.degrees(theta):.1f}°",
            f"• Deflection angle: {deflect_deg:.2f}°",
            "",
            "★ Notice: Deflection drops to exactly 0.0° at:",
            "    θ = 45°  (along line y = x)",
            "    θ = 135° (along line y = -x)",
            "  These are the TWO invariant eigenspaces!"
        ], border_color=C_CYAN if (abs(deflect_deg) < 1.0) else C_BORDER, title_color=C_CYAN)
        
        # Right Plot: Vector Space
        ax_plot = fig.add_axes([0.50, 0.12, 0.46, 0.76])
        draw_grid_and_axes(ax_plot, xlim=(-4.5, 4.5), ylim=(-4.5, 4.5), alpha=0.3)
        
        # Draw the two invariant lines
        ax_plot.plot([-5, 5], [-5, 5], color=C_CYAN, ls=':', lw=1.8, label="Line y = x")
        ax_plot.plot([-5, 5], [5, -5], color=C_GOLD, ls=':', lw=1.8, label="Line y = -x")
        
        # Draw test vector and transformed vector
        draw_vector(ax_plot, v_test * 1.5, color=C_TEXT, label=r"$\mathbf{v}$", lw=2.5)
        draw_vector(ax_plot, Av_test, color=C_ROSE if deflect_deg > 1.0 else C_EMERALD, 
                    label=r"$A\mathbf{v}$", lw=3.5)
        
        write_frame(fig, 1)
        if s == anim_steps - 1:
            write_frame(fig, 840 - anim_steps)
        plt.close(fig)

    # =========================================================================
    # SCENE 4: WORKED EXAMPLE (2:30 - 3:45 = 75 sec = 1800 frames)
    # =========================================================================
    print("[+] Rendering Scene 4: Worked Example (2:30 - 3:45)...")
    
    # 4.1 Step 1: Solving the Characteristic Polynomial (2:30 - 2:55 = 25s = 600 frames)
    fig = init_figure()
    ax_bg = fig.add_axes([0, 0, 1, 1])
    add_header_footer(ax_bg, 4, "Worked Example: Solving the Characteristic Equation", "2:30 - 2:55", 0.52)
    
    add_info_card(ax_bg, (0.06, 0.12), 0.42, 0.75, "Step 1: Set det(A - λI) = 0", [
        "Given the 2x2 symmetric matrix:",
        "     A = [ [3, 1],",
        "           [1, 3] ]",
        "",
        "Subtract λ from the main diagonal:",
        "     (A - λ I) = [ [3-λ,   1 ],",
        "                   [ 1 ,  3-λ] ]",
        "",
        "Calculate the 2x2 determinant:",
        "     det(A - λ I) = (3 - λ)(3 - λ) - (1)(1) = 0",
        "",
        "Expand the quadratic expression:",
        "     (9 - 6λ + λ²) - 1 = 0",
        "     λ² - 6λ + 8 = 0",
        "",
        "Factor the characteristic polynomial:",
        "     (λ - 4)(λ - 2) = 0"
    ], border_color=C_CYAN)
    
    add_info_card(ax_bg, (0.52, 0.12), 0.42, 0.75, "The Distinct Real Eigenvalues", [
        "★ ROOTS OF THE CHARACTERISTIC EQUATION:",
        "",
        "   First Eigenvalue:",
        "       λ₁ = 4    (Dominant stretch factor)",
        "",
        "   Second Eigenvalue:",
        "       λ₂ = 2    (Secondary stretch factor)",
        "",
        "Key Mathematical Insights:",
        "• Trace Check:",
        "    Trace(A) = 3 + 3 = 6",
        "    λ₁ + λ₂  = 4 + 2 = 6  ✓ (Matches perfectly!)",
        "",
        "• Determinant Check:",
        "    det(A) = (3)(3) - (1)(1) = 8",
        "    λ₁ · λ₂ = 4 · 2 = 8    ✓ (Matches perfectly!)",
        "",
        "Next: Find the invariant vector directions (nullspace)."
    ], border_color=C_GOLD)
    
    write_frame(fig, 600)
    plt.close(fig)

    # 4.2 Step 2: Finding Eigenvector for λ₁ = 4 (2:55 - 3:20 = 25s = 600 frames)
    fig = init_figure()
    ax_bg = fig.add_axes([0, 0, 1, 1])
    add_header_footer(ax_bg, 4, "Worked Example: Solving for Eigenvector 1 (λ₁ = 4)", "2:55 - 3:20", 0.60)
    
    add_info_card(ax_bg, (0.06, 0.12), 0.42, 0.75, "Step 2: Solve (A - 4I) v₁ = 0", [
        "Substitute λ₁ = 4 into (A - λI):",
        "     (A - 4I) = [ [3-4,   1 ],",
        "                  [ 1 ,  3-4] ]",
        "              = [ [-1,   1],",
        "                  [ 1,  -1] ]",
        "",
        "Set up the homogeneous linear system:",
        "     [ [-1,  1],     [ x ]     [ 0 ]",
        "       [ 1, -1] ] ·  [ y ]  =  [ 0 ]",
        "",
        "Both rows yield the identical equation:",
        "     -x + y = 0   ===>   y = x",
        "",
        "Choose free parameter x = 1:",
        "     v₁ = [ 1, 1 ]ᵀ",
        "",
        "Any non-zero scalar multiple c · [1, 1]ᵀ is also an eigenvector!"
    ], border_color=C_CYAN)
    
    # Right: Geometric plot of v1
    ax_plot = fig.add_axes([0.52, 0.14, 0.42, 0.71])
    draw_grid_and_axes(ax_plot, xlim=(-4.5, 4.5), ylim=(-4.5, 4.5), alpha=0.3)
    ax_plot.plot([-5, 5], [-5, 5], color=C_CYAN, ls='--', lw=2.5, alpha=0.8)
    draw_vector(ax_plot, np.array([1.0, 1.0]), color=C_CYAN, label=r"$\mathbf{v}_1 = [1, 1]^T$", lw=4.5)
    ax_plot.text(0.3, 3.2, r"Eigenspace $E_1 = \mathrm{span}([1, 1]^T)$", 
                 color=C_CYAN, fontsize=13, weight='bold')
    ax_plot.text(0.3, 2.5, r"Line: $y = x$", color=C_TEXT, fontsize=12)
    ax_plot.text(0.3, 1.8, r"Stretched by factor $\lambda_1 = 4$", color=C_GOLD, fontsize=12)
    
    write_frame(fig, 600)
    plt.close(fig)

    # 4.3 Step 3: Finding Eigenvector for λ₂ = 2 (3:20 - 3:45 = 25s = 600 frames)
    fig = init_figure()
    ax_bg = fig.add_axes([0, 0, 1, 1])
    add_header_footer(ax_bg, 4, "Worked Example: Solving for Eigenvector 2 (λ₂ = 2)", "3:20 - 3:45", 0.68)
    
    add_info_card(ax_bg, (0.06, 0.12), 0.42, 0.75, "Step 3: Solve (A - 2I) v₂ = 0", [
        "Substitute λ₂ = 2 into (A - λI):",
        "     (A - 2I) = [ [3-2,   1 ],",
        "                  [ 1 ,  3-2] ]",
        "              = [ [ 1,   1],",
        "                  [ 1,   1] ]",
        "",
        "Set up the homogeneous linear system:",
        "     [ [1, 1],     [ x ]     [ 0 ]",
        "       [1, 1] ] ·  [ y ]  =  [ 0 ]",
        "",
        "Both rows yield the identical equation:",
        "     x + y = 0   ===>   y = -x",
        "",
        "Choose free parameter x = -1 (or +1):",
        "     v₂ = [ -1, 1 ]ᵀ",
        "",
        "Orthogonality Note:",
        "v₁ · v₂ = (1)(-1) + (1)(1) = 0! (Perpendicular!)"
    ], border_color=C_GOLD)
    
    ax_plot = fig.add_axes([0.52, 0.14, 0.42, 0.71])
    draw_grid_and_axes(ax_plot, xlim=(-4.5, 4.5), ylim=(-4.5, 4.5), alpha=0.3)
    ax_plot.plot([-5, 5], [5, -5], color=C_GOLD, ls='--', lw=2.5, alpha=0.8)
    draw_vector(ax_plot, np.array([-1.0, 1.0]), color=C_GOLD, label=r"$\mathbf{v}_2 = [-1, 1]^T$", lw=4.5)
    ax_plot.text(-4.0, 3.2, r"Eigenspace $E_2 = \mathrm{span}([-1, 1]^T)$", 
                 color=C_GOLD, fontsize=13, weight='bold')
    ax_plot.text(-4.0, 2.5, r"Line: $y = -x$", color=C_TEXT, fontsize=12)
    ax_plot.text(-4.0, 1.8, r"Stretched by factor $\lambda_2 = 2$", color=C_CYAN, fontsize=12)
    
    write_frame(fig, 600)
    plt.close(fig)

    # =========================================================================
    # SCENE 5: INTERPRETATION & VERIFICATION (3:45 - 4:30 = 45 sec = 1080 frames)
    # =========================================================================
    print("[+] Rendering Scene 5: Interpretation & Verification (3:45 - 4:30)...")
    
    # 5.1 Verification: Algebraic & Visual (3:45 - 4:10 = 25s = 600 frames)
    # 96 animated frames (4s) + 504 hold frames (21s)
    anim_steps = 96
    for s in range(anim_steps):
        t = s / (anim_steps - 1)
        scale_1 = 1.0 + 3.0 * t  # from 1 to 4
        scale_2 = 1.0 + 1.0 * t  # from 1 to 2
        
        fig = init_figure()
        ax_bg = fig.add_axes([0, 0, 1, 1])
        add_header_footer(ax_bg, 5, "Interpretation: Verifying Av = λv", "3:45 - 4:10", 0.75 + 0.08 * t)
        
        add_info_card(ax_bg, (0.05, 0.12), 0.42, 0.75, "Direct Algebraic Verification", [
            "1. Test First Eigenpair (λ₁ = 4, v₁ = [1, 1]ᵀ):",
            "   A v₁ = [ [3, 1],   [ 1 ]     [ 3(1) + 1(1) ]     [ 4 ]",
            "            [1, 3] ] [ 1 ]  =  [ 1(1) + 3(1) ]  =  [ 4 ]",
            "        = 4 · [ 1, 1 ]ᵀ  =  λ₁ v₁  ✓",
            "",
            "2. Test Second Eigenpair (λ₂ = 2, v₂ = [-1, 1]ᵀ):",
            "   A v₂ = [ [3, 1],   [-1 ]     [ 3(-1) + 1(1) ]    [-2 ]",
            "            [1, 3] ] [ 1 ]  =  [ 1(-1) + 3(1) ]  =  [ 2 ]",
            "        = 2 · [-1, 1 ]ᵀ  =  λ₂ v₂  ✓",
            "",
            "3. Contrast with Non-Eigenvector u = [1, 0]ᵀ:",
            "   A u  = [3, 1]ᵀ  ≠  c · [1, 0]ᵀ",
            "   (Rotates into a different direction entirely!)"
        ], border_color=C_EMERALD)
        
        ax_plot = fig.add_axes([0.50, 0.12, 0.46, 0.75])
        draw_grid_and_axes(ax_plot, xlim=(-4.5, 4.5), ylim=(-4.5, 4.5), alpha=0.3)
        
        # Invariant lines
        ax_plot.plot([-5, 5], [-5, 5], color=C_CYAN, ls=':', lw=1.5, alpha=0.6)
        ax_plot.plot([-5, 5], [5, -5], color=C_GOLD, ls=':', lw=1.5, alpha=0.6)
        
        # Scaling vectors
        draw_vector(ax_plot, np.array([1.0, 1.0]) * scale_1, color=C_CYAN, 
                    label=f"$A\\mathbf{{v}}_1 = {scale_1:.1f}\\mathbf{{v}}_1$" if t > 0.5 else r"$\mathbf{v}_1$", lw=4)
        draw_vector(ax_plot, np.array([-1.0, 1.0]) * scale_2, color=C_GOLD, 
                    label=f"$A\\mathbf{{v}}_2 = {scale_2:.1f}\\mathbf{{v}}_2$" if t > 0.5 else r"$\mathbf{v}_2$", lw=4)
        
        # Non-eigenvector
        draw_vector(ax_plot, (1-t)*np.array([1.0, 0.0]) + t*np.array([3.0, 1.0]), color=C_ROSE, 
                    label=r"$\mathbf{u} \to A\mathbf{u}$ (Rotated!)", lw=2.5)
        
        write_frame(fig, 1)
        if s == anim_steps - 1:
            write_frame(fig, 504)
        plt.close(fig)

    # 5.2 The Big Picture: Diagonalization & Natural Basis (4:10 - 4:30 = 20s = 480 frames)
    fig = init_figure()
    ax_bg = fig.add_axes([0, 0, 1, 1])
    add_header_footer(ax_bg, 5, "Interpretation: The Natural Coordinate System", "4:10 - 4:30", 0.85)
    
    add_info_card(ax_bg, (0.06, 0.12), 0.42, 0.75, "Decoupling Matrix Dynamics (Diagonalization)", [
        "• What do eigenvectors truly represent?",
        "  They form the NATURAL COORDINATE SYSTEM of matrix A!",
        "",
        "• Diagonal Decomposition:  A = P D P⁻¹",
        "  - P = [ v₁ | v₂ ]  (Eigenvector Matrix)",
        "  - D = [ [λ₁,  0 ],",
        "          [ 0 , λ₂] ] (Pure Diagonal Scaling Matrix!)",
        "",
        "• In the standard basis (x, y):",
        "  Coordinates are coupled and entangled.",
        "",
        "• In the eigenvector basis (v₁, v₂):",
        "  The matrix acts as independent 1D stretches!",
        "  - Axis 1 stretches by factor 4.",
        "  - Axis 2 stretches by factor 2."
    ], border_color=C_PURPLE)
    
    add_info_card(ax_bg, (0.52, 0.12), 0.42, 0.75, "Matrix Powers: Computing A¹⁰⁰ Instantly", [
        "• Consider computing high powers of A (e.g., in Markov Chains):",
        "     A¹⁰⁰  =  (P D P⁻¹)¹⁰⁰  =  P D¹⁰⁰ P⁻¹",
        "",
        "• Computing D¹⁰⁰ is trivial:",
        "     D¹⁰⁰ = [ [4¹⁰⁰,   0  ],",
        "              [  0 ,  2¹⁰⁰] ]",
        "",
        "• As n → ∞:",
        "  The dominant eigenvalue (λ₁ = 4) completely dominates",
        "  the long-term evolution of the system!",
        "",
        "• This is the exact principle behind Google's PageRank,",
        "  population models, and quantum mechanics observables."
    ], border_color=C_CYAN)
    
    write_frame(fig, 480)
    plt.close(fig)

    # =========================================================================
    # SCENE 6: SUMMARY & CREDITS (4:30 - 5:00 = 30 sec = 720 frames)
    # =========================================================================
    print("[+] Rendering Scene 6: Summary & Credits (4:30 - 5:00)...")
    
    # 6.1 Three Core Takeaways (4:30 - 4:45 = 15s = 360 frames)
    fig = init_figure()
    ax_bg = fig.add_axes([0, 0, 1, 1])
    add_header_footer(ax_bg, 6, "Summary: 3 Core Mathematical Takeaways", "4:30 - 4:45", 0.92)
    
    card_w = 0.27
    add_info_card(ax_bg, (0.05, 0.15), card_w, 0.70, "1. Invariant Directions", [
        "• Eigenvectors v ≠ 0 are the",
        "  special vectors that DO NOT",
        "  rotate under transformation A.",
        "",
        "• Av lies strictly on the span(v).",
        "",
        "• They define the intrinsic",
        "  axes along which the matrix",
        "  operates without cross-talk."
    ], border_color=C_CYAN)
    
    add_info_card(ax_bg, (0.36, 0.15), card_w, 0.70, "2. Pure Scaling Factor", [
        "• The eigenvalue λ is the scalar",
        "  stretch / shrink factor.",
        "",
        "• Av = λ v collapses matrix",
        "  multiplication into simple",
        "  arithmetic scaling.",
        "",
        "• Sign of λ determines direction:",
        "  (+) preserves, (-) inverts."
    ], border_color=C_GOLD)
    
    add_info_card(ax_bg, (0.68, 0.15), card_w, 0.70, "3. Algebraic Solution", [
        "• Step 1: Solve det(A - λI) = 0",
        "  for characteristic roots λ.",
        "",
        "• Step 2: Solve (A - λI)v = 0",
        "  to find non-trivial nullspace",
        "  basis vectors.",
        "",
        "• Diagonalizes A = P D P⁻¹."
    ], border_color=C_EMERALD)
    
    write_frame(fig, 360)
    plt.close(fig)

    # 6.2 Closing Frame: References & Disclosures (4:45 - 5:00 = 15s = 360 frames)
    fig = init_figure()
    ax_bg = fig.add_axes([0, 0, 1, 1])
    ax_bg.set_xlim(0, 1)
    ax_bg.set_ylim(0, 1)
    ax_bg.axis('off')
    
    rect_close = FancyBboxPatch((0.08, 0.10), 0.84, 0.80, boxstyle="round,pad=0.03,rounding_size=0.04",
                               fc="#0f172a", ec=C_GOLD, lw=2.5, zorder=2)
    ax_bg.add_patch(rect_close)
    
    ax_bg.text(0.5, 0.82, "PROJECT COMPLETION & ACADEMIC DISCLOSURES", 
               color=C_GOLD, fontsize=20, weight='bold', ha='center')
    ax_bg.plot([0.15, 0.85], [0.77, 0.77], color="#334155", lw=1.5)
    
    # 2-column info
    ax_bg.text(0.14, 0.70, "Project & Submission Information", color=C_CYAN, fontsize=14, weight='bold')
    ax_bg.text(0.14, 0.63, "• Assessment: M3 Internal Assessment (10% Weightage)", color=C_TEXT, fontsize=11)
    ax_bg.text(0.14, 0.57, "• Topic: Eigenvalues & Eigenvectors (Option 1: Animation Video)", color=C_TEXT, fontsize=11)
    ax_bg.text(0.14, 0.51, "• Duration: Exactly 5:00 Minutes (300 seconds, 7200 frames)", color=C_TEXT, fontsize=11)
    ax_bg.text(0.14, 0.45, "• Resolution: 1920x1080 (1080p, 16:9 Landscape MP4)", color=C_TEXT, fontsize=11)
    ax_bg.text(0.14, 0.39, "• Candidate Name: Harsh | ID: M3-STUDENT", color=C_EMERALD, fontsize=12, weight='bold')
    
    ax_bg.text(0.55, 0.70, "Academic Credits & AI Disclosure Policy", color=C_CYAN, fontsize=14, weight='bold')
    ax_bg.text(0.55, 0.63, "• Mathematical References:", color=C_TEXT, fontsize=11, weight='bold')
    ax_bg.text(0.55, 0.58, "   1. Gilbert Strang, 'Introduction to Linear Algebra' (5th Ed.)", color=C_MUTED, fontsize=10)
    ax_bg.text(0.55, 0.53, "   2. Grant Sanderson, 'Essence of Linear Algebra' (3Blue1Brown)", color=C_MUTED, fontsize=10)
    ax_bg.text(0.55, 0.46, "• AI Tool Disclosure (Mandatory Policy Compliance):", color=C_TEXT, fontsize=11, weight='bold')
    ax_bg.text(0.55, 0.41, "   Assisted by Google DeepMind Antigravity for storyboard structure", color=C_MUTED, fontsize=10)
    ax_bg.text(0.55, 0.36, "   and Python Matplotlib frame-rendering script synthesis.", color=C_MUTED, fontsize=10)
    ax_bg.text(0.55, 0.30, "• Audio & Voice-over:", color=C_TEXT, fontsize=11, weight='bold')
    ax_bg.text(0.55, 0.25, "   Narration performed manually by student. No AI voice used.", color=C_GOLD, fontsize=10, weight='bold')
    
    ax_bg.text(0.5, 0.16, "Thank You for Watching! Ready for Viva / Q&A Evaluation.", 
               color=C_CYAN, fontsize=14, weight='bold', ha='center')
    
    add_header_footer(ax_bg, 6, "Summary & Academic Disclosures", "4:45 - 5:00", 1.00)
    write_frame(fig, 360)
    plt.close(fig)

    # Close pipe
    proc.stdin.close()
    proc.wait()
    
    print(f"\n[✓] VIDEO GENERATION COMPLETE!")
    print(f"[✓] Total Frames: {frame_idx} (Target: {TOTAL_FRAMES})")
    print(f"[✓] Duration: {frame_idx / FPS:.2f} seconds ({frame_idx / (FPS*60):.2f} minutes)")
    print(f"[✓] Saved to: {OUTPUT_VIDEO}")

if __name__ == "__main__":
    main()
