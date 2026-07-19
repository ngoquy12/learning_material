import { useState, useEffect, useMemo } from "react";
import { useParams, useNavigate, useSearchParams } from "react-router-dom";
import {
  Card,
  Button,
  Spin,
  Empty,
  Tooltip,
  Upload,
  Popconfirm,
  message,
} from "antd";
import { marked } from "marked";
import {
  Plus,
  ArrowLeft,
  PlayCircle,
  Layers,
  Settings2,
  UploadCloud,
  Rocket,
  Eye,
  Trash2,
  GripVertical,
  ChevronDown,
  ChevronRight,
  BookOpen,
} from "lucide-react";
import {
  useCourse,
  useParseExcel,
  useConfirmImport,
  PMRow,
  useGenerateAllCourse,
} from "../hooks/useCourses";
import {
  useSessions,
  useCreateSession,
  useDeleteSession,
  useReorderSessions,
  useGenerateSession,
  useGeneratePracticeSession,
  useGenerateProjectSession,
  useSessionArtifacts,
} from "../../sessions/hooks/useSessions";
import {
  useLessons,
  useCreateLesson,
  useGenerateLesson,
  useDeleteLesson,
  useReorderLessons,
  useArtifacts,
  ArtifactResponse,
} from "../../lessons/hooks/useLessons";
import { SessionFormModal } from "../../sessions/components/SessionFormModal";
import { LessonFormModal } from "../../lessons/components/LessonFormModal";
import { PMPreviewModal } from "../components/PMPreviewModal";
import { ArtifactPreviewModal } from "../../lessons/components/ArtifactPreviewModal";

import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragEndEvent,
} from "@dnd-kit/core";
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
  useSortable,
} from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import { SessionResponse } from "../../../types/session";
import { LessonResponse } from "../../../types/lesson";

interface SortableSessionItemProps {
  session: SessionResponse;
  isExpanded: boolean;
  onToggle: () => void;
  onAddLesson: () => void;
  onDelete: () => void;
  onPreviewArtifact: (id: number, title: string) => void;
  onPreviewSessionArtifact?: (
    id: number,
    title: string,
    exerciseIndex?: number | null,
  ) => void;
  onGenerateSession: (id: number) => void;
  isGenerating?: boolean;
}

interface SortableLessonItemProps {
  lesson: LessonResponse;
  onPreviewArtifact?: (id: number, title: string) => void;
}

