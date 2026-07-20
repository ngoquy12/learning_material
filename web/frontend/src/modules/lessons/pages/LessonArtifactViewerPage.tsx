import { useState, useEffect, useMemo, useRef } from "react";
import { useParams, useNavigate, useSearchParams } from "react-router-dom";
import {
  Layout,
  Button,
  Spin,
  Alert,
  Radio,
  Progress,
  Card,
  Typography,
  Empty,
  Badge,
  Divider,
  Input,
  message,
} from "antd";
import {
  ArrowLeft,
  BookOpen,
  Award,
  Terminal,
  Network,
  ChevronRight,
  ChevronLeft,
  BookOpenCheck,
  RefreshCw,
  Play,
  CheckCircle2,
  XCircle,
  AlertCircle,
  Copy,
  Check,
  FileCode,
  ZoomIn,
  ZoomOut,
  Maximize2,
  Minimize2,
  HelpCircle,
  CheckSquare,
  ListTodo,
} from "lucide-react";
import { useLesson, useArtifacts, ArtifactResponse } from "../hooks/useLessons";
import { LessonResponse } from "../../../types/lesson";
import { Transformer } from "markmap-lib";
import { Markmap } from "markmap-view";

const transformer = new Transformer();

function MarkmapComponent({ markmapData }: { markmapData: string }) {
  const svgRef = useRef<SVGSVGElement>(null);
  const mmRef = useRef<Markmap | null>(null);
  const [isFullscreen, setIsFullscreen] = useState(false);

  useEffect(() => {
    if (!svgRef.current) return;

    let cleanMd = markmapData.trim();
    if (cleanMd.startsWith("```")) {
      cleanMd = cleanMd.replace(/^```[a-zA-Z]*\r?\n/, "");
      cleanMd = cleanMd.replace(/\r?\n```$/, "");
      cleanMd = cleanMd.trim();
    }

    // Replace markdown image syntax with HTML img tags for inline rendering in Markmap
    cleanMd = cleanMd.replace(/!\[(.*?)\]\((.*?)\)/g, (_match, alt, src) => {
      return `<img src="${src}" alt="${alt}" style="max-height: 100px; max-width: 200px; display: block; margin: 6px auto; border-radius: 4px; border: 1px solid #e2e8f0; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);" />`;
    });

    const { root } = transformer.transform(cleanMd);

    if (!mmRef.current) {
      mmRef.current = Markmap.create(
        svgRef.current,
        {
          autoFit: true,
        },
        root,
      );
    } else {
      mmRef.current.setData(root);
      mmRef.current.fit();
    }
  }, [markmapData]);

  // Fit markmap when fullscreen toggles
  useEffect(() => {
    if (!mmRef.current) return;
    const timer = setTimeout(() => {
      mmRef.current?.fit();
    }, 150);
    return () => clearTimeout(timer);
  }, [isFullscreen]);

  // Handle escape key to exit fullscreen
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isFullscreen) {
        setIsFullscreen(false);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isFullscreen]);

  // Clean up on unmount
  useEffect(() => {
    return () => {
      if (mmRef.current) {
        mmRef.current.destroy();
        mmRef.current = null;
      }
    };
  }, []);

  const containerStyle = isFullscreen
    ? {
        position: "fixed" as const,
        top: 0,
        left: 0,
        width: "100vw",
        height: "100vh",
        backgroundColor: "#ffffff",
        zIndex: 99999,
        overflow: "hidden",
        padding: "20px",
        display: "flex",
        flexDirection: "column" as const,
      }
    : {
        position: "relative" as const,
        width: "100%",
        height: "65vh",
        border: "1px solid #e2e8f0",
        borderRadius: "8px",
        backgroundColor: "#f9fafb",
        overflow: "hidden",
        display: "flex",
        flexDirection: "column" as const,
      };

  return (
    <div style={containerStyle}>
      <div className="absolute top-3 right-3 z-10 flex gap-2">
        <button
          onClick={() => mmRef.current?.fit()}
          className="px-3 py-1.5 text-xs font-semibold bg-white hover:bg-gray-100 text-slate-700 rounded-md border border-gray-200 shadow-sm transition-all cursor-pointer flex items-center gap-1.5"
        >
          Thu phóng vừa màn hình
        </button>
        <button
          onClick={() => setIsFullscreen(!isFullscreen)}
          className="px-3 py-1.5 text-xs font-semibold bg-white hover:bg-gray-100 text-slate-700 rounded-md border border-gray-200 shadow-sm transition-all cursor-pointer flex items-center gap-1.5"
        >
          {isFullscreen ? <Minimize2 size={14} /> : <Maximize2 size={14} />}
          <span>{isFullscreen ? "Thu nhỏ lại" : "Toàn màn hình"}</span>
        </button>
      </div>
      <div className="flex-1 w-full h-full">
        <svg ref={svgRef} className="w-full h-full" />
      </div>
    </div>
  );
}

const { Header, Content } = Layout;
const { Title, Paragraph } = Typography;

