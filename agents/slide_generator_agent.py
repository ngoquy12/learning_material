"""
agents/slide_generator_agent.py

Slide Generator Agent (Rikkei Academy PPTX Master Replay — Clean Google Slides UI with Live Previews)
===================================================================================================
Tự động sinh Slide bài giảng tương tác HTML/CSS/JS tái hiện 100% bố cục
thực tế từ ảnh mẫu PPTX Master & Google Slides UI:

1. Clean Sidebar Menu:
   - Loại bỏ tiêu đề 'Slides Overview' và icon thừa.
   - Thanh cuộn xám nhẹ bo tròn sang trọng (Slim Light Scrollbar).
   - Card Thumbnail chứa **Miniature Live Preview** thu nhỏ thực sự của từng loại Slide.

2. Page Numbering Badge (.corner-page-badge):
   - **Tất cả các slide** đều hiển thị badge đỏ chứa số trang ở góc dưới bên phải.
   - Số trang được đánh liên tục bắt đầu từ **trang 1** (Cover = 1, Agenda = 2, Content 1 = 3,...).

3. Floating Navigation Bar (Dark Navy Glassmorphism Style):
   - Tông màu **Đen Mờ Kính Thủy Tinh (Dark Navy Glassmorphism `rgba(15, 23, 42, 0.94)`)** kết hợp hiệu ứng `backdrop-filter: blur(20px)` và viền sáng tinh tế.
   - Nhãn nút tiếng Việt chuẩn **'Toàn màn hình ⛶'**.

4. Fullscreen Presentation Mode:
   - Khi bấm 'Toàn màn hình ⛶' (hoặc bấm phím F), Menu Sidebar bên trái tự động **ẨN ĐI**, phần Main Stage & Deck Container mở rộng tràn toàn bộ màn hình (100vw x 100vh).

5. Cô lập tuyệt đối cấu trúc Slide (.slide Isolation):
   - Đảm bảo 100% không bao giờ xảy ra lỗi slide dính/chồng lấn lên nhau (`position: absolute; display: none !important; opacity: 0; pointer-events: none`). Chỉ slide có `.active` mới bật `display: flex !important; z-index: 10; opacity: 1`.
"""

