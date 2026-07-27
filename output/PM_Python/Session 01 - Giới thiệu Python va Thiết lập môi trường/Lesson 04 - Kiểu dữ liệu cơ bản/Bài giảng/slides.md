<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Kiểu dữ liệu cơ bản — Rikkei Master Slide Presentation</title>
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

    <div class="slide slide-cover active" data-type="cover" data-title="Kiểu dữ liệu cơ bản">
      <svg class="cover-left-triangle-svg" viewBox="0 0 100 160"><polygon points="0,0 0,160 100,80" fill="#c01e23"/></svg>
      <div class="cover-content-box">
        <div class="cover-session-tag">Session 01:</div>
        <div class="cover-main-title">Kiểu dữ liệu cơ bản</div>
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
<div class="agenda-item-row"><span>2.</span> <span>Kịch bản tuyến tính (Linear script)</span></div>
<div class="agenda-item-row"><span>3.</span> <span>Kiểu dữ liệu int (Integer)</span></div>
<div class="agenda-item-row"><span>4.</span> <span>Kiểu dữ liệu float (Floating-point)</span></div>
<div class="agenda-item-row"><span>5.</span> <span>Kiểu dữ liệu str (String)</span></div>
<div class="agenda-item-row"><span>6.</span> <span>Kiểu dữ liệu bool (Boolean)</span></div>

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
            <div class="inner-white-card"><h4>Trở Ngại Hệ Thống #1</h4><p>- Sự phát sinh thông tin phi cấu trúc trong môi trường thực tế:</p></div>
<div class="inner-white-card"><h4>Trở Ngại Hệ Thống #2</h4><p>- Trong các hệ thống phần mềm doanh nghiệp, dữ liệu thu thập từ người dùng thông qua terminal hoặc các nguồn bên ngoài thường được trả về dưới dạng một chuỗi ký tự thô</p></div>

          </div>
          <div class="card-column-box">
            <div class="column-title" style="color: var(--brand-dark);">Giải Pháp & Cách Khắc Phục</div>
            <div class="inner-white-card"><h4>Hướng Xử Lý Triệt Để #1</h4><p>- Ví dụ, khi một khách hàng mua sản phẩm trên sàn thương mại điện tử, các dữ liệu thô nhận về bao gồm số lượng sản phẩm là "3", đơn giá là "15</p></div>
