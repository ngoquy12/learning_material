<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Toán tử logic — Rikkei Master Slide Presentation</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Fira+Code:wght@500;600&display=swap" rel="stylesheet" />
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', () => {
      if (window.mermaid) {
        mermaid.initialize({ startOnLoad: true, theme: 'dark', securityLevel: 'loose' });
      }
    });
  </script>
  <style>

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

  </style>
</head>
<body>

  <div id="sidebar">
    <div class="sidebar-scroll" id="thumbnail-list"></div>
  </div>

  <div id="main-stage">
    <div id="deck-container">

    <div class="slide slide-cover active" data-type="cover" data-title="Toán tử logic">
      <svg class="cover-left-triangle-svg" viewBox="0 0 100 160"><polygon points="0,0 0,160 100,80" fill="#c01e23"/></svg>
      <div class="cover-content-box">
        <div class="cover-session-tag">Session 02:</div>
        <div class="cover-main-title">Toán tử logic</div>
        <div class="cover-meta-text">Môn học: PYTHON/CORE</div>
      </div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Rikkei Academy Logo" class="cover-bottom-logo" />
      <div class="corner-page-badge">1</div>
      <div class="footer-copyright">© 2026 By Rikkei Academy - All rights reserved.</div>
    </div>

    <div class="slide slide-agenda" data-type="agenda" data-title="Nội dung bài học">
      <div class="agenda-top-left-title">NỘI DUNG BÀI HỌC</div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="agenda-list-box">
        <div class="agenda-item-row"><span>1.</span> <span>Đặt Vấn Đề & Bối Cảnh</span></div>
<div class="agenda-item-row"><span>2.</span> <span>Toán tử logic (Logical Operators)</span></div>
<div class="agenda-item-row"><span>3.</span> <span>Toán tử logic 'and' (Conjunction)</span></div>
<div class="agenda-item-row"><span>4.</span> <span>Toán tử logic 'or' (Disjunction)</span></div>
<div class="agenda-item-row"><span>5.</span> <span>Toán tử logic 'not' (Negation)</span></div>
<div class="agenda-item-row"><span>6.</span> <span>Thứ tự ưu tiên toán tử logic (Precedence)</span></div>

      </div>
      <div class="corner-page-badge">2</div>
      <div class="footer-copyright">© 2026 By Rikkei Academy - All rights reserved.</div>
    </div>

    <div class="slide slide-content-layout" data-type="content" data-title="01. Đặt Vấn Đề & Bối Cảnh Thực Tế Doanh Nghiệp">
      <div class="content-top-accent-bar"></div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        01. Đặt Vấn Đề & Bối Cảnh Thực Tế Doanh Nghiệp
      </div>
      
        <div class="cards-container-row">
          <div class="card-column-box">
            <div class="column-title" style="color: var(--brand-red);">Vấn Đề & Tác Động</div>
            <div class="inner-white-card"><h4>Trở Ngại Hệ Thống #1</h4><p>- Hệ thống xét duyệt tự động của các doanh nghiệp tài chính đòi hỏi quá trình đánh giá hồ sơ khách hàng diễn ra nhanh chóng, nhất quán và tuyệt đối chính xác</p></div>
<div class="inner-white-card"><h4>Trở Ngại Hệ Thống #2</h4><p>- Khi xây dựng thực tế module quyết định giải ngân, lập trình viên thường đối mặt với bài toán kiểm tra tập hợp nhiều điều kiện ràng buộc đồng thời</p></div>

          </div>
          <div class="card-column-box">
            <div class="column-title" style="color: var(--brand-dark);">Giải Pháp & Cách Khắc Phục</div>
            <div class="inner-white-card"><h4>Hướng Xử Lý Triệt Để #1</h4><p>- Ví dụ thực tế: Một khách hàng chỉ được duyệt vay lãi suất ưu đãi nếu đáp ứng ba tiêu chuẩn sau:</p></div>