from __future__ import annotations

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class SlideGeneratorAgent:
    """Agent thiết kế Slide bài giảng chuẩn Rikkei Academy Master PPTX & Google Slides UI."""

    LOGO_URL = "https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png"

    def __init__(self):
        pass

    def _build_css(self) -> str:
        return """
    :root {
      --bg-main: #f1f5f9;
      --bg-sidebar: #ffffff;
      --bg-slide: #ffffff;
      --brand-red: #c01e23;
      --brand-pink-bg: #fdeaea;
      --brand-dark: #000000;
      --text-gray: #475569;
      --font-main: 'Inter', system-ui, -apple-system, sans-serif;
      --font-code: 'Fira Code', monospace;
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }
    html, body {
      width: 100vw; height: 100vh; overflow: hidden;
      background: var(--bg-main); color: var(--brand-dark);
      font-family: var(--font-main);
      display: flex; flex-direction: row;
    }

    /* Sidebar Thumbnails Menu */
    #sidebar {
      width: 240px; height: 100vh;
      background: var(--bg-sidebar);
      border-right: 1px solid #e2e8f0;
      display: flex; flex-direction: column;
      flex-shrink: 0; z-index: 100;
      box-shadow: 2px 0 10px rgba(0,0,0,0.03);
      transition: all 0.2s ease;
    }
    
    .sidebar-scroll {
      flex: 1; overflow-y: auto; padding: 20px 14px;
      display: flex; flex-direction: column; gap: 18px;
    }

    .sidebar-scroll::-webkit-scrollbar { width: 6px; }
    .sidebar-scroll::-webkit-scrollbar-track { background: transparent; }
    .sidebar-scroll::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 999px; }
    .sidebar-scroll::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

    .thumb-item {
      display: flex; align-items: flex-start; gap: 10px; cursor: pointer;
      padding: 4px; border-radius: 8px; transition: all 0.2s ease;
    }
    .thumb-item:hover { background: #f8fafc; }
    .thumb-item.active { background: #fef2f2; }

    .thumb-idx {
      font-size: 13px; font-weight: 700; color: #94a3b8; width: 16px; text-align: right; margin-top: 6px;
    }
    .thumb-item.active .thumb-idx { color: var(--brand-red); font-weight: 800; }

    .thumb-card {
      flex: 1; aspect-ratio: 16 / 9; background: #ffffff;
      border: 1.5px solid #cbd5e1; border-radius: 6px; overflow: hidden;
      position: relative; transition: all 0.2s ease;
      box-shadow: 0 2px 5px rgba(0,0,0,0.04);
      display: flex; flex-direction: column; justify-content: space-between;
    }
    .thumb-item:hover .thumb-card { border-color: #94a3b8; }
    .thumb-item.active .thumb-card {
      border-color: var(--brand-red);
      box-shadow: 0 0 0 2px rgba(192, 30, 35, 0.25), 0 4px 12px rgba(0,0,0,0.08);
    }

    /* Miniature Live Preview Designs */
    .thumb-mini-stage {
      width: 100%; height: 100%; position: relative; background: #ffffff;
      padding: 6px 8px; display: flex; flex-direction: column; justify-content: space-between;
      overflow: hidden; pointer-events: none; user-select: none;
    }

    .thumb-mini-stage.mini-cover { justify-content: center; padding-left: 20px; }
    .mini-cover-tri {
      position: absolute; left: 0; top: 50%; transform: translateY(-50%);
      width: 12px; height: 24px; background: var(--brand-red);
      clip-path: polygon(0 0, 0 100%, 100% 50%);
    }
    .mini-cover-tag { font-size: 7px; font-weight: 800; color: var(--brand-red); }
    .mini-cover-title { font-size: 8px; font-weight: 800; color: #000; line-height: 1.1; margin-top: 2px; }

    .thumb-mini-stage.mini-agenda { padding: 6px 8px; }
    .mini-agenda-h { font-size: 7px; font-weight: 900; color: var(--brand-red); margin-bottom: 4px; }
    .mini-agenda-lines { display: flex; flex-direction: column; gap: 3px; }
    .mini-agenda-line { height: 3px; background: #e2e8f0; border-radius: 2px; width: 85%; }
    .mini-agenda-line:nth-child(2) { width: 70%; }
    .mini-agenda-line:nth-child(3) { width: 90%; }

    .thumb-mini-stage.mini-content { padding: 6px 8px; }
    .mini-top-bar { position: absolute; top: 0; left: 8px; width: 24px; height: 3px; background: var(--brand-red); }
    .mini-content-h { font-size: 7px; font-weight: 800; color: #000; margin-top: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .mini-content-grid { display: flex; gap: 4px; height: 32px; margin-top: 4px; }
    .mini-col-pink { flex: 1; background: var(--brand-pink-bg); border-radius: 3px; padding: 3px; }
    .mini-col-code { flex: 1; background: #0f172a; border-radius: 3px; padding: 3px; }
    .mini-code-line { height: 2px; background: #38bdf8; width: 60%; margin-bottom: 2px; border-radius: 1px; }
    .mini-code-line.w80 { width: 80%; background: #4ade80; }

    .thumb-mini-stage.mini-summary { padding: 6px 8px; }
    .mini-summary-h { font-size: 7px; font-weight: 900; color: var(--brand-red); }
    .mini-timeline-bar { position: absolute; top: 55%; left: 8px; right: 8px; height: 1.5px; background: var(--brand-red); }
    .mini-timeline-dots { display: flex; justify-content: space-around; position: relative; z-index: 2; margin-top: 8px; }
    .mini-dot-box { width: 6px; height: 6px; border-radius: 50%; background: var(--brand-red); border: 1px solid #fff; }

    /* Main Stage */
    #main-stage {
      flex: 1; height: 100vh; position: relative;
      display: flex; align-items: center; justify-content: center;
      background: var(--bg-main); padding: 24px; overflow: hidden;
      transition: all 0.2s ease;
    }

    #deck-container {
      width: 100%; height: 100%;
      max-width: 1400px; max-height: 787.5px;
      position: relative; overflow: hidden;
      background: var(--bg-slide); border-radius: 8px;
      box-shadow: 0 12px 40px rgba(0,0,0,0.12);
      transition: all 0.2s ease;
    }

    /* Fullscreen Mode Styles */
    body.fullscreen-mode #sidebar,
    :fullscreen #sidebar {
      display: none !important;
    }

    body.fullscreen-mode #main-stage,
    :fullscreen #main-stage {
      padding: 0 !important;
      width: 100vw !important;
      height: 100vh !important;
      background: #000000 !important;
    }

    body.fullscreen-mode #deck-container,
    :fullscreen #deck-container {
      max-width: 100vw !important;
      max-height: 100vh !important;
      width: 100vw !important;
      height: 100vh !important;
      border-radius: 0 !important;
      box-shadow: none !important;
    }

    /* Strictly Isolated Slide Frame */
    .slide {
      display: none !important;
      position: absolute; top: 0; left: 0;
      width: 100%; height: 100%;
      background: var(--bg-slide); overflow: hidden;
      flex-direction: column; padding: 40px 60px;
      z-index: 1; opacity: 0; pointer-events: none;
    }

    .slide.active {
      display: flex !important;
      z-index: 10; opacity: 1; pointer-events: auto;
    }

    .footer-copyright {
      position: absolute; bottom: 18px; left: 0; right: 0;
      text-align: center; font-size: 15px; color: var(--text-gray); font-weight: 500;
      z-index: 20; pointer-events: none;
    }

    .top-right-logo {
      position: absolute; top: 24px; right: 48px; height: 42px; width: auto; object-fit: contain;
      z-index: 20;
    }

    .corner-page-badge {
      position: absolute; bottom: 0; right: 0; width: 100px; height: 100px;
      background: var(--brand-red); clip-path: polygon(100% 0, 100% 100%, 0 100%);
      display: flex; align-items: flex-end; justify-content: flex-end;
      padding: 10px 14px; color: #ffffff; font-size: 20px; font-weight: 800;
      font-family: var(--font-code); z-index: 30;
    }

    /* Cover Slide */
    .slide-cover {
      position: relative; background: #ffffff; padding: 0 !important;
      justify-content: center; align-items: flex-start;
    }
    .cover-left-triangle-svg {
      position: absolute; left: 0; top: 40%; transform: translateY(-50%);
      width: 90px; height: 160px; z-index: 5;
    }
    .cover-content-box {
      margin-left: 160px; max-width: 1100px; z-index: 10;
    }
    .cover-session-tag {
      font-size: 38px; font-weight: 800; color: var(--brand-red); margin-bottom: 8px;
    }
    .cover-main-title {
      font-size: 48px; font-weight: 800; color: #000000; line-height: 1.25; margin-bottom: 28px;
    }
    .cover-meta-text {
      font-size: 22px; color: var(--text-gray); font-weight: 600;
    }
    .cover-bottom-logo {
      position: absolute; bottom: 56px; left: 50%; transform: translateX(-50%);
      height: 44px; width: auto; object-fit: contain; z-index: 10;
    }

    /* Agenda Slide */
    .slide-agenda {
      position: relative; background: #ffffff; padding: 50px 70px !important;
    }
    .agenda-top-left-title {
      font-size: 44px; font-weight: 900; color: var(--brand-red); margin-bottom: 40px;
      letter-spacing: 1px; z-index: 10;
    }
    .agenda-list-box {
      margin-left: 20px; max-width: 1100px;
      display: flex; flex-direction: column; gap: 28px; z-index: 10;
    }
    .agenda-item-row {
      font-size: 32px; font-weight: 800; color: #000000; display: flex; align-items: center; gap: 16px;
    }

    /* Content Slide */
    .slide-content-layout {
      position: relative; padding: 40px 60px !important; background: #ffffff;
    }
    .content-top-accent-bar {
      position: absolute; top: 0; left: 60px; width: 220px; height: 20px;
      background: var(--brand-red); z-index: 10;
    }
    .content-header-title {
      font-size: 32px; font-weight: 800; margin-top: 10px; margin-bottom: 24px;
      color: var(--brand-red); display: flex; align-items: center; gap: 10px; z-index: 10;
    }
    .content-header-title .num { color: var(--brand-red); font-weight: 800; }

    .cards-container-row {
      display: flex; gap: 28px; width: 100%; flex: 1; margin-bottom: 40px; z-index: 10;
    }
    .card-column-box {
      flex: 1; background: var(--brand-pink-bg); border-radius: 12px;
      padding: 24px; display: flex; flex-direction: column; gap: 16px; overflow: hidden;
    }
    .column-title {
      font-size: 24px; font-weight: 800; color: #000000; margin-bottom: 4px;
    }
    .inner-white-card {
      background: #ffffff; border-radius: 10px; padding: 16px 20px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    }
    .inner-white-card h4 { font-size: 18px; font-weight: 800; color: #000000; margin-bottom: 4px; }
    .inner-white-card p { font-size: 15px; color: var(--text-gray); line-height: 1.5; }

    .academic-code-box {
      background: #0f172a; border-radius: 10px; padding: 22px;
      font-family: var(--font-code); font-size: 17px; color: #f8fafc;
      line-height: 1.6; height: 100%; overflow: auto;
    }
    .kw { color: #38bdf8; font-weight: 600; }
    .fn { color: #c084fc; }
    .str { color: #4ade80; }
    .cm { color: #94a3b8; font-style: italic; }
    .num-lit { color: #facc15; }

    /* Timeline Summary Slide */
    .slide-summary-timeline {
      position: relative; padding: 50px 70px !important; background: #ffffff;
      display: flex; flex-direction: column; justify-content: flex-start;
    }
    .summary-top-left-title {
      font-size: 44px; font-weight: 900; color: var(--brand-red); margin-bottom: 20px;
      letter-spacing: 1px; z-index: 10;
    }
    .timeline-container {
      width: 100%; flex: 1; position: relative; display: flex; flex-direction: column; justify-content: center; z-index: 10;
      margin-top: -20px;
    }
    .timeline-line {
      position: absolute; top: 50%; left: 0; right: 0; height: 3px; background: var(--brand-red);
      transform: translateY(-50%); z-index: 1;
    }
    .timeline-nodes-grid {
      display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; position: relative; z-index: 2;
    }
    .timeline-node {
      display: flex; flex-direction: column; align-items: center; text-align: center;
    }
    .timeline-dot {
      width: 18px; height: 18px; border-radius: 50%; background: var(--brand-red);
      border: 4px solid #ffffff; box-shadow: 0 0 0 2px var(--brand-red); margin: 16px 0;
    }
    .node-card {
      background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 18px 20px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.06); min-height: 150px; display: flex; flex-direction: column; justify-content: center; width: 100%;
    }
    .node-card h5 { font-size: 18px; font-weight: 800; color: #000000; margin-bottom: 6px; }
    .node-card p { font-size: 14px; color: var(--text-gray); line-height: 1.5; }

    /* Floating Controls Navigation Bar */
    #hover-trigger-zone {
      position: absolute; bottom: 0; left: 0; width: 100%; height: 90px; z-index: 999;
    }
    #controls {
      position: absolute; bottom: 24px; left: 50%; transform: translateX(-50%) translateY(20px);
      background: rgba(15, 23, 42, 0.94); border: 1px solid rgba(255, 255, 255, 0.18);
      backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
      border-radius: 999px; padding: 6px 18px;
      display: flex; align-items: center; gap: 14px; z-index: 1000;
      box-shadow: 0 16px 36px rgba(0, 0, 0, 0.35);
      opacity: 0; pointer-events: none; transition: opacity 0.25s ease, transform 0.25s ease;
    }
    #hover-trigger-zone:hover + #controls, #controls:hover {
      opacity: 1; pointer-events: auto; transform: translateX(-50%) translateY(0);
    }
    .btn-ctrl {
      background: rgba(255, 255, 255, 0.12); border: 1px solid rgba(255, 255, 255, 0.1); color: #ffffff;
      padding: 7px 18px; border-radius: 999px; cursor: pointer; font-size: 13.5px; font-weight: 600;
      transition: all 0.2s ease; display: flex; align-items: center; gap: 6px;
    }
    .btn-ctrl:hover { background: var(--brand-red); border-color: var(--brand-red); transform: translateY(-1px); }
    #slide-indicator { font-size: 14px; font-weight: 700; color: #ffffff; font-family: var(--font-code); padding: 0 4px; }
"""

    def _build_js(self) -> str:
        return """
    let currentIndex = 0;
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;
    const indicator = document.getElementById('slide-indicator');
    const thumbnailList = document.getElementById('thumbnail-list');

    function renderMiniaturePreview(slide, type, title) {
      if (type === 'cover') {
        return `
          <div class="thumb-mini-stage mini-cover">
            <div class="mini-cover-tri"></div>
            <div class="mini-cover-tag">Session 01</div>
            <div class="mini-cover-title">${title}</div>
          </div>`;
      } else if (type === 'agenda') {
        return `
          <div class="thumb-mini-stage mini-agenda">
            <div class="mini-agenda-h">NỘI DUNG BÀI HỌC</div>
            <div class="mini-agenda-lines">
              <div class="mini-agenda-line"></div>
              <div class="mini-agenda-line"></div>
              <div class="mini-agenda-line"></div>
            </div>
          </div>`;
      } else if (type === 'summary') {
        return `
          <div class="thumb-mini-stage mini-summary">
            <div class="mini-summary-h">TỔNG KẾT BÀI HỌC</div>
            <div class="mini-timeline-bar"></div>
            <div class="mini-timeline-dots">
              <div class="mini-dot-box"></div>
              <div class="mini-dot-box"></div>
              <div class="mini-dot-box"></div>
              <div class="mini-dot-box"></div>
            </div>
          </div>`;
      } else {
        return `
          <div class="thumb-mini-stage mini-content">
            <div class="mini-top-bar"></div>
            <div class="mini-content-h">${title}</div>
            <div class="mini-content-grid">
              <div class="mini-col-pink"></div>
              <div class="mini-col-code">
                <div class="mini-code-line"></div>
                <div class="mini-code-line w80"></div>
              </div>
            </div>
          </div>`;
      }
    }

    function buildSidebarThumbnails() {
      if (!thumbnailList) return;
      thumbnailList.innerHTML = '';
      slides.forEach((slide, idx) => {
        const title = slide.getAttribute('data-title') || `Slide ${idx + 1}`;
        const type = slide.getAttribute('data-type') || 'content';
        const item = document.createElement('div');
        item.className = `thumb-item ${idx === currentIndex ? 'active' : ''}`;
        item.onclick = () => goToSlide(idx);
        
        item.innerHTML = `
          <div class="thumb-idx">${idx + 1}</div>
          <div class="thumb-card">
            ${renderMiniaturePreview(slide, type, title)}
          </div>
        `;
        thumbnailList.appendChild(item);
      });
    }

    function goToSlide(index) {
      if (index >= 0 && index < totalSlides) {
        currentIndex = index;
        updateDeck();
      }
    }

    function updateDeck() {
      slides.forEach((slide, idx) => {
        if (idx === currentIndex) {
          slide.classList.add('active');
        } else {
          slide.classList.remove('active');
        }
      });

      const thumbItems = document.querySelectorAll('.thumb-item');
      thumbItems.forEach((item, idx) => {
        if (idx === currentIndex) {
          item.classList.add('active');
          item.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
          item.classList.remove('active');
        }
      });

      if (indicator) {
        indicator.textContent = `${currentIndex + 1} / ${totalSlides}`;
      }
    }

    function nextSlide(e) {
      if (e && e.preventDefault) e.preventDefault();
      if (currentIndex < totalSlides - 1) {
        currentIndex++;
        updateDeck();
      }
    }

    function prevSlide(e) {
      if (e && e.preventDefault) e.preventDefault();
      if (currentIndex > 0) {
        currentIndex--;
        updateDeck();
      }
    }

    function toggleFullscreen(e) {
      if (e && e.preventDefault) e.preventDefault();
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().then(() => {
          document.body.classList.add('fullscreen-mode');
        }).catch(err => {
          console.error(err);
        });
      } else {
        if (document.exitFullscreen) {
          document.exitFullscreen();
        }
      }
    }

    document.addEventListener('fullscreenchange', () => {
      if (document.fullscreenElement) {
        document.body.classList.add('fullscreen-mode');
      } else {
        document.body.classList.remove('fullscreen-mode');
      }
    });

    window.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
        nextSlide();
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        prevSlide();
      } else if (e.key === 'Home') {
        goToSlide(0);
      } else if (e.key === 'End') {
        goToSlide(totalSlides - 1);
      } else if (e.key.toLowerCase() === 'f') {
        toggleFullscreen();
      }
    });

    buildSidebarThumbnails();
    updateDeck();
"""

    def clean_title_string(self, text: str) -> str:
        """Chuyển đổi chuỗi tên/khóa thô (snake_case, identifier) thành tiêu đề Tiếng Việt đẹp, có khoảng trắng và viết hoa chuẩn."""
        if not text:
            return ""
        clean = text.strip()
        if '_' in clean and ' ' not in clean:
            words = clean.split('_')
            clean_words = []
            for w in words:
                w_lower = w.lower()
                if w_lower in ['py', 'pvm', 'cli', 'api', 'http', 'crud', 'sql', 'orm', 'json', 'url', 'id', 'vs', 'code', 'wasm']:
                    clean_words.append(w.upper())
                elif w_lower in ['va', 'va_triet_ly']:
                    clean_words.append("và")
                else:
                    clean_words.append(w.capitalize())
            clean = " ".join(clean_words)
        return clean

    def truncate_title(self, title: str, max_chars: int = 55) -> str:
        """Rút gọn tiêu đề slide nếu quá dài để hiển thị súc tích trên header."""
        if not title:
            return "Nội dung bài học"
        clean = self.clean_title_string(title)
        # Loại bỏ các tiền tố số thứ tự lặp lại nếu có
        clean = re.sub(r'^\d+[\.\:]\s*', '', clean)
        if len(clean) <= max_chars:
            return clean
        # Cắt gọn theo từ
        words = clean.split()
        short_words = []
        char_count = 0
        for w in words:
            if char_count + len(w) > max_chars:
                break
            short_words.append(w)
            char_count += len(w) + 1
        return " ".join(short_words) + "..." if short_words else clean[:max_chars] + "..."

    def _get_dynamic_column_titles_and_cards(self, scene: Dict[str, Any], short_stitle: str, narration: str, bullets: List[str]):
        """Sinh tiêu đề cột và tiêu đề thẻ linh hoạt dựa trên dữ liệu AI truyền hoặc suy luận ngữ cảnh."""
        # 1. Ưu tiên lấy trực tiếp nếu AI / Scene đã cung cấp
        col1_title = scene.get("col1_title")
        col2_title = scene.get("col2_title")
        
        # 2. Nếu chưa có, suy luận dựa trên từ khóa trong tiêu đề slide hoặc nội dung
        title_lower = short_stitle.lower()

        if any(k in title_lower for k in ["vấn đề", "trở ngại", "lỗi", "conflict", "problem"]):
            c1_t = col1_title or "Vấn Đề & Tác Động"
            c2_t = col2_title or "Giải Pháp & Cách Khắc Phục"
            h1 = "Trở Ngại Hệ Thống"
            h2 = "Hướng Xử Lý Triệt Để"
        elif any(k in title_lower for k in ["phân tích", "nguyên lý", "cơ chế", "so sánh", "concept"]):
            c1_t = col1_title or "Phân Tích Cơ Chế"
            c2_t = col2_title or "Đặc Điểm & Ứng Dụng"
            h1 = "Nguyên Lý Hoạt Động"
            h2 = "Bối Cảnh Áp Dụng"
        elif any(k in title_lower for k in ["thành phần", "cấu hình", "môi trường", "biến", "thiết lập"]):
            c1_t = col1_title or "Thành Phần Hệ Thống"
            c2_t = col2_title or "Cấu Hình & Tương Tác"
            h1 = "Thông Số Khởi Tạo"
            h2 = "Quy Tắc Thiết Lập"
        elif any(k in title_lower for k in ["quy trình", "bước", "lệnh", "step", "cli"]):
            c1_t = col1_title or "Các Bước Thực Hiện"
            c2_t = col2_title or "Mã Lệnh & Lưu Ý"
            h1 = "Thao Tác Triển Khai"
            h2 = "Lệnh CLI Tương Tác"
        elif any(k in title_lower for k in ["tổng kết", "sai lầm", "summary"]):
            c1_t = col1_title or "Tổng Kết Kiến Thức"
            c2_t = col2_title or "Sai Lầm Cần Tránh"
            h1 = "Điểm Cốt Lõi"
            h2 = "Lưu Ý Thực Chiến"
        else:
            c1_t = col1_title or "Trọng Tâm Bài Học"
            c2_t = col2_title or "Phân Tích Chi Tiết"
            h1 = "Nội Dung Chính"
            h2 = "Ứng Dụng Thực Tế"

        # Dựng HTML danh sách thẻ cho từng cột
        col1_cards_html = ""
        col2_cards_html = ""

        if len(bullets) >= 2:
            mid = len(bullets) // 2
            for idx, b in enumerate(bullets[:mid]):
                card_tag = f"{h1} #{idx+1}" if len(bullets[:mid]) > 1 else h1
                col1_cards_html += f'<div class="inner-white-card"><h4>{card_tag}</h4><p>{b}</p></div>\n'
            for idx, b in enumerate(bullets[mid:4]):
                card_tag = f"{h2} #{idx+1}" if len(bullets[mid:4]) > 1 else h2
                col2_cards_html += f'<div class="inner-white-card"><h4>{card_tag}</h4><p>{b}</p></div>\n'
        else:
            col1_cards_html = f'<div class="inner-white-card"><h4>{h1}</h4><p>{narration[:200] if narration else "Nội dung phân tích nguyên lý kỹ thuật."}</p></div>'
            col2_cards_html = f'<div class="inner-white-card"><h4>{h2}</h4><p>{narration[200:400] if len(narration) > 200 else "Áp dụng vào xây dựng ứng dụng thực chiến."}</p></div>'

        return c1_t, c2_t, col1_cards_html, col2_cards_html

    def _render_scene_content_html(self, scene: Dict[str, Any], clean_stitle: str) -> str:
        """Hàm dựng nội dung HTML cho 1 slide linh hoạt và đầy đủ thông tin giảng dạy."""
        layout_type = (scene.get("layout_type") or "").upper()
        if layout_type == "CUSTOM_RAW" and scene.get("html_content"):
            return scene.get("html_content")

        narration = scene.get("narration") or scene.get("explanation") or ""
        bullets = scene.get("bullets", [])
        code_sample = scene.get("code_sample") or scene.get("code") or ""
        mermaid_code = scene.get("mermaid") or scene.get("diagram") or ""
        layout_type = (scene.get("layout_type") or "").upper()

        if not bullets and narration:
            raw_sentences = [s.strip() for s in re.split(r'[\.\;\n]', narration) if len(s.strip()) > 10]
            bullets = raw_sentences[:4]

        # 1. MERMAID DIAGRAM
        if "MERMAID" in layout_type or mermaid_code:
            return f"""
        <div style="width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 20px;">
          <div class="mermaid" style="width: 100%; max-height: 480px; overflow: auto; background: #0f172a; padding: 20px; border-radius: 12px; border: 1px solid #334155;">
{mermaid_code}
          </div>
        </div>
"""
        # 2. SINGLE COLUMN FOCUS
        elif "SINGLE_COLUMN" in layout_type:
            bullet_cards_html = "".join([f'<div class="inner-white-card" style="margin-bottom: 12px;"><p>{b}</p></div>' for b in bullets[:4]])
            return f"""
        <div style="max-width: 900px; margin: 0 auto; width: 100%; padding: 20px;">
          <div class="inner-white-card" style="background: #ffffff; border: 2px solid var(--brand-red); border-radius: 12px; padding: 24px;">
            <h3 style="font-size: 22px; font-weight: 800; color: var(--brand-red); margin-bottom: 16px;">{clean_stitle}</h3>
            {bullet_cards_html}
          </div>
        </div>
"""
        # 3. THREE COLUMN CARDS
        elif "THREE_COLUMN" in layout_type and len(bullets) >= 3:
            cols_html = "".join([f'<div class="card-column-box" style="flex: 1; background: #ffffff; border: 1px solid #e2e8f0; padding: 20px; border-radius: 8px;"><h4 style="font-size: 18px; font-weight: 700; color: var(--brand-red); margin-bottom: 10px;">Mục #{idx+1}</h4><p>{b}</p></div>' for idx, b in enumerate(bullets[:3])])
            return f"""
        <div class="cards-container-row" style="gap: 16px;">
          {cols_html}
        </div>
"""
        # 4. WARNING GOTCHAS
        elif "WARNING" in layout_type or "GOTCHAS" in layout_type:
            bullet_cards_html = "".join([f'<div class="inner-white-card" style="margin-bottom: 12px; border-left: 5px solid #ef4444;"><p>{b}</p></div>' for b in bullets[:4]])
            return f"""
        <div style="max-width: 950px; margin: 0 auto; width: 100%; padding: 20px;">
          <div style="background: #fef2f2; border: 2px solid #ef4444; border-radius: 12px; padding: 24px;">
            <h3 style="font-size: 22px; font-weight: 800; color: #991b1b; margin-bottom: 14px;">⚠️ [CẢNH BÁO] Bẫy Cú Pháp &amp; Anti-Pattern</h3>
            {bullet_cards_html}
          </div>
        </div>
"""
        # 5. CODE DEMO EXPLAINER WITH INPUT/OUTPUT & TRICKS FOR LECTURERS
        elif code_sample or "CODE" in layout_type:
            bullet_cards_html = ""
            if bullets:
                for b in bullets[:3]:
                    bullet_cards_html += f'<div class="inner-white-card" style="margin-bottom: 8px;"><p>{b}</p></div>'
            else:
                bullet_cards_html = f'<div class="inner-white-card"><p>{narration[:250] if narration else "Mã nguồn minh họa khái niệm cốt lõi của bài học."}</p></div>'

            lecturer_trick = scene.get("lecturer_trick") or scene.get("trick")
            trick_box_html = ""
            if lecturer_trick:
                trick_box_html = f"""
                <div style="background: #fffbeb; border: 1.5px solid #f59e0b; border-radius: 8px; padding: 8px 12px; margin-top: 8px; color: #92400e; font-size: 13px;">
                  <strong style="color: #d97706;">💡 Mẹo Giảng Dạy &amp; Trick:</strong> {lecturer_trick}
                </div>"""

            ent_scenario = scene.get("enterprise_scenario") or scene.get("scenario")
            scenario_box_html = ""
            if ent_scenario:
                scenario_box_html = f"""
                <div style="background: #eff6ff; border: 1.5px solid #3b82f6; border-radius: 8px; padding: 8px 12px; margin-top: 6px; color: #1e40af; font-size: 13px;">
                  <strong style="color: #2563eb;">🏢 Bối Cảnh Thực Tế:</strong> {ent_scenario}
                </div>"""

            safe_code = code_sample.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            code_lines = safe_code.splitlines()
            formatted_code_lines = []
            for line in code_lines:
                if line.strip().startswith('#'):
                    formatted_code_lines.append(f'<span class="cm">{line}</span>')
                elif any(kw in line for kw in ['def ', 'class ', 'import ', 'from ', 'return ', 'if ', 'else:', 'elif ']):
                    line_esc = line.replace('def ', '<span class="kw">def</span> ').replace('return ', '<span class="kw">return</span> ').replace('import ', '<span class="kw">import</span> ')
                    formatted_code_lines.append(line_esc)
                else:
                    formatted_code_lines.append(line)
            code_display_html = "<br/>".join(formatted_code_lines) if formatted_code_lines else safe_code

            code_output = scene.get("code_output") or scene.get("output")
            output_box_html = ""
            if code_output:
                output_box_html = f"""
                <div style="background: #090d16; border: 1px solid #1e293b; border-radius: 8px; padding: 8px 12px; margin-top: 6px; font-family: var(--font-code); font-size: 12px; color: #10b981;">
                  <strong style="color: #38bdf8;">🖥️ KẾT QUẢ THỰC THI (CONSOLE OUTPUT):</strong>
                  <pre style="margin: 4px 0 0 0; font-family: inherit; color: #34d399; white-space: pre-wrap;">{code_output}</pre>
                </div>"""

            return f"""
        <div class="cards-container-row">
          <div class="card-column-box" style="background: #ffffff; border: 1px solid #e2e8f0; padding: 20px;">
            <h3 style="font-size: 20px; font-weight: 800; margin-bottom: 12px; color: var(--brand-red);">Khái niệm &amp; Phân tích</h3>
            {bullet_cards_html}
            {trick_box_html}
            {scenario_box_html}
          </div>
          <div class="card-column-box" style="background: transparent; padding: 0; display: flex; flex-direction: column;">
            <div class="academic-code-box">
              {code_display_html}
            </div>
            {output_box_html}
          </div>
        </div>
"""
        # 6. TWO COLUMN COMPARE / DEFAULT
        else:
            c1_title, c2_title, col1_cards, col2_cards = self._get_dynamic_column_titles_and_cards(
                scene=scene,
                short_stitle=clean_stitle,
                narration=narration,
                bullets=bullets
            )

            return f"""
        <div class="cards-container-row">
          <div class="card-column-box">
            <div class="column-title" style="color: var(--brand-red);">{c1_title}</div>
            {col1_cards}
          </div>
          <div class="card-column-box">
            <div class="column-title" style="color: var(--brand-dark);">{c2_title}</div>
            {col2_cards}
          </div>
        </div>
"""

    def generate_deck_html(self, lesson_title: str, module_name: str, scenes: List[Dict[str, Any]]) -> str:
        slides_html_parts = []
        total_pages = len(scenes) + 3
        current_year = datetime.now().year
        copyright_text = f"© {current_year} By Rikkei Academy - All rights reserved."

        cover_triangle_svg = """<svg class="cover-left-triangle-svg" viewBox="0 0 100 160"><polygon points="0,0 0,160 100,80" fill="#c01e23"/></svg>"""

        # Tách Session Tag và Tiêu đề bài học thuần túy
        session_match = re.search(r'(Session\s*\d+)', lesson_title, re.IGNORECASE)
        session_tag = f"{session_match.group(1).title()}:" if session_match else "Session 01:"

        # Loại bỏ "Session XX", "Lesson YY", dấu gạch nối ra khỏi tiêu đề chính
        pure_lesson_title = re.sub(r'Session\s*\d+\s*[\:\-]?\s*', '', lesson_title, flags=re.IGNORECASE)
        pure_lesson_title = re.sub(r'Lesson\s*\d+\s*[\:\-]?\s*', '', pure_lesson_title, flags=re.IGNORECASE).strip()
        if pure_lesson_title.startswith('-'):
            pure_lesson_title = pure_lesson_title.lstrip('- ').strip()
        if not pure_lesson_title:
            pure_lesson_title = lesson_title

        clean_cover_title = self.truncate_title(pure_lesson_title, max_chars=65)

        # 1. Cover Slide (Trang 1)
        slides_html_parts.append(f"""
    <div class="slide slide-cover active" data-type="cover" data-title="{clean_cover_title}">
      {cover_triangle_svg}
      <div class="cover-content-box">
        <div class="cover-session-tag">{session_tag}</div>
        <div class="cover-main-title">{clean_cover_title}</div>
        <div class="cover-meta-text">Môn học: {module_name}</div>
      </div>
      <img src="{self.LOGO_URL}" alt="Rikkei Academy Logo" class="cover-bottom-logo" />
      <div class="corner-page-badge">1</div>
      <div class="footer-copyright">{copyright_text}</div>
    </div>
""")

        # 2. Agenda Slide (Trang 2)
        agenda_items_html = ""
        agenda_display_scenes = scenes[:6]  # Tối đa 6 mục chính trên Agenda
        for i, scene in enumerate(agenda_display_scenes, 1):
            raw_stitle = scene.get("short_title") or scene.get("scene_title") or f"Mục {i}"
            stitle_short = self.truncate_title(raw_stitle, max_chars=50)
            agenda_items_html += f'<div class="agenda-item-row"><span>{i}.</span> <span>{stitle_short}</span></div>\n'

        slides_html_parts.append(f"""
    <div class="slide slide-agenda" data-type="agenda" data-title="Nội dung bài học">
      <div class="agenda-top-left-title">NỘI DUNG BÀI HỌC</div>
      <img src="{self.LOGO_URL}" alt="Logo" class="top-right-logo" />
      <div class="agenda-list-box">
        {agenda_items_html}
      </div>
      <div class="corner-page-badge">2</div>
      <div class="footer-copyright">{copyright_text}</div>
    </div>
""")

        # 3..N. Content Slides (Trang 3, 4, ..., N+2)
        for i, scene in enumerate(scenes, 1):
            raw_action_title = scene.get("action_title") or scene.get("scene_title") or scene.get("short_title") or f"Trọng tâm {i}"
            clean_action_title = self.truncate_title(raw_action_title, max_chars=60)
            slide_heading = f"{i:02d}. {clean_action_title}"
            page_num = i + 2

            content_inner_html = self._render_scene_content_html(scene, clean_action_title)

            slides_html_parts.append(f"""
    <div class="slide slide-content-layout" data-type="content" data-title="{slide_heading}">
      <div class="content-top-accent-bar"></div>
      <img src="{self.LOGO_URL}" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        {slide_heading}
      </div>
      {content_inner_html}
      <div class="corner-page-badge">{page_num}</div>
      <div class="footer-copyright">{copyright_text}</div>
    </div>
""")

        # Timeline Summary Slide (Trang cuối N+3)
        recap_page_num = len(scenes) + 3
        timeline_nodes_html = ""
        summary_scenes = scenes[:4]
        for idx, sc in enumerate(summary_scenes, 1):
            raw_stitle = sc.get("short_title") or sc.get("scene_title") or f"Mục {idx}"
            stitle_short = self.truncate_title(raw_stitle, max_chars=35)
            narration_snippet = (sc.get("narration") or "Tóm tắt điểm cốt lõi bài học.")[:90]
            is_top = (idx % 2 == 1)
            if is_top:
                timeline_nodes_html += f"""
          <div class="timeline-node">
            <div class="node-card" style="margin-bottom: 24px;">
              <h5>{idx}. {stitle_short}</h5>
              <p>{narration_snippet}...</p>
            </div>
            <div class="timeline-dot"></div>
          </div>"""
            else:
                timeline_nodes_html += f"""
          <div class="timeline-node">
            <div class="timeline-dot" style="margin-top: 60px;"></div>
            <div class="node-card" style="margin-top: 24px;">
              <h5>{idx}. {stitle_short}</h5>
              <p>{narration_snippet}...</p>
            </div>
          </div>"""

        slides_html_parts.append(f"""
    <div class="slide slide-summary-timeline" data-type="summary" data-title="Tổng kết bài học">
      <div class="summary-top-left-title">TỔNG KẾT BÀI HỌC</div>
      <img src="{self.LOGO_URL}" alt="Logo" class="top-right-logo" />
      <div class="timeline-container">
        <div class="timeline-line"></div>
        <div class="timeline-nodes-grid">
          {timeline_nodes_html}
        </div>
      </div>
      <div class="corner-page-badge">{recap_page_num}</div>
      <div class="footer-copyright">{copyright_text}</div>
    </div>
""")

        full_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{clean_cover_title} — Rikkei Master Slide Presentation</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Fira+Code:wght@500;600&display=swap" rel="stylesheet" />
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', () => {{
      if (window.mermaid) {{
        mermaid.initialize({{ startOnLoad: true, theme: 'dark', securityLevel: 'loose' }});
      }}
    }});
  </script>
  <style>
{self._build_css()}
  </style>