export default function CourseDetailPage() {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const parsedCourseId = Number(courseId);

  const { data: course, isLoading: isLoadingCourse } =
    useCourse(parsedCourseId);
  const { data: sessions, isLoading: isLoadingSessions } =
    useSessions(parsedCourseId);

  const [isSessionModalOpen, setIsSessionModalOpen] = useState(false);
  const [activeSessionId, setActiveSessionId] = useState<number | null>(null);
  const [isLessonModalOpen, setIsLessonModalOpen] = useState(false);
  const [expandedSessionIds, setExpandedSessionIds] = useState<number[]>([]);

  const [searchParams, setSearchParams] = useSearchParams();
  const paramLessonId = searchParams.get("previewLessonId");
  const paramSessionId = searchParams.get("previewSessionId");

  const previewArtifactLesson = useMemo(() => {
    if (!paramLessonId) return null;
    return {
      id: Number(paramLessonId),
      title:
        searchParams.get("previewLessonTitle") || "Chi tiết tài nguyên bài học",
    };
  }, [paramLessonId, searchParams]);

  const paramExerciseIndex = searchParams.get("previewExerciseIndex");

  const previewArtifactSession = useMemo(() => {
    if (!paramSessionId) return null;
    return {
      id: Number(paramSessionId),
      title:
        searchParams.get("previewSessionTitle") ||
        "Chi tiết tài nguyên phiên học",
      exerciseIndex: paramExerciseIndex ? Number(paramExerciseIndex) : null,
    };
  }, [paramSessionId, searchParams, paramExerciseIndex]);

  const setPreviewArtifactLesson = (
    val: { id: number; title: string } | null,
  ) => {
    setSearchParams(
      (prev) => {
        if (val) {
          prev.set("previewLessonId", String(val.id));
          prev.set("previewLessonTitle", val.title);
        } else {
          prev.delete("previewLessonId");
          prev.delete("previewLessonTitle");
        }
        return prev;
      },
      { replace: true },
    );
  };

  const setPreviewArtifactSession = (
    val: { id: number; title: string; exerciseIndex?: number | null } | null,
  ) => {
    setSearchParams(
      (prev) => {
        if (val) {
          prev.set("previewSessionId", String(val.id));
          prev.set("previewSessionTitle", val.title);
          if (val.exerciseIndex !== undefined && val.exerciseIndex !== null) {
            prev.set("previewExerciseIndex", String(val.exerciseIndex));
          } else {
            prev.delete("previewExerciseIndex");
          }
        } else {
          prev.delete("previewSessionId");
          prev.delete("previewSessionTitle");
          prev.delete("previewExerciseIndex");
        }
        return prev;
      },
      { replace: true },
    );
  };
  const [previewData, setPreviewData] = useState<PMRow[] | null>(null);

  const { mutate: createSession, isPending: isCreatingSession } =
    useCreateSession();
  const { mutate: createLesson, isPending: isCreatingLesson } =
    useCreateLesson();
  const { mutate: deleteSession } = useDeleteSession();
  const { mutate: reorderSessions } = useReorderSessions();
  const { mutate: parseExcel, isPending: isParsing } = useParseExcel();
  const { mutate: confirmImport, isPending: isConfirming } = useConfirmImport();
  const { mutate: generateAllCourse, isPending: isGeneratingAll } =
    useGenerateAllCourse();
  const {
    mutate: generateSession,
    isPending: isGeneratingSession,
    variables: generatingSessionId,
  } = useGenerateSession();
  const {
    mutate: generatePracticeSession,
    isPending: isGeneratingPractice,
    variables: generatingPracticeId,
  } = useGeneratePracticeSession();
  const {
    mutate: generateProjectSession,
    isPending: isGeneratingProject,
    variables: generatingProjectId,
  } = useGenerateProjectSession();

  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 5 } }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    }),
  );

  const handleDragEndSession = (event: DragEndEvent) => {
    const { active, over } = event;
    if (over && active.id !== over.id && sessions) {
      const oldIndex = sessions.findIndex((s) => s.id === active.id);
      const newIndex = sessions.findIndex((s) => s.id === over.id);
      const newArray = arrayMove(sessions, oldIndex, newIndex);
      reorderSessions({
        courseId: parsedCourseId,
        item_ids: newArray.map((i) => i.id),
      });
    }
  };

  const toggleSession = (id: number) => {
    setExpandedSessionIds((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id],
    );
  };

  if (isLoadingCourse || isLoadingSessions) {
    return (
      <div className="p-10 flex justify-center">
        <Spin size="large" />
      </div>
    );
  }

  if (!course) {
    return <Empty description="Không tìm thấy môn học!" />;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button
          icon={<ArrowLeft size={16} />}
          onClick={() => navigate("/courses")}
        />
        <div>
          <h2 className="text-2xl font-bold text-gray-800 m-0">
            {course.name}
          </h2>
          <p className="text-gray-500 m-0">
            Công nghệ: {course.technology_stack || "Trống"}
          </p>
        </div>
      </div>

      <Card
        title={
          <div className="flex justify-between items-center w-full">
            <span className="font-semibold text-lg flex items-center gap-2">
              <Layers size={20} className="text-blue-500" /> Danh sách Phiên học
              (Sessions)
            </span>
            <div className="flex gap-2">
              <Button
                type="primary"
                danger
                icon={<Rocket size={16} />}
                loading={isGeneratingAll}
                onClick={() => generateAllCourse(parsedCourseId)}
                disabled={sessions?.length === 0}
              >
                Tạo AI Toàn khóa
              </Button>
              <Upload
                accept=".xlsx,.xls"
                showUploadList={false}
                customRequest={({ file }) => {
                  parseExcel(
                    { courseId: parsedCourseId, file: file as File },
                    { onSuccess: (data) => setPreviewData(data) },
                  );
                }}
              >
                <Button icon={<UploadCloud size={16} />} loading={isParsing}>
                  Import Excel (PM)
                </Button>
              </Upload>
              <Button
                type="primary"
                icon={<Plus size={16} />}
                onClick={() => setIsSessionModalOpen(true)}
              >
                Thêm Session
              </Button>
            </div>
          </div>
        }
        className="shadow-sm"
      >
        {sessions?.length === 0 ? (
          <Empty description="Chưa có session nào. Hãy tạo mới!" />
        ) : (
          <DndContext
            sensors={sensors}
            collisionDetection={closestCenter}
            onDragEnd={handleDragEndSession}
          >
            <SortableContext
              items={sessions?.map((s) => s.id) || []}
              strategy={verticalListSortingStrategy}
            >
              <div className="space-y-3">
                {sessions?.map((session) => (
                  <SortableSessionItem
                    key={session.id}
                    session={session}
                    isExpanded={expandedSessionIds.includes(session.id)}
                    onToggle={() => toggleSession(session.id)}
                    onAddLesson={() => {
                      setActiveSessionId(session.id);
                      setIsLessonModalOpen(true);
                      if (!expandedSessionIds.includes(session.id))
                        toggleSession(session.id);
                    }}
                    onDelete={() => deleteSession(session.id)}
                    onPreviewArtifact={(id: number, title: string) =>
                      setPreviewArtifactLesson({ id, title })
                    }
                    onPreviewSessionArtifact={(
                      id: number,
                      title: string,
                      exerciseIndex?: number | null,
                    ) =>
                      setPreviewArtifactSession({ id, title, exerciseIndex })
                    }
                    onGenerateSession={(id: number) => {
                      const sess = sessions?.find((s) => s.id === id);
                      const sTitle = sess?.title?.toLowerCase() || "";
                      const sName = sess?.name?.toLowerCase() || "";
                      const isPractice =
                        sTitle.includes("thực hành") ||
                        sTitle.includes("practice") ||
                        sName.includes("thực hành") ||
                        sName.includes("practice");
                      const isProject =
                        sTitle.includes("mini project") ||
                        sTitle.includes("project") ||
                        sTitle.includes("dự án") ||
                        sName.includes("mini project") ||
                        sName.includes("project") ||
                        sName.includes("dự án");
                      if (isProject) {
                        generateProjectSession(id);
                      } else if (isPractice) {
                        generatePracticeSession(id);
                      } else {
                        generateSession(id);
                      }
                    }}
                    isGenerating={
                      (isGeneratingSession &&
                        generatingSessionId === session.id) ||
                      (isGeneratingPractice &&
                        generatingPracticeId === session.id) ||
                      (isGeneratingProject &&
                        generatingProjectId === session.id)
                    }
                  />
                ))}
              </div>
            </SortableContext>
          </DndContext>
        )}
      </Card>

      <PMPreviewModal
        open={!!previewData}
        courseId={parsedCourseId}
        initialData={previewData || []}
        isConfirming={isConfirming}
        onCancel={() => setPreviewData(null)}
        onConfirm={(data) => {
          confirmImport(
            { courseId: parsedCourseId, payload: data },
            { onSuccess: () => setPreviewData(null) },
          );
        }}
      />

      <ArtifactPreviewModal
        open={!!previewArtifactLesson}
        lessonId={previewArtifactLesson?.id || null}
        title={previewArtifactLesson?.title || ""}
        onCancel={() => setPreviewArtifactLesson(null)}
      />

      <ArtifactPreviewModal
        open={!!previewArtifactSession}
        sessionId={previewArtifactSession?.id || null}
        title={previewArtifactSession?.title || ""}
        exerciseIndex={previewArtifactSession?.exerciseIndex ?? null}
        onCancel={() => setPreviewArtifactSession(null)}
      />

      <SessionFormModal
        open={isSessionModalOpen}
        courseId={parsedCourseId}
        onCancel={() => setIsSessionModalOpen(false)}
        isPending={isCreatingSession}
        onSubmit={(data) =>
          createSession(data, { onSuccess: () => setIsSessionModalOpen(false) })
        }
      />
      {activeSessionId && (
        <LessonFormModal
          open={isLessonModalOpen}
          sessionId={activeSessionId}
          onCancel={() => setIsLessonModalOpen(false)}
          isPending={isCreatingLesson}
          onSubmit={(data) =>
            createLesson(data, { onSuccess: () => setIsLessonModalOpen(false) })
          }
        />
      )}
    </div>
  );
}