<div class="inner-white-card"><h4>Hướng Xử Lý Triệt Để #2</h4><p>- Tiêu chuẩn 1: Khách hàng phải có điểm tín dụng từ 700 trở lên</p></div>

          </div>
        </div>

      <div class="corner-page-badge">3</div>
      <div class="footer-copyright">© 2026 By Rikkei Academy - All rights reserved.</div>
    </div>

    <div class="slide slide-content-layout" data-type="content" data-title="02. Bản Chất Kỹ Thuật: Toán tử logic (Logical Operators)">
      <div class="content-top-accent-bar"></div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        02. Bản Chất Kỹ Thuật: Toán tử logic (Logical Operators)
      </div>
      
        <div class="cards-container-row">
          <div class="card-column-box" style="background: #ffffff; border: 1px solid #e2e8f0; padding: 20px;">
            <h3 style="font-size: 20px; font-weight: 800; margin-bottom: 12px; color: var(--brand-red);">Khái niệm &amp; Phân tích</h3>
            <div class="inner-white-card" style="margin-bottom: 8px;"><p>Các toán tử dùng để kết hợp các biểu thức so sánh để tạo thành biểu thức logic phức hợp hơn, bao gồm 'and', 'or', và 'not'</p></div><div class="inner-white-card" style="margin-bottom: 8px;"><p>Kết quả trả về luôn là giá trị boolean (True hoặc False)</p></div>
            
                <div style="background: #fffbeb; border: 1.5px solid #f59e0b; border-radius: 8px; padding: 8px 12px; margin-top: 8px; color: #92400e; font-size: 13px;">
                  <strong style="color: #d97706;">💡 Mẹo Giảng Dạy &amp; Trick:</strong> Nhấn mạnh cơ chế hoạt động thực tế của 'Toán tử logic (Logical Operators)' giúp tối ưu hiệu năng và hạn chế lỗi tại runtime.
                </div>
            
                <div style="background: #eff6ff; border: 1.5px solid #3b82f6; border-radius: 8px; padding: 8px 12px; margin-top: 6px; color: #1e40af; font-size: 13px;">
                  <strong style="color: #2563eb;">🏢 Bối Cảnh Thực Tế:</strong> Áp dụng 'Toán tử logic (Logical Operators)' trong module xử lý nghiệp vụ của hệ thống doanh nghiệp thực tế.
                </div>
          </div>
          <div class="card-column-box" style="background: transparent; padding: 0; display: flex; flex-direction: column;">
            <div class="academic-code-box">
              x = True<br/>y = False<br/><br/><span class="cm"># Kiem tra toan tu and, or, not</span><br/>print("Ket qua True and False:", x and y)<br/>print("Ket qua True or False:", x or y)<br/>print("Ket qua not True:", not x)
            </div>
            
                <div style="background: #090d16; border: 1px solid #1e293b; border-radius: 8px; padding: 8px 12px; margin-top: 6px; font-family: var(--font-code); font-size: 12px; color: #10b981;">
                  <strong style="color: #38bdf8;">🖥️ KẾT QUẢ THỰC THI (CONSOLE OUTPUT):</strong>
                  <pre style="margin: 4px 0 0 0; font-family: inherit; color: #34d399; white-space: pre-wrap;">[CONSOLE OUTPUT]: Thực thi chương trình hoàn tất - Không có lỗi Runtime.</pre>
                </div>
          </div>
        </div>

      <div class="corner-page-badge">4</div>
      <div class="footer-copyright">© 2026 By Rikkei Academy - All rights reserved.</div>
    </div>

    <div class="slide slide-content-layout" data-type="content" data-title="03. Bản Chất Kỹ Thuật: Toán tử logic 'and' (Conjunction)">
      <div class="content-top-accent-bar"></div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        03. Bản Chất Kỹ Thuật: Toán tử logic 'and' (Conjunction)
      </div>
      
        <div class="cards-container-row">
          <div class="card-column-box" style="background: #ffffff; border: 1px solid #e2e8f0; padding: 20px;">
            <h3 style="font-size: 20px; font-weight: 800; margin-bottom: 12px; color: var(--brand-red);">Khái niệm &amp; Phân tích</h3>
            <div class="inner-white-card" style="margin-bottom: 8px;"><p>Phép hội logic</p></div><div class="inner-white-card" style="margin-bottom: 8px;"><p>Biểu thức 'A and B' chỉ trả về True khi cả hai vế A và B đều bằng True</p></div><div class="inner-white-card" style="margin-bottom: 8px;"><p>Trả về False trong bất kỳ trường hợp nào khác</p></div>
            
                <div style="background: #fffbeb; border: 1.5px solid #f59e0b; border-radius: 8px; padding: 8px 12px; margin-top: 8px; color: #92400e; font-size: 13px;">
                  <strong style="color: #d97706;">💡 Mẹo Giảng Dạy &amp; Trick:</strong> Nhấn mạnh cơ chế hoạt động thực tế của 'Toán tử logic 'and' (Conjunction)' giúp tối ưu hiệu năng và hạn chế lỗi tại runtime.
                </div>
            
                <div style="background: #eff6ff; border: 1.5px solid #3b82f6; border-radius: 8px; padding: 8px 12px; margin-top: 6px; color: #1e40af; font-size: 13px;">
                  <strong style="color: #2563eb;">🏢 Bối Cảnh Thực Tế:</strong> Áp dụng 'Toán tử logic 'and' (Conjunction)' trong module xử lý nghiệp vụ của hệ thống doanh nghiệp thực tế.
                </div>
          </div>
          <div class="card-column-box" style="background: transparent; padding: 0; display: flex; flex-direction: column;">
            <div class="academic-code-box">
              a = True<br/>b = False<br/>c = False<br/><br/><span class="cm"># Mac dinh: 'not' thuc hien truoc, den 'and', cuoi cung la 'or'</span><br/><span class="cm"># b and not c equivalent to: False and True -&gt; False</span><br/><span class="cm"># a or False equivalent to: True or False -&gt; True</span><br/>ket_qua_mac_dinh = a or b and not c<br/>print("Mac dinh khong ngoac:", ket_qua_mac_dinh)<br/><br/><span class="cm"># Dung ngoac don de thay doi thu tu uu tien</span><br/>ket_qua_thay_doi = (a or b) and (not c)<br/>print("Co dung ngoac don:", ket_qua_thay_doi)
            </div>
            
                <div style="background: #090d16; border: 1px solid #1e293b; border-radius: 8px; padding: 8px 12px; margin-top: 6px; font-family: var(--font-code); font-size: 12px; color: #10b981;">
                  <strong style="color: #38bdf8;">🖥️ KẾT QUẢ THỰC THI (CONSOLE OUTPUT):</strong>
                  <pre style="margin: 4px 0 0 0; font-family: inherit; color: #34d399; white-space: pre-wrap;">[CONSOLE OUTPUT]: Thực thi chương trình hoàn tất - Không có lỗi Runtime.</pre>
                </div>
          </div>
        </div>

      <div class="corner-page-badge">5</div>
      <div class="footer-copyright">© 2026 By Rikkei Academy - All rights reserved.</div>
    </div>

    <div class="slide slide-content-layout" data-type="content" data-title="04. Bản Chất Kỹ Thuật: Toán tử logic 'or' (Disjunction)">
      <div class="content-top-accent-bar"></div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        04. Bản Chất Kỹ Thuật: Toán tử logic 'or' (Disjunction)
      </div>
      
        <div class="cards-container-row">
          <div class="card-column-box" style="background: #ffffff; border: 1px solid #e2e8f0; padding: 20px;">
            <h3 style="font-size: 20px; font-weight: 800; margin-bottom: 12px; color: var(--brand-red);">Khái niệm &amp; Phân tích</h3>
            <div class="inner-white-card" style="margin-bottom: 8px;"><p>Phép tuyển logic</p></div><div class="inner-white-card" style="margin-bottom: 8px;"><p>Biểu thức 'A or B' trả về True khi có ít nhất một vế bằng True</p></div><div class="inner-white-card" style="margin-bottom: 8px;"><p>Chỉ trả về False khi cả hai vế cùng bằng False</p></div>
            
                <div style="background: #fffbeb; border: 1.5px solid #f59e0b; border-radius: 8px; padding: 8px 12px; margin-top: 8px; color: #92400e; font-size: 13px;">
                  <strong style="color: #d97706;">💡 Mẹo Giảng Dạy &amp; Trick:</strong> Nhấn mạnh cơ chế hoạt động thực tế của 'Toán tử logic 'or' (Disjunction)' giúp tối ưu hiệu năng và hạn chế lỗi tại runtime.
                </div>
            
                <div style="background: #eff6ff; border: 1.5px solid #3b82f6; border-radius: 8px; padding: 8px 12px; margin-top: 6px; color: #1e40af; font-size: 13px;">
                  <strong style="color: #2563eb;">🏢 Bối Cảnh Thực Tế:</strong> Áp dụng 'Toán tử logic 'or' (Disjunction)' trong module xử lý nghiệp vụ của hệ thống doanh nghiệp thực tế.
                </div>
          </div>
          <div class="card-column-box" style="background: transparent; padding: 0; display: flex; flex-direction: column;">
            <div class="academic-code-box">
              <span class="cm"># Nhap thong tin tu nguoi dung</span><br/>tuoi_nhap = input("Nhap tuoi cua ban: ")<br/>tuoi = int(tuoi_nhap)<br/><br/>la_hoc_sinh_nhap = input("Co phai hoc sinh khong? (yes/no): ")<br/>la_hoc_sing_hop_le = la_hoc_sinh_nhap.strip().lower() == "yes"<br/><br/><span class="cm"># Kiem tra dieu kien nhan uu dai (theo chuan PEP 8)</span><br/>co_uu_dai = (tuoi &lt; 18) or la_hoc_sing_hop_le<br/><br/><span class="cm"># In ket qua</span><br/>print("Ket qua dung chuan PEP 8 de kiem tra uu dai:", co_uu_dai)
            </div>
            
                <div style="background: #090d16; border: 1px solid #1e293b; border-radius: 8px; padding: 8px 12px; margin-top: 6px; font-family: var(--font-code); font-size: 12px; color: #10b981;">
                  <strong style="color: #38bdf8;">🖥️ KẾT QUẢ THỰC THI (CONSOLE OUTPUT):</strong>
                  <pre style="margin: 4px 0 0 0; font-family: inherit; color: #34d399; white-space: pre-wrap;">[CONSOLE OUTPUT]: Thực thi chương trình hoàn tất - Không có lỗi Runtime.</pre>
                </div>
          </div>
        </div>

      <div class="corner-page-badge">6</div>
      <div class="footer-copyright">© 2026 By Rikkei Academy - All rights reserved.</div>
    </div>

    <div class="slide slide-content-layout" data-type="content" data-title="05. Bản Chất Kỹ Thuật: Toán tử logic 'not' (Negation)">
      <div class="content-top-accent-bar"></div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        05. Bản Chất Kỹ Thuật: Toán tử logic 'not' (Negation)
      </div>
      
        <div class="cards-container-row">
          <div class="card-column-box" style="background: #ffffff; border: 1px solid #e2e8f0; padding: 20px;">
            <h3 style="font-size: 20px; font-weight: 800; margin-bottom: 12px; color: var(--brand-red);">Khái niệm &amp; Phân tích</h3>
            <div class="inner-white-card" style="margin-bottom: 8px;"><p>Phép phủ định logic</p></div><div class="inner-white-card" style="margin-bottom: 8px;"><p>Là toán tử một ngôi dùng để đổi ngược giá trị chân trị của toán hạng</p></div><div class="inner-white-card" style="margin-bottom: 8px;"><p>'not True' trở thành False, và 'not False' trở thành True</p></div>
            
                <div style="background: #fffbeb; border: 1.5px solid #f59e0b; border-radius: 8px; padding: 8px 12px; margin-top: 8px; color: #92400e; font-size: 13px;">
                  <strong style="color: #d97706;">💡 Mẹo Giảng Dạy &amp; Trick:</strong> Nhấn mạnh cơ chế hoạt động thực tế của 'Toán tử logic 'not' (Negation)' giúp tối ưu hiệu năng và hạn chế lỗi tại runtime.
                </div>
            
                <div style="background: #eff6ff; border: 1.5px solid #3b82f6; border-radius: 8px; padding: 8px 12px; margin-top: 6px; color: #1e40af; font-size: 13px;">
                  <strong style="color: #2563eb;">🏢 Bối Cảnh Thực Tế:</strong> Áp dụng 'Toán tử logic 'not' (Negation)' trong module xử lý nghiệp vụ của hệ thống doanh nghiệp thực tế.
                </div>
          </div>
          <div class="card-column-box" style="background: transparent; padding: 0; display: flex; flex-direction: column;">
            <div class="academic-code-box">
              <span class="cm"># Bai toan: Duyet vay von (Thu nhap tren 15 trieu va khong co no xau)</span><br/>thu_nhap = 18<br/>co_no_xau = False<br/><br/><span class="cm"># --- LOI LOGIC THUONG GAP (Dung sai toan tu) ---</span><br/><span class="cm"># duoc_duyet_wrong = thu_nhap &gt; 15 or not co_no_xau  # Loi logic vi or cho phep 1 trong 2 du dieu kien</span><br/><br/><span class="cm"># --- LOGIC CHUAN XAC ---</span><br/>duoc_duyet_dung = (thu_nhap &gt; 15) and (not co_no_xau)<br/><br/>print("Ket qua duyet vay dung logic:", duoc_duyet_dung)
            </div>
            
                <div style="background: #090d16; border: 1px solid #1e293b; border-radius: 8px; padding: 8px 12px; margin-top: 6px; font-family: var(--font-code); font-size: 12px; color: #10b981;">
                  <strong style="color: #38bdf8;">🖥️ KẾT QUẢ THỰC THI (CONSOLE OUTPUT):</strong>
                  <pre style="margin: 4px 0 0 0; font-family: inherit; color: #34d399; white-space: pre-wrap;">[CONSOLE OUTPUT]: Thực thi chương trình hoàn tất - Không có lỗi Runtime.</pre>
                </div>
          </div>
        </div>

      <div class="corner-page-badge">7</div>
      <div class="footer-copyright">© 2026 By Rikkei Academy - All rights reserved.</div>
    </div>

    <div class="slide slide-content-layout" data-type="content" data-title="06. Bản Chất Kỹ Thuật: Thứ tự ưu tiên toán tử logic (Precedence)">
      <div class="content-top-accent-bar"></div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        06. Bản Chất Kỹ Thuật: Thứ tự ưu tiên toán tử logic (Precedence)
      </div>
      
        <div class="cards-container-row">
          <div class="card-column-box" style="background: #ffffff; border: 1px solid #e2e8f0; padding: 20px;">
            <h3 style="font-size: 20px; font-weight: 800; margin-bottom: 12px; color: var(--brand-red);">Khái niệm &amp; Phân tích</h3>
            <div class="inner-white-card" style="margin-bottom: 8px;"><p>Quy tắc quyết định thứ tự tính toán trong biểu thức logic phức hợp</p></div><div class="inner-white-card" style="margin-bottom: 8px;"><p>Độ ưu tiên giảm dần từ: dấu ngoặc tròn '()' -> toán tử 'not' -> toán tử 'and' -> toán tử 'or'</p></div>
            
                <div style="background: #fffbeb; border: 1.5px solid #f59e0b; border-radius: 8px; padding: 8px 12px; margin-top: 8px; color: #92400e; font-size: 13px;">
                  <strong style="color: #d97706;">💡 Mẹo Giảng Dạy &amp; Trick:</strong> Nhấn mạnh cơ chế hoạt động thực tế của 'Thứ tự ưu tiên toán tử logic (Precedence)' giúp tối ưu hiệu năng và hạn chế lỗi tại runtime.
                </div>
            
                <div style="background: #eff6ff; border: 1.5px solid #3b82f6; border-radius: 8px; padding: 8px 12px; margin-top: 6px; color: #1e40af; font-size: 13px;">
                  <strong style="color: #2563eb;">🏢 Bối Cảnh Thực Tế:</strong> Áp dụng 'Thứ tự ưu tiên toán tử logic (Precedence)' trong module xử lý nghiệp vụ của hệ thống doanh nghiệp thực tế.
                </div>
          </div>
          <div class="card-column-box" style="background: transparent; padding: 0; display: flex; flex-direction: column;">
            <div class="academic-code-box">
              x = True<br/>y = False<br/><br/><span class="cm"># Kiem tra toan tu and, or, not</span><br/>print("Ket qua True and False:", x and y)<br/>print("Ket qua True or False:", x or y)<br/>print("Ket qua not True:", not x)
            </div>
            
                <div style="background: #090d16; border: 1px solid #1e293b; border-radius: 8px; padding: 8px 12px; margin-top: 6px; font-family: var(--font-code); font-size: 12px; color: #10b981;">
                  <strong style="color: #38bdf8;">🖥️ KẾT QUẢ THỰC THI (CONSOLE OUTPUT):</strong>
                  <pre style="margin: 4px 0 0 0; font-family: inherit; color: #34d399; white-space: pre-wrap;">[CONSOLE OUTPUT]: Thực thi chương trình hoàn tất - Không có lỗi Runtime.</pre>
                </div>
          </div>
        </div>

      <div class="corner-page-badge">8</div>
      <div class="footer-copyright">© 2026 By Rikkei Academy - All rights reserved.</div>
    </div>

    <div class="slide slide-content-layout" data-type="content" data-title="07. Bản Chất Kỹ Thuật: Ngoặc đơn trong biểu thức logic...">
      <div class="content-top-accent-bar"></div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        07. Bản Chất Kỹ Thuật: Ngoặc đơn trong biểu thức logic...
      </div>
      
        <div class="cards-container-row">
          <div class="card-column-box" style="background: #ffffff; border: 1px solid #e2e8f0; padding: 20px;">
            <h3 style="font-size: 20px; font-weight: 800; margin-bottom: 12px; color: var(--brand-red);">Khái niệm &amp; Phân tích</h3>
            <div class="inner-white-card" style="margin-bottom: 8px;"><p>Cặp ngoặc tròn '()' dùng để gom nhóm các biểu thức con, có độ ưu tiên cao nhất, giúp ép buộc một phần biểu thức tính toán trước và làm mã nguồn rõ ràng, tránh mơ hồ</p></div>
            
                <div style="background: #fffbeb; border: 1.5px solid #f59e0b; border-radius: 8px; padding: 8px 12px; margin-top: 8px; color: #92400e; font-size: 13px;">
                  <strong style="color: #d97706;">💡 Mẹo Giảng Dạy &amp; Trick:</strong> Nhấn mạnh cơ chế hoạt động thực tế của 'Ngoặc đơn trong biểu thức logic (Parentheses)' giúp tối ưu hiệu năng và hạn chế lỗi tại runtime.
                </div>
            
                <div style="background: #eff6ff; border: 1.5px solid #3b82f6; border-radius: 8px; padding: 8px 12px; margin-top: 6px; color: #1e40af; font-size: 13px;">
                  <strong style="color: #2563eb;">🏢 Bối Cảnh Thực Tế:</strong> Áp dụng 'Ngoặc đơn trong biểu thức logic (Parentheses)' trong module xử lý nghiệp vụ của hệ thống doanh nghiệp thực tế.
                </div>
          </div>
          <div class="card-column-box" style="background: transparent; padding: 0; display: flex; flex-direction: column;">
            <div class="academic-code-box">
              x = True<br/>y = False<br/><br/><span class="cm"># Kiem tra toan tu and, or, not</span><br/>print("Ket qua True and False:", x and y)<br/>print("Ket qua True or False:", x or y)<br/>print("Ket qua not True:", not x)
            </div>
            
                <div style="background: #090d16; border: 1px solid #1e293b; border-radius: 8px; padding: 8px 12px; margin-top: 6px; font-family: var(--font-code); font-size: 12px; color: #10b981;">
                  <strong style="color: #38bdf8;">🖥️ KẾT QUẢ THỰC THI (CONSOLE OUTPUT):</strong>
                  <pre style="margin: 4px 0 0 0; font-family: inherit; color: #34d399; white-space: pre-wrap;">[CONSOLE OUTPUT]: Thực thi chương trình hoàn tất - Không có lỗi Runtime.</pre>
                </div>
          </div>
        </div>

      <div class="corner-page-badge">9</div>
      <div class="footer-copyright">© 2026 By Rikkei Academy - All rights reserved.</div>
    </div>

    <div class="slide slide-content-layout" data-type="content" data-title="08. Bản Chất Kỹ Thuật: Chuẩn PEP 8 cho biểu thức logic (PEP 8...">
      <div class="content-top-accent-bar"></div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        08. Bản Chất Kỹ Thuật: Chuẩn PEP 8 cho biểu thức logic (PEP 8...
      </div>
      
        <div class="cards-container-row">
          <div class="card-column-box" style="background: #ffffff; border: 1px solid #e2e8f0; padding: 20px;">
            <h3 style="font-size: 20px; font-weight: 800; margin-bottom: 12px; color: var(--brand-red);">Khái niệm &amp; Phân tích</h3>
            <div class="inner-white-card" style="margin-bottom: 8px;"><p>Các quy tắc định dạng mã nguồn Python như: đặt một khoảng trắng xung quanh các toán tử so sánh (>, <, ==) và toán tử logic (and, or), không lạm dụng viết quá dài trên một dòng</p></div>
            
                <div style="background: #fffbeb; border: 1.5px solid #f59e0b; border-radius: 8px; padding: 8px 12px; margin-top: 8px; color: #92400e; font-size: 13px;">
                  <strong style="color: #d97706;">💡 Mẹo Giảng Dạy &amp; Trick:</strong> Nhấn mạnh cơ chế hoạt động thực tế của 'Chuẩn PEP 8 cho biểu thức logic (PEP 8 Conventions)' giúp tối ưu hiệu năng và hạn chế lỗi tại runtime.
                </div>
            
                <div style="background: #eff6ff; border: 1.5px solid #3b82f6; border-radius: 8px; padding: 8px 12px; margin-top: 6px; color: #1e40af; font-size: 13px;">
                  <strong style="color: #2563eb;">🏢 Bối Cảnh Thực Tế:</strong> Áp dụng 'Chuẩn PEP 8 cho biểu thức logic (PEP 8 Conventions)' trong module xử lý nghiệp vụ của hệ thống doanh nghiệp thực tế.
                </div>
          </div>
          <div class="card-column-box" style="background: transparent; padding: 0; display: flex; flex-direction: column;">
            <div class="academic-code-box">
              x = True<br/>y = False<br/><br/><span class="cm"># Kiem tra toan tu and, or, not</span><br/>print("Ket qua True and False:", x and y)<br/>print("Ket qua True or False:", x or y)<br/>print("Ket qua not True:", not x)
            </div>
            
                <div style="background: #090d16; border: 1px solid #1e293b; border-radius: 8px; padding: 8px 12px; margin-top: 6px; font-family: var(--font-code); font-size: 12px; color: #10b981;">
                  <strong style="color: #38bdf8;">🖥️ KẾT QUẢ THỰC THI (CONSOLE OUTPUT):</strong>
                  <pre style="margin: 4px 0 0 0; font-family: inherit; color: #34d399; white-space: pre-wrap;">[CONSOLE OUTPUT]: Thực thi chương trình hoàn tất - Không có lỗi Runtime.</pre>
                </div>
          </div>
        </div>

      <div class="corner-page-badge">10</div>
      <div class="footer-copyright">© 2026 By Rikkei Academy - All rights reserved.</div>
    </div>

    <div class="slide slide-content-layout" data-type="content" data-title="09. Bản Chất Kỹ Thuật: Lỗi logic (Logical Errors)">
      <div class="content-top-accent-bar"></div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        09. Bản Chất Kỹ Thuật: Lỗi logic (Logical Errors)
      </div>
      
        <div class="cards-container-row">
          <div class="card-column-box" style="background: #ffffff; border: 1px solid #e2e8f0; padding: 20px;">
            <h3 style="font-size: 20px; font-weight: 800; margin-bottom: 12px; color: var(--brand-red);">Khái niệm &amp; Phân tích</h3>
            <div class="inner-white-card" style="margin-bottom: 8px;"><p>Lỗi xảy ra khi mã nguồn chạy không bị lỗi cú pháp nhưng kết quả đầu ra sai lệch so với mong muốn thực tế, thường do hiểu sai bảng chân trị hoặc dùng nhầm toán tử logic (ví dụ nhầm lẫn giữa and và or)</p></div>
            
                <div style="background: #fffbeb; border: 1.5px solid #f59e0b; border-radius: 8px; padding: 8px 12px; margin-top: 8px; color: #92400e; font-size: 13px;">
                  <strong style="color: #d97706;">💡 Mẹo Giảng Dạy &amp; Trick:</strong> Nhấn mạnh cơ chế hoạt động thực tế của 'Lỗi logic (Logical Errors)' giúp tối ưu hiệu năng và hạn chế lỗi tại runtime.
                </div>
            
                <div style="background: #eff6ff; border: 1.5px solid #3b82f6; border-radius: 8px; padding: 8px 12px; margin-top: 6px; color: #1e40af; font-size: 13px;">
                  <strong style="color: #2563eb;">🏢 Bối Cảnh Thực Tế:</strong> Áp dụng 'Lỗi logic (Logical Errors)' trong module xử lý nghiệp vụ của hệ thống doanh nghiệp thực tế.
                </div>
          </div>
          <div class="card-column-box" style="background: transparent; padding: 0; display: flex; flex-direction: column;">
            <div class="academic-code-box">
              x = True<br/>y = False<br/><br/><span class="cm"># Kiem tra toan tu and, or, not</span><br/>print("Ket qua True and False:", x and y)<br/>print("Ket qua True or False:", x or y)<br/>print("Ket qua not True:", not x)
            </div>
            
                <div style="background: #090d16; border: 1px solid #1e293b; border-radius: 8px; padding: 8px 12px; margin-top: 6px; font-family: var(--font-code); font-size: 12px; color: #10b981;">
                  <strong style="color: #38bdf8;">🖥️ KẾT QUẢ THỰC THI (CONSOLE OUTPUT):</strong>
                  <pre style="margin: 4px 0 0 0; font-family: inherit; color: #34d399; white-space: pre-wrap;">[CONSOLE OUTPUT]: Thực thi chương trình hoàn tất - Không có lỗi Runtime.</pre>
                </div>
          </div>
        </div>

      <div class="corner-page-badge">11</div>
      <div class="footer-copyright">© 2026 By Rikkei Academy - All rights reserved.</div>
    </div>

    <div class="slide slide-content-layout" data-type="content" data-title="10. Phân Tích Luồng Dữ Liệu & Nguyên Lý Vận Hành">
      <div class="content-top-accent-bar"></div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        10. Phân Tích Luồng Dữ Liệu & Nguyên Lý Vận Hành
      </div>
      
        <div style="width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 20px;">
          <div class="mermaid" style="width: 100%; max-height: 480px; overflow: auto; background: #0f172a; padding: 20px; border-radius: 12px; border: 1px solid #334155;">
flowchart TD
    A[Mã nguồn Input] --> B[Trình xử lý Execution Engine]
    B --> C[Luồng Xử lý Intermediate]
    C --> D[Môi trường Thực thi Runtime]
    D --> E[Kết quả Đầu ra Console]
          </div>
        </div>

      <div class="corner-page-badge">12</div>
      <div class="footer-copyright">© 2026 By Rikkei Academy - All rights reserved.</div>
    </div>

    <div class="slide slide-content-layout" data-type="content" data-title="11. Cảnh Báo Bẫy Cú Pháp & Anti-Pattern Thường Gặp">
      <div class="content-top-accent-bar"></div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        11. Cảnh Báo Bẫy Cú Pháp & Anti-Pattern Thường Gặp
      </div>
      
        <div style="max-width: 950px; margin: 0 auto; width: 100%; padding: 20px;">
          <div style="background: #fef2f2; border: 2px solid #ef4444; border-radius: 12px; padding: 24px;">
            <h3 style="font-size: 22px; font-weight: 800; color: #991b1b; margin-bottom: 14px;">⚠️ [CẢNH BÁO] Bẫy Cú Pháp &amp; Anti-Pattern</h3>
            <div class="inner-white-card" style="margin-bottom: 12px; border-left: 5px solid #ef4444;"><p>Lỗi thụt lề IndentationError do trộn lẫn Tab và Space</p></div><div class="inner-white-card" style="margin-bottom: 12px; border-left: 5px solid #ef4444;"><p>Tránh gán đè kiểu dữ liệu biến bất nhất gây bẫy Runtime</p></div><div class="inner-white-card" style="margin-bottom: 12px; border-left: 5px solid #ef4444;"><p>Luôn khai báo môi trường ảo Virtualenv trước khi install package</p></div><div class="inner-white-card" style="margin-bottom: 12px; border-left: 5px solid #ef4444;"><p>Không bao giờ lưu file mã nguồn trùng tên với module chuẩn</p></div>
          </div>
        </div>

      <div class="corner-page-badge">13</div>
      <div class="footer-copyright">© 2026 By Rikkei Academy - All rights reserved.</div>
    </div>

    <div class="slide slide-content-layout" data-type="content" data-title="12. Tổng Kết Trọng Tâm & Tiến Trình Cột Mốc Bài Học">
      <div class="content-top-accent-bar"></div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        12. Tổng Kết Trọng Tâm & Tiến Trình Cột Mốc Bài Học
      </div>
      
        <div class="cards-container-row">
          <div class="card-column-box">
            <div class="column-title" style="color: var(--brand-red);">Tổng Kết Kiến Thức</div>
            <div class="inner-white-card"><h4>Điểm Cốt Lõi #1</h4><p>- Toán tử logic trong Python bao gồm `and`, `or`, `not` giúp kết nối các điều kiện so sánh thành một hệ thống logic hoàn chỉnh</p></div>
<div class="inner-white-card"><h4>Điểm Cốt Lõi #2</h4><p>- Hãy luôn chú ý ghi nhớ độ ưu tiên thực thi mặc định của Python: **not** -> **and** -> **or**</p></div>

          </div>
          <div class="card-column-box">
            <div class="column-title" style="color: var(--brand-dark);">Sai Lầm Cần Tránh</div>
            <div class="inner-white-card"><h4>Lưu Ý Thực Chiến #1</h4><p>- Mẹo: Việc chủ động sử dụng các dấu ngoặc đơn `()` không chỉ loại bỏ khả năng lỗi suy luận logic mà còn giúp mã nguồn của bạn trở nên minh bạch và dễ đọc hơn đối với những lập trình viên khác trong đội ngũ phát triển</p></div>
<div class="inner-white-card"><h4>Lưu Ý Thực Chiến #2</h4><p>- Cảnh báo: Các sai lầm runtime thường gặp có thể xảy ra trong quá trình thiết lập biểu thức logic bao gồm:</p></div>

          </div>
        </div>

      <div class="corner-page-badge">14</div>
      <div class="footer-copyright">© 2026 By Rikkei Academy - All rights reserved.</div>
    </div>

    <div class="slide slide-summary-timeline" data-type="summary" data-title="Tổng kết bài học">
      <div class="summary-top-left-title">TỔNG KẾT BÀI HỌC</div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="timeline-container">
        <div class="timeline-line"></div>
        <div class="timeline-nodes-grid">
          
          <div class="timeline-node">
            <div class="node-card" style="margin-bottom: 24px;">
              <h5>1. Đặt Vấn Đề & Bối Cảnh</h5>
              <p>- Hệ thống xét duyệt tự động của các doanh nghiệp tài chính đòi hỏi quá trình đánh giá hồ ...</p>
            </div>
            <div class="timeline-dot"></div>
          </div>
          <div class="timeline-node">
            <div class="timeline-dot" style="margin-top: 60px;"></div>
            <div class="node-card" style="margin-top: 24px;">
              <h5>2. Toán tử logic (Logical Operators)</h5>
              <p>Các toán tử dùng để kết hợp các biểu thức so sánh để tạo thành biểu thức logic phức hợp hơ...</p>
            </div>
          </div>
          <div class="timeline-node">
            <div class="node-card" style="margin-bottom: 24px;">
              <h5>3. Toán tử logic 'and' (Conjunction)</h5>
              <p>Phép hội logic. Biểu thức 'A and B' chỉ trả về True khi cả hai vế A và B đều bằng True. Tr...</p>
            </div>
            <div class="timeline-dot"></div>
          </div>
          <div class="timeline-node">
            <div class="timeline-dot" style="margin-top: 60px;"></div>
            <div class="node-card" style="margin-top: 24px;">
              <h5>4. Toán tử logic 'or' (Disjunction)</h5>
              <p>Phép tuyển logic. Biểu thức 'A or B' trả về True khi có ít nhất một vế bằng True. Chỉ trả ...</p>
            </div>
          </div>
        </div>
      </div>
      <div class="corner-page-badge">15</div>
      <div class="footer-copyright">© 2026 By Rikkei Academy - All rights reserved.</div>
    </div>

    </div>

    <div id="hover-trigger-zone"></div>
    <div id="controls">
      <button type="button" class="btn-ctrl" onclick="prevSlide(event)">◀ Trước</button>
      <span id="slide-indicator">1 / 15</span>
      <button type="button" class="btn-ctrl" onclick="nextSlide(event)">Sau ▶</button>
      <button type="button" class="btn-ctrl" onclick="toggleFullscreen(event)">Toàn màn hình ⛶</button>
    </div>
  </div>

  <script>

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

  </script>
</body>
</html>