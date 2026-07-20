import { useState, useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import {
  Card,
  Tabs,
  Table,
  Tag,
  Button,
  Spin,
  Alert,
  Progress,
  Statistic,
  Row,
  Col,
  Select,
  Input,
  Popconfirm,
  message,
  Typography,
  Badge,
  Steps,
  Tooltip,
  List,
  Modal,
} from "antd";
import {
  Brain,
  Zap,
  Package,
  Shield,
  RefreshCw,
  Trash2,
  Download,
  CheckCircle,
  XCircle,
  AlertTriangle,
  UploadCloud,
  FileText,
  CheckSquare,
  Video,
  Database,
  Play,
  GitBranch,
} from "lucide-react";
import {
  useCacheStats,
  useClearCache,
  useKnowledgeMemories,
  useMemoryCategories,
  useSCORMExport,
  usePrerequisiteReport,
  usePMReview,
  useObsidianExport,
  useVideoRender,
  useSyncDisk,
  useCourseStatus,
  useGenerateAllCourse,
  useGenerateSession,
  useGenerateLesson,
} from "../../../services/hooks";
import {
  getCourses,
  type Course,
  getSCORMDownloadUrl,
  getVideoProjectDetails,
  saveVideoFile,
  getVideoStatus,
  renderVideo,
} from "../../../services/api";

const { Text, Paragraph, Title: AntdTitle } = Typography;

const SEVERITY_COLOR: Record<string, string> = {
  critical: "red",
  high: "orange",
  medium: "gold",
  low: "blue",
};

// Simple custom Markdown rendering for report styling
const renderStyledMarkdown = (text: string) => {
  if (!text) return null;
  return text.split("\n").map((line, idx) => {
    if (line.startsWith("### ")) {
      return (
        <h4 key={idx} className="text-md font-bold text-slate-800 mt-3 mb-1">
          {line.replace("### ", "")}
        </h4>
      );
    }
    if (line.startsWith("## ")) {
      return (
        <h3 key={idx} className="text-lg font-bold text-slate-800 mt-4 mb-2">
          {line.replace("## ", "")}
        </h3>
      );
    }
    if (line.startsWith("# ")) {
      return (
        <h2 key={idx} className="text-xl font-bold text-slate-900 mt-5 mb-3">
          {line.replace("# ", "")}
        </h2>
      );
    }
    if (line.startsWith("- ") || line.startsWith("* ")) {
      return (
        <li key={idx} className="ml-4 list-disc text-slate-700 my-0.5">
          {line.substring(2)}
        </li>
      );
    }
    if (
      line.includes("🔴 **BLOCKER**") ||
      line.includes("BLOCKER") ||
      line.includes("🔴 BLOCKER")
    ) {
      return (
        <div
          key={idx}
          className="p-2 my-2 bg-rose-50 text-rose-700 border-l-4 border-rose-500 rounded font-mono text-xs flex items-center gap-2"
        >
          <XCircle size={14} className="text-rose-500 shrink-0" />
          <span>{line}</span>
        </div>
      );
    }
    if (
      line.includes("🟡 **WARNING**") ||
      line.includes("WARNING") ||
      line.includes("🟡 WARNING")
    ) {
      return (
        <div
          key={idx}
          className="p-2 my-2 bg-amber-50 text-amber-800 border-l-4 border-amber-500 rounded font-mono text-xs flex items-center gap-2"
        >
          <AlertTriangle size={14} className="text-amber-500 shrink-0" />
          <span>{line}</span>
        </div>
      );
    }
    if (line.trim().startsWith("|")) {
      return (
        <div
          key={idx}
          className="font-mono text-xs bg-slate-50 p-1 border-b text-slate-600"
        >
          {line}
        </div>
      );
    }
    return (
      <p
        key={idx}
        className="text-slate-600 my-1 text-sm font-sans leading-relaxed"
      >
        {line}
      </p>
    );
  });
};

export default function PipelineMonitorPage() {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();

  // URL state synchronization
  const activeTab = searchParams.get("tab") || "workflow";
  const selectedCourseId = searchParams.get("courseId")
    ? Number(searchParams.get("courseId"))
    : null;
  const categoryFilter = searchParams.get("category") || undefined;
  const scopeFilter = searchParams.get("scope") || undefined;

  const setActiveTab = (tab: string) => {
    setSearchParams(
      (prev) => {
        prev.set("tab", tab);
        return prev;
      },
      { replace: true },
    );
  };

  const setSelectedCourseId = (courseId: number | null) => {
    setSearchParams(
      (prev) => {
        if (courseId) {
          prev.set("courseId", String(courseId));
        } else {
          prev.delete("courseId");
        }
        return prev;
      },
      { replace: true },
    );
  };

  const setCategoryFilter = (category: string | undefined) => {
    setSearchParams(
      (prev) => {
        if (category) {
          prev.set("category", category);
        } else {
          prev.delete("category");
        }
        return prev;
      },
      { replace: true },
    );
  };

  const setScopeFilter = (scope: string | undefined) => {
    setSearchParams(
      (prev) => {
        if (scope) {
          prev.set("scope", scope);
        } else {
          prev.delete("scope");
        }
        return prev;
      },
      { replace: true },
    );
  };

  const [currentStep, setCurrentStep] = useState(selectedCourseId ? 2 : 0);
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedCourseName, setSelectedCourseName] = useState<string>("");

  // Advanced States
  const [pmFile, setPmFile] = useState<File | null>(null);
  const [videoSession, setVideoSession] = useState<string>("");
  const [videoLesson, setVideoLesson] = useState<string>("");
  const [videoDraft, setVideoDraft] = useState<boolean>(false);
  const [syncLogs, setSyncLogs] = useState<string[]>([]);

  // Video Management States
  const [videoModalVisible, setVideoModalVisible] = useState<boolean>(false);
  const [activeVideoLesson, setActiveVideoLesson] = useState<{ id: number; name: string; title: string } | null>(null);
  const [activeVideoSession, setActiveVideoSession] = useState<string>("");
  const [videoDetails, setVideoDetails] = useState<any>(null);
  const [loadingDetails, setLoadingDetails] = useState<boolean>(false);
  const [editingContent, setEditingContent] = useState<string>("");
  const [activeEditorTab, setActiveEditorTab] = useState<"script" | "html">("script");
  const [savingFile, setSavingFile] = useState<boolean>(false);
  const [renderTaskId, setRenderTaskId] = useState<string | null>(null);
  const [renderStatus, setRenderStatus] = useState<any>(null);
  const [pollingRender, setPollingRender] = useState<boolean>(false);
  const [modalDraft, setModalDraft] = useState<boolean>(false);

  // Custom Hooks & Services
  const {
    data: cacheStats,
    loading: cacheLoading,
    error: cacheError,
    refetch: refetchCache,
  } = useCacheStats();
  const { execute: doClearCache, loading: clearingCache } = useClearCache();
  const { data: memories, loading: memoriesLoading } = useKnowledgeMemories({
    category: categoryFilter,
    scope: scopeFilter,
    limit: 100,
  });
  const { data: categoriesData } = useMemoryCategories();
  const {
    data: prereqReport,
    loading: prereqLoading,
    refetch: refetchPrereq,
  } = usePrerequisiteReport(selectedCourseName || null);

  // Real-time Course Compilation Monitor Hook
  const {
    data: courseStatus,
    loading: statusLoading,
    refetch: refetchCourseStatus,
  } = useCourseStatus(selectedCourseId);

  // Workflow Core Hooks
  const {
    executeReview: runPMReview,
    executeUpdate: runPMUpdate,
    data: pmData,
    loading: pmLoading,
  } = usePMReview();
  const { execute: runSyncDisk, loading: syncLoading } = useSyncDisk();
  const { execute: triggerGenerateAll, loading: generateAllLoading } =
    useGenerateAllCourse();
  const { execute: triggerGenerateSession, loading: generateSessionLoading } =
    useGenerateSession();
  const { execute: triggerGenerateLesson, loading: generateLessonLoading } =
    useGenerateLesson();

  const {
    startExport: startSCORM,
    taskId: scormTaskId,
    status: scormStatus,
    loading: scormLoading,
  } = useSCORMExport();

  const {
    startExport: startObsidian,
    status: obsStatus,
    loading: obsLoading,
  } = useObsidianExport();

  const {
    startRender: startVideo,
    status: vidStatus,
    loading: vidLoading,
  } = useVideoRender();

  const openVideoManager = async (lesson: { id: number; name: string; title: string }, sessionName: string) => {
    setActiveVideoLesson(lesson);
    setActiveVideoSession(sessionName);
    setVideoModalVisible(true);
    setLoadingDetails(true);
    setVideoDetails(null);
    setRenderTaskId(null);
    setRenderStatus(null);
    
    try {
      const details = await getVideoProjectDetails(selectedCourseName, sessionName, lesson.name);
      setVideoDetails(details);
      if (details.project_found) {
        setEditingContent(details.script_md || "");
        setActiveEditorTab("script");
      }
    } catch (e: any) {
      message.error("Lỗi khi tải chi tiết dự án video: " + e.message);
    } finally {
      setLoadingDetails(false);
    }
  };

  const handleSaveFile = async () => {
    if (!activeVideoLesson || !activeVideoSession) return;
    setSavingFile(true);
    try {
      const filename = activeEditorTab === "script" ? "SCRIPT.md" : "index.html";
      await saveVideoFile({
        course_name: selectedCourseName,
        session_id: activeVideoSession,
        lesson_id: activeVideoLesson.name,
        filename,
        content: editingContent
      });
      message.success(`Đã lưu tệp ${filename} thành công!`);
      setVideoDetails((prev: any) => ({
        ...prev,
        [activeEditorTab === "script" ? "script_md" : "index_html"]: editingContent
      }));
    } catch (e: any) {
      message.error("Lỗi khi lưu tệp: " + e.message);
    } finally {
      setSavingFile(false);
    }
  };

  const handleModalRender = async () => {
    if (!activeVideoLesson || !activeVideoSession) return;
    setPollingRender(true);
    setRenderStatus({ status: "running", progress: "Khởi tạo kết xuất..." });
    try {
      const res = await renderVideo({
        course_name: selectedCourseName,
        session_id: activeVideoSession,
        lesson_id: activeVideoLesson.name,
        draft: modalDraft
      });
      setRenderTaskId(res.task_id);
    } catch (e: any) {
      message.error("Lỗi khi khởi chạy render: " + e.message);
      setPollingRender(false);
      setRenderStatus({ status: "failed", error: e.message, progress: "Khỏi chạy thất bại" });
    }
  };

  useEffect(() => {
    if (!renderTaskId) return;
    
    const interval = setInterval(async () => {
      try {
        const s = await getVideoStatus(renderTaskId);
        setRenderStatus(s);
        if (s.status !== 'running') {
          setPollingRender(false);
          clearInterval(interval);
          
          if (s.status === 'completed') {
            message.success("Render video thành công!");
            const details = await getVideoProjectDetails(selectedCourseName, activeVideoSession, activeVideoLesson!.name);
            setVideoDetails(details);
          } else {
            message.error("Render video thất bại: " + (s.error || s.progress));
          }
        }
      } catch (e: any) {
        message.error("Lỗi kiểm tra trạng thái render: " + e.message);
        setPollingRender(false);
        clearInterval(interval);
      }
    }, 2000);
    
    return () => clearInterval(interval);
  }, [renderTaskId]);

  // Load Course list on startup
  useEffect(() => {
    getCourses()
      .then(setCourses)
      .catch(() => {});
  }, []);

  // Sync Course name when course ID changes
  useEffect(() => {
    if (selectedCourseId) {
      const target = courses.find((c) => c.id === selectedCourseId);
      if (target) {
        setSelectedCourseName(target.name);
      }
    } else {
      setSelectedCourseName("");
    }
  }, [selectedCourseId, courses]);

  const handleClearCache = async () => {
    try {
      const result = await doClearCache();
      message.success(
        `Đã xóa thành công ${result.deleted_entries} cache entries.`,
      );
      refetchCache();
    } catch (e: unknown) {
      message.error(e instanceof Error ? e.message : "Lỗi khi xóa cache");
    }
  };

  const handleSyncDisk = async () => {
    setSyncLogs((prev) => [
      ...prev,
      "Bắt đầu quét cấu trúc đĩa và nạp CSDL...",
    ]);
    try {
      const result = await runSyncDisk();
      setSyncLogs((prev) => [
        ...prev,
        `Đồng bộ hoàn tất: ${result.stats.courses_synced} môn học, ${result.stats.sessions_synced} Sessions, ${result.stats.lessons_synced} Lessons.`,
        `Cập nhật thành công ${result.stats.artifacts_updated} học liệu.`,
      ]);
      message.success("Đồng bộ cơ sở dữ liệu thành công!");
      if (selectedCourseId) refetchCourseStatus();
    } catch (e: unknown) {
      setSyncLogs((prev) => [
        ...prev,
        `Lỗi đồng bộ: ${e instanceof Error ? e.message : String(e)}`,
      ]);
      message.error("Đồng bộ thất bại!");
    }
  };

  const handleGenerateAll = async () => {
    if (!selectedCourseId) return;
    try {
      await triggerGenerateAll(selectedCourseId);
      message.success("Đã gửi lệnh biên dịch toàn khóa học tới AI Agent!");
      refetchCourseStatus();
    } catch (e: unknown) {
      message.error(e instanceof Error ? e.message : "Lỗi khởi chạy biên dịch");
    }
  };

  const handleGenerateSession = async (sessionId: number) => {
    try {
      await triggerGenerateSession(sessionId);
      message.success("Đang tạo quiz & mindmap biên dịch Session...");
      refetchCourseStatus();
    } catch (e: unknown) {
      message.error(e instanceof Error ? e.message : "Lỗi biên dịch Session");
    }
  };

  const handleGenerateLesson = async (lessonId: number) => {
    try {
      await triggerGenerateLesson(lessonId);
      message.success("Đang biên dịch học liệu cho Lesson...");
      refetchCourseStatus();
    } catch (e: unknown) {
      message.error(e instanceof Error ? e.message : "Lỗi biên dịch Lesson");
    }
  };

  // Enforce Prerequisite Guard blocker validation
  const hasBlockers = prereqReport?.has_blockers || false;

  const memoriesColumns = [
    {
      title: "Category",
      dataIndex: "category",
      key: "category",
      render: (v: string) => {
        const cat = categoriesData?.categories.find((c) => c.key === v);
        return <Tag color={cat?.color || "default"}>{cat?.label || v}</Tag>;
      },
    },
    {
      title: "Severity",
      dataIndex: "severity",
      key: "severity",
      render: (v: string) => (
        <Tag color={SEVERITY_COLOR[v] || "default"}>{v.toUpperCase()}</Tag>
      ),
    },
    {
      title: "Mô tả chi tiết",
      dataIndex: "description",
      key: "description",
      ellipsis: true,
    },
    {
      title: "Tech Stack",
      dataIndex: "tech_stack",
      key: "tech_stack",
      render: (v?: string) =>
        v ? <Tag>{v}</Tag> : <Text type="secondary">—</Text>,
    },
    {
      title: "Scope",
      dataIndex: "scope",
      key: "scope",
      render: (v?: string) =>
        v ? <Tag color="blue">{v}</Tag> : <Text type="secondary">—</Text>,
    },
    {
      title: "Tần suất lỗi",
      dataIndex: "hit_count",
      key: "hit_count",
      sorter: (a: { hit_count: number }, b: { hit_count: number }) =>
        a.hit_count - b.hit_count,
    },
  ];

  // Render artifact status badge helper
  const renderArtifactBadge = (type: string, status?: string) => {
    const textMap: Record<string, string> = {
      reading: "HTML",
      quiz: "Quiz",
      outline: "Outline",
      walkthrough: "Script",
      pre_quiz: "Pre-Q",
      post_quiz: "Post-Q",
      session_mindmap: "Map",
      session_reading: "Book",
    };

    const label = textMap[type] || type;

    if (status === "Completed") {
      return (
        <Tooltip title="Đã hoàn thành">
          <Badge
            status="success"
            text={
              <Text className="text-emerald-600 font-medium text-xs bg-emerald-50 px-2 py-0.5 rounded border border-emerald-100">
                {label}
              </Text>
            }
          />
        </Tooltip>
      );
    }
    if (status === "Pending") {
      return (
        <Tooltip title="Đang sinh học liệu bằng AI...">
          <Badge
            status="processing"
            text={
              <Text className="text-indigo-600 font-medium text-xs bg-indigo-50 px-2 py-0.5 rounded border border-indigo-100 animate-pulse flex items-center gap-1">
                <Spin size="small" className="scale-75" /> {label}
              </Text>
            }
          />
        </Tooltip>
      );
    }
    if (status === "Failed") {
      return (
        <Tooltip title="Biên dịch thất bại, vui lòng chạy lại">
          <Badge
            status="error"
            text={
              <Text className="text-rose-600 font-medium text-xs bg-rose-50 px-2 py-0.5 rounded border border-rose-100">
                {label}
              </Text>
            }
          />
        </Tooltip>
      );
    }
    return (
      <Tooltip title="Chưa bắt đầu">
        <Badge
          status="default"
          text={
            <Text className="text-slate-400 font-normal text-xs bg-slate-50 px-2 py-0.5 rounded border border-slate-200">
              {label}
            </Text>
          }
        />
      </Tooltip>
    );
  };

  const tabItems = [
    {
      key: "workflow",
      label: (
        <span className="flex items-center gap-1.5 font-semibold">
          <GitBranch size={16} /> Quy trình Biên dịch
        </span>
      ),
      children: (
        <div className="space-y-6">
          {/* Header Controls */}
          <Card className="shadow-sm border-slate-200 rounded-lg">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <AntdTitle level={4} className="m-0 text-slate-800">
                  Thiết lập Bảng điều khiển Quy trình
                </AntdTitle>
                <Paragraph className="text-slate-500 m-0 mt-0.5 text-xs">
                  Chọn môn học mục tiêu để theo dõi trạng thái, đồng bộ cấu
                  trúc, kiểm tra ràng buộc sư phạm và xuất bản học liệu.
                </Paragraph>
              </div>
              <div className="flex gap-2 items-center">
                <Select
                  showSearch
                  allowClear
                  placeholder="Vui lòng chọn môn học..."
                  style={{ width: 320 }}
                  value={selectedCourseId}
                  onChange={(val) => {
                    setSelectedCourseId(val);
                    setCurrentStep(val ? 2 : 0);
                  }}
                  options={courses.map((c) => ({
                    value: c.id,
                    label: `${c.name} (${c.technology_stack || "Chưa rõ"})`,
                  }))}
                  className="rounded-md shadow-sm"
                />
                {selectedCourseId && (
                  <Button
                    icon={
                      <RefreshCw
                        size={14}
                        className={statusLoading ? "animate-spin" : ""}
                      />
                    }
                    onClick={() => {
                      refetchCourseStatus();
                      refetchPrereq();
                    }}
                    disabled={statusLoading}
                  >
                    Tải lại
                  </Button>
                )}
              </div>
            </div>
          </Card>

          {selectedCourseId ? (
            <>
              {/* Stepper Navigator */}
              <Card className="shadow-sm border-slate-200 rounded-lg">
                <Steps
                  current={currentStep}
                  onChange={setCurrentStep}
                  size="small"
                  items={[
                    {
                      title: "Tài liệu PM Excel",
                      description: "Đánh giá cấu trúc",
                    },
                    { title: "Đồng bộ CSDL", description: "Import hệ thống" },
                    {
                      title: "Biên dịch học liệu AI",
                      description: "AI Agent Generator",
                    },
                    {
                      title: "Kiểm tra sư phạm",
                      description: "Prerequisite Guard",
                    },
                    {
                      title: "Xuất bản & Deliver",
                      description: "SCORM, Obsidian, Video",
                    },
                  ]}
                />
              </Card>

              {/* Step 0: PM Reviewer */}
              {currentStep === 0 && (
                <Card
                  title={
                    <span className="flex items-center gap-2">
                      <FileText size={18} className="text-indigo-600" /> Thiết
                      kế & Thẩm định PM Excel
                    </span>
                  }
                  className="shadow-sm border-slate-200"
                >
                  <Alert
                    type="info"
                    showIcon
                    message="Chu kỳ Đánh giá Sư phạm của PM (Program Manager) Excel"
                    description="Trước khi nạp cấu trúc vào cơ sở dữ liệu và kích hoạt AI Agent, file Excel PM cần được đánh giá tính chặt chẽ về mặt khoa học học tập, tránh rò rỉ kiến thức."
                    className="mb-4 text-xs"
                  />
                  <div className="p-6 border-2 border-dashed border-slate-300 rounded-lg bg-slate-50 text-center space-y-3">
                    <UploadCloud size={32} className="mx-auto text-slate-400" />
                    <div>
                      <input
                        type="file"
                        accept=".xlsx"
                        id="pm-upload-btn"
                        className="hidden"
                        onChange={(e) => setPmFile(e.target.files?.[0] || null)}
                      />
                      <label
                        htmlFor="pm-upload-btn"
                        className="cursor-pointer bg-white px-4 py-2 border border-slate-300 rounded-md shadow-sm text-sm hover:bg-slate-50 inline-block font-medium"
                      >
                        {pmFile
                          ? pmFile.name
                          : "Chọn file Excel chương trình (.xlsx)"}
                      </label>
                    </div>
                    {pmFile && (
                      <p className="text-xs text-slate-500">
                        File đã chọn sẵn sàng để gửi thẩm định.
                      </p>
                    )}
                  </div>

                  <div className="flex gap-2 justify-end mt-4">
                    <Button
                      type="primary"
                      icon={<UploadCloud size={14} />}
                      disabled={!pmFile || pmLoading}
                      loading={pmLoading}
                      onClick={() => pmFile && runPMReview(pmFile)}
                    >
                      Bắt đầu thẩm định AI
                    </Button>
                    <Button
                      type="default"
                      danger
                      icon={<CheckSquare size={14} />}
                      disabled={!pmData || pmLoading}
                      loading={pmLoading}
                      onClick={() => pmData && runPMUpdate(pmData)}
                    >
                      AI Tự động sửa cấu trúc PM
                    </Button>
                  </div>

                  {pmData && (
                    <Card
                      title="Báo cáo thẩm định chương trình học từ AI Agent"
                      className="mt-6 bg-slate-50 border-slate-200"
                    >
                      <div className="max-h-96 overflow-auto p-4 bg-white rounded border text-xs leading-relaxed font-sans text-slate-800">
                        {renderStyledMarkdown(pmData.report)}
                      </div>
                      {pmData.new_file_path && (
                        <div className="mt-4 flex justify-between items-center bg-emerald-50 p-3 rounded border border-emerald-200 text-xs">
                          <span className="text-emerald-800 font-medium flex items-center gap-1.5">
                            <CheckCircle
                              size={16}
                              className="text-emerald-600"
                            />{" "}
                            Đã hoàn tất sửa đổi cấu trúc tự động!
                          </span>
                          <Button
                            type="primary"
                            ghost
                            icon={<Download size={14} />}
                            href={pmData.download_url}
                            download
                          >
                            Tải file Excel đã tối ưu (.xlsx)
                          </Button>
                        </div>
                      )}
                    </Card>
                  )}
                </Card>
              )}

              {/* Step 1: DB Sync */}
              {currentStep === 1 && (
                <Card
                  title={
                    <span className="flex items-center gap-2">
                      <Database size={18} className="text-indigo-600" /> Đồng bộ
                      & Nạp Cấu trúc
                    </span>
                  }
                  className="shadow-sm border-slate-200"
                >
                  <Row gutter={16}>
                    <Col span={14}>
                      <Alert
                        type="warning"
                        showIcon
                        message="Đồng bộ đĩa cứng"
                        description="Hệ thống sẽ quét các thư mục output chứa tài liệu biên dịch hiện tại và nạp lại cấu trúc Session, Lesson, Artifacts vào cơ sở dữ liệu SQLite."
                        className="mb-4 text-xs"
                      />
                      <div className="p-6 bg-slate-50 border border-slate-200 rounded-lg space-y-4">
                        <h4 className="text-sm font-semibold text-slate-700 m-0">
                          Hoạt động đồng bộ
                        </h4>
                        <div className="flex gap-2">
                          <Button
                            type="primary"
                            icon={
                              <RefreshCw
                                size={14}
                                className={syncLoading ? "animate-spin" : ""}
                              />
                            }
                            loading={syncLoading}
                            onClick={handleSyncDisk}
                          >
                            Quét & Đồng bộ Cấu trúc DB
                          </Button>
                        </div>

                        <div className="mt-4">
                          <h5 className="text-xs font-semibold text-slate-500 mb-2">
                            Logs hoạt động thời gian thực:
                          </h5>
                          <div className="bg-slate-900 text-emerald-400 p-3 rounded font-mono text-xs max-h-48 overflow-auto space-y-1">
                            {syncLogs.map((log, idx) => (
                              <div key={idx}>&gt; {log}</div>
                            ))}
                            {syncLogs.length === 0 && (
                              <div className="text-slate-500">
                                Chờ lệnh đồng bộ...
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    </Col>
                    <Col span={10}>
                      <Card
                        title="Thống kê cơ sở dữ liệu hiện tại"
                        bordered={false}
                        className="bg-indigo-50"
                      >
                        {statusLoading ? (
                          <div className="flex justify-center p-8">
                            <Spin />
                          </div>
                        ) : (
                          <div className="space-y-3 text-sm">
                            <div className="flex justify-between border-b pb-2">
                              <span className="text-slate-500">
                                Tổng số Session:
                              </span>
                              <strong className="text-slate-800">
                                {courseStatus?.sessions.length || 0} Sessions
                              </strong>
                            </div>
                            <div className="flex justify-between border-b pb-2">
                              <span className="text-slate-500">
                                Tổng số Lesson:
                              </span>
                              <strong className="text-slate-800">
                                {courseStatus?.sessions.reduce(
                                  (acc, s) => acc + s.lessons.length,
                                  0,
                                ) || 0}{" "}
                                Lessons
                              </strong>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-slate-500">
                                Trạng thái sẵn sàng học liệu:
                              </span>
                              <strong className="text-slate-800">
                                {courseStatus?.sessions.every(
                                  (s) =>
                                    s.artifacts.every(
                                      (a) => a.status === "Completed",
                                    ) &&
                                    s.lessons.every((l) =>
                                      l.artifacts.every(
                                        (art) => art.status === "Completed",
                                      ),
                                    ),
                                )
                                  ? "100% Sẵn sàng"
                                  : "Chưa hoàn tất"}
                              </strong>
                            </div>
                          </div>
                        )}
                      </Card>
                    </Col>
                  </Row>
                </Card>
              )}

              {/* Step 2: AI Compiler Monitor */}
              {currentStep === 2 && (
                <Card
                  title={
                    <span className="flex items-center gap-2">
                      <Brain size={18} className="text-indigo-600" /> Giám sát
                      AI Agent Biên dịch Học liệu
                    </span>
                  }
                  extra={
                    <Button
                      type="primary"
                      icon={<Play size={14} />}
                      loading={generateAllLoading}
                      disabled={statusLoading}
                      onClick={handleGenerateAll}
                    >
                      Biên dịch Toàn Bộ Khóa Học (Gemini Core)
                    </Button>
                  }
                  className="shadow-sm border-slate-200"
                >
                  <Alert
                    type="info"
                    showIcon
                    message="Tính năng giám sát học liệu thời gian thực"
                    description="AI Agent sẽ chạy ngầm để biên dịch từng bài đọc HTML, Quiz cuối bài, Mindmap lý thuyết và Video Script. Bảng dưới đây tự động cập nhật trạng thái mỗi 4 giây nếu phát hiện có tác vụ chạy ngầm."
                    className="mb-4! text-xs"
                  />

                  {statusLoading && !courseStatus ? (
                    <div className="flex justify-center p-12">
                      <Spin tip="Đang tải dữ liệu cấu trúc học liệu..." />
                    </div>
                  ) : (
                    <div className="space-y-4!">
                      {courseStatus?.sessions.map((sess) => (
                        <Card
                          key={sess.id}
                          size="small"
                          className="border-slate-200 hover:shadow-md transition-shadow"
                          title={
                            <div className="flex justify-between items-center flex-wrap gap-2 py-1">
                              <div>
                                <span className="font-bold text-slate-800 text-sm bg-slate-100 px-2 py-1 rounded mr-2">
                                  {sess.name}
                                </span>
                                <span className="font-semibold text-slate-700 text-sm">
                                  {sess.title}
                                </span>
                              </div>
                              <div className="flex items-center gap-3">
                                <span className="text-xs text-slate-400">
                                  Học liệu Session:
                                </span>
                                <div className="flex gap-1">
                                  {sess.artifacts.map((a) =>
                                    renderArtifactBadge(a.type, a.status),
                                  )}
                                </div>
                                <Button
                                  size="small"
                                  ghost
                                  type="primary"
                                  icon={<Play size={12} />}
                                  loading={generateSessionLoading}
                                  onClick={() => handleGenerateSession(sess.id)}
                                >
                                  Biên dịch Session
                                </Button>
                              </div>
                            </div>
                          }
                        >
                          <List
                            dataSource={sess.lessons}
                            size="small"
                            renderItem={(les) => (
                              <List.Item
                                key={les.id}
                                className="flex justify-between items-center text-xs py-2 border-b last:border-b-0 hover:bg-slate-50 rounded px-2"
                              >
                                <div className="w-1/3">
                                  <Tooltip title="Bấm để vào Màn hình Học thử (Lý thuyết, Trắc nghiệm & Coding)">
                                    <span
                                      onClick={() =>
                                        navigate(
                                          `/courses/${selectedCourseId}/lessons/${les.id}/viewer`,
                                        )
                                      }
                                      className="cursor-pointer text-indigo-600 hover:text-indigo-800 hover:underline font-semibold"
                                    >
                                      <Text
                                        strong
                                        className="text-indigo-600 hover:text-indigo-800"
                                      >
                                        {les.name}:{" "}
                                      </Text>
                                      {les.title}
                                    </span>
                                  </Tooltip>
                                </div>
                                <div className="flex items-center gap-6">
                                  <div className="flex gap-2">
                                    {les.artifacts.map((a) =>
                                      renderArtifactBadge(a.type, a.status),
                                    )}
                                    {les.artifacts.length === 0 && (
                                      <span className="text-slate-400 italic">
                                        Chưa cấu hình học liệu
                                      </span>
                                    )}
                                  </div>
                                  <div className="flex gap-1.5">
                                    <Button
                                      size="small"
                                      type="primary"
                                      ghost
                                      icon={<Video size={10} />}
                                      onClick={() => openVideoManager(les, sess.name)}
                                    >
                                      Quản lý Video
                                    </Button>
                                    <Button
                                      size="small"
                                      icon={<Play size={10} />}
                                      loading={generateLessonLoading}
                                      onClick={() => handleGenerateLesson(les.id)}
                                    >
                                      Biên dịch
                                    </Button>
                                  </div>
                                </div>
                              </List.Item>
                            )}
                          />
                        </Card>
                      ))}
                    </div>
                  )}
                </Card>
              )}

              {/* Step 3: Prerequisite Guard Check */}
              {currentStep === 3 && (
                <Card
                  title={
                    <span className="flex items-center gap-2">
                      <Shield size={18} className="text-rose-600" /> Thẩm định
                      Sư phạm & Ràng buộc Tiên quyết
                    </span>
                  }
                  className="shadow-sm border-slate-200"
                >
                  <Alert
                    type={hasBlockers ? "error" : "success"}
                    showIcon
                    message={
                      hasBlockers
                        ? "Phát hiện vi phạm ràng buộc tiên quyết nghiêm trọng!"
                        : "Môn học hợp lệ về mặt sư phạm"
                    }
                    description={
                      hasBlockers
                        ? "Các bài học có yếu tố học thuật bị rò rỉ (chưa được dạy bài trước mà đã xuất hiện ở bài sau). Vui lòng kiểm tra báo cáo phía dưới để khắc phục trước khi xuất bản."
                        : "Không tìm thấy blocker nào. Cấu trúc học liệu hoàn toàn hợp lệ."
                    }
                    className="mb-4 text-xs font-medium"
                  />

                  {prereqLoading ? (
                    <div className="flex justify-center p-12">
                      <Spin />
                    </div>
                  ) : (
                    <Row gutter={16}>
                      <Col span={8}>
                        <div className="space-y-4">
                          <Card
                            size="small"
                            className="bg-rose-50 border-rose-200"
                          >
                            <Statistic
                              title={
                                <span className="text-rose-800 font-semibold">
                                  Số lỗi BLOCKER
                                </span>
                              }
                              value={prereqReport?.blocker_count || 0}
                              valueStyle={{ color: "#cf1322", fontWeight: 800 }}
                              prefix={
                                <XCircle
                                  size={16}
                                  className="text-rose-600 mr-1 inline"
                                />
                              }
                            />
                          </Card>
                          <Card
                            size="small"
                            className="bg-amber-50 border-amber-200"
                          >
                            <Statistic
                              title={
                                <span className="text-amber-800 font-semibold">
                                  Số cảnh báo WARNING
                                </span>
                              }
                              value={prereqReport?.warning_count || 0}
                              valueStyle={{ color: "#d4780a", fontWeight: 800 }}
                              prefix={
                                <AlertTriangle
                                  size={16}
                                  className="text-amber-600 mr-1 inline"
                                />
                              }
                            />
                          </Card>
                          <Button
                            block
                            size="large"
                            icon={<Shield size={14} />}
                            onClick={() => refetchPrereq()}
                          >
                            Chạy lại Prerequisite Guard
                          </Button>
                        </div>
                      </Col>
                      <Col span={16}>
                        <Card
                          title="Nội dung Báo cáo Prerequisite Guard chi tiết"
                          className="border-slate-200"
                        >
                          <div className="max-h-[50vh] overflow-auto p-4 bg-slate-900 text-slate-100 rounded font-mono text-xs leading-relaxed">
                            {prereqReport?.report_content ||
                              "Chưa sinh báo cáo. Hãy chọn chạy --approve-pm ở agent để tạo báo cáo."}
                          </div>
                        </Card>
                      </Col>
                    </Row>
                  )}
                </Card>
              )}

              {/* Step 4: Multi-Format Exports */}
              {currentStep === 4 && (
                <Card
                  title={
                    <span className="flex items-center gap-2">
                      <Package size={18} className="text-indigo-600" /> Xuất bản
                      & Deploy Đa định dạng
                    </span>
                  }
                  className="shadow-sm border-slate-200"
                >
                  {hasBlockers && (
                    <Alert
                      type="error"
                      showIcon
                      message="Cảnh báo Kỷ luật Sư phạm nghiêm ngặt"
                      description="Hệ thống đã phát hiện Blocker trong Prerequisite Guard. Nút export SCORM và Obsidian tạm thời bị VÔ HIỆU HÓA để đảm bảo tiêu chuẩn chất lượng học liệu đầu ra."
                      className="mb-6 text-xs font-semibold"
                    />
                  )}

                  <Row gutter={[16, 16]}>
                    {/* SCORM */}
                    <Col xs={24} md={8}>
                      <Card
                        title="Đóng gói SCORM 1.2 Package"
                        className="h-full flex flex-col justify-between border-slate-200 hover:shadow-md transition-shadow"
                      >
                        <div>
                          <p className="text-xs text-slate-500 mb-4">
                            Đóng gói toàn bộ bài học HTML, quiz, cấu trúc tuần
                            tự thành file .zip tiêu chuẩn Moodle/Canvas LMS.
                          </p>
                        </div>
                        <div className="space-y-4">
                          <Button
                            type="primary"
                            block
                            icon={<Package size={14} />}
                            loading={scormLoading}
                            disabled={hasBlockers}
                            onClick={() => startSCORM(selectedCourseName)}
                          >
                            Bắt đầu Export SCORM
                          </Button>

                          {scormLoading && (
                            <Progress
                              percent={45}
                              status="active"
                              strokeColor="#4f46e5"
                              size="small"
                            />
                          )}

                          {scormStatus?.status === "completed" && (
                            <div className="bg-emerald-50 border border-emerald-200 p-3 rounded text-xs space-y-2">
                              <span className="text-emerald-800 font-semibold block">
                                Đóng gói thành công!
                              </span>
                              <Button
                                type="primary"
                                size="small"
                                icon={<Download size={12} />}
                                href={
                                  scormTaskId
                                    ? getSCORMDownloadUrl(scormTaskId)
                                    : "#"
                                }
                                download
                              >
                                Tải SCORM Package (.zip)
                              </Button>
                            </div>
                          )}
                        </div>
                      </Card>
                    </Col>

                    {/* Obsidian Export */}
                    <Col xs={24} md={8}>
                      <Card
                        title="Đồ thị tri thức Obsidian"
                        className="h-full flex flex-col justify-between border-slate-200 hover:shadow-md transition-shadow"
                      >
                        <div>
                          <p className="text-xs text-slate-500 mb-4">
                            Kết xuất cấu trúc học liệu thành một Vault Obsidian
                            hoàn chỉnh để giáo viên và học sinh dễ dàng hình
                            dung mối quan hệ các bài học.
                          </p>
                        </div>
                        <div className="space-y-4">
                          <Input
                            placeholder="File PM tham chiếu (Nếu có)"
                            value={
                              pmData?.file_path ||
                              "output/tmp_uploads/Excel_PM.xlsx"
                            }
                            disabled
                            size="small"
                            className="bg-slate-50 font-mono text-[10px]"
                          />
                          <Button
                            type="primary"
                            block
                            icon={<Brain size={14} />}
                            loading={obsLoading}
                            disabled={hasBlockers || !pmData?.file_path}
                            onClick={() =>
                              pmData?.file_path &&
                              startObsidian(pmData.file_path)
                            }
                          >
                            Tạo Obsidian Vault
                          </Button>

                          {obsStatus?.status === "completed" && (
                            <Alert
                              type="success"
                              showIcon
                              message="Tạo Vault thành công"
                              description={
                                <span className="text-[10px] font-mono break-all">
                                  {obsStatus.vault_path}
                                </span>
                              }
                            />
                          )}
                        </div>
                      </Card>
                    </Col>

                    {/* Hyperframes Video Render */}
                    <Col xs={24} md={8}>
                      <Card
                        title="Hyperframes Video Render"
                        className="h-full flex flex-col justify-between border-slate-200 hover:shadow-md transition-shadow"
                      >
                        <div>
                          <p className="text-xs text-slate-500 mb-4">
                            Kích hoạt công nghệ Hyperframes kết xuất tệp kịch
                            bản `SCRIPT.md` thành video bài giảng MP4 hoàn chỉnh
                            kèm phụ đề.
                          </p>
                        </div>
                        <div className="space-y-3">
                          <Select
                            placeholder="Chọn Session"
                            style={{ width: "100%" }}
                            size="small"
                            value={videoSession || undefined}
                            onChange={(val) => {
                              setVideoSession(val);
                              setVideoLesson("");
                            }}
                            options={courseStatus?.sessions.map((s) => ({
                              value: s.name,
                              label: `${s.name} - ${s.title}`,
                            }))}
                          />
                          <Select
                            placeholder="Chọn Lesson"
                            style={{ width: "100%" }}
                            size="small"
                            value={videoLesson || undefined}
                            disabled={!videoSession}
                            onChange={setVideoLesson}
                            options={courseStatus?.sessions
                              .find((s) => s.name === videoSession)
                              ?.lessons.map((l) => ({
                                value: l.name,
                                label: `${l.name} - ${l.title}`,
                              }))}
                          />
                          <div className="flex items-center justify-between py-1.5 bg-indigo-50/50 rounded-md px-2.5 border border-indigo-100/50 my-1">
                            <span className="text-[11px] text-indigo-700 font-semibold">Chế độ Draft (Render nhanh 1-2p)</span>
                            <label className="relative inline-flex items-center cursor-pointer">
                              <input
                                type="checkbox"
                                checked={videoDraft}
                                onChange={(e) => setVideoDraft(e.target.checked)}
                                className="sr-only peer"
                              />
                              <div className="w-8 h-4 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-3 after:w-3 after:transition-all peer-checked:bg-indigo-600"></div>
                            </label>
                          </div>
                          <Button
                            type="primary"
                            block
                            icon={<Video size={14} />}
                            loading={vidLoading}
                            disabled={
                              !selectedCourseName ||
                              !videoSession ||
                              !videoLesson
                            }
                            onClick={() =>
                              startVideo({
                                course_name: selectedCourseName,
                                session_id: videoSession,
                                lesson_id: videoLesson,
                                draft: videoDraft,
                              })
                            }
                          >
                            Bắt đầu Render Video
                          </Button>

                          {vidStatus?.status === "running" && (
                            <div className="text-[10px] text-indigo-600 flex items-center gap-1">
                              <Spin size="small" className="scale-75" />{" "}
                              {vidStatus.progress}
                            </div>
                          )}

                          {vidStatus?.status === "completed" && (
                            <Alert
                              type="success"
                              showIcon
                              message="Render hoàn tất!"
                              description={
                                <a
                                  href={vidStatus.video_url}
                                  target="_blank"
                                  rel="noreferrer"
                                  className="text-xs font-semibold underline"
                                >
                                  Tải Video MP4 bài học
                                </a>
                              }
                            />
                          )}
                        </div>
                      </Card>
                    </Col>
                  </Row>
                </Card>
              )}
            </>
          ) : (
            <div className="p-16 text-center bg-slate-50 border border-dashed rounded-lg">
              <Brain size={48} className="mx-auto text-slate-300 mb-3" />
              <h3 className="text-slate-600 font-semibold">
                Chưa chọn môn học
              </h3>
              <p className="text-slate-400 text-xs mt-1">
                Vui lòng chọn môn học ở thanh công cụ phía trên để kích hoạt quy
                trình điều phối AI Agent.
              </p>
            </div>
          )}
        </div>
      ),
    },
    {
      key: "knowledge-memory",
      label: (
        <span className="flex items-center gap-1.5 font-semibold">
          <Brain size={16} /> Bộ nhớ Tri thức (Knowledge)
        </span>
      ),
      children: (
        <div className="space-y-4">
          <Card className="shadow-sm border-slate-200">
            <div className="flex gap-3 flex-wrap">
              <Select
                allowClear
                placeholder="Lọc theo phân loại lỗi"
                style={{ width: 220 }}
                onChange={setCategoryFilter}
                options={categoriesData?.categories.map((c) => ({
                  value: c.key,
                  label: c.label,
                }))}
              />
              <Input
                allowClear
                placeholder="Lọc theo Scope (ví dụ: html, quiz...)"
                style={{ width: 220 }}
                onChange={(e) => setScopeFilter(e.target.value || undefined)}
              />
            </div>
          </Card>
          <Table
            dataSource={memories || []}
            columns={memoriesColumns}
            loading={memoriesLoading}
            rowKey="id"
            size="small"
            pagination={{ pageSize: 15, showTotal: (t) => `${t} memories` }}
            className="shadow-sm border border-slate-100 rounded-lg overflow-hidden"
            expandable={{
              expandedRowRender: (record) => (
                <div className="p-4 space-y-3 bg-slate-50 rounded">
                  {record.bad_example && (
                    <div>
                      <Tag
                        color="red"
                        className="inline-flex items-center gap-1"
                      >
                        <XCircle size={12} /> Ví dụ vi phạm thiết kế
                      </Tag>
                      <pre className="mt-1.5 text-xs bg-red-50 p-3 rounded overflow-auto border border-red-100 font-mono">
                        {record.bad_example}
                      </pre>
                    </div>
                  )}
                  {record.good_example && (
                    <div>
                      <Tag
                        color="green"
                        className="inline-flex items-center gap-1"
                      >
                        <CheckCircle size={12} /> Ví dụ chuẩn hóa sư phạm
                      </Tag>
                      <pre className="mt-1.5 text-xs bg-green-50 p-3 rounded overflow-auto border border-green-100 font-mono">
                        {record.good_example}
                      </pre>
                    </div>
                  )}
                </div>
              ),
              rowExpandable: (record) =>
                !!(record.bad_example || record.good_example),
            }}
          />
        </div>
      ),
    },
    {
      key: "cache",
      label: (
        <span className="flex items-center gap-1.5 font-semibold">
          <Zap size={16} /> Bộ đệm Semantic Cache
        </span>
      ),
      children: (
        <div className="space-y-4">
          {cacheError && <Alert type="warning" message={cacheError} showIcon />}
          {cacheLoading ? (
            <div className="flex justify-center p-12">
              <Spin />
            </div>
          ) : cacheStats ? (
            <>
              <Row gutter={[16, 16]}>
                <Col xs={24} sm={8}>
                  <Card
                    bordered={false}
                    className="bg-amber-50 shadow-sm border border-amber-100"
                  >
                    <Statistic
                      title="Responses đã cache"
                      value={cacheStats.total_cached_responses}
                      valueStyle={{ color: "#d4780a", fontWeight: 800 }}
                    />
                  </Card>
                </Col>
                <Col xs={24} sm={8}>
                  <Card
                    bordered={false}
                    className="bg-emerald-50 shadow-sm border border-emerald-100"
                  >
                    <Statistic
                      title="Tổng lần Cache HIT thành công"
                      value={cacheStats.total_cache_hits}
                      valueStyle={{ color: "#389e0d", fontWeight: 800 }}
                    />
                  </Card>
                </Col>
                <Col xs={24} sm={8}>
                  <Card
                    bordered={false}
                    className="bg-indigo-50 shadow-sm border border-indigo-100"
                  >
                    <Statistic
                      title="Tokens tiết kiệm ước tính (LLM)"
                      value={cacheStats.estimated_tokens_saved.toLocaleString()}
                      valueStyle={{ color: "#4f46e5", fontWeight: 800 }}
                    />
                  </Card>
                </Col>
              </Row>

              <Card
                title="Phân tích hiệu năng Cache theo Agent"
                bordered={false}
                className="shadow-sm border-slate-200 mt-4"
                extra={
                  <div className="flex gap-2">
                    <Button
                      icon={<RefreshCw size={14} />}
                      onClick={refetchCache}
                    >
                      Cập nhật số liệu
                    </Button>
                    <Popconfirm
                      title="Xóa toàn bộ semantic cache?"
                      description="Toàn bộ LLM call tiếp theo sẽ bị gọi lại API tốn phí. Bạn có chắc chắn?"
                      onConfirm={handleClearCache}
                      okText="Đồng ý xóa"
                      cancelText="Hủy"
                      okButtonProps={{ danger: true }}
                    >
                      <Button
                        danger
                        icon={<Trash2 size={14} />}
                        loading={clearingCache}
                      >
                        Xóa Sạch Cache
                      </Button>
                    </Popconfirm>
                  </div>
                }
              >
                {Object.entries(cacheStats.by_agent).map(([agent, info]) => (
                  <div
                    key={agent}
                    className="flex justify-between items-center py-3 border-b border-slate-200 last:border-0"
                  >
                    <span className="font-semibold text-slate-700 text-sm">
                      {agent}
                    </span>
                    <div className="flex gap-6 items-center text-xs text-slate-500">
                      <span>{info.cached} cached responses</span>
                      <span className="text-emerald-600 font-semibold">
                        {info.hits} hits
                      </span>
                      <Progress
                        percent={
                          info.cached
                            ? Math.round((info.hits / info.cached) * 100)
                            : 0
                        }
                        size="small"
                        style={{ width: 100 }}
                        strokeColor="#10b981"
                      />
                    </div>
                  </div>
                ))}
                {Object.keys(cacheStats.by_agent).length === 0 && (
                  <Text type="secondary">
                    Chưa có dữ liệu cache nào được khởi tạo.
                  </Text>
                )}
              </Card>
            </>
          ) : null}
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start flex-wrap gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-900 m-0 tracking-tight flex items-center gap-2">
            Operations & AI Pipeline Center
          </h1>
          <p className="text-slate-500 text-sm mt-1">
            Trung tâm kiểm soát, tối ưu hóa sư phạm, quản lý Semantic Cache và
            biên dịch đa định dạng khóa học.
          </p>
        </div>
        <div className="bg-indigo-50 border border-indigo-100 rounded-lg px-4 py-2 text-xs flex items-center gap-2 shadow-sm text-indigo-700 font-semibold">
          <Zap size={16} className="text-indigo-600 animate-bounce" />
          <span>Agentic Pipeline: Đang hoạt động</span>
        </div>
      </div>

      <Tabs
        activeKey={activeTab}
        onChange={setActiveTab}
        items={tabItems}
        size="large"
        className="custom-pipeline-tabs"
      />

      <Modal
        title={
          <span className="flex items-center gap-2 text-indigo-600 text-sm md:text-base font-bold">
            <Video size={18} /> Quản lý và Thiết kế Video: {activeVideoLesson?.name} - {activeVideoLesson?.title}
          </span>
        }
        visible={videoModalVisible}
        onCancel={() => {
          setVideoModalVisible(false);
          setActiveVideoLesson(null);
        }}
        footer={null}
        width={1200}
        bodyStyle={{ padding: "16px" }}
      >
        {loadingDetails ? (
          <div className="flex flex-col items-center justify-center p-16 space-y-3">
            <Spin size="large" />
            <Text type="secondary">Đang tải cấu trúc và tệp tin của Video...</Text>
          </div>
        ) : videoDetails && !videoDetails.project_found ? (
          <div className="text-center p-12 space-y-4">
            <AlertTriangle size={48} className="mx-auto text-amber-500" />
            <div>
              <h4 className="font-semibold text-slate-800">Chưa tìm thấy Dự án Video cho bài học này</h4>
              <p className="text-xs text-slate-500 mt-1 max-w-md mx-auto">
                Dự án video (HyperFrames) chưa được khởi tạo. Vui lòng bấm biên dịch bài học này ở bước Biên dịch AI trước để tạo mã nguồn, lời thoại (TTS) và cấu trúc mặc định.
              </p>
            </div>
            <Button 
              type="primary" 
              onClick={async () => {
                if (activeVideoLesson) {
                  setLoadingDetails(true);
                  try {
                    await handleGenerateLesson(activeVideoLesson.id);
                    const details = await getVideoProjectDetails(selectedCourseName, activeVideoSession, activeVideoLesson.name);
                    setVideoDetails(details);
                    if (details.project_found) {
                      setEditingContent(details.script_md || "");
                      setActiveEditorTab("script");
                    }
                  } catch (e: any) {
                    message.error("Lỗi khi tạo video: " + e.message);
                  } finally {
                    setLoadingDetails(false);
                  }
                }
              }}
            >
              Khởi tạo/Biên dịch Video bài học
            </Button>
          </div>
        ) : (
          <Row gutter={16}>
            <Col span={12} className="flex flex-col space-y-3">
              <div className="flex justify-between items-center bg-slate-100 p-1.5 rounded-lg border">
                <div className="flex gap-1">
                  <Button
                    size="small"
                    type={activeEditorTab === "script" ? "primary" : "text"}
                    onClick={() => {
                      setActiveEditorTab("script");
                      setEditingContent(videoDetails?.script_md || "");
                    }}
                    className="text-xs font-semibold"
                  >
                    Kịch bản (SCRIPT.md)
                  </Button>
                  <Button
                    size="small"
                    type={activeEditorTab === "html" ? "primary" : "text"}
                    onClick={() => {
                      setActiveEditorTab("html");
                      setEditingContent(videoDetails?.index_html || "");
                    }}
                    className="text-xs font-semibold"
                  >
                    Mã nguồn (index.html)
                  </Button>
                </div>
                <Button
                  size="small"
                  type="primary"
                  ghost
                  icon={<RefreshCw size={12} className={savingFile ? "animate-spin" : ""} />}
                  loading={savingFile}
                  onClick={handleSaveFile}
                  className="text-xs"
                >
                  Lưu thay đổi
                </Button>
              </div>
              
              <div className="relative flex-1">
                <textarea
                  value={editingContent}
                  onChange={(e) => setEditingContent(e.target.value)}
                  className="w-full h-[55vh] font-mono text-xs p-4 bg-slate-900 text-indigo-200 rounded-lg border focus:ring-2 focus:ring-indigo-500 outline-none leading-relaxed resize-none"
                  placeholder="Nhập nội dung chỉnh sửa..."
                />
                <div className="absolute bottom-2 right-2 px-2 py-1 bg-slate-800 text-[10px] text-slate-400 rounded border border-slate-700">
                  {activeEditorTab === "script" ? "Markdown Mode" : "HTML Mode"}
                </div>
              </div>
            </Col>
            
            <Col span={12} className="flex flex-col space-y-4">
              <Tabs
                defaultActiveKey="preview"
                size="small"
                items={[
                  {
                    key: "preview",
                    label: <span className="font-semibold text-xs flex items-center gap-1"><Play size={12} /> Live Preview (Trực quan)</span>,
                    children: (
                      <div className="space-y-2">
                        <div className="w-full bg-slate-950 rounded-lg overflow-hidden border border-slate-800 relative aspect-video flex items-center justify-center">
                          {videoDetails?.preview_url ? (
                            <iframe
                              key={videoDetails.preview_url}
                              src={videoDetails.preview_url}
                              className="w-full h-full border-none bg-white"
                              title="HyperFrames Live Preview"
                            />
                          ) : (
                            <Text type="secondary" className="text-xs">Không có đường dẫn xem trước</Text>
                          )}
                        </div>
                        <div className="flex justify-between items-center bg-slate-50 p-2 rounded-lg border border-slate-200">
                          <span className="text-[10px] text-slate-500 italic">Preview chạy trực tiếp HTML/GSAP từ đĩa cứng.</span>
                          <Button
                            size="small"
                            type="default"
                            icon={<RefreshCw size={11} />}
                            onClick={() => {
                              setVideoDetails((prev: any) => ({
                                ...prev,
                                preview_url: prev.preview_url.split('?')[0] + "?t=" + Date.now()
                              }));
                            }}
                          >
                            Tải lại Preview
                          </Button>
                        </div>
                      </div>
                    )
                  },
                  {
                    key: "render",
                    label: <span className="font-semibold text-xs flex items-center gap-1"><Video size={12} /> Render Video & Xuất bản</span>,
                    children: (
                      <div className="space-y-4 p-1">
                        <div className="bg-slate-50 p-3 rounded-lg border space-y-3">
                          <div className="flex items-center justify-between">
                            <div>
                              <Text strong className="text-slate-800 text-xs">Cấu hình kết xuất bài học</Text>
                              <Paragraph className="text-[10px] text-slate-500 m-0 mt-0.5">
                                Chọn render nháp để kiểm tra thời gian thực, hoặc chất lượng cao để xuất bản.
                              </Paragraph>
                            </div>
                            <div className="flex items-center gap-2 bg-white px-2 py-1 rounded border">
                              <span className="text-[11px] text-slate-600 font-semibold">Render Nháp (Nhanh)</span>
                              <label className="relative inline-flex items-center cursor-pointer">
                                <input
                                  type="checkbox"
                                  checked={modalDraft}
                                  onChange={(e) => setModalDraft(e.target.checked)}
                                  className="sr-only peer"
                                />
                                <div className="w-8 h-4 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-3 after:w-3 after:transition-all peer-checked:bg-indigo-600"></div>
                              </label>
                            </div>
                          </div>
                          
                          <Button
                            type="primary"
                            block
                            icon={<Video size={14} />}
                            onClick={handleModalRender}
                            loading={pollingRender}
                          >
                            Bắt đầu kết xuất MP4
                          </Button>
                        </div>
                        
                        {renderStatus && (
                          <div className="bg-indigo-50/50 p-3 rounded-lg border border-indigo-100/50 space-y-2.5">
                            <div className="flex justify-between items-center text-xs">
                              <span className="text-indigo-800 font-semibold flex items-center gap-1.5">
                                <Spin size="small" className="scale-75" /> Trạng thái: {renderStatus.progress}
                              </span>
                              <span className="font-bold text-indigo-700">{renderStatus.percent || 0}%</span>
                            </div>
                            <Progress 
                              percent={renderStatus.percent || 0} 
                              status={renderStatus.status === "failed" ? "exception" : "active"}
                              strokeColor="#4f46e5" 
                              showInfo={false} 
                            />
                            {renderStatus.error && (
                              <Alert type="error" message={renderStatus.error} banner className="text-[10px] rounded p-1" />
                            )}
                          </div>
                        )}
                        
                        {videoDetails?.video_url ? (
                          <div className="space-y-2">
                            <Text strong className="text-slate-800 text-xs">Video bài giảng đã xuất bản:</Text>
                            <div className="w-full bg-black rounded-lg overflow-hidden border aspect-video">
                              <video 
                                controls 
                                className="w-full h-full" 
                                src={videoDetails.video_url} 
                                key={videoDetails.video_url}
                              />
                            </div>
                            <Button 
                              type="primary" 
                              ghost 
                              block 
                              icon={<Download size={14} />}
                              href={videoDetails.video_url}
                              download
                            >
                              Tải video MP4 chất lượng cao
                            </Button>
                          </div>
                        ) : (
                          <div className="p-8 text-center bg-slate-50 border rounded-lg">
                            <Video size={32} className="mx-auto text-slate-300 mb-2" />
                            <Text type="secondary" className="text-xs">Chưa có video được render cho bài học này.</Text>
                          </div>
                        )}
                      </div>
                    )
                  }
                ]}
              />
            </Col>
          </Row>
        )}
      </Modal>
    </div>
  );
}
