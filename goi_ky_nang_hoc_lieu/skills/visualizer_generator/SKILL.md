---
name: visualizer_generator
description: Generate dynamic, topic-specific interactive visualizers (HTML/JS/CSS State Machine Engine) for learning materials. Target output language is 100% Accented Vietnamese.
---

# Interactive Visualizer Generator Skill — Rikkei Education Standards

## 1. Objective

This skill instructs the AI Agent to build "Interactive Visualizer" components that dynamically adapt to **any lesson topic** (not hardcoded strictly to Stack/Heap). Based on `lesson_title` and `tech_stack`, the Agent automatically designs Canvas layouts, Legends, Realtime Stats, and a JavaScript State Machine Engine.

---

## 2. Recommended Visualizer Archetypes

Depending on lesson content, select 1 of the following archetypes for the `Canvas` UI:

1. **Memory & Variable Allocator (Memory Model):**
   - **Use case:** Variable declarations, data types, pointers, references.
   - **UI:** Two-column split layout (Stack & Heap).
2. **Logic & Branching Flow (Flow Model):**
   - **Use case:** Operators, if/else, switch case.
   - **UI:** Flowchart or Decision Tree. Nodes illuminate based on execution paths (True/False).
3. **Loop & Iterator Track (Loop Model):**
   - **Use case:** For loops, While loops, Iterators, Array Traversal.
   - **UI:** Timeline track or 1D Array boxes. A pointer moves across elements step-by-step.
4. **Data Structure & Graph (Data Structure Model):**
   - **Use case:** Trees, Graphs, LinkedLists, Dictionaries.
   - **UI:** Interconnected Nodes linked with SVG arrows.
5. **Web Service & Architecture (Web Model):**
   - **Use case:** Web Frameworks, Backend API, Request/Response lifecycle, Middleware, Database.
   - **UI:** Client (Browser) -> Server -> Database. Packets animate between layers.

---

## 3. Output Schema (JSON Format)

The Agent MUST generate a JSON data payload containing 6 core components to embed into HTML templates:

```json
{
  "canvas_title": "Icon + Visualizer Title (e.g. 🔄 Trực quan hóa Vòng lặp For)",
  "legend_html": "Color legend items (e.g. <div class='legend-item'>...</div>)",
  "stats_html": "3 realtime stat cards (e.g. Iteration count, Time elapsed, Temp variables)",
  "code_tracker_html": "Sample code snippet wrapped in <span class='code-line' id='line-X'>...</span>",
  "input_label": "Title for input field (e.g. TỰ NHẬP MẢNG DỮ LIỆU)",
  "input_default": "Default input value",
  "engine_js": "Self-contained ES6 JavaScript (Class InteractiveVisualizerEngine)"
}
```

---

## 4. Core Principles of JavaScript State Machine Engine (`engine_js`)

The JavaScript engine MUST be self-contained and adhere to a State Machine model:

1. **Class Architecture:**
   ```javascript
   class InteractiveVisualizerEngine {
     constructor() {
       this.steps = [];
       this.currentStep = 0;
       this.init();
     }
     init() {
       this.generateSteps();
       this.render();
     }
     generateSteps() {
       /* Pre-compute all states for algorithm execution */
     }
     render() {
       /* Update DOM (Canvas, Stats, Code Tracker Highlight) based on this.steps[this.currentStep] */
     }
     step() {
       /* Increment currentStep and call render() */
     }
   }
   ```
2. **Pre-computed State Array:** The entire execution process MUST be pre-computed and stored in `this.steps`. Each `step` object contains the complete UI state for that frame (e.g. pointer position, variable values, active code line ID, log message).
3. **No External Dependencies:** Use Vanilla JS and direct DOM manipulation ONLY. FORBIDDEN to use React/Vue. Use Template Literals for dynamic HTML generation inside `render()`.
4. **Dynamic CSS Variables:** Reuse project CSS tokens: `var(--primary)`, `var(--bg-panel)`, `var(--text-main)`, `var(--color-idle)`, `var(--color-done)`.

---

## 5. Agent Execution Workflow

1. **Analyze:** Read `lesson_title` and learning objectives to select the target Archetype.
2. **Storyboard:** Design the 5-10 line code snippet (`code_tracker_html`) and state transformation keyframes.
3. **Implement JS:** Write state computation in `generateSteps()` and DOM rendering in `render()`.
4. **Return Payload:** Package into clean valid JSON.