const SortableSessionItem = ({
  session,
  isExpanded,
  onToggle,
  onAddLesson,
  onDelete,
  onPreviewArtifact,
  onPreviewSessionArtifact,
  onGenerateSession,
  isGenerating,
}: SortableSessionItemProps) => {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: session.id });

  const { data: artifacts } = useSessionArtifacts(session.id);
  const isPending = artifacts?.some((a) => a.status === "Pending");
  const [prevPending, setPrevPending] = useState(false);
  useEffect(() => {
    if (prevPending && !isPending && artifacts && artifacts.length > 0) {
      const hasFailed = artifacts.some((a) => a.status === "Failed");
      if (hasFailed) {
        message.error({
          content: `Phiên học ${session.name} tạo tài nguyên thất bại!`,
          key: "generate-session",
          duration: 3,
        });
      } else {
        message.success({
          content: `Phiên học ${session.name} đã tạo xong tài nguyên thành công!`,
          key: "generate-session",
          duration: 3,
        });
      }
    }
    setPrevPending(!!isPending);
  }, [isPending, artifacts, session.name, prevPending]);

  const isPracticeSession =
    session.title?.toLowerCase().includes("thực hành") ||
    session.title?.toLowerCase().includes("practice") ||
    session.name?.toLowerCase().includes("thực hành") ||
    session.name?.toLowerCase().includes("practice");

  const isProjectSession =
    session.title?.toLowerCase().includes("mini project") ||
    session.title?.toLowerCase().includes("project") ||
    session.title?.toLowerCase().includes("dự án") ||
    session.name?.toLowerCase().includes("mini project") ||
    session.name?.toLowerCase().includes("project") ||
    session.name?.toLowerCase().includes("dự án");

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    zIndex: isDragging ? 10 : 1,
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={`border rounded-lg bg-white overflow-hidden ${isDragging ? "shadow-lg border-blue-400" : "border-gray-200"}`}
    >
      <div className="flex justify-between items-center bg-gray-50 p-3 border-b border-gray-100">
        <div className="flex items-center gap-3">
          <div
            {...attributes}
            {...listeners}
            className="cursor-grab p-1 hover:bg-gray-200 rounded text-gray-400"
          >
            <GripVertical size={16} />
          </div>
          <button
            onClick={onToggle}
            className="flex items-center gap-2 hover:text-blue-600 transition-colors"
          >
            {isExpanded ? (
              <ChevronDown size={18} />
            ) : (
              <ChevronRight size={18} />
            )}
            <span className="font-medium text-gray-700">
              {session.name}: {session.title}
            </span>
          </button>
        </div>
        <div className="flex gap-2">
          {!isPracticeSession && !isProjectSession && (
            <Button
              size="small"
              icon={<Plus size={14} />}
              onClick={onAddLesson}
            >
              Thêm Lesson
            </Button>
          )}
          <Popconfirm
            title="Xóa Session này?"
            description={
              isPracticeSession
                ? "Xóa session thực hành này?"
                : isProjectSession
                  ? "Xóa session dự án này?"
                  : "Tất cả Lesson bên trong sẽ bị xóa theo!"
            }
            onConfirm={onDelete}
            okText="Xóa"
            cancelText="Hủy"
            okButtonProps={{ danger: true }}
          >
            <Button size="small" danger icon={<Trash2 size={14} />} />
          </Popconfirm>
        </div>
      </div>

      {isExpanded && (
        <div className="p-4 bg-white space-y-4">
          <div
            className={`${isProjectSession ? "bg-purple-50/50 border-purple-100" : isPracticeSession ? "bg-indigo-50/50 border-indigo-100" : "bg-blue-50/50 border-blue-100"} p-3 rounded-lg border flex justify-between items-center`}
          >
            <div>
              <div
                className={`font-semibold ${isProjectSession ? "text-purple-900" : isPracticeSession ? "text-indigo-900" : "text-blue-900"} text-sm flex items-center gap-1.5`}
              >
                <Rocket
                  size={14}
                  className={
                    isProjectSession
                      ? "text-purple-600"
                      : isPracticeSession
                        ? "text-indigo-600"
                        : "text-blue-600"
                  }
                />{" "}
                {isProjectSession
                  ? "Tài nguyên Mini Project"
                  : isPracticeSession
                    ? "Tài nguyên thực hành (Phân tầng)"
                    : "Tài nguyên Session (Tổng hợp)"}
              </div>
              <div
                className={`text-xs ${isProjectSession ? "text-purple-700/80" : isPracticeSession ? "text-indigo-700/80" : "text-blue-700/80"}`}
              >
                {isProjectSession
                  ? "Tài liệu đặc tả SRS, Đề bài dự án & Bộ bài kiểm tra đầu giờ của dự án."
                  : isPracticeSession
                    ? "Bộ bài tập thực hành phân tầng từ cơ bản đến nâng cao cho học viên."
                    : "Quizz đầu giờ, Quizz cuối giờ, Sơ đồ tư duy & Bài đọc tổng hợp của session."}
              </div>
            </div>
            <div className="flex gap-2">
              <Button
                size="small"
                icon={<Eye size={14} />}
                onClick={() =>
                  navigate(`/courses/${courseId}/sessions/${session.id}/viewer`)
                }
                className={
                  isProjectSession
                    ? "text-purple-600 border-purple-600 hover:bg-purple-50"
                    : isPracticeSession
                      ? "text-indigo-600 border-indigo-600 hover:bg-indigo-50"
                      : "text-blue-600 border-blue-600 hover:bg-blue-50"
                }
                disabled={
                  isProjectSession
                    ? !artifacts?.some(
                        (a) =>
                          [
                            "project_entry_tests",
                            "project_srs",
                            "project_mini_project",
                          ].includes(a.type) && a.status === "Completed",
                      )
                    : !artifacts?.some(
                        (a) =>
                          a.type === "session_homework" &&
                          a.status === "Completed",
                      )
                }
              >
                Xem chi tiết
              </Button>
              <Button
                size="small"
                type="primary"
                icon={<PlayCircle size={14} />}
                loading={isGenerating || isPending}
                onClick={() => onGenerateSession(session.id)}
                className={
                  isProjectSession
                    ? "bg-purple-600 hover:bg-purple-700"
                    : isPracticeSession
                      ? "bg-indigo-600 hover:bg-indigo-700"
                      : ""
                }
              >
                {isPending
                  ? "AI đang tạo..."
                  : isProjectSession
                    ? "Tạo Mini Project"
                    : isPracticeSession
                      ? "Tạo bài thực hành"
                      : "Tạo AI Session"}
              </Button>
            </div>
          </div>

          {isProjectSession ? (
            <ProjectArtifactList
              session={session}
              artifacts={artifacts}
              onPreviewSessionArtifact={onPreviewSessionArtifact}
            />
          ) : isPracticeSession ? (
            <ExerciseList
              session={session}
              artifacts={artifacts}
              onPreviewSessionArtifact={onPreviewSessionArtifact}
            />
          ) : (
            <LessonList
              sessionId={session.id}
              onPreviewArtifact={onPreviewArtifact}
            />
          )}
        </div>
      )}
    </div>
  );
};