</head>
<body>

  <div id="sidebar">
    <div class="sidebar-scroll" id="thumbnail-list"></div>
  </div>

  <div id="main-stage">
    <div id="deck-container">
{"".join(slides_html_parts)}
    </div>

    <div id="hover-trigger-zone"></div>
    <div id="controls">
      <button type="button" class="btn-ctrl" onclick="prevSlide(event)">◀ Trước</button>
      <span id="slide-indicator">1 / {total_pages}</span>
      <button type="button" class="btn-ctrl" onclick="nextSlide(event)">Sau ▶</button>
      <button type="button" class="btn-ctrl" onclick="toggleFullscreen(event)">Toàn màn hình ⛶</button>
    </div>
  </div>

  <script>
{self._build_js()}
  </script>
</body>
</html>"""
        return full_html

    def generate_session_deck_html(self, session_title: str, module_name: str, lessons_data: List[Dict[str, Any]]) -> str:
        """Sinh duy nhất một file Master Slide HTML tổng hợp toàn bộ các Lesson trong một Session.
        lessons_data: List[{ 'lesson_id': 'Lesson 01', 'lesson_title': '...', 'scenes': [...] }, ...]
        """
        all_slides_html_parts = []
        total_pages = 2  # Cover + Session Agenda

        for l_data in lessons_data:
            total_pages += len(l_data.get("scenes", []))

        current_year = datetime.now().year
        copyright_text = f"© {current_year} By Rikkei Academy - All rights reserved."
        cover_triangle_svg = """<svg class="cover-left-triangle-svg" viewBox="0 0 100 160"><polygon points="0,0 0,160 100,80" fill="#be111c"/></svg>"""

        clean_session_title = self.clean_title_string(session_title)
        
        # Parse Session prefix vs main topic name
        m_sess = re.search(r'^(Session\s*\d+)\s*[:-]\s*(.*)', clean_session_title, re.IGNORECASE)
        if m_sess:
            session_tag_text = m_sess.group(1).strip()
            main_title_text = m_sess.group(2).strip()
        else:
            session_tag_text = "Session Slide Master"
            main_title_text = clean_session_title

        clean_module_name = module_name.replace("NIKKEI ACADEMY", "Lập trình Python").replace("RIKKEI ACADEMY", "Lập trình Python").strip()
        if not clean_module_name or clean_module_name.isupper():
            clean_module_name = "Lập trình Python"

        # 1. Master Cover Slide
        all_slides_html_parts.append(f"""
    <div class="slide slide-cover active" data-type="cover" data-title="{clean_session_title}">
      {cover_triangle_svg}
      <div class="cover-content-box">
        <div class="cover-session-tag" style="color: #be111c; font-size: 22px; font-weight: 800; text-transform: none; margin-bottom: 8px;">{session_tag_text}</div>
        <div class="cover-main-title" style="color: #0f172a; font-size: 34px; font-weight: 900; text-transform: none; line-height: 1.25;">{main_title_text}</div>
        <div class="cover-meta-text" style="color: #475569; font-size: 14px; text-transform: none; margin-top: 12px;">Môn học: {clean_module_name} — Tổng số bài học: {len(lessons_data)}</div>
      </div>
      <img src="{self.LOGO_URL}" alt="Rikkei Education Logo" class="cover-bottom-logo" />
      <div class="corner-page-badge">1</div>
      <div class="footer-copyright">{copyright_text}</div>
    </div>
