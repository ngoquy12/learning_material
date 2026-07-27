import { useState, useEffect, useMemo, useRef } from "react";
import { useParams, useNavigate, useSearchParams } from "react-router-dom";
import {
  Layout,
  Button,
  Spin,
  Alert,
  Progress,
  Card,
  Typography,
  Empty,
  Badge,
  Input,
  Tag,
  Radio,
  Popconfirm,
  Divider,
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
  Maximize2,
  Minimize2,
  HelpCircle,
  Save,
  Plus,
  Trash2,
  Edit3,
  Video,
  PlayCircle,
  VideoOff,
  Clock,
} from "lucide-react";
import {
  useLesson,
  useArtifacts,
  useUpdateArtifact,
  useCreateArtifact,
  ArtifactResponse,
} from "../hooks/useLessons";
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
        height: "100%",
        flex: 1,
        backgroundColor: "#ffffff",
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

  const videoArtifact = useMemo(() => {
    return artifacts?.find((a) => a.type === "video");
  }, [artifacts]);

  const videoQuizArtifact = useMemo(() => {
    return artifacts?.find(
      (a) =>
        a.type === "video_quiz" ||
        a.type === "popup_quiz" ||
        a.type === "video_quizzes",
    );
  }, [artifacts]);

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

  // Filter artifact tabs that are available
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
      key: "video",
      label: "Video bài giảng",
      icon: <PlayCircle size={16} />,
      exists: true,
    },
    {
      key: "video_quiz",
      label: "Câu hỏi Popup",
      icon: <Clock size={16} />,
      exists: true,
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
    },
  ].filter(
    (t) =>
      t.exists ||
      t.key === "practice" ||
      t.key === "video" ||
      t.key === "video_quiz",
  );

  return (
    <Layout className="h-[calc(100vh-200px)] bg-slate-50 rounded-lg overflow-hidden border border-slate-200">
      {/* Top Learning Navigation Bar */}
      <Header
        className="bg-white px-4 flex items-center justify-between border-b border-slate-200 h-16"
        style={{ background: "#fff", padding: "0 16px" }}
      >
        <div className="flex items-center gap-3 overflow-hidden">
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
          {!activeArtifact &&
          activeTab !== "practice" &&
          activeTab !== "video" &&
          activeTab !== "video_quiz" ? (
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
              {activeTab === "video" && (
                <VideoViewer artifact={videoArtifact} lesson={lesson} />
              )}
              {activeTab === "video_quiz" && (
                <VideoQuizViewer artifact={videoQuizArtifact} lesson={lesson} />
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
function ReadingViewer({ artifact }: { artifact: ArtifactResponse }) {
  const iframeRef = useRef<HTMLIFrameElement>(null);

  // Load content into iframe only when artifact content changes
  useEffect(() => {
    const iframe = iframeRef.current;
    if (!iframe || !artifact?.content) return;

    const doc = iframe.contentDocument || iframe.contentWindow?.document;
    if (!doc) return;

    doc.open();
    doc.write(artifact.content);
    doc.close();

    const win = iframe.contentWindow as
      | (Window & { initApp?: () => void })
      | null;
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

  return (
    <div className="flex-1 flex min-h-0 bg-white">
      <div className="flex-1 flex flex-col min-h-0 overflow-hidden bg-white">
        <iframe
          ref={iframeRef}
          className="w-full flex-1 border-0"
          title="Reading Frame"
          sandbox="allow-same-origin allow-scripts"
        />
      </div>
    </div>
  );
}

// ──────────────────────────────────────────────────────────
// 2. Outline / Mindmap Viewer Component
// ──────────────────────────────────────────────────────────
function OutlineViewer({ artifact }: { artifact: ArtifactResponse }) {
  if (!artifact?.content) {
    return (
      <div className="flex-1 flex items-center justify-center bg-white p-8">
        <Empty description="Không có dữ liệu sơ đồ tư duy." />
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col min-h-0 w-full h-full bg-white relative">
      <MarkmapComponent markmapData={artifact.content} />
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
  const [viewMode, setViewMode] = useState<"list" | "test">("list");
  const [editingField, setEditingField] = useState<{
    qIdx: number;
    field: "question" | "explanation" | number;
  } | null>(null);

  const { mutate: updateArtifact, isPending: isUpdating } = useUpdateArtifact();

  // Test mode states
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
        ];

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

  // Handlers for editing
  const handleUpdateQuestionText = (qIdx: number, text: string) => {
    setQuestions((prev) => {
      const next = [...prev];
      next[qIdx] = { ...next[qIdx], question_text: text };
      return next;
    });
  };

  const handleUpdateOptionText = (qIdx: number, oIdx: number, text: string) => {
    setQuestions((prev) => {
      const next = [...prev];
      const opts = [...next[qIdx].options];
      opts[oIdx] = { ...opts[oIdx], option_text: text };
      next[qIdx] = { ...next[qIdx], options: opts };
      return next;
    });
  };

  const handleSetCorrectOption = (qIdx: number, correctOIdx: number) => {
    setQuestions((prev) => {
      const next = [...prev];
      const opts = next[qIdx].options.map((opt, idx) => ({
        ...opt,
        is_correct: idx === correctOIdx,
      }));
      next[qIdx] = { ...next[qIdx], options: opts };
      return next;
    });
  };

  const handleUpdateExplanation = (qIdx: number, text: string) => {
    setQuestions((prev) => {
      const next = [...prev];
      next[qIdx] = { ...next[qIdx], explanation: text };
      return next;
    });
  };

  const handleAddQuestion = () => {
    const newQuestion: Question = {
      question_text: "Nhập nội dung câu hỏi mới...",
      options: [
        { option_text: "Phương án A", is_correct: true },
        { option_text: "Phương án B", is_correct: false },
        { option_text: "Phương án C", is_correct: false },
        { option_text: "Phương án D", is_correct: false },
      ],
      explanation: "Giải thích chi tiết của câu hỏi...",
    };
    setQuestions((prev) => [...prev, newQuestion]);
  };

  const handleDeleteQuestion = (qIdx: number) => {
    setQuestions((prev) => prev.filter((_, idx) => idx !== qIdx));
  };

  const handleSaveToDb = () => {
    if (!artifact) return;

    const formattedQuiz = questions.map((q) => {
      const correctIdx = q.options.findIndex((o) => o.is_correct);
      return {
        question_content: q.question_text,
        answer_1: q.options[0]?.option_text || "",
        answer_2: q.options[1]?.option_text || "",
        answer_3: q.options[2]?.option_text || "",
        answer_4: q.options[3]?.option_text || "",
        isCorrect: correctIdx !== -1 ? correctIdx + 1 : 1,
        explanation: q.explanation || "",
      };
    });

    const updatedContentJson = {
      ...(artifact.content_json || {}),
      quiz: formattedQuiz,
    };

    updateArtifact({
      artifactId: artifact.id,
      payload: { content_json: updatedContentJson },
    });
  };

  // Test mode handlers
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

  if (questions.length === 0 && viewMode === "list") {
    return (
      <div className="flex-1 flex flex-col items-center justify-center p-12 bg-white space-y-4">
        <HelpCircle size={48} className="text-slate-300 animate-bounce" />
        <Title level={5} className="text-slate-500">
          Chưa có câu hỏi trắc nghiệm nào trong bài học này.
        </Title>
        <Button
          type="primary"
          icon={<Plus size={16} />}
          onClick={handleAddQuestion}
          className="bg-indigo-600 font-semibold"
        >
          Tạo câu hỏi đầu tiên
        </Button>
      </div>
    );
  }

  const score = calculateScore();
  const scorePercent =
    questions.length > 0 ? Math.round((score / questions.length) * 100) : 0;

  return (
    <div className="flex-1 flex flex-col min-h-0 bg-slate-100 overflow-hidden">
      {/* Sub Header Action Bar */}
      <div className="bg-white border-b border-slate-200 px-6 py-3 flex items-center justify-between shadow-sm shrink-0">
        <div className="flex items-center gap-2">
          <HelpCircle size={20} className="text-indigo-600" />
          <span className="font-bold text-slate-800 text-base">
            {viewMode === "list"
              ? `Danh Sách Câu Hỏi Trắc Nghiệm (${questions.length} câu)`
              : `Làm Bài Test Trắc Nghiệm (Thử nghiệm)`}
          </span>
        </div>

        <div className="flex items-center gap-2">
          {viewMode === "list" ? (
            <>
              <Button
                type="primary"
                icon={<Save size={16} />}
                loading={isUpdating}
                onClick={handleSaveToDb}
                className="bg-emerald-600 hover:bg-emerald-700 font-bold"
              >
                Lưu
              </Button>
              <Button
                icon={<Plus size={16} />}
                onClick={handleAddQuestion}
                className="font-semibold"
              >
                Thêm câu hỏi
              </Button>
              <Button
                type="default"
                icon={<Play size={16} />}
                onClick={() => {
                  handleResetQuiz();
                  setViewMode("test");
                }}
                className="bg-indigo-50 text-indigo-700 border-indigo-200 hover:bg-indigo-100 font-bold"
              >
                Làm bài Test thử
              </Button>
            </>
          ) : (
            <Button
              icon={<Edit3 size={16} />}
              onClick={() => setViewMode("list")}
              className="font-semibold"
            >
              Quay lại Biên tập
            </Button>
          )}
        </div>
      </div>

      {/* Main Container */}
      {viewMode === "list" ? (
        /* ──────────────────────────────────────────────────────────
           LIST VIEW MODE: Render All Questions with Inline Editing
           ────────────────────────────────────────────────────────── */
        <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6 max-w-4xl mx-auto w-full">
          {questions.map((q, qIdx) => (
            <Card
              key={qIdx}
              className="shadow-sm border-slate-200 rounded-xl overflow-hidden"
              title={
                <div className="flex items-center justify-between w-full">
                  <span className="font-bold text-indigo-700 text-sm">
                    Câu {qIdx + 1}:
                  </span>
                  <Popconfirm
                    title="Xóa câu hỏi này?"
                    onConfirm={() => handleDeleteQuestion(qIdx)}
                    okText="Xóa"
                    cancelText="Hủy"
                    okButtonProps={{ danger: true }}
                  >
                    <Button
                      danger
                      type="text"
                      size="small"
                      icon={<Trash2 size={16} />}
                    />
                  </Popconfirm>
                </div>
              }
            >
              <div className="space-y-4">
                {/* Question Content Field */}
                <div>
                  <div className="text-xs font-semibold text-slate-400 mb-1">
                    Nội dung câu hỏi (Click để sửa text):
                  </div>
                  {editingField?.qIdx === qIdx &&
                  editingField?.field === "question" ? (
                    <Input.TextArea
                      autoFocus
                      rows={2}
                      value={q.question_text}
                      onChange={(e) =>
                        handleUpdateQuestionText(qIdx, e.target.value)
                      }
                      onBlur={() => setEditingField(null)}
                      className="font-bold text-slate-800 text-sm md:text-base border-indigo-400"
                    />
                  ) : (
                    <div
                      onClick={() =>
                        setEditingField({ qIdx, field: "question" })
                      }
                      className="font-bold text-slate-800 text-sm md:text-base p-3 bg-slate-50 border border-slate-200 rounded-lg cursor-pointer hover:border-indigo-400 hover:bg-indigo-50/30 transition-all flex items-center justify-between group"
                    >
                      <span className="flex-1">
                        {q.question_text || "Nhấp vào đây để nhập câu hỏi..."}
                      </span>
                      <Edit3
                        size={14}
                        className="text-slate-400 opacity-0 group-hover:opacity-100 transition-opacity ml-2 shrink-0"
                      />
                    </div>
                  )}
                </div>

                {/* Options List Field */}
                <div>
                  <div className="text-xs font-semibold text-slate-400 mb-2">
                    Các đáp án lựa chọn (Tích chọn Radio cho Đáp án ĐÚNG - Click
                    text để sửa):
                  </div>
                  <div className="space-y-2">
                    {q.options.map((opt, oIdx) => {
                      const optionLetters = ["A", "B", "C", "D"];
                      const letter = optionLetters[oIdx] || `${oIdx + 1}`;
                      const isEditingOption =
                        editingField?.qIdx === qIdx &&
                        editingField?.field === oIdx;

                      return (
                        <div
                          key={oIdx}
                          className={`flex items-center gap-3 p-2.5 rounded-lg border transition-all ${
                            opt.is_correct
                              ? "bg-emerald-50/50 border-emerald-300"
                              : "bg-white border-slate-200"
                          }`}
                        >
                          <Radio
                            checked={opt.is_correct}
                            onChange={() => handleSetCorrectOption(qIdx, oIdx)}
                          />
                          <span
                            className={`font-bold text-xs md:text-sm ${
                              opt.is_correct
                                ? "text-emerald-700"
                                : "text-slate-500"
                            }`}
                          >
                            {letter}.
                          </span>

                          {isEditingOption ? (
                            <Input
                              autoFocus
                              value={opt.option_text}
                              onChange={(e) =>
                                handleUpdateOptionText(
                                  qIdx,
                                  oIdx,
                                  e.target.value,
                                )
                              }
                              onBlur={() => setEditingField(null)}
                              className="flex-1 text-xs md:text-sm font-medium border-indigo-400"
                            />
                          ) : (
                            <div
                              onClick={() =>
                                setEditingField({ qIdx, field: oIdx })
                              }
                              className="flex-1 text-xs md:text-sm font-medium text-slate-700 cursor-pointer hover:text-indigo-600 flex items-center justify-between group"
                            >
                              <span>
                                {opt.option_text ||
                                  "Nhấp vào đây để nhập đáp án..."}
                              </span>
                              <Edit3
                                size={12}
                                className="text-slate-400 opacity-0 group-hover:opacity-100 transition-opacity ml-1 shrink-0"
                              />
                            </div>
                          )}

                          {opt.is_correct && (
                            <Tag color="success" className="font-bold">
                              Đáp án đúng
                            </Tag>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Explanation Field */}
                <div>
                  <div className="text-xs font-bold text-slate-700 flex items-center gap-1.5 mb-1.5">
                    <HelpCircle size={14} className="text-indigo-600" />
                    <span>Giải thích chi tiết đáp án</span>
                    <span className="text-[11px] font-normal text-slate-400">
                      (Click để sửa text)
                    </span>
                  </div>
                  {editingField?.qIdx === qIdx &&
                  editingField?.field === "explanation" ? (
                    <Input.TextArea
                      autoFocus
                      rows={2}
                      value={q.explanation}
                      onChange={(e) =>
                        handleUpdateExplanation(qIdx, e.target.value)
                      }
                      onBlur={() => setEditingField(null)}
                      className="text-xs md:text-sm text-indigo-950 font-medium border-indigo-400 rounded-xl p-3 bg-white"
                      placeholder="Nhập nội dung giải thích chi tiết..."
                    />
                  ) : (
                    <div
                      onClick={() =>
                        setEditingField({ qIdx, field: "explanation" })
                      }
                      className="p-3 bg-indigo-50/60 border border-indigo-100 rounded-xl cursor-pointer hover:border-indigo-300 hover:bg-indigo-50 transition-all flex items-start justify-between group"
                    >
                      <span className="text-xs md:text-sm text-indigo-950 font-medium leading-relaxed flex-1">
                        {q.explanation ||
                          "Nhấp vào đây để bổ sung giải thích chi tiết cho đáp án..."}
                      </span>
                      <Edit3
                        size={14}
                        className="text-indigo-400 opacity-0 group-hover:opacity-100 transition-opacity ml-2 mt-0.5 shrink-0"
                      />
                    </div>
                  )}
                </div>
              </div>
            </Card>
          ))}

          <div className="text-center pt-4 pb-8">
            <Button
              type="primary"
              size="large"
              icon={<Save size={18} />}
              loading={isUpdating}
              onClick={handleSaveToDb}
              className="bg-emerald-600 hover:bg-emerald-700 font-bold px-8"
            >
              Lưu tất cả thay đổi vào Database
            </Button>
          </div>
        </div>
      ) : (
        /* ──────────────────────────────────────────────────────────
           TEST MODE: Interactive Quiz Player View
           ────────────────────────────────────────────────────────── */
        <div className="flex-1 flex flex-col md:flex-row min-h-0 overflow-hidden">
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
                            Object.keys(selectedAnswers).length <
                            questions.length
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
                      {activeQuestion?.question_text}
                    </Title>

                    <div className="space-y-3">
                      {activeQuestion?.options.map((opt, i) => {
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
                              className={`text-xs md:text-sm font-semibold ${
                                isSelected
                                  ? "text-indigo-800 font-bold"
                                  : "text-slate-700"
                              }`}
                            >
                              {opt.option_text}
                            </span>
                            <div
                              className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${
                                isSelected
                                  ? "border-indigo-600 bg-indigo-600"
                                  : "border-slate-300"
                              }`}
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
                          <CheckCircle2
                            size={24}
                            className="text-emerald-500"
                          />
                        ) : (
                          <AlertCircle size={24} className="text-amber-500" />
                        )}
                        <Title
                          level={3}
                          className="text-slate-800 font-bold m-0"
                        >
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

                  {showExplanation && (
                    <div className="text-left mt-8 space-y-6 border-t border-slate-100 pt-6">
                      <Title level={4} className="text-slate-700">
                        Đánh giá từng câu hỏi
                      </Title>
                      {questions.map((q, idx) => {
                        const selected = selectedAnswers[idx];
                        const isCorrect =
                          selected !== undefined &&
                          q.options[selected]?.is_correct;
                        return (
                          <Card
                            key={idx}
                            size="small"
                            className={`border-l-4 ${
                              isCorrect
                                ? "border-l-emerald-500 bg-emerald-50/10"
                                : "border-l-rose-500 bg-rose-50/10"
                            }`}
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
                                    <XCircle
                                      size={16}
                                      className="text-rose-500"
                                    />
                                  ) : (
                                    <div className="w-4 h-4 rounded-full border border-slate-300" />
                                  )}
                                  <span
                                    className={`${
                                      opt.is_correct
                                        ? "text-emerald-700 font-bold"
                                        : selected === oIdx
                                          ? "text-rose-700 font-bold"
                                          : "text-slate-600"
                                    }`}
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
          </div>
        </div>
      )}
    </div>
  );
}

// ──────────────────────────────────────────────────────────
// 4. Video Viewer Component
// ──────────────────────────────────────────────────────────
function VideoViewer({
  artifact,
  lesson,
}: {
  artifact: ArtifactResponse | undefined;
  lesson: LessonResponse;
}) {
  const { mutate: createArtifact, isPending: isCreating } = useCreateArtifact();

  const handleCreateVideo = () => {
    createArtifact({
      lesson_id: lesson.id,
      type: "video",
      status: "Pending",
    });
  };

  // State 1: Chưa có video
  if (!artifact || artifact.status === "None") {
    return (
      <div className="flex-1 flex items-center justify-center p-8 bg-slate-100 min-h-0">
        <Card className="max-w-xl w-full text-center p-8 shadow-sm border-slate-200 rounded-2xl space-y-6">
          <div className="w-20 h-20 mx-auto rounded-full bg-slate-100 border border-slate-200 flex items-center justify-center">
            <VideoOff size={40} className="text-slate-400" />
          </div>
          <div className="space-y-2">
            <Tag color="warning" className="font-bold">
              Chưa có Video
            </Tag>
            <Title level={4} className="text-slate-800 font-bold m-0">
              Bài học này chưa có video bài giảng
            </Title>
            <Paragraph className="text-slate-500 text-sm">
              Bạn chưa khởi tạo video bài giảng cho bài học{" "}
              <strong className="text-slate-700">{lesson.name}</strong>. Nhấn
              vào nút bên dưới để bắt đầu khởi tạo ngay.
            </Paragraph>
          </div>
          <Button
            type="primary"
            size="large"
            icon={<Video size={18} />}
            loading={isCreating}
            onClick={handleCreateVideo}
            className="bg-indigo-600 hover:bg-indigo-700 font-bold px-8 h-11"
          >
            Tạo ngay Video Bài Giảng
          </Button>
        </Card>
      </div>
    );
  }

  // State 2: Đang khởi tạo video
  if (
    artifact.status === "Pending" ||
    artifact.status === "Processing" ||
    artifact.status === "in_progress"
  ) {
    return (
      <div className="flex-1 flex items-center justify-center p-8 bg-slate-100 min-h-0">
        <Card className="max-w-xl w-full text-center p-8 shadow-sm border-slate-200 rounded-2xl space-y-6">
          <div className="w-20 h-20 mx-auto rounded-full bg-indigo-50 border border-indigo-100 flex items-center justify-center">
            <RefreshCw size={36} className="text-indigo-600 animate-spin" />
          </div>
          <div className="space-y-2">
            <Tag color="processing" className="font-bold">
              Đang khởi tạo
            </Tag>
            <Title level={4} className="text-slate-800 font-bold m-0">
              Đang khởi tạo video bài giảng. Vui lòng chờ...
            </Title>
            <Paragraph className="text-slate-500 text-sm max-w-md mx-auto">
              Hệ thống AI đang tổng hợp slide, xử lý giọng đọc và tạo video bài
              học. Tiến trình sẽ tự động cập nhật khi hoàn tất.
            </Paragraph>
          </div>
          <Progress
            percent={65}
            status="active"
            strokeColor={{ "0%": "#6366f1", "100%": "#10b981" }}
            showInfo={false}
          />
        </Card>
      </div>
    );
  }

  // State 3: Video đã tạo thành công
  const videoUrl = artifact.content || artifact.content_json?.video_url;

  return (
    <div className="flex-1 flex flex-col min-h-0 bg-slate-900 overflow-hidden">
      <div className="bg-slate-950 px-6 py-3 border-b border-slate-800 flex items-center justify-between shrink-0">
        <div className="flex items-center gap-2">
          <PlayCircle size={20} className="text-indigo-400" />
          <span className="font-bold text-slate-200 text-sm md:text-base">
            Video Bài Giảng: {lesson.name} - {lesson.title}
          </span>
        </div>
        <Tag color="success" className="font-bold">
          Sẵn sàng phát
        </Tag>
      </div>

      <div className="flex-1 flex items-center justify-center p-4 md:p-6 overflow-hidden">
        {videoUrl ? (
          <video
            controls
            src={videoUrl}
            className="w-full max-w-5xl max-h-[75vh] rounded-2xl shadow-2xl bg-black border border-slate-800 outline-none"
          >
            Trình duyệt của bạn không hỗ trợ phát video HTML5.
          </video>
        ) : (
          <div className="text-slate-400 font-medium">
            URL video chưa sẵn sàng hoặc đang cập nhật.
          </div>
        )}
      </div>
    </div>
  );
}

// ──────────────────────────────────────────────────────────
// 5. Video Quiz Viewer Component (Popup Questions)
// ──────────────────────────────────────────────────────────
interface VideoQuizItem {
  id?: string | number;
  timestamp: string;
  question_text: string;
  options: { option_text: string; is_correct: boolean }[];
  explanation?: string;
}

interface RawPopupQuizOption {
  option_text?: string;
  is_correct?: boolean;
}

interface RawPopupQuizItem {
  timestamp?: string;
  question_text?: string;
  question_content?: string;
  options?: (string | RawPopupQuizOption)[];
  answer_1?: string;
  answer_2?: string;
  answer_3?: string;
  answer_4?: string;
  isCorrect?: number;
  explanation?: string;
}

function VideoQuizViewer({
  artifact,
  lesson,
}: {
  artifact: ArtifactResponse | undefined;
  lesson: LessonResponse;
}) {
  const [quizzes, setQuizzes] = useState<VideoQuizItem[]>([]);
  const [editingField, setEditingField] = useState<{
    qIdx: number;
    field: "timestamp" | "question" | "explanation" | number;
  } | null>(null);

  const { mutate: updateArtifact, isPending: isUpdating } = useUpdateArtifact();
  const { mutate: createArtifact, isPending: isCreating } = useCreateArtifact();

  useEffect(() => {
    if (!artifact?.content_json) return;
    const raw = artifact.content_json;
    let list: VideoQuizItem[] = [];

    if (raw.popup_quizzes && Array.isArray(raw.popup_quizzes)) {
      list = raw.popup_quizzes.map((q: RawPopupQuizItem) => ({
        timestamp: q.timestamp || "01:00",
        question_text: q.question_text || q.question_content || "",
        options: Array.isArray(q.options)
          ? q.options.map((opt: string | RawPopupQuizOption) => ({
              option_text:
                typeof opt === "string" ? opt : opt.option_text || "",
              is_correct: typeof opt === "string" ? false : !!opt.is_correct,
            }))
          : [
              {
                option_text: q.answer_1 || "Đáp án A",
                is_correct: q.isCorrect === 1,
              },
              {
                option_text: q.answer_2 || "Đáp án B",
                is_correct: q.isCorrect === 2,
              },
              {
                option_text: q.answer_3 || "Đáp án C",
                is_correct: q.isCorrect === 3,
              },
              {
                option_text: q.answer_4 || "Đáp án D",
                is_correct: q.isCorrect === 4,
              },
            ],
        explanation: q.explanation || "",
      }));
    } else if (raw.video_quizzes && Array.isArray(raw.video_quizzes)) {
      list = raw.video_quizzes;
    }

    setQuizzes(list);
  }, [artifact]);

  const handleCreateVideoQuizArtifact = () => {
    const defaultInitialQuizzes: VideoQuizItem[] = [
      {
        timestamp: "01:30",
        question_text:
          "Theo video vừa xem, kiến thức trọng tâm bài học này là gì?",
        options: [
          {
            option_text: "Phương án đúng theo nội dung bài học",
            is_correct: true,
          },
          { option_text: "Phương án gây nhiễu A", is_correct: false },
          { option_text: "Phương án gây nhiễu B", is_correct: false },
          { option_text: "Phương án gây nhiễu C", is_correct: false },
        ],
        explanation: "Giải thích đáp án tại mốc 01:30...",
      },
    ];

    createArtifact({
      lesson_id: lesson.id,
      type: "video_quiz",
      content_json: { popup_quizzes: defaultInitialQuizzes },
      status: "Completed",
    });
  };

  const handleUpdateTimestamp = (qIdx: number, val: string) => {
    setQuizzes((prev) => {
      const next = [...prev];
      next[qIdx] = { ...next[qIdx], timestamp: val };
      return next;
    });
  };

  const handleUpdateQuestion = (qIdx: number, text: string) => {
    setQuizzes((prev) => {
      const next = [...prev];
      next[qIdx] = { ...next[qIdx], question_text: text };
      return next;
    });
  };

  const handleUpdateOptionText = (qIdx: number, oIdx: number, text: string) => {
    setQuizzes((prev) => {
      const next = [...prev];
      const opts = [...next[qIdx].options];
      opts[oIdx] = { ...opts[oIdx], option_text: text };
      next[qIdx] = { ...next[qIdx], options: opts };
      return next;
    });
  };

  const handleSetCorrectOption = (qIdx: number, correctOIdx: number) => {
    setQuizzes((prev) => {
      const next = [...prev];
      const opts = next[qIdx].options.map((opt, idx) => ({
        ...opt,
        is_correct: idx === correctOIdx,
      }));
      next[qIdx] = { ...next[qIdx], options: opts };
      return next;
    });
  };

  const handleUpdateExplanation = (qIdx: number, text: string) => {
    setQuizzes((prev) => {
      const next = [...prev];
      next[qIdx] = { ...next[qIdx], explanation: text };
      return next;
    });
  };

  const handleAddPopupQuestion = () => {
    const newItem: VideoQuizItem = {
      timestamp: "02:00",
      question_text: "Nhập câu hỏi Popup tại mốc thời gian...",
      options: [
        { option_text: "Phương án A", is_correct: true },
        { option_text: "Phương án B", is_correct: false },
        { option_text: "Phương án C", is_correct: false },
        { option_text: "Phương án D", is_correct: false },
      ],
      explanation: "Giải thích đáp án...",
    };
    setQuizzes((prev) => [...prev, newItem]);
  };

  const handleDeletePopupQuestion = (qIdx: number) => {
    setQuizzes((prev) => prev.filter((_, idx) => idx !== qIdx));
  };

  const handleSaveToDb = () => {
    if (!artifact) return;
    updateArtifact({
      artifactId: artifact.id,
      payload: {
        content_json: {
          ...(artifact.content_json || {}),
          popup_quizzes: quizzes,
        },
      },
    });
  };

  if (!artifact) {
    return (
      <div className="flex-1 flex items-center justify-center p-8 bg-slate-100 min-h-0">
        <Card className="max-w-xl w-full text-center p-8 shadow-sm border-slate-200 rounded-2xl space-y-6">
          <div className="w-20 h-20 mx-auto rounded-full bg-slate-100 border border-slate-200 flex items-center justify-center">
            <Clock size={40} className="text-slate-400" />
          </div>
          <div className="space-y-2">
            <Title level={4} className="text-slate-800 font-bold m-0">
              Chưa có danh sách Câu hỏi Popup Video
            </Title>
            <Paragraph className="text-slate-500 text-sm">
              Câu hỏi Popup sẽ tự động hiển thị ngắt ngang video tại mốc thời
              gian bạn thiết lập để kiểm tra sinh viên có thực sự xem video hay
              không.
            </Paragraph>
          </div>
          <Button
            type="primary"
            size="large"
            icon={<Plus size={18} />}
            loading={isCreating}
            onClick={handleCreateVideoQuizArtifact}
            className="bg-indigo-600 hover:bg-indigo-700 font-bold px-8 h-11"
          >
            Tạo Danh Sách Câu Hỏi Popup
          </Button>
        </Card>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col min-h-0 bg-slate-100 overflow-hidden">
      {/* Sub Header Action Bar */}
      <div className="bg-white border-b border-slate-200 px-6 py-3 flex items-center justify-between shadow-sm shrink-0">
        <div className="flex items-center gap-2">
          <Clock size={20} className="text-indigo-600" />
          <span className="font-bold text-slate-800 text-base">
            Danh Sách Câu Hỏi Popup Theo Mốc Thời Gian Video ({quizzes.length}{" "}
            câu)
          </span>
        </div>

        <div className="flex items-center gap-2">
          <Button
            type="primary"
            icon={<Save size={16} />}
            loading={isUpdating}
            onClick={handleSaveToDb}
            className="bg-emerald-600 hover:bg-emerald-700 font-bold"
          >
            Lưu vào Database
          </Button>
          <Button
            icon={<Plus size={16} />}
            onClick={handleAddPopupQuestion}
            className="font-semibold"
          >
            Thêm câu hỏi Popup
          </Button>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6 max-w-4xl mx-auto w-full">
        {quizzes.map((q, qIdx) => (
          <Card
            key={qIdx}
            className="shadow-sm border-slate-200 rounded-xl overflow-hidden mt-4!"
            title={
              <div className="flex items-center justify-between w-full gap-3">
                <div className="flex items-center gap-2 flex-1 min-w-0">
                  <span className="font-bold text-indigo-700 text-sm shrink-0">
                    Câu hỏi {qIdx + 1}:
                  </span>
                  {/* Question Text 100% remaining space */}
                  <div className="flex-1 min-w-0">
                    {editingField?.qIdx === qIdx &&
                    editingField?.field === "question" ? (
                      <Input
                        autoFocus
                        value={q.question_text}
                        onChange={(e) =>
                          handleUpdateQuestion(qIdx, e.target.value)
                        }
                        onBlur={() => setEditingField(null)}
                        className="w-full font-bold text-slate-800 text-sm border-indigo-400"
                      />
                    ) : (
                      <div
                        onClick={() =>
                          setEditingField({ qIdx, field: "question" })
                        }
                        className="font-bold text-slate-800 text-sm rounded-lg cursor-pointer hover:border-indigo-400 hover:bg-indigo-50/30 transition-all flex items-center justify-between group px-2 py-1 w-full"
                      >
                        <span className="flex-1 truncate">
                          {q.question_text || "Nhấp vào đây để nhập câu hỏi..."}
                        </span>
                        <Edit3
                          size={14}
                          className="text-slate-400 opacity-0 group-hover:opacity-100 transition-opacity ml-2 shrink-0"
                        />
                      </div>
                    )}
                  </div>
                </div>
                <Popconfirm
                  title="Xóa câu hỏi popup này?"
                  onConfirm={() => handleDeletePopupQuestion(qIdx)}
                  okText="Xóa"
                  cancelText="Hủy"
                  okButtonProps={{ danger: true }}
                >
                  <Button
                    danger
                    type="text"
                    size="small"
                    icon={<Trash2 size={16} />}
                  />
                </Popconfirm>
              </div>
            }
          >
            <div className="space-y-4">
              {/* Timestamp Field */}
              <div className="flex items-center gap-3 p-3 bg-slate-50 border border-slate-200 rounded-lg">
                <span className="text-xs font-bold text-slate-600 shrink-0 flex items-center gap-1.5">
                  <Clock size={14} className="text-indigo-600" /> Thời gian show
                  Popup (phút:giây):
                </span>
                {editingField?.qIdx === qIdx &&
                editingField?.field === "timestamp" ? (
                  <Input
                    autoFocus
                    size="small"
                    value={q.timestamp}
                    onChange={(e) =>
                      handleUpdateTimestamp(qIdx, e.target.value)
                    }
                    onBlur={() => setEditingField(null)}
                    className="w-32 font-mono font-bold text-indigo-700 border-indigo-400"
                    placeholder="01:30"
                  />
                ) : (
                  <div
                    onClick={() =>
                      setEditingField({ qIdx, field: "timestamp" })
                    }
                    className="font-mono font-extrabold text-indigo-700 text-sm bg-white px-3 py-1 border border-slate-200 rounded cursor-pointer hover:border-indigo-400 transition-all flex items-center gap-2 group"
                  >
                    <span>{q.timestamp || "00:00"}</span>
                    <Edit3
                      size={12}
                      className="text-slate-400 opacity-0 group-hover:opacity-100"
                    />
                  </div>
                )}
              </div>

              {/* Options */}
              <div>
                <div className="space-y-2">
                  {q.options.map((opt, oIdx) => {
                    const letter = ["A", "B", "C", "D"][oIdx] || `${oIdx + 1}`;
                    const isEditingOpt =
                      editingField?.qIdx === qIdx &&
                      editingField?.field === oIdx;

                    return (
                      <div
                        key={oIdx}
                        className={`flex items-center gap-3 p-2.5 rounded-lg border transition-all ${
                          opt.is_correct
                            ? "bg-emerald-50/50 border-emerald-300"
                            : "bg-white border-slate-200"
                        }`}
                      >
                        <Radio
                          checked={opt.is_correct}
                          onChange={() => handleSetCorrectOption(qIdx, oIdx)}
                        />
                        <span
                          className={`font-bold text-xs md:text-sm ${
                            opt.is_correct
                              ? "text-emerald-700"
                              : "text-slate-500"
                          }`}
                        >
                          {letter}.
                        </span>

                        {isEditingOpt ? (
                          <Input
                            autoFocus
                            value={opt.option_text}
                            onChange={(e) =>
                              handleUpdateOptionText(qIdx, oIdx, e.target.value)
                            }
                            onBlur={() => setEditingField(null)}
                            className="flex-1 text-xs md:text-sm font-medium border-indigo-400"
                          />
                        ) : (
                          <div
                            onClick={() =>
                              setEditingField({ qIdx, field: oIdx })
                            }
                            className="flex-1 text-xs md:text-sm font-medium text-slate-700 cursor-pointer hover:text-indigo-600 flex items-center justify-between group"
                          >
                            <span>
                              {opt.option_text || "Nhấp để nhập đáp án..."}
                            </span>
                            <Edit3
                              size={12}
                              className="text-slate-400 opacity-0 group-hover:opacity-100 transition-opacity ml-1 shrink-0"
                            />
                          </div>
                        )}

                        {opt.is_correct && (
                          <Tag color="success" className="font-bold">
                            Đáp án đúng
                          </Tag>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Explanation */}
              <div>
                <div className="text-xs font-bold text-slate-700 flex items-center gap-1.5 mb-1.5">
                  <HelpCircle size={14} className="text-indigo-600" />
                  <span>Giải thích chi tiết đáp án</span>
                  <span className="text-[11px] font-normal text-slate-400">
                    (Click để sửa text)
                  </span>
                </div>
                {editingField?.qIdx === qIdx &&
                editingField?.field === "explanation" ? (
                  <Input.TextArea
                    autoFocus
                    rows={2}
                    value={q.explanation}
                    onChange={(e) =>
                      handleUpdateExplanation(qIdx, e.target.value)
                    }
                    onBlur={() => setEditingField(null)}
                    className="text-xs md:text-sm text-indigo-950 font-medium border-indigo-400 rounded-xl p-3 bg-white"
                    placeholder="Nhập nội dung giải thích chi tiết..."
                  />
                ) : (
                  <div
                    onClick={() =>
                      setEditingField({ qIdx, field: "explanation" })
                    }
                    className="p-3 bg-indigo-50/60 border border-indigo-100 rounded-xl cursor-pointer hover:border-indigo-300 hover:bg-indigo-50 transition-all flex items-start justify-between group"
                  >
                    <span className="text-xs md:text-sm text-indigo-950 font-medium leading-relaxed flex-1">
                      {q.explanation ||
                        "Nhấp vào đây để bổ sung giải thích chi tiết cho đáp án..."}
                    </span>
                    <Edit3
                      size={14}
                      className="text-indigo-400 opacity-0 group-hover:opacity-100 transition-opacity ml-2 mt-0.5 shrink-0"
                    />
                  </div>
                )}
              </div>
            </div>
          </Card>
        ))}

        <div className="text-center pt-4 pb-8">
          <Button
            type="primary"
            size="large"
            icon={<Save size={18} />}
            loading={isUpdating}
            onClick={handleSaveToDb}
            className="bg-emerald-600 hover:bg-emerald-700 font-bold px-8"
          >
            Lưu tất cả thay đổi vào Database
          </Button>
        </div>
      </div>
    </div>
  );
}

// ──────────────────────────────────────────────────────────
// 6. Practical Lab Viewer Component (Text Practice Exercise)
// ──────────────────────────────────────────────────────────
function PracticeLabViewer({
  artifact,
  lesson,
}: {
  artifact: ArtifactResponse | undefined;
  lesson: LessonResponse;
}) {
  const [practiceContent, setPracticeContent] = useState<string>("");
  const [isEditing, setIsEditing] = useState<boolean>(false);
  const { mutate: updateArtifact, isPending: isUpdating } = useUpdateArtifact();

  useEffect(() => {
    if (artifact?.content) {
      setPracticeContent(artifact.content);
    } else if (artifact?.content_json?.practice_text) {
      setPracticeContent(artifact.content_json.practice_text);
    } else {
      const defaultText = `BÀI TẬP THỰC HÀNH TỰ LUYỆN TƯƠNG TỰ
Bài học: ${lesson.name} - ${lesson.title}

1. MỤC TIÊU BÀI TẬP:
- Ôn tập và tự thực hành lại kiến thức đã học trong video bài giảng.
- Vận dụng trực tiếp các cú pháp, hàm và logic bài học vào một bài tập thực tế tương tự.

2. YÊU CẦU CHI TIẾT ĐỀ BÀI:
${lesson.details || "Hãy viết chương trình xử lý bài toán tương tự như bài học trong video, đảm bảo chạy đúng các yêu cầu đầu ra."}

3. HƯỚNG DẪN CÁC BƯỚC THỰC HIỆN:
- Bước 1: Mở môi trường lập trình (IDE / Editor) trên máy tính của bạn.
- Bước 2: Quan sát ví dụ trong bài giảng và tự viết lại bài tập theo yêu cầu trên.
- Bước 3: Kiểm thử kết quả đầu ra và so sánh với Kết quả mong đợi (Expected Outcome).`;
      setPracticeContent(defaultText);
    }
  }, [artifact, lesson]);

  const handleSaveToDb = () => {
    if (!artifact) return;
    updateArtifact({
      artifactId: artifact.id,
      payload: {
        content: practiceContent,
        content_json: {
          ...(artifact.content_json || {}),
          practice_text: practiceContent,
        },
      },
    });
  };

  return (
    <div className="flex-1 flex flex-col min-h-0 bg-slate-100 overflow-hidden">
      {/* Sub Header Action Bar */}
      <div className="bg-white border-b border-slate-200 px-6 py-3 flex items-center justify-between shadow-sm shrink-0">
        <div className="flex items-center gap-2">
          <Terminal size={20} className="text-indigo-600" />
          <span className="font-bold text-slate-800 text-base">
            Đề Bài Thực Hành Luyện Tập ({lesson.name})
          </span>
        </div>

        <div className="flex items-center gap-2">
          {artifact && (
            <Button
              type="primary"
              icon={<Save size={16} />}
              loading={isUpdating}
              onClick={handleSaveToDb}
              className="bg-emerald-600 hover:bg-emerald-700 font-bold"
            >
              Lưu vào Database
            </Button>
          )}
          <Button
            icon={<Edit3 size={16} />}
            onClick={() => setIsEditing(!isEditing)}
            className="font-semibold"
          >
            {isEditing ? "Xem bản xem trước" : "Chỉnh sửa đề bài"}
          </Button>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 overflow-y-auto p-4 md:p-8 max-w-4xl mx-auto w-full">
        <Card className="shadow-sm border-slate-200 rounded-xl p-4 md:p-6 space-y-6">
          <div className="border-b border-slate-100 pb-4">
            <Title level={3} className="m-0 text-slate-800 font-bold">
              {lesson.name}: {lesson.title}
            </Title>
          </div>

          {isEditing ? (
            <div className="space-y-2">
              <div className="text-xs font-semibold text-slate-500">
                Soạn thảo Đề bài Thực hành:
              </div>
              <Input.TextArea
                rows={14}
                value={practiceContent}
                onChange={(e) => setPracticeContent(e.target.value)}
                className="font-mono text-sm border-indigo-300 p-4 rounded-lg"
                placeholder="Nhập nội dung đề bài thực hành..."
              />
            </div>
          ) : (
            <div
              onClick={() => setIsEditing(true)}
              className="cursor-pointer group relative p-4 rounded-xl border border-transparent hover:border-indigo-200 hover:bg-indigo-50/20 transition-all space-y-4"
            >
              <div className="absolute top-3 right-3 text-slate-400 opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-1 text-xs font-semibold bg-indigo-50 px-2.5 py-1 rounded-md border border-indigo-100">
                <Edit3 size={13} /> Click để sửa text
              </div>
              <div className="prose prose-slate max-w-none text-slate-700 text-sm md:text-base leading-relaxed space-y-3 whitespace-pre-wrap font-sans">
                {practiceContent}
              </div>
            </div>
          )}

          <Divider />

          {lesson.expected_output && (
            <Alert
              title={
                <span className="font-bold text-slate-800 text-sm tracking-wider flex items-center gap-1.5">
                  Kết quả mong đợi khi sinh viên làm bài (Expected Outcome):
                </span>
              }
              description={
                <div className="text-slate-700 bg-white p-3 rounded border border-emerald-200 mt-2 font-medium">
                  {lesson.expected_output}
                </div>
              }
              type="success"
              showIcon={false}
              className="bg-emerald-50/60 border-emerald-200 rounded-xl"
            />
          )}
        </Card>
      </div>
    </div>
  );
}