const LessonList = ({
  sessionId,
  onPreviewArtifact,
}: {
  sessionId: number;
  onPreviewArtifact: (id: number, title: string) => void;
}) => {
  const { data: lessons, isLoading } = useLessons(sessionId);
  const { mutate: reorderLessons } = useReorderLessons();

  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 5 } }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    }),
  );

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;
    if (over && active.id !== over.id && lessons) {
      const oldIndex = lessons.findIndex((l) => l.id === active.id);
      const newIndex = lessons.findIndex((l) => l.id === over.id);
      const newArray = arrayMove(lessons, oldIndex, newIndex);
      reorderLessons({ sessionId, item_ids: newArray.map((i) => i.id) });
    }
  };

  if (isLoading) return <Spin size="small" />;
  if (!lessons || lessons.length === 0)
    return (
      <p className="text-gray-400 text-sm italic m-0">Chưa có bài học nào.</p>
    );

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCenter}
      onDragEnd={handleDragEnd}
    >
      <SortableContext
        items={lessons.map((l) => l.id)}
        strategy={verticalListSortingStrategy}
      >
        <div className="space-y-2">
          {lessons.map((lesson) => (
            <SortableLessonItem
              key={lesson.id}
              lesson={lesson}
              onPreviewArtifact={onPreviewArtifact}
            />
          ))}
        </div>
      </SortableContext>
    </DndContext>
  );
};