""")

        # 2. Master Session Agenda Slide
        session_agenda_items_html = ""
        for i, l_data in enumerate(lessons_data, 1):
            l_title = l_data.get("lesson_title", f"Bài học {i}")
            clean_l_title = self.clean_title_string(l_title)
            session_agenda_items_html += f'<div class="agenda-item-row" style="font-size: 15px; margin-bottom: 10px;"><span>{i:02d}.</span> <span style="font-weight: 600; color: #0f172a;">{clean_l_title}</span></div>\n'

        all_slides_html_parts.append(f"""
    <div class="slide slide-agenda" data-type="agenda" data-title="Nội dung tổng quan Session">
      <div class="agenda-top-left-title" style="color: #be111c; font-weight: 800; font-size: 22px; text-transform: none;">Nội dung tổng quan Session</div>
      <img src="{self.LOGO_URL}" alt="Logo" class="top-right-logo" />
      <div class="agenda-list-box" style="margin-top: 24px;">
        {session_agenda_items_html}
      </div>
      <div class="corner-page-badge">2</div>
      <div class="footer-copyright">{copyright_text}</div>
    </div>
""")

        current_page = 3
        # Iteration across lessons & scenes
        for l_idx, l_data in enumerate(lessons_data, 1):
            l_title = l_data.get("lesson_title", f"Bài học {l_idx}")
            clean_l_title = self.clean_title_string(l_title)
            scenes = l_data.get("scenes", [])

            for s_idx, scene in enumerate(scenes, 1):
                raw_stitle = scene.get("action_title") or scene.get("short_title") or scene.get("scene_title") or f"Chủ đề {s_idx}"
                clean_stitle = self.clean_title_string(raw_stitle)
                
                # Strip duplicate "01.", "[01.01]" prefixes from clean_stitle
                clean_stitle = re.sub(r'^\s*(\[\d+\.\d+\]|\d+\.)\s*', '', clean_stitle).strip()

                main_large_title = f"{clean_l_title} - {s_idx}"
                slide_heading_attr = f"{main_large_title} - {clean_stitle}"

                content_inner_html = self._render_scene_content_html(scene, clean_stitle)
                all_slides_html_parts.append(f"""
    <div class="slide slide-content-layout" data-type="content" data-title="{slide_heading_attr}">
      <div class="content-top-accent-bar" style="background: #be111c;"></div>
      <img src="{self.LOGO_URL}" alt="Logo" class="top-right-logo" />
      <div class="content-header-box" style="margin-bottom: 16px;">
        <h2 style="font-family: 'Montserrat', sans-serif; font-weight: 800; font-size: 22px; color: #be111c; margin: 0; line-height: 1.2; text-transform: none;">
          {main_large_title}
        </h2>
        <h3 style="font-family: 'Inter', sans-serif; font-weight: 700; font-size: 16px; color: #0f172a; margin-top: 6px; line-height: 1.3; text-transform: none;">
          {clean_stitle}
        </h3>
      </div>
      {content_inner_html}
      <div class="corner-page-badge">{current_page}</div>
      <div class="footer-copyright">{copyright_text}</div>
    </div>
