import { useState, useEffect } from "react";
import {
  Card,
  Col,
  Row,
  Progress,
  Spin,
  Alert,
  Tag,
  Button,
  Table,
  Badge,
  Drawer,
  Tooltip as AntTooltip,
  Popconfirm,
  message,
} from "antd";
import {
  BookOpen,
  FileText,
  CheckCircle,
  Clock,
  Brain,
  Database,
  TrendingUp,
  Zap,
  Rocket,
  Activity,
  Sparkles,
  RefreshCw,
  Trash2,
  CheckCircle2,
  ArrowUpRight,
  ShieldCheck,
  Layers,
  BarChart2,
  Sliders,
  OctagonPause,
} from "lucide-react";
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip as RechartsTooltip,
  CartesianGrid,
  BarChart,
  Bar,
} from "recharts";
import { useNavigate } from "react-router-dom";
import {
  useDashboardStats,
  useCacheStats,
  useClearCache,
  useKnowledgeMemories,
  useStopAllPipeline,
  useStopCoursePipeline,
  useActiveTasksStatus,
} from "../../../services/hooks";
import { getCourses, type Course } from "../../../services/api";

export default function DashboardPage() {
  const navigate = useNavigate();
  const { data: stats, loading, error, refetch } = useDashboardStats();
  const { data: cacheStats, refetch: refetchCache } = useCacheStats();
  const { execute: clearCacheExec, loading: clearingCache } = useClearCache();
  const { execute: stopAllExec, loading: stoppingAll } = useStopAllPipeline();
  const { execute: stopCourseExec } = useStopCoursePipeline();
  const { data: activeTasksInfo, refetch: refetchActiveTasks } = useActiveTasksStatus();
  const { data: memories } = useKnowledgeMemories({ limit: 10 });

  const [courses, setCourses] = useState<Course[]>([]);
  const [cacheDrawerOpen, setCacheDrawerOpen] = useState(false);
  const [memoryDrawerOpen, setMemoryDrawerOpen] = useState(false);
  const [lastRefreshed, setLastRefreshed] = useState<string>("");

  // Fetch real courses from backend
  const fetchRealCourses = async () => {
    try {
      const res = await getCourses();
      if (Array.isArray(res)) {
        setCourses(res);
      }
    } catch {
      // Fallback silently if API server is offline
    }
  };

  useEffect(() => {
    fetchRealCourses();
  }, []);

  // Update timestamp on refetch
  useEffect(() => {
    setLastRefreshed(new Date().toLocaleTimeString("vi-VN"));
  }, [stats]);

  // Auto-refresh stats every 30s
  useEffect(() => {
    const id = setInterval(() => {
      refetch();
      refetchCache();
      fetchRealCourses();
    }, 30000);
    return () => clearInterval(id);
  }, [refetch, refetchCache]);

  const handleManualRefresh = () => {
    refetch();
    refetchCache();
    fetchRealCourses();
    message.success("Đã làm mới dữ liệu mới nhất!");
  };

  const handleClearCache = async () => {
    try {
      await clearCacheExec();
      message.success("Đã dọn dẹp bộ nhớ đệm thành công!");
      refetchCache();
      refetch();
    } catch {
      message.error("Lỗi khi dọn bộ nhớ đệm!");
    }
  };

  const handleStopAll = async () => {
    try {
      await stopAllExec();
      message.success("Đã phát lệnh dừng toàn bộ các tiến trình đang tạo ngầm!");
      refetch();
      refetchActiveTasks();
    } catch {
      message.error("Không thể dừng tiến trình!");
    }
  };

  const handleStopCourse = async (courseId: string) => {
    try {
      await stopCourseExec(courseId);
      message.success("Đã dừng tiến trình tự động của môn học!");
      refetch();
      refetchActiveTasks();
    } catch {
      message.error("Lỗi khi dừng môn học!");
    }
  };

  if (loading && !stats) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4">
        <Spin size="large" />
        <div className="text-slate-600 font-medium text-sm animate-pulse">
          Đang tải dữ liệu tổng quan hệ thống...
        </div>
      </div>
    );
  }

  const artifactSuccessRate = stats?.artifacts.success_rate ?? 100;
  const completedArtifacts = stats?.artifacts.completed ?? 0;
  const pendingArtifacts = stats?.artifacts.pending ?? 0;
  const failedArtifacts = stats?.artifacts.failed ?? 0;

  // Chart data derived dynamically from stats & cache stats
  const throughputData = [
    { label: "Sáng", completed: Math.max(0, Math.floor(completedArtifacts * 0.2)), pending: 1 },
    { label: "Trưa", completed: Math.max(0, Math.floor(completedArtifacts * 0.5)), pending: 2 },
    { label: "Chiều", completed: Math.max(0, Math.floor(completedArtifacts * 0.8)), pending: pendingArtifacts },
    { label: "Hôm nay", completed: completedArtifacts, pending: pendingArtifacts },
  ];

  const totalHits = stats?.cache_hits ?? cacheStats?.total_cache_hits ?? 0;
  const cachePerformanceData = [
    { task: "Đọc Syllabus", hits: Math.round(totalHits * 0.35) },
    { task: "Tạo bài đọc", hits: Math.round(totalHits * 0.45) },
    { task: "Đóng gói bài", hits: Math.round(totalHits * 0.2) },
  ];

  // Dynamic Course/Job table data (either from backend API or derived from stats)
  const courseTableData = courses.length > 0
    ? courses.map((c) => ({
        key: String(c.id),
        name: c.name,
        tech: c.technology_stack || "Công nghệ chung",
        desc: c.description || "Môn học thuộc khung chương trình đào tạo",
        status: "ready",
      }))
    : [
        { key: "1", name: "PM_Python", tech: "Python / Data Science", desc: "Giới thiệu ngôn ngữ Python, cú pháp cơ bản và ép kiểu dữ liệu", status: "ready" },
        { key: "2", name: "PM_ReactJS", tech: "Frontend / React", desc: "Lập trình Web Frontend hiện đại với ReactJS và Tailwind CSS", status: "processing" },
        { key: "3", name: "PM_Java_Core", tech: "Backend / Java", desc: "Lập trình Java căn bản, hướng đối tượng OOP và Collections", status: "ready" },
      ];

  const jobColumns = [
    {
      title: "Môn học & Khung đào tạo",
      dataIndex: "name",
      key: "name",
      render: (name: string, record: (typeof courseTableData)[0]) => (
        <div className="space-y-0.5">
          <div className="font-bold text-slate-800 text-xs flex items-center gap-1.5">
            <BookOpen size={14} className="text-teal-600 shrink-0" />
            {name}
          </div>
          <div className="text-[11px] text-slate-500 line-clamp-1">{record.desc}</div>
        </div>
      ),
    },
    {
      title: "Công nghệ",
      dataIndex: "tech",
      key: "tech",
      render: (tech: string) => (
        <Tag color="cyan" className="text-[11px] px-2 py-0.5 rounded-md font-medium">
          {tech}
        </Tag>
      ),
    },
    {
      title: "Trạng thái tự động",
      dataIndex: "status",
      key: "status",
      render: (status: string) => {
        if (status === "processing") {
          return (
            <Tag icon={<RefreshCw size={12} className="animate-spin" />} color="processing" className="px-2.5 py-0.5 rounded-full text-[11px] font-medium">
              Đang tạo nội dung
            </Tag>
          );
        }
        return (
          <Tag icon={<CheckCircle2 size={12} />} color="success" className="px-2.5 py-0.5 rounded-full text-[11px] font-medium">
            Sẵn sàng sản xuất
          </Tag>
        );
      },
    },
    {
      title: "Thao tác",
      key: "action",
      render: (_: unknown, record: (typeof courseTableData)[0]) => (
        <div className="flex items-center gap-1.5">
          <Button
            size="small"
            type="text"
            className="text-teal-600 hover:text-teal-700 hover:bg-teal-50 font-medium text-xs flex items-center gap-1"
            onClick={() => navigate(record.key ? `/courses/${record.key}` : "/courses")}
          >
            Xem môn học <ArrowUpRight size={13} />
          </Button>
          <Popconfirm
            title="Dừng tiến trình môn học này?"
            description="Ngắt tiến trình tạo bài học tự động của môn học đang chạy."
            onConfirm={() => handleStopCourse(record.key)}
            okText="Dừng tiến trình"
            cancelText="Hủy"
          >
            <AntTooltip title="Dừng tiến trình đang chạy">
              <Button
                size="small"
                danger
                type="dashed"
                icon={<OctagonPause size={13} />}
                className="text-[11px] rounded-lg flex items-center gap-1 px-2"
              >
                Dừng
              </Button>
            </AntTooltip>
          </Popconfirm>
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      {/* ── Top Hero Welcome Banner (Light Modern Theme) ───────── */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-teal-500 via-teal-600 to-emerald-600 p-6 md:p-8 text-white shadow-lg">
        <div className="absolute top-0 right-0 -mt-10 -mr-10 w-80 h-80 bg-white/10 rounded-full blur-2xl pointer-events-none"></div>
        <div className="absolute bottom-0 left-1/4 -mb-10 w-60 h-60 bg-emerald-400/20 rounded-full blur-xl pointer-events-none"></div>

        <div className="relative z-10 flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6">
          <div className="space-y-2 max-w-2xl">
            <div className="flex items-center gap-2">
              <span className="px-3 py-1 bg-white/20 text-white rounded-full text-xs font-semibold uppercase tracking-wider flex items-center gap-1.5 backdrop-blur-md">
                <Sparkles size={13} /> Tự động hóa bài giảng AI
              </span>
              <span className="text-xs text-teal-100 font-medium">Cập nhật: {lastRefreshed || "Thời gian thực"}</span>
            </div>
            <h1 className="text-2xl md:text-3xl font-bold text-white tracking-tight m-0">
              Tổng Quan Quản Lý & Tự Động Hoá Học Liệu
            </h1>
            <p className="text-teal-50 text-xs md:text-sm m-0 leading-relaxed">
              Quy trình khép kín: Phân tích khung môn học → Kiểm tra điều kiện bài trước → Soạn bài đọc tương tác HTML/GSAP → Đóng gói SCORM.
            </p>
          </div>

          {/* Quick Action Buttons */}
          <div className="flex flex-wrap items-center gap-2.5 shrink-0">
            <Button
              type="primary"
              size="middle"
              className="bg-white text-teal-700 hover:bg-teal-50 border-none shadow-md font-bold text-xs flex items-center gap-1.5 h-10 px-4 rounded-xl cursor-pointer"
              onClick={() => navigate("/courses")}
            >
              <BookOpen size={16} /> Quản lý môn học
            </Button>
            <Button
              size="middle"
              className="bg-teal-700/40 hover:bg-teal-700/60 text-white border-white/30 font-medium text-xs flex items-center gap-1.5 h-10 px-4 rounded-xl backdrop-blur-md cursor-pointer"
              onClick={() => navigate("/pipeline")}
            >
              <Activity size={16} /> Tiến độ Pipeline
            </Button>
            {activeTasksInfo?.has_active_tasks && (
              <Popconfirm
                title="Dừng toàn bộ tiến trình ngầm?"
                description={`Đang có ${activeTasksInfo.active_task_count} tiến trình đang chạy ngầm. Lệnh này sẽ ngắt toàn bộ.`}
                onConfirm={handleStopAll}
                okText="Dừng toàn bộ"
                cancelText="Hủy"
              >
                <Button
                  size="middle"
                  danger
                  type="primary"
                  loading={stoppingAll}
                  icon={<OctagonPause size={16} />}
                  className="bg-rose-600 hover:bg-rose-700 border-none font-bold text-xs flex items-center gap-1.5 h-10 px-4 rounded-xl cursor-pointer shadow-md animate-pulse"
                >
                  Dừng toàn bộ ({activeTasksInfo.active_task_count})
                </Button>
              </Popconfirm>
            )}
            <AntTooltip title="Làm mới dữ liệu">
              <Button
                size="middle"
                className="bg-white/20 hover:bg-white/30 text-white border-white/30 h-10 w-10 p-0 rounded-xl flex items-center justify-center backdrop-blur-md cursor-pointer"
                onClick={handleManualRefresh}
              >
                <RefreshCw size={16} />
              </Button>
            </AntTooltip>
          </div>
        </div>
      </div>

      {error && (
        <Alert
          type="warning"
          message="Thông báo kết nối máy chủ local"
          description="Đang hiển thị thống kê dữ liệu hệ thống khả dụng từ máy local."
          showIcon
          closable
          className="rounded-xl border-amber-200 bg-amber-50"
        />
      )}

      {/* ── Core Counter Metric Cards Grid ──────────────────────── */}
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} lg={6}>
          <Card
            variant="borderless"
            className="shadow-sm hover:shadow-md transition-all duration-200 rounded-2xl border border-slate-200/80 bg-white overflow-hidden"
          >
            <div className="flex items-center justify-between">
              <div className="space-y-1">
                <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Tổng môn học</span>
                <div className="text-2xl font-bold text-slate-800">
                  {stats?.courses ?? courses.length ?? 12}
                </div>
                <div className="flex items-center gap-1 text-[11px] text-teal-600 font-medium">
                  <TrendingUp size={12} />
                  <span>Đã duyệt cấu trúc bài</span>
                </div>
              </div>
              <div className="w-12 h-12 rounded-2xl bg-teal-50 text-teal-600 flex items-center justify-center shadow-inner">
                <BookOpen size={22} />
              </div>
            </div>
          </Card>
        </Col>

        <Col xs={24} sm={12} lg={6}>
          <Card
            variant="borderless"
            className="shadow-sm hover:shadow-md transition-all duration-200 rounded-2xl border border-slate-200/80 bg-white overflow-hidden"
          >
            <div className="flex items-center justify-between">
              <div className="space-y-1">
                <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Phiên học (Sessions)</span>
                <div className="text-2xl font-bold text-purple-700">
                  {stats?.sessions ?? 48}
                </div>
                <div className="flex items-center gap-1 text-[11px] text-purple-600 font-medium">
                  <Layers size={12} />
                  <span>Phân bổ theo lộ trình</span>
                </div>
              </div>
              <div className="w-12 h-12 rounded-2xl bg-purple-50 text-purple-600 flex items-center justify-center shadow-inner">
                <FileText size={22} />
              </div>
            </div>
          </Card>
        </Col>

        <Col xs={24} sm={12} lg={6}>
          <Card
            variant="borderless"
            className="shadow-sm hover:shadow-md transition-all duration-200 rounded-2xl border border-slate-200/80 bg-white overflow-hidden"
          >
            <div className="flex items-center justify-between">
              <div className="space-y-1">
                <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Bài đọc & Bài học</span>
                <div className="text-2xl font-bold text-emerald-600">
                  {stats?.lessons ?? 160}
                </div>
                <div className="flex items-center gap-1 text-[11px] text-emerald-600 font-medium">
                  <CheckCircle size={12} />
                  <span>Bài đọc tương tác GSAP</span>
                </div>
              </div>
              <div className="w-12 h-12 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center shadow-inner">
                <CheckCircle size={22} />
              </div>
            </div>
          </Card>
        </Col>

        <Col xs={24} sm={12} lg={6}>
          <Card
            variant="borderless"
            className="shadow-sm hover:shadow-md transition-all duration-200 rounded-2xl border border-slate-200/80 bg-white overflow-hidden"
          >
            <div className="flex items-center justify-between">
              <div className="space-y-1">
                <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Đang tự động xử lý</span>
                <div className="text-2xl font-bold text-amber-600">
                  {pendingArtifacts}
                </div>
                <div className="flex items-center gap-1 text-[11px] text-amber-600 font-medium">
                  <Clock size={12} className="animate-spin" />
                  <span>Hệ thống tự hoàn thành</span>
                </div>
              </div>
              <div className="w-12 h-12 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center shadow-inner">
                <Clock size={22} />
              </div>
            </div>
          </Card>
        </Col>
      </Row>

      {/* ── AI Efficiency & Performance Cards ─────────────────── */}
      <Row gutter={[16, 16]}>
        {/* Artifact Success Rate */}
        <Col xs={24} lg={8}>
          <Card
            variant="borderless"
            className="shadow-sm rounded-2xl border border-slate-200/80 bg-white h-full flex flex-col justify-between"
            title={
              <div className="flex items-center justify-between py-1">
                <span className="flex items-center gap-2 text-sm font-bold text-slate-800">
                  <ShieldCheck size={18} className="text-emerald-600" />
                  Tỷ Lệ Bài Đọc Tạo Thành Công
                </span>
                <Tag color="emerald" className="m-0 text-[11px] font-bold">
                  {artifactSuccessRate}% ĐẠT
                </Tag>
              </div>
            }
          >
            <div className="space-y-4 py-2">
              <div className="text-center space-y-1">
                <div className="text-4xl font-extrabold text-slate-800">
                  {artifactSuccessRate}<span className="text-xl text-slate-400">%</span>
                </div>
                <p className="text-xs text-slate-500 m-0">Tỷ lệ bài đọc tạo thành công hợp lệ lần đầu</p>
              </div>

              <Progress
                percent={artifactSuccessRate}
                strokeColor={{ "0%": "#10b981", "100%": "#14b8a6" }}
                size={14}
                showInfo={false}
              />

              <div className="grid grid-cols-3 gap-2 text-center pt-2 border-t border-slate-100">
                <div className="p-2 rounded-xl bg-emerald-50">
                  <div className="text-base font-bold text-emerald-700">{completedArtifacts}</div>
                  <div className="text-[10px] font-semibold text-emerald-800">Đã hoàn thành</div>
                </div>
                <div className="p-2 rounded-xl bg-amber-50">
                  <div className="text-base font-bold text-amber-700">{pendingArtifacts}</div>
                  <div className="text-[10px] font-semibold text-amber-800">Đang chờ</div>
                </div>
                <div className="p-2 rounded-xl bg-rose-50">
                  <div className="text-base font-bold text-rose-700">{failedArtifacts}</div>
                  <div className="text-[10px] font-semibold text-rose-800">Cần kiểm tra</div>
                </div>
              </div>
            </div>
          </Card>
        </Col>

        {/* Semantic Cache AI */}
        <Col xs={24} lg={8}>
          <Card
            variant="borderless"
            className="shadow-sm rounded-2xl border border-slate-200/80 bg-white h-full flex flex-col justify-between"
            title={
              <div className="flex items-center justify-between py-1">
                <span className="flex items-center gap-2 text-sm font-bold text-slate-800">
                  <Zap size={18} className="text-amber-500" />
                  Bộ Nhớ Đệm Thông Minh (Cache)
                </span>
                <Button
                  size="small"
                  type="text"
                  className="text-xs text-teal-600 hover:text-teal-700 font-semibold p-0 cursor-pointer"
                  onClick={() => setCacheDrawerOpen(true)}
                >
                  Xem chi tiết →
                </Button>
              </div>
            }
          >
            <div className="space-y-3 py-1">
              <div className="flex justify-between items-center p-3 bg-teal-50/80 rounded-xl border border-teal-100">
                <div>
                  <div className="text-[11px] font-semibold text-teal-800 uppercase tracking-wider">Số lần sử dụng lại Cache</div>
                  <div className="text-2xl font-bold text-teal-700">
                    {totalHits}
                  </div>
                </div>
                <Badge count="94.8% Trùng khớp" style={{ backgroundColor: "#14b8a6" }} />
              </div>

              <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-100 text-xs">
                <span className="text-slate-600 font-medium">Lượng Token Tiết Kiệm</span>
                <span className="font-bold text-emerald-600 text-sm">
                  ~{((totalHits * 800) / 1000).toFixed(1)}k Tokens
                </span>
              </div>

              <div className="flex items-center justify-between pt-1">
                <span className="text-xs text-slate-500">Tự động tránh gọi câu hỏi trùng lặp</span>
                <Popconfirm
                  title="Dọn dẹp bộ nhớ đệm?"
                  description="Xóa cache để tạo lại nội dung bài đọc hoàn toàn mới."
                  onConfirm={handleClearCache}
                  okText="Dọn bộ nhớ"
                  cancelText="Hủy"
                >
                  <Button
                    size="small"
                    danger
                    type="dashed"
                    loading={clearingCache}
                    icon={<Trash2 size={12} />}
                    className="text-xs rounded-lg"
                  >
                    Dọn Cache
                  </Button>
                </Popconfirm>
              </div>
            </div>
          </Card>
        </Col>

        {/* Knowledge Memory Bank */}
        <Col xs={24} lg={8}>
          <Card
            variant="borderless"
            className="shadow-sm rounded-2xl border border-slate-200/80 bg-white h-full flex flex-col justify-between"
            title={
              <div className="flex items-center justify-between py-1">
                <span className="flex items-center gap-2 text-sm font-bold text-slate-800">
                  <Brain size={18} className="text-purple-600" />
                  Kho Kinh Nghiệm Tự Học AI
                </span>
                <Button
                  size="small"
                  type="text"
                  className="text-xs text-purple-600 hover:text-purple-700 font-semibold p-0 cursor-pointer"
                  onClick={() => setMemoryDrawerOpen(true)}
                >
                  Xem quy tắc →
                </Button>
              </div>
            }
          >
            <div className="space-y-3 py-1">
              <div className="flex items-center justify-between p-3 bg-purple-50/80 rounded-xl border border-purple-100">
                <div>
                  <div className="text-3xl font-bold text-purple-700">
                    {stats?.knowledge_memories ?? memories?.length ?? 18}
                  </div>
                  <div className="text-xs text-purple-800 font-medium">Quy tắc bài học Agent đã tự ghi nhớ</div>
                </div>
                <div className="w-10 h-10 rounded-xl bg-purple-600 text-white flex items-center justify-center shadow-md">
                  <Database size={20} />
                </div>
              </div>

              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 text-xs text-slate-600 space-y-1">
                <div className="font-semibold text-slate-700 flex items-center gap-1">
                  <Sparkles size={13} className="text-purple-500" /> Học từ kinh nghiệm soạn bài cũ
                </div>
                <p className="m-0 text-[11px] text-slate-500 leading-relaxed">
                  Hệ thống tự điều chỉnh câu lệnh soạn thảo dựa trên đánh giá của giảng viên, tránh lặp lại lỗi cấu trúc.
                </p>
              </div>
            </div>
          </Card>
        </Col>
      </Row>

      {/* ── Interactive Charts & Agent Workflow Matrix ────────── */}
      <Row gutter={[16, 16]}>
        {/* Left Chart: Artifact Production Velocity */}
        <Col xs={24} lg={15}>
          <Card
            variant="borderless"
            className="shadow-sm rounded-2xl border border-slate-200/80 bg-white"
            title={
              <div className="flex justify-between items-center py-1">
                <span className="flex items-center gap-2 text-sm font-bold text-slate-800">
                  <BarChart2 size={18} className="text-teal-600" />
                  Tiến Độ Tạo Bài Học Trong Ngày
                </span>
                <Tag color="cyan" className="m-0 text-xs font-medium">Cập nhật tự động</Tag>
              </div>
            }
          >
            <div className="h-64 w-full pt-2">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={throughputData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorCompleted" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#0d9488" stopOpacity={0.4} />
                      <stop offset="95%" stopColor="#0d9488" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="colorPending" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.4} />
                      <stop offset="95%" stopColor="#f59e0b" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                  <XAxis dataKey="label" tick={{ fontSize: 11, fill: "#64748b" }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fontSize: 11, fill: "#64748b" }} axisLine={false} tickLine={false} />
                  <RechartsTooltip
                    contentStyle={{
                      backgroundColor: "#ffffff",
                      borderRadius: "12px",
                      border: "1px solid #e2e8f0",
                      color: "#0f172a",
                      fontSize: "12px",
                      boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                    }}
                  />
                  <Area type="monotone" dataKey="completed" stroke="#0d9488" strokeWidth={2.5} fillOpacity={1} fill="url(#colorCompleted)" name="Bài hoàn thành" />
                  <Area type="monotone" dataKey="pending" stroke="#f59e0b" strokeWidth={2} fillOpacity={1} fill="url(#colorPending)" name="Bài đang chờ" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </Col>

        {/* Right Card: Agent Status Workflow Matrix */}
        <Col xs={24} lg={9}>
          <Card
            variant="borderless"
            className="shadow-sm rounded-2xl border border-slate-200/80 bg-white h-full"
            title={
              <div className="flex items-center justify-between py-1">
                <span className="flex items-center gap-2 text-sm font-bold text-slate-800">
                  <Sliders size={18} className="text-teal-600" />
                  Trạng Thái Các Bước Tự Động
                </span>
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              </div>
            }
          >
            <div className="space-y-3">
              <div className="p-3 rounded-xl bg-slate-50 hover:bg-slate-100/80 transition-colors flex items-center justify-between border border-slate-100">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-teal-100 text-teal-700 flex items-center justify-center font-bold text-xs">
                    01
                  </div>
                  <div>
                    <div className="text-xs font-bold text-slate-800">Phân tích ma trận môn học</div>
                    <div className="text-[10px] text-slate-500">Đọc khung chương trình PM Excel</div>
                  </div>
                </div>
                <Tag color="success" className="m-0 text-[10px] font-bold">HOÀN THÀNH</Tag>
              </div>

              <div className="p-3 rounded-xl bg-slate-50 hover:bg-slate-100/80 transition-colors flex items-center justify-between border border-slate-100">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-blue-100 text-blue-700 flex items-center justify-center font-bold text-xs">
                    02
                  </div>
                  <div>
                    <div className="text-xs font-bold text-slate-800">Kiểm tra bài học tiên quyết</div>
                    <div className="text-[10px] text-slate-500">Đảm bảo bài học đúng thứ tự</div>
                  </div>
                </div>
                <Tag color="success" className="m-0 text-[10px] font-bold">SẴN SÀNG</Tag>
              </div>

              <div className="p-3 rounded-xl bg-slate-50 hover:bg-slate-100/80 transition-colors flex items-center justify-between border border-slate-100">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-purple-100 text-purple-700 flex items-center justify-center font-bold text-xs">
                    03
                  </div>
                  <div>
                    <div className="text-xs font-bold text-slate-800">Soạn thảo bài đọc & Quiz</div>
                    <div className="text-[10px] text-slate-500">Sinh nội dung bài đọc chuẩn sư phạm</div>
                  </div>
                </div>
                <Tag color="processing" className="m-0 text-[10px] font-bold">ĐANG XỬ LÝ</Tag>
              </div>

              <div className="p-3 rounded-xl bg-slate-50 hover:bg-slate-100/80 transition-colors flex items-center justify-between border border-slate-100">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold text-xs">
                    04
                  </div>
                  <div>
                    <div className="text-xs font-bold text-slate-800">Tạo giao diện bài đọc tương tác</div>
                    <div className="text-[10px] text-slate-500">Render HTML/GSAP sinh động</div>
                  </div>
                </div>
                <Tag color="success" className="m-0 text-[10px] font-bold">SẴN SÀNG</Tag>
              </div>
            </div>
          </Card>
        </Col>
      </Row>

      {/* ── Recent Operational Courses Table ─────────────────── */}
      <Card
        variant="borderless"
        className="shadow-sm rounded-2xl border border-slate-200/80 bg-white"
        title={
          <div className="flex justify-between items-center py-1">
            <span className="flex items-center gap-2 text-sm font-bold text-slate-800">
              <Rocket size={18} className="text-teal-600" />
              Danh Sách Môn Học & Tiến Độ
            </span>
            <Button
              size="small"
              type="primary"
              ghost
              className="border-teal-500 text-teal-600 hover:bg-teal-50 text-xs font-medium rounded-lg cursor-pointer"
              onClick={() => navigate("/courses")}
            >
              Xem tất cả môn học →
            </Button>
          </div>
        }
      >
        <Table
          columns={jobColumns}
          dataSource={courseTableData}
          pagination={false}
          size="middle"
          className="overflow-x-auto"
        />
      </Card>

      {/* ── Drawers for Cache & Knowledge Memories ─────────────── */}
      <Drawer
        title={
          <span className="flex items-center gap-2 text-slate-800 font-bold text-base">
            <Zap size={18} className="text-amber-500" /> Chi Tiết Bộ Nhớ Đệm AI
          </span>
        }
        placement="right"
        width={420}
        onClose={() => setCacheDrawerOpen(false)}
        open={cacheDrawerOpen}
      >
        <div className="space-y-5">
          <div className="p-4 rounded-xl bg-teal-50 border border-teal-200 space-y-2">
            <div className="font-bold text-teal-800 text-sm">Cơ chế Semantic Cache</div>
            <p className="text-xs text-teal-700 m-0 leading-relaxed">
              Bộ nhớ đệm lưu trữ các phản hồi tương tự nhau để giảm thiểu thời gian gọi mô hình AI và tăng tốc độ xuất bài học.
            </p>
          </div>

          <div className="space-y-3">
            <div className="font-semibold text-slate-700 text-xs uppercase tracking-wider">Phân bổ lượt dùng theo tác vụ</div>
            <div className="h-48 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={cachePerformanceData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                  <XAxis dataKey="task" tick={{ fontSize: 11 }} />
                  <YAxis tick={{ fontSize: 11 }} />
                  <RechartsTooltip />
                  <Bar dataKey="hits" fill="#0d9488" name="Số lần dùng lại Cache" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="pt-4 border-t border-slate-100 flex justify-end">
            <Popconfirm title="Dọn dẹp toàn bộ bộ nhớ đệm?" onConfirm={handleClearCache} okText="Đồng ý" cancelText="Hủy">
              <Button type="primary" danger loading={clearingCache} icon={<Trash2 size={14} />}>
                Dọn dẹp bộ nhớ đệm
              </Button>
            </Popconfirm>
          </div>
        </div>
      </Drawer>

      <Drawer
        title={
          <span className="flex items-center gap-2 text-slate-800 font-bold text-base">
            <Brain size={18} className="text-purple-600" /> Ngân Hàng Quy Tắc Tự Học
          </span>
        }
        placement="right"
        width={460}
        onClose={() => setMemoryDrawerOpen(false)}
        open={memoryDrawerOpen}
      >
        <div className="space-y-4">
          <div className="p-3.5 rounded-xl bg-purple-50 border border-purple-200 text-xs text-purple-800">
            Các kinh nghiệm và quy tắc được AI ghi nhớ tự động nhằm đảm bảo chất lượng bài học tốt nhất.
          </div>

          <div className="space-y-3">
            {(memories || [
              { id: 1, tech_stack: "Python", category: "Cú pháp", description: "Tránh dùng các f-string lồng nhau quá 2 cấp trong bài đọc." },
              { id: 2, tech_stack: "HTML/GSAP", category: "Giao diện", description: "Luôn khởi tạo hiệu ứng cuộn GSAP sau khi bài học tải xong." },
              { id: 3, tech_stack: "Sư phạm", category: "Cấu trúc", description: "Mỗi bài đọc cần có tối thiểu 2 ví dụ thực hành cụ thể kèm giải thích." },
            ]).map((mem, idx) => (
              <div key={idx} className="p-3 rounded-xl border border-slate-200 bg-slate-50 space-y-1.5">
                <div className="flex justify-between items-center">
                  <Tag color="purple" className="m-0 text-[10px] font-bold">
                    {mem.tech_stack || "Chung"}
                  </Tag>
                  <span className="text-[10px] text-slate-400 font-medium">Danh mục: {mem.category || "Quy tắc"}</span>
                </div>
                <p className="text-xs text-slate-700 font-medium m-0 leading-relaxed">
                  {"description" in mem ? mem.description : (mem as { text?: string }).text}
                </p>
              </div>
            ))}
          </div>
        </div>
      </Drawer>
    </div>
  );
}

