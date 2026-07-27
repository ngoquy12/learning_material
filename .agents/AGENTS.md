# Project Rules & Customizations

## HTML Layout & Component Formatting Rules

### 1. Khảo thí & Đánh giá năng lực tự học (Self-Test & Accordion Component Rules)
Whenever creating, modifying, or regenerating HTML reading materials or learning components (`reading.html`, `reading_all.html`, or generated HTML components):

1. **Strict Left-Alignment**:
   - The `.selftest-question` element MUST use `justify-content: flex-start !important; gap: 8px !important; text-align: left !important;`.
   - NEVER use `justify-content: space-between` on `.selftest-question` containers as it forces flex child text nodes to align to the far right margin.
   - All accordion answer elements (`.selftest-answer`, `.selftest-answer p`, `.selftest-answer ul`, `.selftest-answer ol`, `.selftest-answer li`) MUST have `text-align: left !important;`.

2. **CSS Rule Standard**:
   Ensure the following CSS rule is included in the `<style>` block:
   ```css
   .selftest-question { 
       font-weight: 600; 
       color: var(--primary); 
       cursor: pointer; 
       text-align: left !important; 
       display: flex; 
       align-items: center; 
       justify-content: flex-start !important; 
       gap: 8px !important; 
   }
   .selftest-answer { 
       margin-top: 12px; 
       padding-top: 12px; 
       border-top: 1px solid var(--border-color); 
       display: none; 
       color: var(--text-main); 
       text-align: left !important; 
   }
   .selftest-answer * {
       text-align: left !important;
   }
   ```

3. **High-Contrast Dark Mode Code Trackers**:
   - Inside dark-theme code blocks (e.g. `.code-tracker-panel` or `bg-slate-900`), NEVER use dark inline colors (`#005cc5`, `#032f62`, `#d73a49`).
   - ALWAYS use bright, high-contrast dark theme colors (`#79c0ff` for variables, `#7ee787` for strings/numbers, `#ff7b72` for keywords, `#ffa657` for functions).

4. **Accented Vietnamese Standard**:
   - All text, titles, questions, answers, SVG labels, and Mermaid flowchart node labels MUST use proper Vietnamese diacritics (dấu tiếng Việt). Never leave un-accented Vietnamese words in production reading content.

5. **No Forced Generic Comparison Tables**:
   - DO NOT forcibly inject a generic C/C++/Java comparison table into every lesson.
   - Only include a comparison table if the lesson explicitly requires comparing two contrasting concepts (e.g. `for` vs `while`, `break` vs `continue`, `f-string` vs `.format()`). Keep general topic lessons focused directly on the core material without clutter.

6. **Synchronized Visualizer DOM IDs & Engine Contract**:
   - All interactive visualizer JS scripts MUST strictly reference standard HTML DOM element IDs (`#visualizer-canvas`, `#custom-data-input`, `#stepper-progress`, `#stepper-bar`, `#console-output`).
   - NEVER use mismatched legacy IDs like `canvas-area` or `custom-input-data` inside JS scripts to guarantee 100% immediate execution on initial generation.
