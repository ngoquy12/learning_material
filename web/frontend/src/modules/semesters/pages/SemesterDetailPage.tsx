import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button, Table, Tag, Breadcrumb, Popconfirm, Tooltip, Spin, Alert } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { Plus, Eye, Edit, Trash2, Calendar, ArrowLeft, BookOpen } from 'lucide-react';
import { useSemester, useUpdateSemester, useDeleteSemester } from '../hooks/useSemesters';
import { useMajor } from '../../majors/hooks/useMajors';
import { useCourses, useCreateCourse, useUpdateCourse, useDeleteCourse } from '../../courses/hooks/useCourses';
import { CourseResponse, CourseCreate } from '../../../types/course';
import { SemesterFormModal } from '../components/SemesterFormModal';
import { CourseFormModal } from '../../courses/components/CourseFormModal';

export default function SemesterDetailPage() {
  const { semesterId } = useParams<{ semesterId: string }>();
  const idNum = semesterId ? parseInt(semesterId, 10) : null;
  const navigate = useNavigate();

  const { data: semester, isLoading: loadingSemester } = useSemester(idNum);
  const { data: major } = useMajor(semester?.major_id || null);
  const { data: courses, isLoading: loadingCourses } = useCourses(idNum || undefined);

  // Modals state
  const [isSemesterModalOpen, setIsSemesterModalOpen] = useState(false);
  const [isCourseModalOpen, setIsCourseModalOpen] = useState(false);
  const [editingCourse, setEditingCourse] = useState<CourseResponse | null>(null);

  // Mutations
  const { mutate: updateSemester, isPending: isUpdatingSemester } = useUpdateSemester();
  const { mutate: deleteSemester } = useDeleteSemester();

  const { mutate: createCourse, isPending: isCreatingCourse } = useCreateCourse();
  const { mutate: updateCourse, isPending: isUpdatingCourse } = useUpdateCourse();
  const { mutate: deleteCourse } = useDeleteCourse();

  if (loadingSemester) {
    return (
      <div className="flex justify-center items-center min-h-[60vh]">
        <Spin size="large" tip="Đang tải chi tiết Học kỳ..." />
      </div>
    );
  }

  if (!semester) {
    return (
      <Alert
        type="error"
        message="Không tìm thấy Học kỳ"
        description="Học kỳ này không tồn tại hoặc đã bị xóa."
        action={
          <Button icon={<ArrowLeft size={14} />} onClick={() => navigate('/semesters')}>
            Quay lại danh sách
          </Button>
        }
      />
    );
  }

  const handleOpenCreateCourse = () => {
    setEditingCourse(null);
    setIsCourseModalOpen(true);
  };

  const handleOpenEditCourse = (c: CourseResponse) => {
    setEditingCourse(c);
    setIsCourseModalOpen(true);
  };

  const handleCourseSubmit = (data: CourseCreate) => {
    if (editingCourse) {
      updateCourse(
        { id: editingCourse.id, payload: data },
        { onSuccess: () => setIsCourseModalOpen(false) }
      );
    } else {
      createCourse(data, { onSuccess: () => setIsCourseModalOpen(false) });
    }
  };

  const courseColumns: ColumnsType<CourseResponse> = [
    { title: 'ID', dataIndex: 'id', width: 70, render: (id) => <Tag color="geekblue">#{id}</Tag> },
    {
      title: 'Tên môn học',
      dataIndex: 'name',
      render: (name, record) => (
        <div className="flex items-center gap-2">
          <BookOpen size={16} className="text-teal-600 shrink-0" />
          <span
            className="font-semibold text-slate-800 hover:text-teal-600 cursor-pointer"
            onClick={() => navigate(`/courses/${record.id}`)}
          >
            {name}
          </span>
        </div>
      ),
    },
    {
      title: 'Công nghệ',
      dataIndex: 'technology_stack',
      render: (stack) => (
        <Tag color="emerald" className="font-mono text-xs">
          {stack || 'python/core'}
        </Tag>
      ),
    },
    {
      title: 'Hành động',
      key: 'action',
      width: 220,
      render: (_, record) => (
        <div className="flex items-center gap-1.5">
          <Tooltip title="Xem chi tiết môn học & bài giảng AI">
            <Button
              size="small"
              type="primary"
              className="bg-teal-600 hover:bg-teal-700 font-medium text-xs flex items-center gap-1"
              icon={<Eye size={13} />}
              onClick={() => navigate(`/courses/${record.id}`)}
            >
              Chi tiết
            </Button>
          </Tooltip>

          <Tooltip title="Sửa môn học">
            <Button
              size="small"
              type="default"
              className="text-amber-600 border-amber-300 hover:bg-amber-50 text-xs flex items-center gap-1"
              icon={<Edit size={13} />}
              onClick={() => handleOpenEditCourse(record)}
            >
              Sửa
            </Button>
          </Tooltip>

          <Popconfirm
            title="Xóa môn học này?"
            description="Tất cả các bài học và dữ liệu liên quan sẽ bị xóa."
            onConfirm={() => deleteCourse(record.id)}
            okText="Xóa"
            cancelText="Hủy"
          >
            <Tooltip title="Xóa môn học">
              <Button
                size="small"
                danger
                type="dashed"
                icon={<Trash2 size={13} />}
                className="text-xs"
              />
            </Tooltip>
          </Popconfirm>
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      {/* Breadcrumbs */}
      <Breadcrumb
        items={[
          { title: <span className="cursor-pointer" onClick={() => navigate('/semesters')}>Kỳ học</span> },
          { title: semester.name },
        ]}
      />

      {/* Semester Detail Header Card */}
      <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm relative overflow-hidden">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1.5">
            <div className="flex items-center gap-2">
              <Tag color="purple" className="font-bold">Học Kỳ #{semester.id}</Tag>
              {major && (
                <Tag
                  color="cyan"
                  className="cursor-pointer font-medium"
                  onClick={() => navigate(`/majors/${major.id}`)}
                >
                  Chuyên ngành: {major.name}
                </Tag>
              )}
            </div>
            <h1 className="text-2xl font-bold text-slate-900 m-0 flex items-center gap-2">
              <Calendar className="text-teal-600" size={28} /> {semester.name}
            </h1>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            <Button
              type="default"
              icon={<Edit size={15} />}
              onClick={() => setIsSemesterModalOpen(true)}
            >
              Sửa Học Kỳ
            </Button>
            <Popconfirm
              title="Xóa Học Kỳ?"
              onConfirm={() => {
                deleteSemester(semester.id, {
                  onSuccess: () => navigate('/semesters'),
                });
              }}
              okText="Xóa"
              cancelText="Hủy"
            >
              <Button danger icon={<Trash2 size={15} />}>
                Xóa
              </Button>
            </Popconfirm>
          </div>
        </div>
      </div>

      {/* Child Courses Section */}
      <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 className="text-lg font-bold text-slate-800 m-0 flex items-center gap-2">
              <BookOpen className="text-teal-600" size={20} /> Danh Sách Môn Học Thuộc Kỳ: {semester.name}
            </h2>
            <p className="text-slate-500 text-xs mt-1">
              Hiển thị toàn bộ các môn học thuộc học kỳ này. Bấm vào chi tiết để xem chương trình và AI Pipeline.
            </p>
          </div>

          <Button
            type="primary"
            icon={<Plus size={15} />}
            className="bg-teal-600 hover:bg-teal-700 font-semibold text-xs rounded-xl h-10 px-4 flex items-center gap-1.5 shrink-0"
            onClick={handleOpenCreateCourse}
          >
            Thêm Môn Học Thuộc Học Kỳ Này
          </Button>
        </div>

        <Table
          columns={courseColumns}
          dataSource={courses}
          rowKey="id"
          loading={loadingCourses}
          pagination={{ pageSize: 10 }}
        />
      </div>

      {/* Semester Edit Modal */}
      <SemesterFormModal
        open={isSemesterModalOpen}
        onCancel={() => setIsSemesterModalOpen(false)}
        isPending={isUpdatingSemester}
        initialValues={semester}
        onSubmit={(data) => {
          updateSemester(
            { id: semester.id, payload: data },
            { onSuccess: () => setIsSemesterModalOpen(false) }
          );
        }}
      />

      {/* Course Add/Edit Modal pre-filled with this semester_id */}
      <CourseFormModal
        open={isCourseModalOpen}
        onCancel={() => setIsCourseModalOpen(false)}
        isPending={isCreatingCourse || isUpdatingCourse}
        initialValues={editingCourse}
        fixedSemesterId={semester.id}
        onSubmit={handleCourseSubmit}
      />
    </div>
  );
}