export default function LessonArtifactViewerPage() {
  const { courseId, lessonId } = useParams();
  const navigate = useNavigate();
  const parsedLessonId = Number(lessonId);

  const { data: lesson, isLoading: isLoadingLesson } =
    useLesson(parsedLessonId);
  const { data: artifacts, isLoading: isLoadingArtifacts } =
    useArtifacts(parsedLessonId);

  const [searchParams, setSearchParams] = useSearchParams();
  const activeTab = searchParams.get("tab") || "reading";

  const setActiveTab = (tab: string) => {
    setSearchParams(
      (prev) => {
        prev.set("tab", tab);
        return prev;
      },
      { replace: true },
    );
  };

  // Load first available artifact type as default tab
  useEffect(() => {
    if (!searchParams.get("tab") && artifacts && artifacts.length > 0) {
      const types = artifacts.map((a) => a.type);
      let defaultTab = types[0];
      if (types.includes("reading")) {
        defaultTab = "reading";
      } else if (types.includes("quiz")) {
        defaultTab = "quiz";
      } else if (types.includes("practice")) {
        defaultTab = "practice";
      } else if (types.includes("outline")) {
        defaultTab = "outline";
      }
      setSearchParams(
        (prev) => {
          prev.set("tab", defaultTab);
          return prev;
        },
        { replace: true },
      );
    }
  }, [artifacts, searchParams, setSearchParams]);

  const activeArtifact = useMemo(() => {
    return artifacts?.find(
      (a) =>
        a.type === activeTab ||
        (activeTab === "quiz" &&
          (a.type === "pre_quiz" || a.type === "post_quiz")),
    );
  }, [artifacts, activeTab]);

  if (isLoadingLesson || isLoadingArtifacts) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="text-center space-y-4">
          <Spin size="large" />
          <div className="text-slate-500 font-medium">
            Đang chuẩn bị môi trường học tập...
          </div>
        </div>
      </div>
    );
  }

  if (!lesson) {
    return (
      <div className="p-8 text-center bg-slate-50 min-h-screen flex flex-col justify-center items-center">
        <AlertCircle size={48} className="text-red-500 mb-4" />
        <Title level={4}>Không tìm thấy bài học</Title>
        <Paragraph>Mã bài học không hợp lệ hoặc dữ liệu đã bị xóa.</Paragraph>
        <Button
          icon={<ArrowLeft size={16} />}
          onClick={() => navigate(`/courses/${courseId}`)}
        >
          Quay lại môn học
        </Button>
      </div>
    );
  }

  // Filter artifact tabs that are completed
  const availableTabs = [
    {
      key: "reading",
      label: "Bài học lý thuyết",
      icon: <BookOpen size={16} />,
      exists: artifacts?.some((a) => a.type === "reading"),
    },
    {
      key: "outline",
      label: "Sơ đồ tư duy (MD)",
      icon: <Network size={16} />,
      exists: artifacts?.some(
        (a) => a.type === "outline" || a.type === "session_mindmap",
      ),
    },
    {
      key: "quiz",
      label: "Quizz Trắc nghiệm",
      icon: <HelpCircle size={16} />,
      exists: artifacts?.some(
        (a) =>
          a.type === "quiz" || a.type === "pre_quiz" || a.type === "post_quiz",
      ),
    },
    {
      key: "practice",
      label: "Thực hành Lab",
      icon: <Terminal size={16} />,
      exists: true,
    }, // Always show Lab workspace (can fallback to template if not generated)
  ].filter((t) => t.exists || t.key === "practice");

  return (
    <Layout className="h-[calc(100vh-200px)] bg-slate-50 rounded-lg overflow-hidden border border-slate-200">
      {/* Top Learning Navigation Bar */}
      <Header
        className="bg-white px-4 flex items-center justify-between border-b border-slate-200 h-16"
        style={{ background: "#fff", padding: "0 16px" }}
      >
        <div className="flex items-center gap-3 overflow-hidden">
          <Button
            type="text"
            icon={<ArrowLeft size={18} className="text-slate-600" />}
            onClick={() => navigate(`/courses/${courseId}`)}
            className="hover:bg-slate-100"
          />
          <Divider type="vertical" className="h-6 border-slate-200" />
          <div
            className="truncate flex flex-col justify-center"
            style={{ lineHeight: "normal" }}
          >
            <span className="text-xs font-semibold text-indigo-600 bg-indigo-50 font-mono px-2 py-0.5 rounded w-max block mb-2">
              {lesson.name}
            </span>
            <Title
              level={5}
              className="m-0 mt-1 truncate text-slate-800 text-sm font-bold block"
              style={{ lineHeight: "1.3", margin: 0 }}
            >
              {lesson.title}
            </Title>
          </div>
        </div>

        {/* Tab Selector */}
        <div className="flex items-center gap-1.5">
          {availableTabs.map((tab) => (
            <Button
              key={tab.key}
              type={activeTab === tab.key ? "primary" : "text"}
              icon={tab.icon}
              className={`font-semibold rounded-lg text-xs md:text-sm px-3 py-1.5 h-auto flex items-center gap-1.5 ${
                activeTab === tab.key
                  ? "bg-indigo-600 hover:bg-indigo-700"
                  : "text-slate-600 hover:bg-slate-100"
              }`}
              onClick={() => setActiveTab(tab.key)}
            >
              {tab.label}
            </Button>
          ))}
        </div>
      </Header>

      {/* Main Workspace */}
      <Layout>
        <Content className="relative flex flex-col min-h-0 bg-slate-50">
          {!activeArtifact && activeTab !== "practice" ? (
            <div className="p-12 text-center flex flex-col items-center justify-center h-full bg-white">
              <BookOpenCheck
                size={64}
                className="text-slate-300 mb-4 animate-pulse"
              />
              <Title level={4} className="text-slate-700">
                Học liệu đang được sinh
              </Title>
              <Paragraph className="text-slate-500 max-w-md">
                Phần này chưa được biên dịch thành công hoặc đang chạy dưới nền.
                Quay lại màn hình Pipeline Monitor để theo dõi trạng thái AI.
              </Paragraph>
              <Button
                type="primary"
                ghost
                icon={<RefreshCw size={14} />}
                onClick={() => window.location.reload()}
              >
                Tải lại trang
              </Button>
            </div>
          ) : (
            <div className="flex-1 flex flex-col min-h-0">
              {activeTab === "reading" && activeArtifact && (
                <ReadingViewer artifact={activeArtifact} />
              )}
              {activeTab === "outline" && activeArtifact && (
                <OutlineViewer artifact={activeArtifact} />
              )}
              {activeTab === "quiz" && activeArtifact && (
                <QuizViewer artifact={activeArtifact} />
              )}
              {activeTab === "practice" && (
                <PracticeLabViewer artifact={activeArtifact} lesson={lesson} />
              )}
            </div>
          )}
        </Content>
      </Layout>
    </Layout>
  );
}

// ──────────────────────────────────────────────────────────
// 1. Reading Viewer Component
// ──────────────────────────────────────────────────────────
interface HeadingItem {
  id: string;
  text: string;
  level: number;
}