const SortableLessonItem = ({ lesson }: SortableLessonItemProps) => {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: lesson.id });
  const { mutate: generateLesson, isPending } = useGenerateLesson();
  const { mutate: deleteLesson } = useDeleteLesson();

  const { data: artifacts } = useArtifacts(lesson.id);
  const isLessonPending = artifacts?.some((a) => a.status === "Pending");
  const [prevLessonPending, setPrevLessonPending] = useState(false);

  useEffect(() => {
    if (
      prevLessonPending &&
      !isLessonPending &&
      artifacts &&
      artifacts.length > 0
    ) {
      const hasFailed = artifacts.some((a) => a.status === "Failed");
      if (hasFailed) {
        message.error({
          content: `Bài học ${lesson.name} tạo tài nguyên thất bại!`,
          key: "generate-lesson",
          duration: 3,
        });
      } else {
        message.success({
          content: `Bài học ${lesson.name} đã tạo xong tài nguyên thành công!`,
          key: "generate-lesson",
          duration: 3,
        });
      }
    }
    setPrevLessonPending(!!isLessonPending);
  }, [isLessonPending, artifacts, lesson.name, prevLessonPending]);

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    zIndex: isDragging ? 10 : 1,
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={`flex justify-between items-center p-3 border rounded-lg bg-gray-50 ${isDragging ? "shadow-md border-blue-400" : "border-gray-100 hover:border-blue-200"}`}
    >
      <div className="flex items-center gap-3">
        <div
          {...attributes}
          {...listeners}
          className="cursor-grab p-1 hover:bg-gray-200 rounded text-gray-400"
        >
          <GripVertical size={16} />
        </div>
        <div>
          <div className="font-medium text-gray-800">{lesson.name}</div>
          <div className="text-sm text-gray-500">{lesson.title}</div>
        </div>
      </div>
      <div className="flex gap-2">
        <Tooltip title="Vào Màn hình Học thử (Lý thuyết, Trắc nghiệm & Thực hành coding)">
          <Button
            size="small"
            type="primary"
            icon={<BookOpen size={14} />}
            onClick={() =>
              navigate(`/courses/${courseId}/lessons/${lesson.id}/viewer`)
            }
            className="bg-indigo-600 border-indigo-600 hover:bg-indigo-700 flex items-center gap-1"
          >
            Học thử
          </Button>
        </Tooltip>
        <Tooltip title="Xem Tài nguyên">
          <Button
            size="small"
            icon={<Eye size={14} />}
            onClick={() =>
              navigate(`/courses/${courseId}/lessons/${lesson.id}/viewer`)
            }
            className="text-green-600 border-green-600 hover:bg-green-50"
          >
            Tài nguyên
          </Button>
        </Tooltip>
        <Tooltip title="Chạy AI sinh học liệu (HTML/Quizz)">
          <Button
            type="primary"
            ghost
            size="small"
            icon={<PlayCircle size={14} />}
            className="flex items-center gap-1"
            loading={isPending || isLessonPending}
            onClick={() => generateLesson(lesson.id)}
          >
            {isLessonPending ? "Đang tạo..." : "Tạo AI"}
          </Button>
        </Tooltip>
        <Tooltip title="Cấu hình">
          <Button size="small" icon={<Settings2 size={14} />} />
        </Tooltip>
        <Popconfirm
          title="Xóa Lesson?"
          onConfirm={() => deleteLesson(lesson.id)}
          okText="Xóa"
          cancelText="Hủy"
          okButtonProps={{ danger: true }}
        >
          <Button size="small" danger icon={<Trash2 size={14} />} />
        </Popconfirm>
      </div>
    </div>
  );
};

