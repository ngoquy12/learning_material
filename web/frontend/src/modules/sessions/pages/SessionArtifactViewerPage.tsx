import { useEffect, useMemo } from "react";
import { useParams, useNavigate, useSearchParams } from "react-router-dom";
import { Layout, Button, Spin, Empty, Divider, Typography, Collapse } from "antd";
import {
  ArrowLeft,
  BookOpen,
  HelpCircle,
  Network,
  BookOpenCheck,
  RefreshCw,
  FolderLock,
  ListTodo,
} from "lucide-react";
import { useSessions, useSessionArtifacts } from "../hooks/useSessions";
import { ArtifactVersionWrapper, QuizEditor, MarkmapComponent } from "../../lessons/components/ArtifactPreviewModal";
import { ArtifactResponse } from "../../lessons/hooks/useLessons";
import { marked } from "marked";
import DOMPurify from "dompurify";

const { Header, Content } = Layout;
const { Title, Paragraph } = Typography;

interface HomeworkExercise {
  index: number;
  level: string;
  folder_name: string;
  title: string;
  content: string;
  rubric: string;
}

interface ProjectEntryTest {
  title?: string;
  content?: string;
}

export default function SessionArtifactViewerPage() {
  const { courseId, sessionId } = useParams();
  const navigate = useNavigate();
  const parsedCourseId = Number(courseId);
  const parsedSessionId = Number(sessionId);

  const { data: sessions, isLoading: isLoadingSessions } = useSessions(parsedCourseId);
  const { data: artifacts, isLoading: isLoadingArtifacts } = useSessionArtifacts(parsedSessionId);

  const session = useMemo(() => {
    return sessions?.find((s) => s.id === parsedSessionId);
  }, [sessions, parsedSessionId]);

  const [searchParams, setSearchParams] = useSearchParams();
  const activeTab = searchParams.get("tab") || "";

  const setActiveTab = (tab: string) => {
    setSearchParams(
      (prev) => {
        prev.set("tab", tab);
        return prev;
      },
      { replace: true }
    );
  };

  // Determine the list of available tabs dynamically
  const availableTabs = useMemo(() => {
    if (!artifacts || artifacts.length === 0) return [];

    const tabsList: Array<{
      key: string;
      label: string;
      icon: React.ReactNode;
      artifact: ArtifactResponse;
      subType?: "levels" | "comprehensive";
    }> = [];

    // Order: reading -> mindmap -> pre_quiz -> post_quiz -> homework_levels -> homework_comprehensive -> project artifacts
    const sortedTypes = [
      "session_reading",
      "session_mindmap",
      "pre_quiz",
      "post_quiz",
      "session_homework",
      "project_entry_tests",
      "project_srs",
      "project_mini_project",
    ];

    const artifactsMap = artifacts.reduce<Record<string, ArtifactResponse>>((acc, art) => {
      acc[art.type] = art;
      return acc;
    }, {});

    for (const type of sortedTypes) {
      const art = artifactsMap[type];
      if (!art) continue;

      if (type === "session_reading") {
        tabsList.push({
          key: "session_reading",
          label: "Bài đọc tổng hợp",
          icon: <BookOpen size={16} />,
          artifact: art,
        });
      } else if (type === "session_mindmap") {
        tabsList.push({
          key: "session_mindmap",
          label: "Sơ đồ tổng hợp (MD)",
          icon: <Network size={16} />,
          artifact: art,
        });
      } else if (type === "pre_quiz") {
        tabsList.push({
          key: "pre_quiz",
          label: "Quizz đầu giờ",
          icon: <HelpCircle size={16} />,
          artifact: art,
        });
      } else if (type === "post_quiz") {
        tabsList.push({
          key: "post_quiz",
          label: "Quizz cuối giờ",
          icon: <HelpCircle size={16} />,
          artifact: art,
        });
      } else if (type === "session_homework") {
        tabsList.push({
          key: "session_homework_levels",
          label: "Bài tập phân tầng",
          icon: <ListTodo size={16} />,
          artifact: art,
          subType: "levels",
        });
        tabsList.push({
          key: "session_homework_comprehensive",
          label: "Bài tập tổng hợp",
          icon: <ListTodo size={16} />,
          artifact: art,
          subType: "comprehensive",
        });
      } else if (type === "project_entry_tests") {
        tabsList.push({
          key: "project_entry_tests",
          label: "Bài kiểm tra đầu giờ",
          icon: <HelpCircle size={16} />,
          artifact: art,
        });
      } else if (type === "project_srs") {
        tabsList.push({
          key: "project_srs",
          label: "Tài liệu đặc tả SRS",
          icon: <BookOpen size={16} />,
          artifact: art,
        });
      } else if (type === "project_mini_project") {
        tabsList.push({
          key: "project_mini_project",
          label: "Đề bài Mini Project",
          icon: <BookOpenCheck size={16} />,
          artifact: art,
        });
      }
    }

    return tabsList;
  }, [artifacts]);

  // Handle setting default tab when artifacts load
  useEffect(() => {
    if (!searchParams.get("tab") && availableTabs.length > 0) {
      setActiveTab(availableTabs[0].key);
    }
  }, [availableTabs, searchParams]);

  const activeTabItem = useMemo(() => {
    return availableTabs.find((t) => t.key === activeTab) || availableTabs[0] || null;
  }, [availableTabs, activeTab]);

  const renderContent = (artifact: ArtifactResponse, subType?: "levels" | "comprehensive") => {
    if (artifact.status === "Pending") {
      return (
        <div className="flex flex-col justify-center items-center h-[50vh] gap-4 bg-slate-50 rounded-xl border border-dashed border-slate-300">
          <Spin size="large" />
          <div className="text-slate-500 italic font-medium">
            AI Agent đang miệt mài biên dịch nội dung {artifact.type}...
          </div>
        </div>
      );
    }

    if (artifact.status === "Failed") {
      return (
        <div className="flex flex-col justify-center items-center h-[50vh] gap-4 bg-rose-50 rounded-xl border border-dashed border-rose-300 p-6 text-center">
          <FolderLock size={48} className="text-rose-500" />
          <div className="text-rose-600 font-bold text-lg">
            Gặp lỗi trong quá trình tự động sinh phần {artifact.type}.
          </div>
          <div className="text-slate-500 text-sm max-w-md w-full flex flex-col items-center">
            {artifact.content ? (
              <span className="text-rose-600 font-mono text-xs block bg-rose-100/50 p-3 rounded border border-rose-200 mt-2 text-left whitespace-pre-wrap max-h-[25vh] overflow-y-auto w-full max-w-lg">
                Chi tiết lỗi: {artifact.content}
              </span>
            ) : (
              "Vui lòng quay lại danh sách khóa học và bấm \"Tạo AI Session\" để hệ thống tự động sinh lại dữ liệu."
            )}
          </div>
        </div>
      );
    }

    // Mindmap Render
    if (artifact.type === "session_mindmap" && artifact.content) {
      return <MarkmapComponent markmapData={artifact.content} />;
    }

    // Quiz Render
    if ((artifact.type === "pre_quiz" || artifact.type === "post_quiz") && artifact.content_json) {
      return (
        <QuizEditor
          artifact={artifact}
          lessonId={null}
          sessionId={parsedSessionId}
        />
      );
    }

    // Homework / Comprehensive Exercises Render
    if (artifact.type === "session_homework" && artifact.content_json && subType) {
      const allExercises = (artifact.content_json.exercises || []) as HomeworkExercise[];
      const exercises = allExercises.filter((ex) => {
        if (subType === "levels") {
          return ex.index >= 1 && ex.index <= 5;
        } else {
          return ex.index === 6;
        }
      });

      if (exercises.length === 0) {
        return <Empty description="Chưa có dữ liệu bài tập trong cấu trúc JSON." />;
      }

      const collapseItems = exercises.map((ex: HomeworkExercise, i: number) => {
        const htmlContent = DOMPurify.sanitize(marked.parse(ex.content || "") as string);
        const htmlRubric = DOMPurify.sanitize(marked.parse(ex.rubric || "") as string);
        return {
          key: String(i),
          label: (
            <div className="flex justify-between items-center w-full py-1 pr-4">
              <span className="font-bold text-sm md:text-base text-slate-800">
                Bài {ex.index}: {ex.title ? ex.title.replace(/<\/?[^>]+(>|$)/g, "").trim() : ""}
              </span>
              <span className="px-3 py-1 bg-teal-100 text-teal-800 text-xs font-bold rounded-full uppercase tracking-wider">
                {ex.level}
              </span>
            </div>
          ),
          children: (
            <div className="space-y-6">
              <div>
                <div className="font-bold text-slate-700 mb-2 border-l-4 border-teal-500 pl-2.5 text-xs md:text-sm uppercase tracking-wider">
                  Đề bài &amp; Yêu cầu
                </div>
                <div
                  className="markdown-content text-slate-700 bg-slate-50/50 p-5 rounded-xl border border-slate-100 leading-relaxed text-sm"
                  dangerouslySetInnerHTML={{ __html: htmlContent }}
                />
              </div>
              {ex.rubric && (
                <div>
                  <div className="font-bold text-slate-700 mb-2 border-l-4 border-amber-500 pl-2.5 text-xs md:text-sm uppercase tracking-wider">
                    Tiêu chí chấm điểm (Rubric AI)
                  </div>
                  <div
                    className="markdown-content text-slate-600 bg-amber-50/10 p-5 rounded-xl border border-amber-100/60 leading-relaxed text-sm"
                    dangerouslySetInnerHTML={{ __html: htmlRubric }}
                  />
                </div>
              )}
            </div>
          ),
        };
      });

      return (
        <div className="space-y-6 max-w-5xl mx-auto pb-12">
          <div className="bg-gradient-to-r from-teal-50 to-indigo-50/30 p-4 rounded-xl border border-teal-100/80 mb-2">
            <h3 className="text-lg font-bold text-teal-900 mb-1">
              {subType === "levels" ? "Danh sách bài tập tự luận phân tầng" : "Bài tập tổng hợp cuối buổi"}
            </h3>
            <p className="text-xs text-teal-700/90 m-0">
              {subType === "levels"
                ? "Tổng hợp các bài tập tự luận nâng cao năng lực lập trình từ Vận dụng cơ bản, Vận dụng chuyên sâu, Phân tích cho đến Sáng tạo."
                : "Bài tập tích hợp tổng hợp kiến thức toàn bộ buổi học giúp hệ thống hóa kỹ năng lập trình thực tế."}
            </p>
          </div>
          <Collapse
            defaultActiveKey={["0"]}
            expandIconPosition="start"
            className="bg-white border-teal-100/60 shadow-sm rounded-xl overflow-hidden"
            items={collapseItems}
          />
        </div>
      );
    }

    if (
      (artifact.type === "project_srs" ||
        artifact.type === "project_mini_project") &&
      artifact.content
    ) {
      let markdown = artifact.content.trim();
      if (markdown.startsWith("```")) {
        markdown = markdown.replace(/^```[a-zA-Z]*\r?\n/, "");
        markdown = markdown.replace(/\r?\n```$/, "");
        markdown = markdown.trim();
      }

      const rawHtml = DOMPurify.sanitize(marked.parse(markdown) as string);

      let htmlRubric = "";
      if (artifact.type === "project_mini_project" && artifact.content_json?.rubric) {
        let rubricMd = artifact.content_json.rubric.trim();
        if (rubricMd.startsWith("```")) {
          rubricMd = rubricMd.replace(/^```[a-zA-Z]*\r?\n/, "");
          rubricMd = rubricMd.replace(/\r?\n```$/, "");
          rubricMd = rubricMd.trim();
        }
        htmlRubric = DOMPurify.sanitize(marked.parse(rubricMd) as string);
      }

      return (
        <div className="max-w-5xl mx-auto space-y-6 pb-12">
          <div
            className="markdown-content text-slate-700 bg-white leading-relaxed text-sm"
            dangerouslySetInnerHTML={{ __html: rawHtml }}
          />
          {htmlRubric && (
            <div>
              <div className="font-bold text-slate-700 mb-2 border-l-4 border-green-500 pl-2.5 text-xs md:text-sm uppercase tracking-wider">
                Tiêu chí chấm điểm (AI)
              </div>
              <div
                className="markdown-content text-slate-600 bg-green-50/10 p-5 rounded-xl border border-green-100 leading-relaxed text-sm"
                dangerouslySetInnerHTML={{ __html: htmlRubric }}
              />
            </div>
          )}
        </div>
      );
    }

    if (artifact.type === "project_entry_tests" && artifact.content_json?.entry_tests) {
      const allTests = (artifact.content_json.entry_tests || []) as ProjectEntryTest[];
      const collapseItems = allTests.map((test: ProjectEntryTest, idx: number) => {
        const htmlContent = DOMPurify.sanitize(marked.parse(test.content || "") as string);
        return {
          key: String(idx),
          label: (
            <div className="flex justify-between items-center w-full py-1 pr-4">
              <span className="font-bold text-sm md:text-base text-slate-800">
                Đề kiểm tra {idx + 1}: {test.title || `Bài kiểm tra đầu giờ ${idx + 1}`}
              </span>
            </div>
          ),
          children: (
            <div className="space-y-4">
              <div className="font-bold text-slate-700 mb-2 border-l-4 border-amber-500 pl-2.5 text-xs md:text-sm uppercase tracking-wider">
                Nội dung câu hỏi
              </div>
              <div
                className="markdown-content text-slate-700 bg-slate-50/50 p-5 rounded-xl border border-slate-100 leading-relaxed text-sm"
                dangerouslySetInnerHTML={{ __html: htmlContent }}
              />
            </div>
          ),
        };
      });

      return (
        <div className="space-y-6 max-w-5xl mx-auto pb-12">
          <div className="bg-gradient-to-r from-amber-50 to-orange-50/30 p-4 rounded-xl border border-amber-100/80 mb-2">
            <h3 className="text-lg font-bold text-amber-900 mb-1">
              Danh sách bài kiểm tra đầu giờ (Entry Tests)
            </h3>
            <p className="text-xs text-amber-700/90 m-0">
              Đề kiểm tra trắc nghiệm/tự luận ngắn đầu giờ của Mini Project giúp đánh giá kiến thức nền tảng của học viên.
            </p>
          </div>
          <Collapse
            defaultActiveKey={["0"]}
            expandIconPosition="start"
            className="bg-white border-amber-100/60 shadow-sm rounded-xl overflow-hidden"
            items={collapseItems}
          />
        </div>
      );
    }

    // Default Render: session_reading HTML
    return (
      <div className="bg-white border border-slate-200 rounded-xl h-[70vh] shadow-inner overflow-hidden">
        <iframe
          srcDoc={artifact.content ?? undefined}
          className="w-full h-full border-0"
          sandbox="allow-same-origin allow-scripts"
        />
      </div>
    );
  };

  if (isLoadingSessions || isLoadingArtifacts) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="text-center space-y-4">
          <Spin size="large" />
          <div className="text-slate-500 font-semibold text-sm">
            Đang tải tài nguyên học tập cấp Session...
          </div>
        </div>
      </div>
    );
  }

  if (!session) {
    return (
      <div className="p-8 text-center bg-slate-50 min-h-screen flex flex-col justify-center items-center">
        <Title level={4} className="text-slate-800">Không tìm thấy Session</Title>
        <Paragraph className="text-slate-500">Mã phiên học không hợp lệ hoặc dữ liệu không tồn tại.</Paragraph>
        <Button
          icon={<ArrowLeft size={16} />}
          onClick={() => navigate(`/courses/${courseId}`)}
          type="primary"
          className="bg-teal-600 border-teal-600 hover:bg-teal-700"
        >
          Quay lại môn học
        </Button>
      </div>
    );
  }

  return (
    <Layout className="min-h-[calc(100vh-112px)] bg-slate-50 rounded-xl overflow-hidden border border-slate-200">
      {/* Dynamic Header */}
      <Header className="bg-white px-5 flex items-center justify-between border-b border-slate-200 h-16" style={{ background: "#fff", padding: "0 20px" }}>
        <div className="flex items-center gap-3 overflow-hidden">
          <Button
            type="text"
            icon={<ArrowLeft size={18} className="text-slate-600" />}
            onClick={() => navigate(`/courses/${courseId}`)}
            className="hover:bg-slate-100 flex items-center justify-center"
          />
          <Divider type="vertical" className="h-6 border-slate-200" />
          <div className="truncate flex flex-col justify-center" style={{ lineHeight: "normal" }}>
            <span className="text-xs font-bold text-teal-600 bg-teal-50 px-2 py-0.5 rounded font-mono w-max block mb-2">
              {session.name}
            </span>
            <Title
              level={5}
              className="m-0 mt-1 truncate text-slate-800 text-sm font-bold block"
              style={{ lineHeight: "1.3", margin: 0 }}
            >
              {session.title}
            </Title>
          </div>
        </div>

        {/* Dynamic tabs list */}
        <div className="flex items-center gap-1.5 overflow-x-auto max-w-[50%] md:max-w-[70%]">
          {availableTabs.map((tab) => (
            <Button
              key={tab.key}
              type={activeTab === tab.key ? "primary" : "text"}
              icon={tab.icon}
              className={`font-semibold rounded-lg text-xs md:text-sm px-3.5 py-2 h-auto flex items-center gap-1.5 transition-all ${
                activeTab === tab.key
                  ? "bg-teal-600 hover:bg-teal-700 text-white shadow-sm"
                  : "text-slate-600 hover:bg-slate-100"
              }`}
              onClick={() => setActiveTab(tab.key)}
            >
              {tab.label}
            </Button>
          ))}
        </div>
      </Header>

      <Content className="p-4 md:p-6 bg-slate-50 overflow-y-auto">
        {availableTabs.length === 0 ? (
          <div className="p-12 text-center flex flex-col items-center justify-center h-full bg-white rounded-xl border">
            <BookOpenCheck
              size={64}
              className="text-slate-300 mb-4 animate-pulse"
            />
            <Title level={4} className="text-slate-700">
              Chưa sinh tài nguyên Session
            </Title>
            <Paragraph className="text-slate-500 max-w-md">
              Session này chưa được sinh các tài nguyên tổng hợp. Vui lòng quay lại trang khóa học và bấm "Tạo AI Session" để bắt đầu.
            </Paragraph>
            <Button
              type="primary"
              icon={<RefreshCw size={14} />}
              onClick={() => window.location.reload()}
              className="bg-teal-600 border-teal-600 hover:bg-teal-700 font-semibold"
            >
              Tải lại dữ liệu
            </Button>
          </div>
        ) : activeTabItem ? (
          <div className="animate-fade-in bg-white p-5 rounded-xl border border-slate-200/60 shadow-sm min-h-[60vh]">
            <ArtifactVersionWrapper
              artifact={activeTabItem.artifact}
              lessonId={null}
              sessionId={parsedSessionId}
            >
              {(previewedArt) => renderContent(previewedArt, activeTabItem.subType)}
            </ArtifactVersionWrapper>
          </div>
        ) : null}
      </Content>
    </Layout>
  );
}