function ReadingViewer({ artifact }: { artifact: ArtifactResponse }) {
  const [fontSize, setFontSize] = useState<number>(16);
  const [fontFamily, setFontFamily] = useState<string>("font-sans");
  const [theme, setTheme] = useState<"light" | "sepia" | "dark">("light");
  const [focusMode, setFocusMode] = useState<boolean>(false);
  const [headings, setHeadings] = useState<HeadingItem[]>([]);
  const [scrollPercent, setScrollPercent] = useState<number>(0);
  const iframeRef = useRef<HTMLIFrameElement>(null);

  // Generate Table of Contents from HTML
  useEffect(() => {
    if (artifact?.content) {
      const parser = new DOMParser();
      const doc = parser.parseFromString(artifact.content, "text/html");
      const headingElements = doc.querySelectorAll("h1, h2, h3");
      const list: HeadingItem[] = [];

      headingElements.forEach((el, index) => {
        const id = el.id || `heading-${index}`;
        el.id = id; // Ensure element has id
        list.push({
          id,
          text: el.textContent || "",
          level: parseInt(el.tagName[1]),
        });
      });
      setHeadings(list);
    }
  }, [artifact]);

  // Load content into iframe only when artifact content changes
  useEffect(() => {
    const iframe = iframeRef.current;
    if (!iframe || !artifact?.content) return;

    const doc = iframe.contentDocument || iframe.contentWindow?.document;
    if (!doc) return;

    doc.open();
    doc.write(artifact.content);
    doc.close();

    const win = iframe.contentWindow as (Window & { initApp?: () => void }) | null;
    if (win && typeof win.initApp === "function") {
      try {
        win.initApp();
      } catch (e) {
        console.error(
          "Failed to re-initialize visualizer app on frame content load",
          e,
        );
      }
    }
  }, [artifact]);

  // Inject/update themes and styles dynamically without reloading iframe content
  useEffect(() => {
    const iframe = iframeRef.current;
    if (!iframe || !artifact?.content) return;

    const doc = iframe.contentDocument || iframe.contentWindow?.document;
    if (!doc) return;

    // Check if style element already exists, if not, create it
    let styleEl = doc.getElementById(
      "iframe-injected-styles",
    ) as HTMLStyleElement;
    if (!styleEl) {
      styleEl = doc.createElement("style");
      styleEl.id = "iframe-injected-styles";
      doc.head.appendChild(styleEl);
    }

    styleEl.innerHTML = `
      body {
        font-size: ${fontSize}px !important;
        line-height: 1.7 !important;
        padding: 24px !important;
        margin: 0 auto !important;
        max-width: 1200px !important;
        transition: all 0.3s ease;
      }
      @media (min-width: 768px) {
        body {
          padding: 40px !important;
        }
      }
      pre, code {
        font-family: 'Fira Code', Consolas, Monaco, monospace !important;
        border-radius: 6px !important;
      }
      pre {
        background-color: #0f172a !important;
        color: #f8fafc !important;
        padding: 16px !important;
        overflow-x: auto !important;
        border: 1px solid #334155 !important;
        position: relative;
      }
      blockquote {
        border-left: 4px solid #6366f1 !important;
        background-color: #f5f3ff !important;
        padding: 12px 20px !important;
        margin-left: 0 !important;
        border-radius: 0 8px 8px 0 !important;
      }
      /* Sepia Theme */
      body.theme-sepia {
        background-color: #fcf6e8 !important;
        color: #433422 !important;
      }
      body.theme-sepia blockquote {
        background-color: #f5edd6 !important;
        border-left-color: #b45309 !important;
        color: #78350f !important;
      }
      /* Dark Theme */
      body.theme-dark {
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
      }
      body.theme-dark blockquote {
        background-color: #1e293b !important;
        border-left-color: #818cf8 !important;
        color: #cbd5e1 !important;
      }
      body.theme-dark a {
        color: #818cf8 !important;
      }
      /* Custom Font Families */
      body.font-sans { font-family: 'Outfit', 'Inter', system-ui, sans-serif !important; }
      body.font-serif { font-family: 'Georgia', 'Playfair Display', serif !important; }
      body.font-mono { font-family: 'Fira Code', 'Courier New', monospace !important; }
    `;

    // Apply active classes to body
    if (doc.body) {
      doc.body.className = `${fontFamily} theme-${theme}`;
    }

    // Handle iframe scroll to update progress bar
    const handleScroll = () => {
      const scrollHeight =
        doc.documentElement.scrollHeight - doc.documentElement.clientHeight;
      if (scrollHeight > 0) {
        const percent = Math.min(
          100,
          Math.round((doc.documentElement.scrollTop / scrollHeight) * 100),
        );
        setScrollPercent(percent);
      }
    };
    doc.addEventListener("scroll", handleScroll);

    return () => doc.removeEventListener("scroll", handleScroll);
  }, [artifact, fontSize, fontFamily, theme]);

  const scrollToHeading = (id: string) => {
    const iframe = iframeRef.current;
    if (!iframe) return;
    const doc = iframe.contentDocument || iframe.contentWindow?.document;
    if (!doc) return;
    const element = doc.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <div className="flex-1 flex min-h-0 bg-white">
      {/* Table of Contents Sidebar */}
      {!focusMode && headings.length > 0 && (
        <div className="w-64 border-r border-slate-200 bg-slate-50 flex-col min-h-0 hidden md:flex">
          <div className="p-4 border-b border-slate-200 bg-white flex items-center justify-between">
            <span className="font-bold text-slate-700 text-xs uppercase tracking-wider flex items-center gap-1.5">
              <ListTodo size={14} className="text-indigo-600" /> Mục lục bài đọc
            </span>
            <Badge
              count={headings.length}
              className="site-badge-count-4"
              style={{ backgroundColor: "#6366f1" }}
            />
          </div>
          <div className="flex-1 overflow-y-auto p-2 space-y-1">
            {headings.map((h, i) => (
              <button
                key={i}
                onClick={() => scrollToHeading(h.id)}
                className={`w-full text-left px-3 py-2 rounded-lg text-xs font-semibold transition-colors flex items-start gap-1.5 ${
                  h.level === 1
                    ? "text-slate-800 hover:bg-slate-100 pl-3 font-bold"
                    : h.level === 2
                      ? "text-slate-600 hover:bg-slate-100 pl-6 font-medium"
                      : "text-slate-500 hover:bg-slate-100 pl-9 font-normal"
                }`}
              >
                <ChevronRight
                  size={10}
                  className="mt-1 text-slate-400 shrink-0"
                />
                <span>{h.text}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-h-0">
        {/* Settings Bar */}
        <div className="h-12 border-b border-slate-200 bg-slate-50 px-4 flex items-center justify-between">
          {/* Scroll progress indicator */}
          <div className="absolute top-16 left-0 right-0 h-1 bg-slate-100 z-10">
            <div
              className="h-full bg-indigo-600 transition-all duration-150"
              style={{ width: `${scrollPercent}%` }}
            />
          </div>

          <div className="flex items-center gap-4">
            {/* Font Family Selector */}
            <Radio.Group
              size="small"
              value={fontFamily}
              onChange={(e) => setFontFamily(e.target.value)}
            >
              <Radio.Button value="font-sans">Sans</Radio.Button>
              <Radio.Button value="font-serif">Serif</Radio.Button>
              <Radio.Button value="font-mono">Mono</Radio.Button>
            </Radio.Group>

            {/* Font Size adjuster */}
            <div className="flex items-center gap-1 bg-white border border-slate-200 rounded px-1.5 py-0.5">
              <Button
                type="text"
                size="small"
                icon={<ZoomOut size={12} />}
                onClick={() => setFontSize(Math.max(12, fontSize - 2))}
              />
              <span className="text-xs font-bold text-slate-600 w-8 text-center">
                {fontSize}px
              </span>
              <Button
                type="text"
                size="small"
                icon={<ZoomIn size={12} />}
                onClick={() => setFontSize(Math.min(24, fontSize + 2))}
              />
            </div>
          </div>

          <div className="flex items-center gap-3">
            {/* Theme Selector */}
            <Radio.Group
              size="small"
              value={theme}
              onChange={(e) => setTheme(e.target.value)}
            >
              <Radio.Button value="light" className="hover:text-indigo-600">
                Sáng
              </Radio.Button>
              <Radio.Button
                value="sepia"
                className="bg-[#fcf6e8] text-[#433422]"
              >
                Sepia
              </Radio.Button>
              <Radio.Button
                value="dark"
                className="bg-slate-900 text-slate-100"
              >
                Tối
              </Radio.Button>
            </Radio.Group>

            <Divider type="vertical" className="border-slate-300" />

            {/* Focus mode toggler */}
            <Button
              size="small"
              icon={
                focusMode ? <Minimize2 size={14} /> : <Maximize2 size={14} />
              }
              onClick={() => setFocusMode(!focusMode)}
              className="text-slate-600 hover:text-indigo-600 flex items-center"
            >
              {focusMode ? "Hiện lục mục" : "Đọc tập trung"}
            </Button>
          </div>
        </div>

        {/* Dynamic Iframe Panel */}
        <div
          className={`flex-1 flex flex-col min-h-0 overflow-hidden transition-all ${
            theme === "dark"
              ? "bg-slate-900"
              : theme === "sepia"
                ? "bg-[#fcf6e8]"
                : "bg-white"
          }`}
        >
          <iframe
            ref={iframeRef}
            className="w-full flex-1 border-0"
            title="Reading Frame"
            sandbox="allow-same-origin allow-scripts"
          />
        </div>
      </div>
    </div>
  );
}

// ──────────────────────────────────────────────────────────
// 2. Outline / Mindmap Viewer Component
// ──────────────────────────────────────────────────────────
function OutlineViewer({ artifact }: { artifact: ArtifactResponse }) {
  return (
    <div className="flex-1 flex flex-col bg-slate-50 p-6 overflow-y-auto pr-2">
      <Card
        title={
          <div className="flex items-center gap-2">
            <Network className="text-indigo-600" size={18} />
            <span className="font-bold text-slate-800">
              Sơ đồ Cấu trúc & Bản đồ Tư duy Bài học
            </span>
          </div>
        }
        className="w-full max-w-5xl mx-auto shadow-sm border-slate-200 rounded-xl"
      >
        <Paragraph className="text-slate-500 mb-6 text-xs md:text-sm font-semibold">
          Xem sơ đồ trực quan và hệ thống hóa kiến thức thông qua Mindmap tương
          tác của Markmap. Bạn có thể kéo thả để di chuyển và cuộn chuột để
          phóng to/thu nhỏ.
        </Paragraph>
        {artifact?.content ? (
          <MarkmapComponent markmapData={artifact.content} />
        ) : (
          <Empty description="Không có dữ liệu sơ đồ tư duy." />
        )}
      </Card>
    </div>
  );
}

// ──────────────────────────────────────────────────────────
// 3. Quiz / Exercises Viewer Component
// ──────────────────────────────────────────────────────────
interface QuestionOption {
  option_text: string;
  is_correct: boolean;
}

interface Question {
  question_text: string;
  options: QuestionOption[];
  explanation: string;
}

interface RawQuizQuestion {
  question_content?: string;
  question?: string;
  answer_1?: string;
  answer_2?: string;
  answer_3?: string;
  answer_4?: string;
  isCorrect?: number | string;
  explanation?: string;
  [key: string]: string | number | boolean | undefined;
}

interface RawQuestionOption {
  option_text?: string;
  is_correct?: boolean;
}

interface RawQuestionDetail {
  question_text?: string;
  question?: string;
  options?: Array<RawQuestionOption | string>;
  correct_option_index?: number;
  explanation?: string;
}

function QuizViewer({ artifact }: { artifact: ArtifactResponse }) {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIdx, setCurrentIdx] = useState<number>(0);
  const [selectedAnswers, setSelectedAnswers] = useState<
    Record<number, number>
  >({});
  const [isSubmitted, setIsSubmitted] = useState<boolean>(false);
  const [showExplanation, setShowExplanation] = useState<boolean>(false);

  // Normalize JSON quiz data structure from Database
  useEffect(() => {
    if (!artifact?.content_json) return;
    const rawData = artifact.content_json;
    let list: Question[] = [];

    if (rawData.quiz && Array.isArray(rawData.quiz)) {
      list = rawData.quiz.map((q: RawQuizQuestion) => {
        const isCorrectIdx = Number(q.isCorrect) || 1;
        const options = [
          { option_text: q.answer_1 || "", is_correct: isCorrectIdx === 1 },
          { option_text: q.answer_2 || "", is_correct: isCorrectIdx === 2 },
          { option_text: q.answer_3 || "", is_correct: isCorrectIdx === 3 },
          { option_text: q.answer_4 || "", is_correct: isCorrectIdx === 4 },
        ].filter((o) => o.option_text !== "");

        let explanation = q.explanation || "";
        if (!explanation) {
          explanation =
            (q[`explanation_answer_${isCorrectIdx}`] as string) || "";
        }

        return {
          question_text: q.question_content || q.question || "",
          options,
          explanation,
        };
      });
    } else if (rawData.questions && Array.isArray(rawData.questions)) {
      list = rawData.questions.map((q: RawQuestionDetail) => {
        let options: QuestionOption[] = [];
        if (Array.isArray(q.options)) {
          options = q.options.map(
            (opt: RawQuestionOption | string, idx: number) => {
              if (typeof opt === "object" && opt !== null) {
                return {
                  option_text: opt.option_text || "",
                  is_correct: !!opt.is_correct,
                };
              }
              return {
                option_text: String(opt),
                is_correct: idx === q.correct_option_index,
              };
            },
          );
        }
        return {
          question_text: q.question_text || q.question || "",
          options,
          explanation: q.explanation || "",
        };
      });
    } else if (rawData.lesson_quiz && Array.isArray(rawData.lesson_quiz)) {
      list = rawData.lesson_quiz.map((q: RawQuestionDetail) => {
        let options: QuestionOption[] = [];
        if (Array.isArray(q.options)) {
          options = q.options.map(
            (opt: RawQuestionOption | string, idx: number) => {
              if (typeof opt === "object" && opt !== null) {
                return {
                  option_text: opt.option_text || "",
                  is_correct: !!opt.is_correct,
                };
              }
              return {
                option_text: String(opt),
                is_correct: idx === q.correct_option_index,
              };
            },
          );
        }
        return {
          question_text: q.question_text || q.question || "",
          options,
          explanation: q.explanation || "",
        };
      });
    }

    setQuestions(list);
    setCurrentIdx(0);
    setSelectedAnswers({});
    setIsSubmitted(false);
    setShowExplanation(false);
  }, [artifact]);

  const activeQuestion = questions[currentIdx];

  const handleSelectOption = (optIdx: number) => {
    if (isSubmitted) return;
    setSelectedAnswers((prev) => ({ ...prev, [currentIdx]: optIdx }));
  };

  const calculateScore = () => {
    let correct = 0;
    questions.forEach((q, i) => {
      const selected = selectedAnswers[i];
      if (selected !== undefined && q.options[selected]?.is_correct) {
        correct++;
      }
    });
    return correct;
  };

  const handleResetQuiz = () => {
    setSelectedAnswers({});
    setIsSubmitted(false);
    setCurrentIdx(0);
    setShowExplanation(false);
  };

  if (questions.length === 0) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center p-12 bg-white">
        <HelpCircle size={48} className="text-slate-300 mb-4 animate-bounce" />
        <Title level={5} className="text-slate-500">
          Môn học này không có câu hỏi trắc nghiệm trích xuất.
        </Title>
      </div>
    );
  }

  const score = calculateScore();
  const scorePercent = Math.round((score / questions.length) * 100);

  return (
    <div className="flex-1 flex flex-col md:flex-row min-h-0 bg-slate-100">
      {/* Left Workspace: Active Question or Final Screen */}
      <div className="flex-1 p-4 md:p-6 overflow-y-auto flex justify-center items-start">
        <div className="w-full max-w-3xl space-y-4">
          {!isSubmitted ? (
            <Card
              className="shadow-sm border-slate-200 rounded-xl"
              title={
                <div className="flex justify-between items-center w-full">
                  <span className="font-bold text-slate-800 text-xs md:text-sm">
                    Câu hỏi {currentIdx + 1} / {questions.length}
                  </span>
                  <Badge
                    count={
                      selectedAnswers[currentIdx] !== undefined
                        ? "Đã trả lời"
                        : "Chưa trả lời"
                    }
                    style={{
                      backgroundColor:
                        selectedAnswers[currentIdx] !== undefined
                          ? "#22c55e"
                          : "#94a3b8",
                    }}
                  />
                </div>
              }
              actions={[
                <div
                  className="flex justify-between items-center px-6 py-2"
                  key="actions"
                >
                  <Button
                    icon={<ChevronLeft size={16} />}
                    onClick={() =>
                      setCurrentIdx((prev) => Math.max(0, prev - 1))
                    }
                    disabled={currentIdx === 0}
                    className="font-semibold flex items-center"
                  >
                    Quay lại
                  </Button>
                  {currentIdx === questions.length - 1 ? (
                    <Button
                      type="primary"
                      icon={<Award size={16} />}
                      onClick={() => setIsSubmitted(true)}
                      disabled={
                        Object.keys(selectedAnswers).length < questions.length
                      }
                      className="font-bold bg-indigo-600 hover:bg-indigo-700 flex items-center"
                    >
                      Nộp bài
                    </Button>
                  ) : (
                    <Button
                      type="primary"
                      icon={<ChevronRight size={16} />}
                      onClick={() =>
                        setCurrentIdx((prev) =>
                          Math.min(questions.length - 1, prev + 1),
                        )
                      }
                      className="font-semibold bg-slate-800 hover:bg-slate-700 flex items-center"
                    >
                      Tiếp theo
                    </Button>
                  )}
                </div>,
              ]}
            >
              <div className="space-y-6">
                <Title level={4} className="text-slate-800 leading-snug">
                  {activeQuestion.question_text}
                </Title>

                {/* Options List */}
                <div className="space-y-3">
                  {activeQuestion.options.map((opt, i) => {
                    const isSelected = selectedAnswers[currentIdx] === i;
                    return (
                      <div
                        key={i}
                        onClick={() => handleSelectOption(i)}
                        className={`p-4 rounded-xl border-2 cursor-pointer transition-all flex items-center justify-between ${
                          isSelected
                            ? "border-indigo-600 bg-indigo-50/50 shadow-sm"
                            : "border-slate-200 hover:border-slate-300 hover:bg-slate-50"
                        }`}
                      >
                        <span
                          className={`text-xs md:text-sm font-semibold ${isSelected ? "text-indigo-800 font-bold" : "text-slate-700"}`}
                        >
                          {opt.option_text}
                        </span>
                        <div
                          className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${isSelected ? "border-indigo-600 bg-indigo-600" : "border-slate-300"}`}
                        >
                          {isSelected && (
                            <div className="w-2 h-2 rounded-full bg-white" />
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </Card>
          ) : (
            // Results Dashboard Panel
            <Card className="shadow-sm border-slate-200 rounded-xl text-center p-6 space-y-6">
              <div className="max-w-md mx-auto space-y-4">
                <Progress
                  type="circle"
                  percent={scorePercent}
                  strokeColor={{ "0%": "#10b981", "100%": "#6366f1" }}
                  strokeWidth={10}
                  width={140}
                  format={() => (
                    <div className="space-y-0.5">
                      <div className="text-3xl font-extrabold text-slate-800">
                        {score}/{questions.length}
                      </div>
                      <div className="text-xs font-semibold text-slate-400">
                        Chính xác
                      </div>
                    </div>
                  )}
                />

                <div className="flex flex-col items-center gap-2">
                  <div className="flex items-center gap-2">
                    {scorePercent >= 80 ? (
                      <Award
                        size={24}
                        className="text-yellow-500 animate-bounce"
                      />
                    ) : scorePercent >= 50 ? (
                      <CheckCircle2 size={24} className="text-emerald-500" />
                    ) : (
                      <AlertCircle size={24} className="text-amber-500" />
                    )}
                    <Title level={3} className="text-slate-800 font-bold m-0">
                      {scorePercent >= 80
                        ? "Xuất sắc!"
                        : scorePercent >= 50
                          ? "Làm tốt lắm!"
                          : "Cần ôn luyện thêm!"}
                    </Title>
                  </div>
                  <Paragraph className="text-slate-500">
                    Bạn đạt tỉ lệ đúng {scorePercent}% trong bài trắc nghiệm
                    nhanh bài học này.
                  </Paragraph>
                </div>

                <div className="flex gap-3 justify-center">
                  <Button
                    icon={<RefreshCw size={16} />}
                    onClick={handleResetQuiz}
                    className="font-semibold"
                  >
                    Làm lại
                  </Button>
                  <Button
                    type="primary"
                    icon={<BookOpen size={16} />}
                    className="font-bold bg-indigo-600"
                    onClick={() => setShowExplanation(!showExplanation)}
                  >
                    {showExplanation
                      ? "Ẩn đáp án chi tiết"
                      : "Xem đáp án chi tiết"}
                  </Button>
                </div>
              </div>

              {/* Detailed Review Option */}
              {showExplanation && (
                <div className="text-left mt-8 space-y-6 border-t border-slate-100 pt-6">
                  <Title level={4} className="text-slate-700">
                    Đánh giá từng câu hỏi
                  </Title>
                  {questions.map((q, idx) => {
                    const selected = selectedAnswers[idx];
                    const isCorrect =
                      selected !== undefined && q.options[selected]?.is_correct;
                    return (
                      <Card
                        key={idx}
                        size="small"
                        className={`border-l-4 ${isCorrect ? "border-l-emerald-500 bg-emerald-50/10" : "border-l-rose-500 bg-rose-50/10"}`}
                      >
                        <div className="font-bold text-slate-800 mb-2">
                          Câu {idx + 1}: {q.question_text}
                        </div>
                        <div className="space-y-1.5 pl-2 mb-3">
                          {q.options.map((opt, oIdx) => (
                            <div
                              key={oIdx}
                              className="flex items-center gap-2 text-xs md:text-sm"
                            >
                              {opt.is_correct ? (
                                <CheckCircle2
                                  size={16}
                                  className="text-emerald-500"
                                />
                              ) : selected === oIdx ? (
                                <XCircle size={16} className="text-rose-500" />
                              ) : (
                                <div className="w-4 h-4 rounded-full border border-slate-300" />
                              )}
                              <span
                                className={`${opt.is_correct ? "text-emerald-700 font-bold" : selected === oIdx ? "text-rose-700 font-bold" : "text-slate-600"}`}
                              >
                                {opt.option_text}
                              </span>
                            </div>
                          ))}
                        </div>
                        {q.explanation && (
                          <Alert
                            message={
                              <span className="font-bold text-xs text-indigo-800">
                                Giải thích chi tiết của AI:
                              </span>
                            }
                            description={
                              <span className="text-xs text-indigo-700 font-semibold">
                                {q.explanation}
                              </span>
                            }
                            type="info"
                            showIcon
                            className="bg-indigo-50/50 border-indigo-100 rounded-lg"
                          />
                        )}
                      </Card>
                    );
                  })}
                </div>
              )}
            </Card>
          )}
        </div>
      </div>

      {/* Right Sidebar: Questions Grid Navigator */}
      <div className="w-full md:w-64 border-t md:border-t-0 md:border-l border-slate-200 bg-white p-4 flex flex-col shrink-0">
        <span className="font-bold text-slate-700 text-xs uppercase tracking-wider mb-4 flex items-center gap-1.5">
          <Award size={14} className="text-indigo-600" /> Danh sách câu hỏi
        </span>
        <div className="grid grid-cols-5 gap-2 overflow-y-auto">
          {questions.map((_, i) => {
            const isAnswered = selectedAnswers[i] !== undefined;
            const isActive = currentIdx === i;
            let btnClass = "bg-slate-50 text-slate-600 border-slate-200";
            if (isSubmitted) {
              const isCorrect =
                selectedAnswers[i] !== undefined &&
                questions[i].options[selectedAnswers[i]]?.is_correct;
              btnClass = isCorrect
                ? "bg-emerald-500 text-white border-emerald-500"
                : "bg-rose-500 text-white border-rose-500";
            } else if (isActive) {
              btnClass =
                "border-indigo-600 bg-indigo-50 text-indigo-600 ring-2 ring-indigo-200";
            } else if (isAnswered) {
              btnClass = "bg-slate-800 text-white border-slate-800";
            }

            return (
              <button
                key={i}
                onClick={() => !isSubmitted && setCurrentIdx(i)}
                className={`h-10 rounded-lg border font-bold text-sm transition-all flex items-center justify-center ${btnClass}`}
              >
                {i + 1}
              </button>
            );
          })}
        </div>

        {/* Legend */}
        <div className="mt-8 space-y-2 border-t border-slate-100 pt-4 text-xs font-semibold text-slate-500">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded bg-slate-50 border border-slate-200" />
            <span>Chưa trả lời</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded bg-slate-800" />
            <span>Đã làm</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded border border-indigo-600 bg-indigo-50" />
            <span>Câu hiện tại</span>
          </div>
          {isSubmitted && (
            <>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded bg-emerald-500" />
                <span>Trả lời đúng</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded bg-rose-500" />
                <span>Trả lời sai</span>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

// ──────────────────────────────────────────────────────────
// 4. Practical Lab Viewer Component (Workspace Layout)
// ──────────────────────────────────────────────────────────
function PracticeLabViewer({
  artifact,
  lesson,
}: {
  artifact: ArtifactResponse | undefined;
  lesson: LessonResponse;
}) {
  const [activeFile, setActiveFile] = useState<string>("app.py");
  const [codeContent, setCodeContent] = useState<string>(
    `# Khởi động Code Lab: ${lesson.title}\n\ndef solve_problem():\n    # Hãy viết thuật toán xử lý của bạn ở đây\n    pass\n`,
  );
  const [terminalLogs, setTerminalLogs] = useState<string[]>([]);
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [runSuccess, setRunSuccess] = useState<boolean | null>(null);
  const [copying, setCopying] = useState<boolean>(false);
  const [completedSteps, setCompletedSteps] = useState<Record<number, boolean>>(
    {},
  );

  const labDetails = useMemo(() => {
    // Attempt to extract structured lab json from the parent json or format mock data
    const json = artifact?.content_json;
    if (json?.practical_lab) {
      return json.practical_lab;
    }

    // Fallback template matching technology stack
    return {
      title: `Luyện tập thực hành: ${lesson.title}`,
      objectives: [
        "Hiểu và vận dụng thành thạo lý thuyết đã học vào mã nguồn thực tế.",
        "Thiết lập cấu trúc chương trình tối ưu và xử lý các ràng buộc logic.",
        "Chạy kiểm thử thành công và tối ưu độ phức tạp thuật toán.",
      ],
      description: {
        inputs: "IDE Editor đã được thiết lập sẵn môi trường ngôn ngữ phù hợp.",
        steps: [
          "Phân tích yêu cầu bài toán được mô tả chi tiết trong phần Details của bài học.",
          "Đọc hiểu và bổ sung code vào hàm `solve_problem()` trên bảng soạn thảo code.",
          'Bấm nút "Chạy kiểm thử" để chạy tập lệnh tự động đánh giá.',
          "Sửa lỗi cú pháp và kiểm thử biên (nếu có) cho đến khi 100% test cases chuyển màu xanh.",
        ],
      },
      evaluation: {
        checklist: [
          "Chạy thành công không sinh lỗi runtime (Python/JS exception).",
          "Vượt qua các Test Cases kiểm thử tự động.",
          "Độ phức tạp tối ưu không làm treo máy.",
        ],
      },
    };
  }, [artifact, lesson]);

  // Mock File system list based on stack
  const filesList = [
    { name: "app.py", language: "python" },
    { name: "tests.py", language: "python" },
    { name: "README.md", language: "markdown" },
  ];

  const handleCopyCode = () => {
    navigator.clipboard.writeText(codeContent);
    setCopying(true);
    message.success("Đã sao chép mã nguồn!");
    setTimeout(() => setCopying(false), 2000);
  };

  const handleRunTests = () => {
    if (isRunning) return;
    setIsRunning(true);
    setRunSuccess(null);
    setTerminalLogs([
      `$ pytest tests.py`,
      `============================= test session starts =============================`,
      `platform win32 -- Python 3.14.0, pytest-8.1.1, pluggy-1.4.0`,
      `rootdir: /workspace/elearning_lab`,
      `collected 3 items`,
      ``,
      `Đang chạy biên dịch và kiểm thử mã nguồn...`,
    ]);

    // Animate terminal outputs
    setTimeout(() => {
      setTerminalLogs((prev) => [
        ...prev,
        `tests.py::test_basic_flow [SUCCESS] PASS (0.01s)`,
      ]);
    }, 1000);

    setTimeout(() => {
      setTerminalLogs((prev) => [
        ...prev,
        `tests.py::test_border_cases [SUCCESS] PASS (0.02s)`,
      ]);
    }, 1800);

    setTimeout(() => {
      setTerminalLogs((prev) => [
        ...prev,
        `tests.py::test_performance_criteria [SUCCESS] PASS (0.12s)`,
        ``,
        `=========================== 3 passed in 0.35s ===========================`,
        `[SUCCESS] HOÀN THÀNH: Tất cả kiểm thử đều vượt qua! Học viên đã nắm rõ lý thuyết buổi học.`,
      ]);
      setIsRunning(false);
      setRunSuccess(true);
    }, 2500);
  };

  const toggleStep = (idx: number) => {
    setCompletedSteps((prev) => ({ ...prev, [idx]: !prev[idx] }));
  };

  return (
    <div className="flex-1 flex flex-col lg:flex-row min-h-0 bg-slate-100 overflow-hidden">
      {/* Left Workspace: Lab Instructions Manual */}
      <div className="w-full lg:w-[450px] border-r border-slate-200 bg-white p-4 md:p-6 overflow-y-auto shrink-0 flex flex-col min-h-0">
        <div className="space-y-6">
          <div>
            <div className="flex items-center gap-1.5 text-xs font-semibold text-indigo-600 mb-1">
              <CheckSquare size={14} /> Môi trường thực hành tự động
            </div>
            <Title level={4} className="m-0 text-slate-800 leading-snug">
              {labDetails.title}
            </Title>
          </div>

          <Divider className="my-2" />

          {/* Objectives */}
          <div className="space-y-2">
            <span className="font-bold text-slate-700 text-xs uppercase tracking-wider flex items-center gap-1.5">
              <Award size={14} className="text-indigo-600" /> Mục tiêu thực hành
            </span>
            <ul className="list-disc pl-5 space-y-1 text-slate-600 text-xs md:text-sm font-semibold">
              {labDetails.objectives.map((obj: string, i: number) => (
                <li key={i}>{obj}</li>
              ))}
            </ul>
          </div>

          {/* Setup / Preparation */}
          {labDetails.description?.inputs && (
            <div className="space-y-2">
              <span className="font-bold text-slate-700 text-xs uppercase tracking-wider">
                📥 Chuẩn bị đầu vào
              </span>
              <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg font-mono text-xs text-slate-600">
                {labDetails.description.inputs}
              </div>
            </div>
          )}

          {/* Step-by-step interactive instructions checklist */}
          <div className="space-y-2">
            <span className="font-bold text-slate-700 text-xs uppercase tracking-wider flex items-center gap-1.5">
              <ListTodo size={14} className="text-indigo-600" /> Các bước thực
              hiện
            </span>
            <div className="space-y-2">
              {labDetails.description?.steps?.map((step: string, i: number) => (
                <div
                  key={i}
                  onClick={() => toggleStep(i)}
                  className={`p-3 rounded-lg border-2 cursor-pointer transition-all flex items-start gap-3 ${
                    completedSteps[i]
                      ? "border-indigo-600 bg-indigo-50/30"
                      : "border-slate-100 hover:border-slate-200 hover:bg-slate-50"
                  }`}
                >
                  <div
                    className={`w-5 h-5 rounded border-2 flex items-center justify-center mt-0.5 transition-all ${
                      completedSteps[i]
                        ? "border-indigo-600 bg-indigo-600 text-white"
                        : "border-slate-300"
                    }`}
                  >
                    {completedSteps[i] && <Check size={12} strokeWidth={3} />}
                  </div>
                  <span
                    className={`text-xs md:text-sm font-semibold leading-relaxed ${
                      completedSteps[i]
                        ? "text-indigo-800/80 line-through"
                        : "text-slate-700"
                    }`}
                  >
                    {step}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Checklist Evaluation */}
          {labDetails.evaluation?.checklist && (
            <div className="space-y-2">
              <span className="font-bold text-slate-700 text-xs uppercase tracking-wider flex items-center gap-1.5">
                🎯 Tiêu chuẩn đánh giá
              </span>
              <ul className="list-disc pl-5 space-y-1 text-slate-600 text-xs md:text-sm font-semibold">
                {labDetails.evaluation.checklist.map(
                  (item: string, i: number) => (
                    <li key={i}>{item}</li>
                  ),
                )}
              </ul>
            </div>
          )}
        </div>
      </div>

      {/* Right Workspace: Mock IDE Panel */}
      <div className="flex-1 flex flex-col min-h-0 bg-slate-900 border-l border-slate-800">
        {/* IDE Header Tabs */}
        <div className="h-10 bg-slate-950 flex items-center justify-between px-3 shrink-0">
          <div className="flex gap-1.5">
            {filesList.map((f) => (
              <button
                key={f.name}
                onClick={() => {
                  setActiveFile(f.name);
                  if (f.name === "README.md") {
                    setCodeContent(
                      `# README - ${lesson.title}\n\nHọc viên hãy đọc hướng dẫn thực hành và lập trình trong file app.py.`,
                    );
                  } else if (f.name === "tests.py") {
                    setCodeContent(
                      `# Pytest test cases\n\ndef test_basic_flow():\n    assert True\n\ndef test_border_cases():\n    assert True\n\ndef test_performance_criteria():\n    assert True`,
                    );
                  } else {
                    setCodeContent(
                      `# Khởi động Code Lab: ${lesson.title}\n\ndef solve_problem():\n    # Hãy viết thuật toán xử lý của bạn ở đây\n    pass\n`,
                    );
                  }
                }}
                className={`px-3 py-1.5 text-xs font-semibold rounded-t-lg transition-colors flex items-center gap-1.5 ${
                  activeFile === f.name
                    ? "bg-slate-900 text-slate-100 border-t-2 border-t-indigo-500"
                    : "text-slate-400 hover:bg-slate-900/50 hover:text-slate-200"
                }`}
              >
                <FileCode size={12} className="text-indigo-400" />
                <span>{f.name}</span>
              </button>
            ))}
          </div>

          <div className="flex gap-2">
            <Button
              size="small"
              type="text"
              icon={
                copying ? (
                  <Check size={14} className="text-emerald-500" />
                ) : (
                  <Copy size={14} />
                )
              }
              onClick={handleCopyCode}
              className="text-slate-400 hover:text-slate-200 hover:bg-slate-800"
            />
            <Button
              size="small"
              type="primary"
              icon={<Play size={12} />}
              loading={isRunning}
              onClick={handleRunTests}
              className="bg-indigo-600 hover:bg-indigo-700 text-xs font-bold flex items-center gap-1.5 h-7"
            >
              Chạy Test Cases
            </Button>
          </div>
        </div>

        {/* IDE Code Editor */}
        <div className="flex-1 min-h-0 bg-slate-950 p-2 flex">
          {/* Line Numbers */}
          <div className="w-10 select-none text-slate-600 font-mono text-right pr-3 pt-1 text-xs border-r border-slate-800 space-y-1">
            {Array.from({ length: codeContent.split("\n").length }).map(
              (_, i) => (
                <div key={i}>{i + 1}</div>
              ),
            )}
          </div>

          {/* Code Textarea */}
          <Input.TextArea
            value={codeContent}
            onChange={(e) => setCodeContent(e.target.value)}
            className="flex-1 bg-transparent border-0 text-slate-100 font-mono text-xs focus:ring-0 resize-none hover:bg-transparent focus:bg-transparent pt-1 pl-3 overflow-y-auto outline-none"
            style={{ boxShadow: "none" }}
          />
        </div>

        {/* Mock Terminal Output Console */}
        <div className="h-48 border-t border-slate-800 bg-slate-950 flex flex-col min-h-0 shrink-0">
          <div className="h-8 bg-slate-900 border-b border-slate-800 flex items-center px-4 justify-between">
            <span className="text-slate-400 text-xs font-bold flex items-center gap-1.5">
              <Terminal size={12} /> Terminal Output
            </span>
            {runSuccess !== null && (
              <Badge
                status={runSuccess ? "success" : "error"}
                text={
                  <span
                    className={`text-[10px] font-bold uppercase ${runSuccess ? "text-emerald-500" : "text-rose-500"}`}
                  >
                    {runSuccess ? "SUCCESS" : "FAILED"}
                  </span>
                }
              />
            )}
          </div>
          <div className="flex-1 p-4 font-mono text-xs text-slate-300 overflow-y-auto space-y-1 bg-black">
            {terminalLogs.length === 0 ? (
              <div className="text-slate-500 italic">
                Môi trường thực hành sẵn sàng. Bấm nút "Chạy Test Cases" để chạy
                script kiểm thử.
              </div>
            ) : (
              terminalLogs.map((log, i) => {
                let colorClass = "text-slate-300";
                if (log.includes("[SUCCESS]") || log.includes("passed"))
                  colorClass = "text-emerald-400 font-bold";
                if (log.includes("$")) colorClass = "text-indigo-400 font-bold";
                if (log.includes("HOÀN THÀNH"))
                  colorClass =
                    "text-indigo-300 font-extrabold bg-indigo-950/20 p-2 rounded block mt-2 border border-indigo-900/30";
                return (
                  <div key={i} className={colorClass}>
                    {log}
                  </div>
                );
              })
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
