# M3 Internal Assessment: Animation Video Project (Option 1)

## 📌 Project Information
- **Course:** Mathematics III (Linear Algebra, Calculus & Optimization)
- **Weightage:** 10% of Internal Assessment
- **Topic:** **Eigenvalues and Eigenvectors: Visualizing Invariant Directions & Matrix Scaling**
- **Format:** 16:9 Landscape, 1080p (1920×1080), 24 FPS, MP4 Format
- **Duration:** Exactly 5:00 minutes (300 seconds, 7,200 frames)
- **Audio:** Silent video track ready for manual student voice-over (as AI voices are strictly prohibited).
- **Public GitHub Repository:** [https://github.com/harsh999-hub/Math-video](https://github.com/harsh999-hub/Math-video)

---

## 📂 Repository Contents & Structure

```
Math-video/
├── _Video.mp4                    # Final 1080p 16:9 MP4 video (5:00 duration)
├── Storyboard.pdf                # 6-Scene Storyboard PDF submission
├── _Code/
│   ├── generate_video.py         # Full Python / Matplotlib / FFmpeg animation generator
│   ├── generate_storyboard.py    # ReportLab script generating the official PDF storyboard
│   └── requirements.txt          # Python dependencies
└── README.md                     # Complete project documentation, script & Viva prep guide
```

---

## 🎯 Learning Objective
> *"By the end of this video, the viewer will be able to geometrically identify invariant directions under a 2D linear transformation, solve the characteristic equation $\det(A - \lambda I) = 0$ to find eigenvalues, and compute the corresponding eigenvectors that form the transformation's natural coordinate system."*

---

## 🎬 6-Scene Storyboard Summary

| Scene | Time | Purpose | Visual & Mathematical Plan |
|---|---|---|---|
| **Scene 1: Hook / Context** | 0:00 – 0:45 | Spark curiosity & motivate invariant directions | Title card, 2D grid warping under random matrices, vectors tilting off course vs. an invariant diagonal vector. Real-world applications (Google PageRank, Bridge Resonance, PCA). |
| **Scene 2: Concept Introduction** | 0:45 – 1:30 | Define $A\mathbf{v} = \lambda \mathbf{v}$ and notation | Breakdown of $A$, $\mathbf{v} \neq \mathbf{0}$, $\lambda$. Step-by-step derivation of $(A - \lambda I)\mathbf{v} = \mathbf{0}$ and geometric meaning of $\det(A - \lambda I) = 0$. |
| **Scene 3: Visual Intuition** | 1:30 – 2:30 | Build geometric understanding | Transforming the Cartesian plane under $A = \begin{pmatrix}3 & 1\\1 & 3\end{pmatrix}$. 360° input vector sweep displaying angular deflection dropping to $0^\circ$ at $\theta = 45^\circ$ and $\theta = 135^\circ$. |
| **Scene 4: Worked Example** | 2:30 – 3:45 | Step-by-step algebraic solution | Solving $\det(A - \lambda I) = \lambda^2 - 6\lambda + 8 = 0$ to obtain $\lambda_1 = 4, \lambda_2 = 2$. Solving $(A - 4I)\mathbf{v}_1 = \mathbf{0} \implies \mathbf{v}_1 = [1, 1]^T$ and $(A - 2I)\mathbf{v}_2 = \mathbf{0} \implies \mathbf{v}_2 = [-1, 1]^T$. |
| **Scene 5: Interpretation & Verification** | 3:45 – 4:30 | Connect algebra back to geometry | Direct verification $A\mathbf{v}_1 = 4\mathbf{v}_1$ and $A\mathbf{v}_2 = 2\mathbf{v}_2$. Visualizing stretching along eigenspaces. Matrix diagonalization ($A = PDP^{-1}$) and decoupled dynamics. |
| **Scene 6: Summary & Credits** | 4:30 – 5:00 | Reinforce takeaways & cite sources | 3 core mathematical takeaways, textbook citations, AI tool disclosures, and closing frame. |

---

## 🎙️ Complete Voice-Over Script (For Student Recording)

Read this script aloud into a microphone while playing `_Video.mp4`. The pacing matches the video visual holds and transitions.

### **Scene 1: Hook & Context (0:00 – 0:45)**
- **[0:00 – 0:10]** *"Hello everyone, and welcome to this visual exploration of Linear Algebra for our M3 Internal Assessment. Today, we are investigating one of the most powerful and intuitive concepts in mathematics: Eigenvalues and Eigenvectors."*
- **[0:10 – 0:25]** *"Whenever a square matrix acts on space, it distorts the coordinate grid—stretching, squishing, and shearing vectors. If you pick almost any random vector, like the pink or orange arrows shown here, the transformation knocks them off course, swinging them away from their original directional line."*
- **[0:25 – 0:45]** *"This leads to our guiding question: Does ANY non-zero vector keep its original direction? Look at the glowing cyan vector along the diagonal: as space warps, it does NOT rotate! It simply stretches. These special invariant directions are called eigenvectors, and their scaling factors are eigenvalues. They are essential across engineering—from preventing bridges from collapsing due to resonant frequencies, to power algorithms like Google PageRank and PCA in machine learning."*

---

### **Scene 2: Concept Introduction (0:45 – 1:30)**
- **[0:45 – 1:05]** *"Let's establish the mathematical foundation. The fundamental eigen-equation is $A\mathbf{v} = \lambda \mathbf{v}$. Notice how remarkable this is: complicated matrix-vector multiplication collapses into simple scalar multiplication! Here, $A$ is an $n \times n$ transformation matrix, $\mathbf{v}$ is a non-zero vector defining the invariant direction, and $\lambda$ is a scalar called the eigenvalue. The magnitude of $\lambda$ tells us how much the vector stretches, and its sign indicates whether the orientation is preserved or flipped."*
- **[1:05 – 1:30]** *"How do we find these values algebraically? We rewrite the equation by moving $\lambda \mathbf{v}$ to the left: $A\mathbf{v} - \lambda \mathbf{v} = \mathbf{0}$. Because we cannot subtract a scalar directly from a matrix, we introduce the identity matrix $I$, giving $(A - \lambda I)\mathbf{v} = \mathbf{0}$. Now, if $(A - \lambda I)$ were invertible, the only solution would be the trivial zero vector $\mathbf{v} = \mathbf{0}$, which has no direction! Therefore, for a non-zero eigenvector to exist in the nullspace, space must be squashed into a lower dimension. This requires the determinant to equal zero: $\det(A - \lambda I) = 0$. This is the famous Characteristic Equation."*

---

### **Scene 3: Visual Intuition (1:30 – 2:30)**
- **[1:30 – 1:55]** *"Now, let's build visual intuition with a concrete example. Consider the symmetric matrix $A = \begin{pmatrix}3 & 1\\1 & 3\end{pmatrix}$. Watch the coordinate grid deform: the standard unit vectors $\hat{i}$ and $\hat{j}$ are rotated into $[3, 1]^T$ and $[1, 3]^T$. The square cells are stretched into diamonds. But notice the visual symmetry: there are two prominent perpendicular axes along $y = x$ and $y = -x$."*
- **[1:55 – 2:30]** *"To prove this rigorously, let's perform an experiment. We sweep a unit test vector $\mathbf{v}$ through 360 degrees and measure the angular deflection between $\mathbf{v}$ and $A\mathbf{v}$. Look at the graph on the left: for almost every angle, the deflection is non-zero, meaning the vector rotates. But at exactly $\theta = 45^\circ$ and $\theta = 135^\circ$, the deflection drops to zero degrees! These two special angles correspond precisely to the invariant eigenspaces of matrix $A$."*

---

### **Scene 4: Worked Example (2:30 – 3:45)**
- **[2:30 – 2:55]** *"Let's calculate these values algebraically. Step 1: Solve the characteristic equation $\det(A - \lambda I) = 0$. Subtracting $\lambda$ along the main diagonal gives the determinant of $\begin{pmatrix}3-\lambda & 1\\1 & 3-\lambda\end{pmatrix}$. Expanding this $(3-\lambda)^2 - 1 = 0$, which gives $\lambda^2 - 6\lambda + 8 = 0$. Factoring the quadratic yields $(\lambda - 4)(\lambda - 2) = 0$. We find two distinct real eigenvalues: $\lambda_1 = 4$ and $\lambda_2 = 2$. We can double-check our work: the sum $4 + 2 = 6$ matches the trace of $A$, and the product $4 \times 2 = 8$ matches the determinant of $A$."*
- **[2:55 – 3:20]** *"Step 2: Find the eigenvector for $\lambda_1 = 4$. We substitute $\lambda = 4$ into $(A - \lambda I)\mathbf{v} = \mathbf{0}$, giving $\begin{pmatrix}-1 & 1\\1 & -1\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix} = \begin{pmatrix}0\\0\end{pmatrix}$. Both rows reduce to the single linear equation $-x + y = 0$, or $y = x$. Choosing $x = 1$ yields our first eigenvector $\mathbf{v}_1 = \begin{pmatrix}1\\1\end{pmatrix}$. Any vector along the line $y = x$ forms the eigenspace $E_1$."*
- **[3:20 – 3:45]** *"Step 3: Find the eigenvector for $\lambda_2 = 2$. Substituting $\lambda = 2$ gives $\begin{pmatrix}1 & 1\\1 & 1\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix} = \begin{pmatrix}0\\0\end{pmatrix}$. This yields the equation $x + y = 0$, or $y = -x$. Setting $x = -1$ gives our second eigenvector $\mathbf{v}_2 = \begin{pmatrix}-1\\1\end{pmatrix}$. Notice that because $A$ is symmetric, our two eigenvectors are orthogonal: their dot product $(1)(-1) + (1)(1) = 0$."*

---

### **Scene 5: Interpretation & Verification (3:45 – 4:30)**
- **[3:45 – 4:10]** *"Let's verify our results algebraically and geometrically. Multiplying $A$ by $\mathbf{v}_1$, we get $\begin{pmatrix}3 & 1\\1 & 3\end{pmatrix}\begin{pmatrix}1\\1\end{pmatrix} = \begin{pmatrix}4\\4\end{pmatrix}$, which is exactly $4 \times \mathbf{v}_1$. Geometrically, the vector stretches by a factor of 4 along the line $y = x$. For $\mathbf{v}_2$, $A\begin{pmatrix}-1\\1\end{pmatrix} = \begin{pmatrix}-2\\2\end{pmatrix} = 2 \times \mathbf{v}_2$, stretching by a factor of 2 along $y = -x$. In contrast, a non-eigenvector like $[1, 0]^T$ gets rotated into $[3, 1]^T$."*
- **[4:10 – 4:30]** *"Why is this so important? Because eigenvectors form the natural coordinate system of the matrix! By diagonalizing $A = PDP^{-1}$, where $D$ is a diagonal matrix containing the eigenvalues, we decouple the system. Computing high matrix powers like $A^{100}$ becomes trivial because $D^{100}$ simply raises $4^{100}$ and $2^{100}$. Over time, the dominant eigenvalue $\lambda_1 = 4$ completely dictates the behavior of the system."*

---

### **Scene 6: Summary & Credits (4:30 – 5:00)**
- **[4:30 – 4:45]** *"To summarize, here are the three core takeaways: First, eigenvectors are the invariant directions of a linear transformation that experience zero rotation. Second, eigenvalues are the scalar factors that quantify how much space stretches or shrinks along those axes. Third, we find them by solving $\det(A - \lambda I) = 0$ for eigenvalues and finding the nullspace basis for eigenvectors."*
- **[4:45 – 5:00]** *"This concludes our video for the M3 Internal Assessment. References include Gilbert Strang's Linear Algebra and Grant Sanderson's 3Blue1Brown series. This project adheres to academic guidelines: animation scripts were synthesized with AI tool assistance, and narration is presented manually. Thank you for watching!"*

---

## 🎓 Individual Viva / Q&A Preparation Guide

Be prepared to answer these questions during your in-person viva evaluation:

### **Q1: Why must the determinant $\det(A - \lambda I)$ equal zero?**
> **Answer:** "If $\det(A - \lambda I) \neq 0$, the matrix $(A - \lambda I)$ is invertible (non-singular). If a matrix is invertible, the equation $(A - \lambda I)\mathbf{v} = \mathbf{0}$ can be multiplied by $(A - \lambda I)^{-1}$ on both sides, which forces $\mathbf{v} = \mathbf{0}$. But by definition, an eigenvector must be non-zero ($\mathbf{v} \neq \mathbf{0}$) because the zero vector has no direction. Therefore, $(A - \lambda I)$ must be singular and compress space, which happens if and only if $\det(A - \lambda I) = 0$."

### **Q2: Why are the two eigenvectors in your example perpendicular (orthogonal)?**
> **Answer:** "Our matrix $A = \begin{pmatrix}3 & 1\\1 & 3\end{pmatrix}$ is a real symmetric matrix ($A = A^T$). By the Spectral Theorem, any real symmetric matrix has real eigenvalues and orthogonal eigenvectors corresponding to distinct eigenvalues. Here $\mathbf{v}_1 \cdot \mathbf{v}_2 = (1)(-1) + (1)(1) = -1 + 1 = 0$, confirming they are perpendicular."

### **Q3: What do the Trace and Determinant shortcuts tell us?**
> **Answer:** 
> - $\text{Trace}(A) = \sum \lambda_i = 3 + 3 = 6$, and $\lambda_1 + \lambda_2 = 4 + 2 = 6$.
> - $\det(A) = \prod \lambda_i = (3)(3) - (1)(1) = 8$, and $\lambda_1 \cdot \lambda_2 = 4 \times 2 = 8$.
> This provides an immediate mathematical verification of our eigenvalues.

### **Q4: How did you create the animation without proprietary software?**
> **Answer:** "I authored a Python script using Matplotlib and NumPy to compute the exact matrix transformations and vector rotations. The script renders high-resolution frames using off-screen Agg backend, which are piped directly into an FFmpeg H.264 video encoding stream at 1080p, 24 FPS. The timing is organized into a 6-scene storyboard spanning 5 minutes."

---

## 🛠️ How to Re-render Video & Storyboard

### **Requirements:**
```bash
pip install -r _Code/requirements.txt
```

### **Render Video (`_Video.mp4`):**
```bash
python3 _Code/generate_video.py
```

### **Generate Storyboard PDF (`Storyboard.pdf`):**
```bash
python3 _Code/generate_storyboard.py
```

---

## 📜 Academic Integrity & AI Disclosure
In compliance with the project guidelines:
- **AI Tool Disclosure:** Storyboard structuring and Python rendering script implementation were synthesized with assistance from Google DeepMind's Antigravity assistant.
- **Voice-over & Narration:** Performed independently and manually by the student. No synthetic/AI voice audio is included.
- **Mathematical Calculations:** Independently verified by hand.
