import { useState } from "react";
import { Table, Button, Card, Tag, Popconfirm, Tooltip, Select } from "antd";
import type { ColumnsType } from "antd/es/table";
import { Plus, Eye, Edit, Trash2, BookOpen } from "lucide-react";
import {
  useCourses,
  useCreateCourse,
  useUpdateCourse,
  useDeleteCourse,
} from "../hooks/useCourses";
import { useSemesters } from "../../semesters/hooks/useSemesters";
import { CourseResponse, CourseCreate } from "../../../types/course";
import { CourseFormModal } from "../components/CourseFormModal";
import { useNavigate } from "react-router-dom";

export default function CourseListPage() {
  const navigate = useNavigate();
  const [selectedSemesterId, setSelectedSemesterId] = useState<
    number | undefined
  >(undefined);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingCourse, setEditingCourse] = useState<CourseResponse | null>(
    null,
  );

  const { data: semesters } = useSemesters();
  const { data: courses, isLoading } = useCourses(selectedSemesterId);
  const { mutate: createCourse, isPending: isCreating } = useCreateCourse();
  const { mutate: updateCourse, isPending: isUpdating } = useUpdateCourse();
  const { mutate: deleteCourse } = useDeleteCourse();

  const handleOpenCreate = () => {
    setEditingCourse(null);
    setIsModalOpen(true);
  };

  const handleOpenEdit = (c: CourseResponse) => {
    setEditingCourse(c);
    setIsModalOpen(true);
  };

  const handleSubmit = (data: CourseCreate) => {
    if (editingCourse) {
      updateCourse(
        { id: editingCourse.id, payload: data },
        { onSuccess: () => setIsModalOpen(false) },
      );
    } else {
      createCourse(data, { onSuccess: () => setIsModalOpen(false) });
    }
  };

  const columns: ColumnsType<CourseResponse> = [
    {
      title: "ID",
      dataIndex: "id",
      width: 70,
      render: (id) => <Tag color="geekblue">#{id}</Tag>,
    },
    {
      title: "Tên môn học",
      dataIndex: "name",
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
      title: "Công nghệ",
      dataIndex: "technology_stack",
      render: (tech) => (
        <Tag color={tech ? "emerald" : "default"} className="font-mono text-xs">
          {tech || "Chưa thiết lập"}
        </Tag>
      ),
    },
    {
      title: "Học kỳ",
      dataIndex: "semester_id",
      render: (sId) => {
        const sem = semesters?.find((s) => s.id === sId);
        return (
          <Tag
            color="purple"
            className="cursor-pointer"
            onClick={() => navigate(`/semesters/${sId}`)}
          >
            {sem?.name || `Kỳ #${sId}`}
          </Tag>
        );
      },
    },
    {
      title: "Hành động",
      key: "action",
      width: 220,
      render: (_, record) => (
        <div className="flex items-center gap-1.5">
          <Tooltip title="Xem chi tiết môn học & AI Pipeline">
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

          <Tooltip title="Chỉnh sửa thông tin">
            <Button
              size="small"
              type="default"
              className="text-amber-600 border-amber-300 hover:bg-amber-50 text-xs flex items-center gap-1"
              icon={<Edit size={13} />}
              onClick={() => handleOpenEdit(record)}
            >
              Sửa
            </Button>
          </Tooltip>

          <Popconfirm
            title="Xóa Môn học này?"
            description="Tất cả bài học và dữ liệu môn học sẽ bị ảnh hưởng."
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
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 tracking-tight flex items-center gap-2.5">
            <BookOpen className="text-teal-600" size={26} /> Quản lý Môn Học
          </h1>
          <p className="text-slate-500 text-xs md:text-sm mt-1">
            Quản lý các môn học trong hệ thống, lọc theo Học Kỳ và thiết lập
            biên dịch bài giảng AI.
          </p>
        </div>
        <div className="flex items-center gap-3 shrink-0">
          <Select
            allowClear
            placeholder="Lọc theo Học Kỳ"
            style={{ width: 220 }}
            value={selectedSemesterId}
            onChange={(val) => setSelectedSemesterId(val)}
            options={semesters?.map((s) => ({ value: s.id, label: s.name }))}
          />
          <Button
            type="primary"
            size="large"
            icon={<Plus size={16} />}
            className="bg-teal-600 hover:bg-teal-700 shadow-md font-semibold text-sm rounded-xl h-11 px-5 flex items-center gap-1.5"
            onClick={handleOpenCreate}
          >
            Thêm Môn Học
          </Button>
        </div>
      </div>

      <Card bordered={false} className="shadow-sm rounded-2xl">
        <Table
          columns={columns}
          dataSource={courses}
          rowKey="id"
          loading={isLoading}
          pagination={{ pageSize: 10, showSizeChanger: true }}
        />
      </Card>

      <CourseFormModal
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        isPending={isCreating || isUpdating}
        initialValues={editingCourse}
        fixedSemesterId={selectedSemesterId}
        onSubmit={handleSubmit}
      />
    </div>
  );
}