interface HomeworkExercise {
  index: number;
  level: string;
  folder_name: string;
  title: string;
  content: string;
  rubric: string;
}

const ExerciseList = ({
  session,
  artifacts,
  onPreviewSessionArtifact,
}: {
  session: SessionResponse;
  artifacts?: ArtifactResponse[];
  onPreviewSessionArtifact?: (
    id: number,
    title: string,
    exerciseIndex?: number | null,
  ) => void;
}) => {
  const homeworkArtifact = artifacts?.find(
    (a) => a.type === "session_homework",
  );
  const exercises = (homeworkArtifact?.content_json?.exercises ||
    []) as HomeworkExercise[];

  const getPlainTextFromMarkdown = (markdown: string) => {
    if (!markdown) return "";
    try {
      const rawHtml = marked.parse(markdown) as string;
      return rawHtml
        .replace(/<\/?[^>]+(>|$)/g, " ")
        .replace(/\s+/g, " ")
        .trim();
    } catch {
      return markdown.replace(/[#*`\n]/g, " ");
    }
  };

  if (!homeworkArtifact) {
    return (
      <p className="text-gray-400 text-sm italic m-0">
        Chưa có thông tin bài thực hành.
      </p>
    );
  }

  if (homeworkArtifact.status === "Pending") {
    return (
      <div className="flex items-center gap-2 text-gray-500 text-sm italic py-2">
        <Spin size="small" />
        <span>Đang sinh bộ bài tập thực hành...</span>
      </div>
    );
  }

  if (homeworkArtifact.status === "Failed") {
    return (
      <p className="text-red-500 text-sm font-medium m-0">
        Không thể sinh bài tập thực hành.
      </p>
    );
  }

  if (exercises.length === 0) {
    return (
      <p className="text-gray-400 text-sm italic m-0">
        Chưa có bài thực hành nào được tạo. Hãy nhấn "Tạo bài thực hành" phía
        trên.
      </p>
    );
  }

  return (
    <div className="space-y-2">
      {exercises.map((ex: HomeworkExercise, idx: number) => {
        const levelColors: Record<string, string> = {
          Dễ: "bg-green-50 text-green-700 border-green-200",
          "Trung bình": "bg-blue-50 text-blue-700 border-blue-200",
          Khá: "bg-amber-50 text-amber-700 border-amber-200",
          Giỏi: "bg-orange-50 text-orange-700 border-orange-200",
          "Xuất sắc": "bg-red-50 text-red-700 border-red-200",
        };
        const badgeClass =
          levelColors[ex.level] || "bg-gray-50 text-gray-700 border-gray-200";

        return (
          <div
            key={idx}
            className="flex justify-between items-center p-3 border rounded-lg bg-gray-50 border-gray-100 hover:border-blue-200 transition-all duration-200"
          >
            <div className="flex items-center gap-4 flex-1 min-w-0">
              <div className="w-24 flex-shrink-0">
                <span
                  className={`inline-block w-full text-center px-2 py-0.5 text-xs font-semibold rounded-full border ${badgeClass}`}
                >
                  {ex.level}
                </span>
              </div>
              <div className="flex-1 min-w-0">
                <div className="font-semibold text-gray-800 text-sm">
                  Bài {ex.index || idx + 1}:{" "}
                  {ex.title
                    ? ex.title.replace(/<\/?[^>]+(>|$)/g, "").trim()
                    : ""}
                </div>
                <div className="text-xs text-gray-500 truncate max-w-[600px]">
                  {getPlainTextFromMarkdown(ex.content || "").substring(
                    0,
                    120,
                  ) + "..."}
                </div>
              </div>
            </div>
            <div className="flex gap-2 flex-shrink-0 ml-4">
              <Button
                size="small"
                icon={<Eye size={12} />}
                onClick={() =>
                  onPreviewSessionArtifact &&
                  onPreviewSessionArtifact(
                    session.id,
                    session.title || "Bài thực hành",
                    ex.index,
                  )
                }
                className="text-indigo-600 border-indigo-600 hover:bg-indigo-50 flex items-center gap-1"
              >
                Xem chi tiết
              </Button>
            </div>
          </div>
        );
      })}
    </div>
  );
};

interface ProjectEntryTest {
  title?: string;
  content?: string;
}

const ProjectArtifactList = ({
  session,
  artifacts,
  onPreviewSessionArtifact,
}: {
  session: SessionResponse;
  artifacts?: ArtifactResponse[];
  onPreviewSessionArtifact?: (
    id: number,
    title: string,
    exerciseIndex?: number | null,
  ) => void;
}) => {
  const getPlainTextFromMarkdown = (markdown: string) => {
    if (!markdown) return "";
    try {
      const rawHtml = marked.parse(markdown) as string;
      return rawHtml
        .replace(/<\/?[^>]+(>|$)/g, " ")
        .replace(/\s+/g, " ")
        .trim();
    } catch {
      return markdown.replace(/[#*`\n]/g, " ");
    }
  };

  const entryTestsArt = artifacts?.find(
    (a) => a.type === "project_entry_tests",
  );
  const srsArt = artifacts?.find((a) => a.type === "project_srs");
  const miniProjectArt = artifacts?.find(
    (a) => a.type === "project_mini_project",
  );

  const entryTests = (entryTestsArt?.content_json?.entry_tests ||
    []) as ProjectEntryTest[];

  if (
    (!entryTestsArt && !srsArt && !miniProjectArt) ||
    entryTestsArt?.status === "Pending" ||
    srsArt?.status === "Pending" ||
    miniProjectArt?.status === "Pending"
  ) {
    const isPending =
      entryTestsArt?.status === "Pending" ||
      srsArt?.status === "Pending" ||
      miniProjectArt?.status === "Pending";
    if (isPending) {
      return (
        <div className="flex items-center gap-2 text-gray-500 text-sm italic py-2">
          <Spin size="small" />
          <span>Đang sinh bộ tài nguyên Mini Project...</span>
        </div>
      );
    }
    return (
      <p className="text-gray-400 text-sm italic m-0">
        Chưa có thông tin dự án. Hãy nhấn "Tạo Mini Project" phía trên.
      </p>
    );
  }

  return (
    <div className="space-y-4">
      {/* 1. SRS Document */}
      {srsArt && srsArt.status === "Completed" && (
        <div className="flex justify-between items-center p-3 border rounded-lg bg-gray-50 border-gray-100 hover:border-blue-200 transition-all duration-200">
          <div className="flex items-center gap-4 flex-1 min-w-0">
            <div className="w-24 flex-shrink-0">
              <span className="inline-block w-full text-center px-2 py-0.5 text-xs font-semibold rounded-full border bg-blue-50 text-blue-700 border-blue-200">
                Đặc tả SRS
              </span>
            </div>
            <div className="flex-1 min-w-0">
              <div className="font-semibold text-gray-800 text-sm">
                Tài liệu đặc tả yêu cầu phần mềm SRS
              </div>
              <div className="text-xs text-gray-500 truncate max-w-[600px]">
                {srsArt.content_json?.title ||
                  getPlainTextFromMarkdown(srsArt.content || "").substring(
                    0,
                    120,
                  )}
              </div>
            </div>
          </div>
          <div className="flex gap-2 flex-shrink-0 ml-4">
            <Button
              size="small"
              icon={<Eye size={12} />}
              onClick={() =>
                onPreviewSessionArtifact &&
                onPreviewSessionArtifact(
                  session.id,
                  "Tài liệu đặc tả SRS",
                  null,
                )
              }
              className="text-blue-600 border-blue-600 hover:bg-blue-50 flex items-center gap-1"
            >
              Xem chi tiết
            </Button>
          </div>
        </div>
      )}

      {/* 2. Mini Project Prompt */}
      {miniProjectArt && miniProjectArt.status === "Completed" && (
        <div className="flex justify-between items-center p-3 border rounded-lg bg-gray-50 border-gray-100 hover:border-blue-200 transition-all duration-200">
          <div className="flex items-center gap-4 flex-1 min-w-0">
            <div className="w-24 flex-shrink-0">
              <span className="inline-block w-full text-center px-2 py-0.5 text-xs font-semibold rounded-full border bg-purple-50 text-purple-700 border-purple-200">
                Đề bài
              </span>
            </div>
            <div className="flex-1 min-w-0">
              <div className="font-semibold text-gray-800 text-sm">
                Đề bài & Yêu cầu Mini Project
              </div>
              <div className="text-xs text-gray-500 truncate max-w-[600px]">
                {miniProjectArt.content_json?.title ||
                  getPlainTextFromMarkdown(
                    miniProjectArt.content || "",
                  ).substring(0, 120)}
              </div>
            </div>
          </div>
          <div className="flex gap-2 flex-shrink-0 ml-4">
            <Button
              size="small"
              icon={<Eye size={12} />}
              onClick={() =>
                onPreviewSessionArtifact &&
                onPreviewSessionArtifact(
                  session.id,
                  "Đề bài Mini Project",
                  null,
                )
              }
              className="text-purple-600 border-purple-600 hover:bg-purple-50 flex items-center gap-1"
            >
              Xem chi tiết
            </Button>
          </div>
        </div>
      )}

      {/* 3. Entry Tests */}
      {entryTestsArt &&
        entryTestsArt.status === "Completed" &&
        entryTests.length > 0 && (
          <div className="border rounded-lg bg-gray-50/30 p-3 space-y-2 border-gray-200">
            <div className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
              Danh sách bài kiểm tra đầu giờ (Entry Tests)
            </div>
            {entryTests.map((test: ProjectEntryTest, idx: number) => (
              <div
                key={idx}
                className="flex justify-between items-center p-2.5 border rounded bg-white border-gray-100 hover:border-blue-200 transition-all duration-200"
              >
                <div className="flex items-center gap-3 flex-1 min-w-0">
                  <span className="px-2 py-0.5 text-xs font-semibold rounded bg-amber-50 text-amber-700 border border-amber-200">
                    Đề {idx + 1}
                  </span>
                  <div className="flex-1 min-w-0">
                    <div className="font-semibold text-gray-700 text-xs">
                      {test.title || `Bài kiểm tra đầu giờ ${idx + 1}`}
                    </div>
                  </div>
                </div>
                <div className="flex gap-2 flex-shrink-0 ml-4">
                  <Button
                    size="small"
                    icon={<Eye size={10} />}
                    onClick={() =>
                      onPreviewSessionArtifact &&
                      onPreviewSessionArtifact(
                        session.id,
                        "Bài kiểm tra đầu giờ",
                        idx + 1,
                      )
                    }
                    className="text-amber-600 border-amber-600 hover:bg-amber-50 flex items-center gap-1 text-[11px]"
                  >
                    Xem chi tiết
                  </Button>
                </div>
              </div>
            ))}
          </div>
        )}
    </div>
  );
};