<div class="inner-white-card"><h4>Hướng Xử Lý Triệt Để #2</h4><p>5", và trạng thái áp dụng mã giảm giá là "True"</p></div>

          </div>
        </div>

      <div class="corner-page-badge">3</div>
      <div class="footer-copyright">© 2026 By Rikkei Academy - All rights reserved.</div>
    </div>

    <div class="slide slide-content-layout" data-type="content" data-title="02. Bản Chất Kỹ Thuật: Kịch bản tuyến tính (Linear script)">
      <div class="content-top-accent-bar"></div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        02. Bản Chất Kỹ Thuật: Kịch bản tuyến tính (Linear script)
      </div>
      
        <div class="cards-container-row">
          <div class="card-column-box" style="background: #ffffff; border: 1px solid #e2e8f0; padding: 20px;">
            <h3 style="font-size: 20px; font-weight: 800; margin-bottom: 12px; color: var(--brand-red);">Khái niệm &amp; Phân tích</h3>
            <div class="inner-white-card" style="margin-bottom: 8px;"><p>Tập hợp các dòng lệnh được trình biên dịch thực thi tuần tự từ trên xuống dưới một lần duy nhất, không rẽ nhánh hay lặp lại</p></div>
            
                <div style="background: #fffbeb; border: 1.5px solid #f59e0b; border-radius: 8px; padding: 8px 12px; margin-top: 8px; color: #92400e; font-size: 13px;">
                  <strong style="color: #d97706;">💡 Mẹo Giảng Dạy &amp; Trick:</strong> Nhấn mạnh cơ chế hoạt động thực tế của 'Kịch bản tuyến tính (Linear script)' giúp tối ưu hiệu năng và hạn chế lỗi tại runtime.
                </div>
            
                <div style="background: #eff6ff; border: 1.5px solid #3b82f6; border-radius: 8px; padding: 8px 12px; margin-top: 6px; color: #1e40af; font-size: 13px;">
                  <strong style="color: #2563eb;">🏢 Bối Cảnh Thực Tế:</strong> Áp dụng 'Kịch bản tuyến tính (Linear script)' trong module xử lý nghiệp vụ của hệ thống doanh nghiệp thực tế.
                </div>
          </div>
          <div class="card-column-box" style="background: transparent; padding: 0; display: flex; flex-direction: column;">
            <div class="academic-code-box">
              <span class="cm"># Viet va chay chuong trinh tuyen tinh dau tien</span><br/>print("Bat dau thiet lap moi truong Code...")<br/>print("Chay thanh cong tap tin Python tuyen tinh!")
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

    <div class="slide slide-content-layout" data-type="content" data-title="03. Bản Chất Kỹ Thuật: Kiểu dữ liệu int (Integer)">
      <div class="content-top-accent-bar"></div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        03. Bản Chất Kỹ Thuật: Kiểu dữ liệu int (Integer)
      </div>
      
        <div class="cards-container-row">
          <div class="card-column-box" style="background: #ffffff; border: 1px solid #e2e8f0; padding: 20px;">
            <h3 style="font-size: 20px; font-weight: 800; margin-bottom: 12px; color: var(--brand-red);">Khái niệm &amp; Phân tích</h3>
            <div class="inner-white-card" style="margin-bottom: 8px;"><p>Kiểu dữ liệu số nguyên, đại diện cho các số nguyên dương, nguyên âm hoặc số không, không chứa phần thập phân</p></div>
            
                <div style="background: #fffbeb; border: 1.5px solid #f59e0b; border-radius: 8px; padding: 8px 12px; margin-top: 8px; color: #92400e; font-size: 13px;">
                  <strong style="color: #d97706;">💡 Mẹo Giảng Dạy &amp; Trick:</strong> Nhấn mạnh cơ chế hoạt động thực tế của 'Kiểu dữ liệu int (Integer)' giúp tối ưu hiệu năng và hạn chế lỗi tại runtime.
                </div>
            
                <div style="background: #eff6ff; border: 1.5px solid #3b82f6; border-radius: 8px; padding: 8px 12px; margin-top: 6px; color: #1e40af; font-size: 13px;">
                  <strong style="color: #2563eb;">🏢 Bối Cảnh Thực Tế:</strong> Áp dụng 'Kiểu dữ liệu int (Integer)' trong module xử lý nghiệp vụ của hệ thống doanh nghiệp thực tế.
                </div>
          </div>
          <div class="card-column-box" style="background: transparent; padding: 0; display: flex; flex-direction: column;">
            <div class="academic-code-box">
              <span class="cm"># Khai bao va phan biet 4 kieu du lieu co ban</span><br/>tuoi = 18<br/>chieu_cao = 1.72<br/>ten = "Minh Anh"<br/>la_hoc_vien = True<br/><br/>print(tuoi)<br/>print(chieu_cao)<br/>print(ten)<br/>print(la_hoc_vien)
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

    <div class="slide slide-content-layout" data-type="content" data-title="04. Bản Chất Kỹ Thuật: Kiểu dữ liệu float (Floating-point)">
      <div class="content-top-accent-bar"></div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        04. Bản Chất Kỹ Thuật: Kiểu dữ liệu float (Floating-point)
      </div>
      
        <div class="cards-container-row">
          <div class="card-column-box" style="background: #ffffff; border: 1px solid #e2e8f0; padding: 20px;">
            <h3 style="font-size: 20px; font-weight: 800; margin-bottom: 12px; color: var(--brand-red);">Khái niệm &amp; Phân tích</h3>
            <div class="inner-white-card" style="margin-bottom: 8px;"><p>Kiểu dữ liệu biểu diễn số thực, có chứa phần thập phân ngăn cách bởi dấu chấm (</p></div>
            
                <div style="background: #fffbeb; border: 1.5px solid #f59e0b; border-radius: 8px; padding: 8px 12px; margin-top: 8px; color: #92400e; font-size: 13px;">
                  <strong style="color: #d97706;">💡 Mẹo Giảng Dạy &amp; Trick:</strong> Nhấn mạnh cơ chế hoạt động thực tế của 'Kiểu dữ liệu float (Floating-point)' giúp tối ưu hiệu năng và hạn chế lỗi tại runtime.
                </div>
            
                <div style="background: #eff6ff; border: 1.5px solid #3b82f6; border-radius: 8px; padding: 8px 12px; margin-top: 6px; color: #1e40af; font-size: 13px;">
                  <strong style="color: #2563eb;">🏢 Bối Cảnh Thực Tế:</strong> Áp dụng 'Kiểu dữ liệu float (Floating-point)' trong module xử lý nghiệp vụ của hệ thống doanh nghiệp thực tế.
                </div>
          </div>
          <div class="card-column-box" style="background: transparent; padding: 0; display: flex; flex-direction: column;">
            <div class="academic-code-box">
              <span class="cm"># Thao tac tinhtoan hoc va xuly ghep chuoi co ban</span><br/>so_a = 15<br/>so_b = 4<br/><br/>tong = so_a + so_b<br/>thuong = so_a / so_b<br/><br/>ho = "Nguyen"<br/>ten_dem = "Van"<br/>ten_day_du = ho + " " + ten_dem<br/>print(ten_day_du)
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

    <div class="slide slide-content-layout" data-type="content" data-title="05. Bản Chất Kỹ Thuật: Kiểu dữ liệu str (String)">
      <div class="content-top-accent-bar"></div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        05. Bản Chất Kỹ Thuật: Kiểu dữ liệu str (String)
      </div>
      
        <div class="cards-container-row">
          <div class="card-column-box" style="background: #ffffff; border: 1px solid #e2e8f0; padding: 20px;">
            <h3 style="font-size: 20px; font-weight: 800; margin-bottom: 12px; color: var(--brand-red);">Khái niệm &amp; Phân tích</h3>
            <div class="inner-white-card" style="margin-bottom: 8px;"><p>Kiểu chuỗi ký tự dùng để biểu diễn văn bản, được đặt trong cặp dấu nháy đơn hoặc nháy kép</p></div>
            
                <div style="background: #fffbeb; border: 1.5px solid #f59e0b; border-radius: 8px; padding: 8px 12px; margin-top: 8px; color: #92400e; font-size: 13px;">
                  <strong style="color: #d97706;">💡 Mẹo Giảng Dạy &amp; Trick:</strong> Nhấn mạnh cơ chế hoạt động thực tế của 'Kiểu dữ liệu str (String)' giúp tối ưu hiệu năng và hạn chế lỗi tại runtime.
                </div>
            
                <div style="background: #eff6ff; border: 1.5px solid #3b82f6; border-radius: 8px; padding: 8px 12px; margin-top: 6px; color: #1e40af; font-size: 13px;">
                  <strong style="color: #2563eb;">🏢 Bối Cảnh Thực Tế:</strong> Áp dụng 'Kiểu dữ liệu str (String)' trong module xử lý nghiệp vụ của hệ thống doanh nghiệp thực tế.
                </div>
          </div>
          <div class="card-column-box" style="background: transparent; padding: 0; display: flex; flex-direction: column;">
            <div class="academic-code-box">
              <span class="cm"># Bieu thuc so sanh va logic don gian</span><br/>tuoi_hoc_sinh = 16<br/>tuoi_hop_le = tuoi_hoc_sinh &gt;= 18<br/>co_dong_y = True<br/><br/>duoc_phe_duyet = tuoi_hop_le and co_dong_y<br/>print(duoc_phe_duyet)
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

    <div class="slide slide-content-layout" data-type="content" data-title="06. Bản Chất Kỹ Thuật: Kiểu dữ liệu bool (Boolean)">
      <div class="content-top-accent-bar"></div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        06. Bản Chất Kỹ Thuật: Kiểu dữ liệu bool (Boolean)
      </div>
      
        <div class="cards-container-row">
          <div class="card-column-box" style="background: #ffffff; border: 1px solid #e2e8f0; padding: 20px;">
            <h3 style="font-size: 20px; font-weight: 800; margin-bottom: 12px; color: var(--brand-red);">Khái niệm &amp; Phân tích</h3>
            <div class="inner-white-card" style="margin-bottom: 8px;"><p>Kiểu dữ liệu logic chỉ nhận một trong hai giá trị duy nhất là True (Đúng) hoặc False (Sai)</p></div>
            
                <div style="background: #fffbeb; border: 1.5px solid #f59e0b; border-radius: 8px; padding: 8px 12px; margin-top: 8px; color: #92400e; font-size: 13px;">
                  <strong style="color: #d97706;">💡 Mẹo Giảng Dạy &amp; Trick:</strong> Nhấn mạnh cơ chế hoạt động thực tế của 'Kiểu dữ liệu bool (Boolean)' giúp tối ưu hiệu năng và hạn chế lỗi tại runtime.
                </div>
            
                <div style="background: #eff6ff; border: 1.5px solid #3b82f6; border-radius: 8px; padding: 8px 12px; margin-top: 6px; color: #1e40af; font-size: 13px;">
                  <strong style="color: #2563eb;">🏢 Bối Cảnh Thực Tế:</strong> Áp dụng 'Kiểu dữ liệu bool (Boolean)' trong module xử lý nghiệp vụ của hệ thống doanh nghiệp thực tế.
                </div>
          </div>
          <div class="card-column-box" style="background: transparent; padding: 0; display: flex; flex-direction: column;">
            <div class="academic-code-box">
              <span class="cm"># Cach sua loi TypeError bang co che ep kieu (Type Casting)</span><br/>chuoi_so = "2024"<br/><span class="cm"># loi_chua_ep_kieu = chuoi_so + 1 # Se gay ra loi TypeError</span><br/><br/><span class="cm"># Khac phuc bang cach ep kieu chuoi ve dang so nguyen</span><br/>nam_so_nguyen = int(chuoi_so)<br/>nam_tiep_theo = nam_so_nguyen + 1<br/>print(nam_tiep_theo)
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

    <div class="slide slide-content-layout" data-type="content" data-title="07. Bản Chất Kỹ Thuật: Các phép toán số học cơ bản">
      <div class="content-top-accent-bar"></div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        07. Bản Chất Kỹ Thuật: Các phép toán số học cơ bản
      </div>
      
        <div class="cards-container-row">
          <div class="card-column-box" style="background: #ffffff; border: 1px solid #e2e8f0; padding: 20px;">
            <h3 style="font-size: 20px; font-weight: 800; margin-bottom: 12px; color: var(--brand-red);">Khái niệm &amp; Phân tích</h3>
            <div class="inner-white-card" style="margin-bottom: 8px;"><p>Các phép tính toán học cơ bản áp dụng cho kiểu số bao gồm cộng (+), trừ (-), nhân (*) và chia thập phân (/)</p></div>
            
                <div style="background: #fffbeb; border: 1.5px solid #f59e0b; border-radius: 8px; padding: 8px 12px; margin-top: 8px; color: #92400e; font-size: 13px;">
                  <strong style="color: #d97706;">💡 Mẹo Giảng Dạy &amp; Trick:</strong> Nhấn mạnh cơ chế hoạt động thực tế của 'Các phép toán số học cơ bản' giúp tối ưu hiệu năng và hạn chế lỗi tại runtime.
                </div>
            
                <div style="background: #eff6ff; border: 1.5px solid #3b82f6; border-radius: 8px; padding: 8px 12px; margin-top: 6px; color: #1e40af; font-size: 13px;">
                  <strong style="color: #2563eb;">🏢 Bối Cảnh Thực Tế:</strong> Áp dụng 'Các phép toán số học cơ bản' trong module xử lý nghiệp vụ của hệ thống doanh nghiệp thực tế.
                </div>
          </div>
          <div class="card-column-box" style="background: transparent; padding: 0; display: flex; flex-direction: column;">
            <div class="academic-code-box">
              <span class="cm"># Chuong trinh tinh toan tuyen tinh hoan chinh nhan dau vao</span><br/>nhap_chieu_dai = input("Nhap chieu dai: ")<br/>nhap_chieu_rong = input("Nhap chieu rong: ")<br/><br/><span class="cm"># Ep kieu str sang float de thuc hien tinh toan</span><br/>dai = float(nhap_chieu_dai)<br/>rong = float(nhap_chieu_rong)<br/><br/>dien_tich = dai * rong<br/>print("Dien tich hinh chu nhat la: " + str(dien_tich))
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

    <div class="slide slide-content-layout" data-type="content" data-title="08. Bản Chất Kỹ Thuật: Ghép chuỗi (String Concatenation)">
      <div class="content-top-accent-bar"></div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        08. Bản Chất Kỹ Thuật: Ghép chuỗi (String Concatenation)
      </div>
      
        <div class="cards-container-row">
          <div class="card-column-box" style="background: #ffffff; border: 1px solid #e2e8f0; padding: 20px;">
            <h3 style="font-size: 20px; font-weight: 800; margin-bottom: 12px; color: var(--brand-red);">Khái niệm &amp; Phân tích</h3>
            <div class="inner-white-card" style="margin-bottom: 8px;"><p>Thao tác nối các chuỗi ký tự lại với nhau bằng toán tử cộng (+)</p></div>
            
                <div style="background: #fffbeb; border: 1.5px solid #f59e0b; border-radius: 8px; padding: 8px 12px; margin-top: 8px; color: #92400e; font-size: 13px;">
                  <strong style="color: #d97706;">💡 Mẹo Giảng Dạy &amp; Trick:</strong> Nhấn mạnh cơ chế hoạt động thực tế của 'Ghép chuỗi (String Concatenation)' giúp tối ưu hiệu năng và hạn chế lỗi tại runtime.
                </div>
            
                <div style="background: #eff6ff; border: 1.5px solid #3b82f6; border-radius: 8px; padding: 8px 12px; margin-top: 6px; color: #1e40af; font-size: 13px;">
                  <strong style="color: #2563eb;">🏢 Bối Cảnh Thực Tế:</strong> Áp dụng 'Ghép chuỗi (String Concatenation)' trong module xử lý nghiệp vụ của hệ thống doanh nghiệp thực tế.
                </div>
          </div>
          <div class="card-column-box" style="background: transparent; padding: 0; display: flex; flex-direction: column;">
            <div class="academic-code-box">
              <span class="cm"># Viet va chay chuong trinh tuyen tinh dau tien</span><br/>print("Bat dau thiet lap moi truong Code...")<br/>print("Chay thanh cong tap tin Python tuyen tinh!")
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

    <div class="slide slide-content-layout" data-type="content" data-title="09. Bản Chất Kỹ Thuật: Phép so sánh quan hệ">
      <div class="content-top-accent-bar"></div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        09. Bản Chất Kỹ Thuật: Phép so sánh quan hệ
      </div>
      
        <div class="cards-container-row">
          <div class="card-column-box" style="background: #ffffff; border: 1px solid #e2e8f0; padding: 20px;">
            <h3 style="font-size: 20px; font-weight: 800; margin-bottom: 12px; color: var(--brand-red);">Khái niệm &amp; Phân tích</h3>
            <div class="inner-white-card" style="margin-bottom: 8px;"><p>Các biểu thức sử dụng toán tử so sánh (như ==, !=, >, <, >=, <=) để so khớp hai giá trị và trả về True hoặc False</p></div>
            
                <div style="background: #fffbeb; border: 1.5px solid #f59e0b; border-radius: 8px; padding: 8px 12px; margin-top: 8px; color: #92400e; font-size: 13px;">
                  <strong style="color: #d97706;">💡 Mẹo Giảng Dạy &amp; Trick:</strong> Nhấn mạnh cơ chế hoạt động thực tế của 'Phép so sánh quan hệ' giúp tối ưu hiệu năng và hạn chế lỗi tại runtime.
                </div>
            
                <div style="background: #eff6ff; border: 1.5px solid #3b82f6; border-radius: 8px; padding: 8px 12px; margin-top: 6px; color: #1e40af; font-size: 13px;">
                  <strong style="color: #2563eb;">🏢 Bối Cảnh Thực Tế:</strong> Áp dụng 'Phép so sánh quan hệ' trong module xử lý nghiệp vụ của hệ thống doanh nghiệp thực tế.
                </div>
          </div>
          <div class="card-column-box" style="background: transparent; padding: 0; display: flex; flex-direction: column;">
            <div class="academic-code-box">
              <span class="cm"># Viet va chay chuong trinh tuyen tinh dau tien</span><br/>print("Bat dau thiet lap moi truong Code...")<br/>print("Chay thanh cong tap tin Python tuyen tinh!")
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

    <div class="slide slide-content-layout" data-type="content" data-title="10. Bản Chất Kỹ Thuật: Biểu thức logic đơn giản">
      <div class="content-top-accent-bar"></div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        10. Bản Chất Kỹ Thuật: Biểu thức logic đơn giản
      </div>
      
        <div class="cards-container-row">
          <div class="card-column-box" style="background: #ffffff; border: 1px solid #e2e8f0; padding: 20px;">
            <h3 style="font-size: 20px; font-weight: 800; margin-bottom: 12px; color: var(--brand-red);">Khái niệm &amp; Phân tích</h3>
            <div class="inner-white-card" style="margin-bottom: 8px;"><p>Sự kết hợp giữa nhiều biểu thức so sánh quan hệ thông qua các toán tử logic gồm and, or và not</p></div>
            
                <div style="background: #fffbeb; border: 1.5px solid #f59e0b; border-radius: 8px; padding: 8px 12px; margin-top: 8px; color: #92400e; font-size: 13px;">
                  <strong style="color: #d97706;">💡 Mẹo Giảng Dạy &amp; Trick:</strong> Nhấn mạnh cơ chế hoạt động thực tế của 'Biểu thức logic đơn giản' giúp tối ưu hiệu năng và hạn chế lỗi tại runtime.
                </div>
            
                <div style="background: #eff6ff; border: 1.5px solid #3b82f6; border-radius: 8px; padding: 8px 12px; margin-top: 6px; color: #1e40af; font-size: 13px;">
                  <strong style="color: #2563eb;">🏢 Bối Cảnh Thực Tế:</strong> Áp dụng 'Biểu thức logic đơn giản' trong module xử lý nghiệp vụ của hệ thống doanh nghiệp thực tế.
                </div>
          </div>
          <div class="card-column-box" style="background: transparent; padding: 0; display: flex; flex-direction: column;">
            <div class="academic-code-box">
              <span class="cm"># Viet va chay chuong trinh tuyen tinh dau tien</span><br/>print("Bat dau thiet lap moi truong Code...")<br/>print("Chay thanh cong tap tin Python tuyen tinh!")
            </div>
            
                <div style="background: #090d16; border: 1px solid #1e293b; border-radius: 8px; padding: 8px 12px; margin-top: 6px; font-family: var(--font-code); font-size: 12px; color: #10b981;">
                  <strong style="color: #38bdf8;">🖥️ KẾT QUẢ THỰC THI (CONSOLE OUTPUT):</strong>
                  <pre style="margin: 4px 0 0 0; font-family: inherit; color: #34d399; white-space: pre-wrap;">[CONSOLE OUTPUT]: Thực thi chương trình hoàn tất - Không có lỗi Runtime.</pre>
                </div>
          </div>
        </div>

      <div class="corner-page-badge">12</div>
      <div class="footer-copyright">© 2026 By Rikkei Academy - All rights reserved.</div>
    </div>

    <div class="slide slide-content-layout" data-type="content" data-title="11. Bản Chất Kỹ Thuật: Cơ chế ép kiểu (Type Casting)">
      <div class="content-top-accent-bar"></div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        11. Bản Chất Kỹ Thuật: Cơ chế ép kiểu (Type Casting)
      </div>
      
        <div class="cards-container-row">
          <div class="card-column-box" style="background: #ffffff; border: 1px solid #e2e8f0; padding: 20px;">
            <h3 style="font-size: 20px; font-weight: 800; margin-bottom: 12px; color: var(--brand-red);">Khái niệm &amp; Phân tích</h3>
            <div class="inner-white-card" style="margin-bottom: 8px;"><p>Quá trình chuyển đổi dữ liệu từ kiểu này sang kiểu khác một cách chủ động bằng cách sử dụng các hàm tích hợp sẵn như int(), float(), str(), bool()</p></div>
            
                <div style="background: #fffbeb; border: 1.5px solid #f59e0b; border-radius: 8px; padding: 8px 12px; margin-top: 8px; color: #92400e; font-size: 13px;">
                  <strong style="color: #d97706;">💡 Mẹo Giảng Dạy &amp; Trick:</strong> Nhấn mạnh cơ chế hoạt động thực tế của 'Cơ chế ép kiểu (Type Casting)' giúp tối ưu hiệu năng và hạn chế lỗi tại runtime.
                </div>
            
                <div style="background: #eff6ff; border: 1.5px solid #3b82f6; border-radius: 8px; padding: 8px 12px; margin-top: 6px; color: #1e40af; font-size: 13px;">
                  <strong style="color: #2563eb;">🏢 Bối Cảnh Thực Tế:</strong> Áp dụng 'Cơ chế ép kiểu (Type Casting)' trong module xử lý nghiệp vụ của hệ thống doanh nghiệp thực tế.
                </div>
          </div>
          <div class="card-column-box" style="background: transparent; padding: 0; display: flex; flex-direction: column;">
            <div class="academic-code-box">
              <span class="cm"># Viet va chay chuong trinh tuyen tinh dau tien</span><br/>print("Bat dau thiet lap moi truong Code...")<br/>print("Chay thanh cong tap tin Python tuyen tinh!")
            </div>
            
                <div style="background: #090d16; border: 1px solid #1e293b; border-radius: 8px; padding: 8px 12px; margin-top: 6px; font-family: var(--font-code); font-size: 12px; color: #10b981;">
                  <strong style="color: #38bdf8;">🖥️ KẾT QUẢ THỰC THI (CONSOLE OUTPUT):</strong>
                  <pre style="margin: 4px 0 0 0; font-family: inherit; color: #34d399; white-space: pre-wrap;">[CONSOLE OUTPUT]: Thực thi chương trình hoàn tất - Không có lỗi Runtime.</pre>
                </div>
          </div>
        </div>

      <div class="corner-page-badge">13</div>
      <div class="footer-copyright">© 2026 By Rikkei Academy - All rights reserved.</div>
    </div>

    <div class="slide slide-content-layout" data-type="content" data-title="12. Bản Chất Kỹ Thuật: Lỗi sai kiểu dữ liệu (TypeError)">
      <div class="content-top-accent-bar"></div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        12. Bản Chất Kỹ Thuật: Lỗi sai kiểu dữ liệu (TypeError)
      </div>
      
        <div class="cards-container-row">
          <div class="card-column-box" style="background: #ffffff; border: 1px solid #e2e8f0; padding: 20px;">
            <h3 style="font-size: 20px; font-weight: 800; margin-bottom: 12px; color: var(--brand-red);">Khái niệm &amp; Phân tích</h3>
            <div class="inner-white-card" style="margin-bottom: 8px;"><p>Lỗi xảy ra khi thực thi một thao tác toán học hay hàm trên hai kiểu dữ liệu không tương thích với nhau (ví dụ: cộng một chuỗi với một số)</p></div>
            
                <div style="background: #fffbeb; border: 1.5px solid #f59e0b; border-radius: 8px; padding: 8px 12px; margin-top: 8px; color: #92400e; font-size: 13px;">
                  <strong style="color: #d97706;">💡 Mẹo Giảng Dạy &amp; Trick:</strong> Nhấn mạnh cơ chế hoạt động thực tế của 'Lỗi sai kiểu dữ liệu (TypeError)' giúp tối ưu hiệu năng và hạn chế lỗi tại runtime.
                </div>
            
                <div style="background: #eff6ff; border: 1.5px solid #3b82f6; border-radius: 8px; padding: 8px 12px; margin-top: 6px; color: #1e40af; font-size: 13px;">
                  <strong style="color: #2563eb;">🏢 Bối Cảnh Thực Tế:</strong> Áp dụng 'Lỗi sai kiểu dữ liệu (TypeError)' trong module xử lý nghiệp vụ của hệ thống doanh nghiệp thực tế.
                </div>
          </div>
          <div class="card-column-box" style="background: transparent; padding: 0; display: flex; flex-direction: column;">
            <div class="academic-code-box">
              <span class="cm"># Viet va chay chuong trinh tuyen tinh dau tien</span><br/>print("Bat dau thiet lap moi truong Code...")<br/>print("Chay thanh cong tap tin Python tuyen tinh!")
            </div>
            
                <div style="background: #090d16; border: 1px solid #1e293b; border-radius: 8px; padding: 8px 12px; margin-top: 6px; font-family: var(--font-code); font-size: 12px; color: #10b981;">
                  <strong style="color: #38bdf8;">🖥️ KẾT QUẢ THỰC THI (CONSOLE OUTPUT):</strong>
                  <pre style="margin: 4px 0 0 0; font-family: inherit; color: #34d399; white-space: pre-wrap;">[CONSOLE OUTPUT]: Thực thi chương trình hoàn tất - Không có lỗi Runtime.</pre>
                </div>
          </div>
        </div>

      <div class="corner-page-badge">14</div>
      <div class="footer-copyright">© 2026 By Rikkei Academy - All rights reserved.</div>
    </div>

    <div class="slide slide-content-layout" data-type="content" data-title="13. Bản Chất Kỹ Thuật: Hàm nhập dữ liệu input()">
      <div class="content-top-accent-bar"></div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        13. Bản Chất Kỹ Thuật: Hàm nhập dữ liệu input()
      </div>
      
        <div class="cards-container-row">
          <div class="card-column-box" style="background: #ffffff; border: 1px solid #e2e8f0; padding: 20px;">
            <h3 style="font-size: 20px; font-weight: 800; margin-bottom: 12px; color: var(--brand-red);">Khái niệm &amp; Phân tích</h3>
            <div class="inner-white-card" style="margin-bottom: 8px;"><p>Hàm dừng chương trình tạm thời để chờ người dùng nhập dữ liệu từ bàn phím</p></div><div class="inner-white-card" style="margin-bottom: 8px;"><p>Kết quả trả về của hàm này luôn ở dạng chuỗi (str)</p></div>
            
                <div style="background: #fffbeb; border: 1.5px solid #f59e0b; border-radius: 8px; padding: 8px 12px; margin-top: 8px; color: #92400e; font-size: 13px;">
                  <strong style="color: #d97706;">💡 Mẹo Giảng Dạy &amp; Trick:</strong> Nhấn mạnh cơ chế hoạt động thực tế của 'Hàm nhập dữ liệu input()' giúp tối ưu hiệu năng và hạn chế lỗi tại runtime.
                </div>
            
                <div style="background: #eff6ff; border: 1.5px solid #3b82f6; border-radius: 8px; padding: 8px 12px; margin-top: 6px; color: #1e40af; font-size: 13px;">
                  <strong style="color: #2563eb;">🏢 Bối Cảnh Thực Tế:</strong> Áp dụng 'Hàm nhập dữ liệu input()' trong module xử lý nghiệp vụ của hệ thống doanh nghiệp thực tế.
                </div>
          </div>
          <div class="card-column-box" style="background: transparent; padding: 0; display: flex; flex-direction: column;">
            <div class="academic-code-box">
              <span class="cm"># Viet va chay chuong trinh tuyen tinh dau tien</span><br/>print("Bat dau thiet lap moi truong Code...")<br/>print("Chay thanh cong tap tin Python tuyen tinh!")
            </div>
            
                <div style="background: #090d16; border: 1px solid #1e293b; border-radius: 8px; padding: 8px 12px; margin-top: 6px; font-family: var(--font-code); font-size: 12px; color: #10b981;">
                  <strong style="color: #38bdf8;">🖥️ KẾT QUẢ THỰC THI (CONSOLE OUTPUT):</strong>
                  <pre style="margin: 4px 0 0 0; font-family: inherit; color: #34d399; white-space: pre-wrap;">[CONSOLE OUTPUT]: Thực thi chương trình hoàn tất - Không có lỗi Runtime.</pre>
                </div>
          </div>
        </div>

      <div class="corner-page-badge">15</div>
      <div class="footer-copyright">© 2026 By Rikkei Academy - All rights reserved.</div>
    </div>

    <div class="slide slide-content-layout" data-type="content" data-title="14. Phân Tích Luồng Dữ Liệu & Nguyên Lý Vận Hành">
      <div class="content-top-accent-bar"></div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        14. Phân Tích Luồng Dữ Liệu & Nguyên Lý Vận Hành
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

      <div class="corner-page-badge">16</div>
      <div class="footer-copyright">© 2026 By Rikkei Academy - All rights reserved.</div>
    </div>

    <div class="slide slide-content-layout" data-type="content" data-title="15. Cảnh Báo Bẫy Cú Pháp & Anti-Pattern Thường Gặp">
      <div class="content-top-accent-bar"></div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        15. Cảnh Báo Bẫy Cú Pháp & Anti-Pattern Thường Gặp
      </div>
      
        <div style="max-width: 950px; margin: 0 auto; width: 100%; padding: 20px;">
          <div style="background: #fef2f2; border: 2px solid #ef4444; border-radius: 12px; padding: 24px;">
            <h3 style="font-size: 22px; font-weight: 800; color: #991b1b; margin-bottom: 14px;">⚠️ [CẢNH BÁO] Bẫy Cú Pháp &amp; Anti-Pattern</h3>
            <div class="inner-white-card" style="margin-bottom: 12px; border-left: 5px solid #ef4444;"><p>Lỗi thụt lề IndentationError do trộn lẫn Tab và Space</p></div><div class="inner-white-card" style="margin-bottom: 12px; border-left: 5px solid #ef4444;"><p>Tránh gán đè kiểu dữ liệu biến bất nhất gây bẫy Runtime</p></div><div class="inner-white-card" style="margin-bottom: 12px; border-left: 5px solid #ef4444;"><p>Luôn khai báo môi trường ảo Virtualenv trước khi install package</p></div><div class="inner-white-card" style="margin-bottom: 12px; border-left: 5px solid #ef4444;"><p>Không bao giờ lưu file mã nguồn trùng tên với module chuẩn</p></div>
          </div>
        </div>

      <div class="corner-page-badge">17</div>
      <div class="footer-copyright">© 2026 By Rikkei Academy - All rights reserved.</div>
    </div>

    <div class="slide slide-content-layout" data-type="content" data-title="16. Tổng Kết Trọng Tâm & Tiến Trình Cột Mốc Bài Học">
      <div class="content-top-accent-bar"></div>
      <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Logo" class="top-right-logo" />
      <div class="content-header-title">
        16. Tổng Kết Trọng Tâm & Tiến Trình Cột Mốc Bài Học
      </div>
      
        <div class="cards-container-row">
          <div class="card-column-box">
            <div class="column-title" style="color: var(--brand-red);">Tổng Kết Kiến Thức</div>
            <div class="inner-white-card"><h4>Điểm Cốt Lõi #1</h4><p>- Phân loại kiểu dữ liệu cốt lõi: Ghi nhớ rõ chức năng của 4 kiểu dữ liệu cơ bản bao gồm `int` (số nguyên), `float` (số thực), `str` (chuỗi văn bản), và `bool` (luận lý)</p></div>
<div class="inner-white-card"><h4>Điểm Cốt Lõi #2</h4><p>- Kiểm tra kiểu dữ liệu: Luôn dùng hàm dựng sẵn `type()` để giám sát kiểu dữ liệu thực tế của biến trong quá trình phát triển mã nguồn</p></div>

          </div>
          <div class="card-column-box">
            <div class="column-title" style="color: var(--brand-dark);">Sai Lầm Cần Tránh</div>
            <div class="inner-white-card"><h4>Lưu Ý Thực Chiến #1</h4><p>- Cảnh báo các sai lầm runtime thường gặp:</p></div>
<div class="inner-white-card"><h4>Lưu Ý Thực Chiến #2</h4><p>- Lỗi **TypeError**: Xuất hiện khi cố thực hiện phép toán không tương thích kiểu, ví dụ cộng trực tiếp một chuỗi văn bản với số nguyên mà không chuyển đổi kiểu trước</p></div>

          </div>
        </div>

      <div class="corner-page-badge">18</div>
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
              <p>- Sự phát sinh thông tin phi cấu trúc trong môi trường thực tế:
  - Trong các hệ thống phầ...</p>
            </div>
            <div class="timeline-dot"></div>
          </div>
          <div class="timeline-node">
            <div class="timeline-dot" style="margin-top: 60px;"></div>
            <div class="node-card" style="margin-top: 24px;">
              <h5>2. Kịch bản tuyến tính (Linear script)</h5>
              <p>Tập hợp các dòng lệnh được trình biên dịch thực thi tuần tự từ trên xuống dưới một lần duy...</p>
            </div>
          </div>
          <div class="timeline-node">
            <div class="node-card" style="margin-bottom: 24px;">
              <h5>3. Kiểu dữ liệu int (Integer)</h5>
              <p>Kiểu dữ liệu số nguyên, đại diện cho các số nguyên dương, nguyên âm hoặc số không, không c...</p>
            </div>
            <div class="timeline-dot"></div>
          </div>
          <div class="timeline-node">
            <div class="timeline-dot" style="margin-top: 60px;"></div>
            <div class="node-card" style="margin-top: 24px;">
              <h5>4. Kiểu dữ liệu float (Floating-point)</h5>
              <p>Kiểu dữ liệu biểu diễn số thực, có chứa phần thập phân ngăn cách bởi dấu chấm (.)....</p>
            </div>
          </div>
        </div>
      </div>
      <div class="corner-page-badge">19</div>
      <div class="footer-copyright">© 2026 By Rikkei Academy - All rights reserved.</div>
    </div>

    </div>

    <div id="hover-trigger-zone"></div>
    <div id="controls">
      <button type="button" class="btn-ctrl" onclick="prevSlide(event)">◀ Trước</button>
      <span id="slide-indicator">1 / 19</span>
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