""")
                current_page += 1

        full_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{clean_session_title} — Presentation</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Montserrat:wght@700;800;900&family=Fira+Code:wght@500;600&display=swap" rel="stylesheet" />
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', () => {{
      if (window.mermaid) {{
        mermaid.initialize({{ startOnLoad: true, theme: 'dark', securityLevel: 'loose' }});
      }}
    }});
  </script>
  <style>
{self._build_css()}
  </style>
</head>
<body>

  <div id="sidebar">
    <div class="sidebar-scroll" id="thumbnail-list"></div>
  </div>

  <div id="main-stage">
    <div id="deck-container">
{"".join(all_slides_html_parts)}
    </div>

    <div id="hover-trigger-zone"></div>
    <div id="controls">
      <button type="button" class="btn-ctrl" onclick="prevSlide(event)">◀ Trước</button>
      <span id="slide-indicator">1 / {total_pages}</span>
      <button type="button" class="btn-ctrl" onclick="nextSlide(event)">Sau ▶</button>
      <button type="button" class="btn-ctrl" onclick="toggleFullscreen(event)">Toàn màn hình ⛶</button>
    </div>
  </div>

  <script>
{self._build_js()}
  </script>
</body>
</html>"""
        return full_html


slide_generator_agent = SlideGeneratorAgent()
