import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button, Table, Tag, Breadcrumb, Popconfirm, Tooltip, Spin, Alert } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { Plus, Eye, Edit, Trash2, Layers, ArrowLeft, Calendar } from 'lucide-react';
import { useMajor, useUpdateMajor, useDeleteMajor } from '../hooks/useMajors';
import { useProgram } from '../../programs/hooks/usePrograms';
import { useSemesters, useCreateSemester, useUpdateSemester, useDeleteSemester } from '../../semesters/hooks/useSemesters';
import { SemesterResponse, SemesterCreate } from '../../../types/semester';
import { MajorFormModal } from '../components/MajorFormModal';
import { SemesterFormModal } from '../../semesters/components/SemesterFormModal';

export default function MajorDetailPage() {
  const { majorId } = useParams<{ majorId: string }>();
  const idNum = majorId ? parseInt(majorId, 10) : null;
  const navigate = useNavigate();

  const { data: major, isLoading: loadingMajor } = useMajor(idNum);
  const { data: program } = useProgram(major?.program_id || null);
  const { data: semesters, isLoading: loadingSemesters } = useSemesters(idNum || undefined);

  // Modals state
  const [isMajorModalOpen, setIsMajorModalOpen] = useState(false);
  const [isSemesterModalOpen, setIsSemesterModalOpen] = useState(false);
  const [editingSemester, setEditingSemester] = useState<SemesterResponse | null>(null);

  // Mutations
  const { mutate: updateMajor, isPending: isUpdatingMajor } = useUpdateMajor();
  const { mutate: deleteMajor } = useDeleteMajor();

  const { mutate: createSemester, isPending: isCreatingSemester } = useCreateSemester();
  const { mutate: updateSemester, isPending: isUpdatingSemester } = useUpdateSemester();
  const { mutate: deleteSemester } = useDeleteSemester();

  if (loadingMajor) {
    return (
      <div className="flex justify-center items-center min-h-[60vh]">
        <Spin size="large" tip="Đang tải chi tiết Chuyên ngành..." />
      </div>
    );
  }

  if (!major) {
    return (
      <Alert
        type="error"
        message="Không tìm thấy Chuyên ngành"
        description="Chuyên ngành này không tồn tại hoặc đã bị xóa."
        action={
          <Button icon={<ArrowLeft size={14} />} onClick={() => navigate('/majors')}>
            Quay lại danh sách
          </Button>
        }
      />
    );
  }

  const handleOpenCreateSemester = () => {
    setEditingSemester(null);
    setIsSemesterModalOpen(true);
  };

  const handleOpenEditSemester = (sem: SemesterResponse) => {
    setEditingSemester(sem);
    setIsSemesterModalOpen(true);
  };

  const handleSemesterSubmit = (data: SemesterCreate) => {
    if (editingSemester) {
      updateSemester(
        { id: editingSemester.id, payload: data },
        { onSuccess: () => setIsSemesterModalOpen(false) }
      );
    } else {
      createSemester(data, { onSuccess: () => setIsSemesterModalOpen(false) });
    }
  };

  const semesterColumns: ColumnsType<SemesterResponse> = [
    { title: 'ID', dataIndex: 'id', width: 70, render: (id) => <Tag color="purple">#{id}</Tag> },
    {
      title: 'Tên kỳ học',
      dataIndex: 'name',
      render: (name, record) => (
        <div className="flex items-center gap-2">
          <Calendar size={16} className="text-teal-600 shrink-0" />
          <span
            className="font-semibold text-slate-800 hover:text-teal-600 cursor-pointer"
            onClick={() => navigate(`/semesters/${record.id}`)}
          >
            {name}
          </span>
        </div>
      ),
    },
    {
      title: 'Hành động',
      key: 'action',
      width: 220,
      render: (_, record) => (
        <div className="flex items-center gap-1.5">
          <Tooltip title="Xem danh sách các môn học thuộc kỳ này">
            <Button
              size="small"
              type="primary"
              className="bg-teal-600 hover:bg-teal-700 font-medium text-xs flex items-center gap-1"
              icon={<Eye size={13} />}
              onClick={() => navigate(`/semesters/${record.id}`)}
            >
              Chi tiết
            </Button>
          </Tooltip>

          <Tooltip title="Sửa kỳ học">
            <Button
              size="small"
              type="default"
              className="text-amber-600 border-amber-300 hover:bg-amber-50 text-xs flex items-center gap-1"
              icon={<Edit size={13} />}
              onClick={() => handleOpenEditSemester(record)}
            >
              Sửa
            </Button>
          </Tooltip>

          <Popconfirm
            title="Xóa kỳ học này?"
            description="Các môn học thuộc kỳ học này sẽ bị ảnh hưởng."
            onConfirm={() => deleteSemester(record.id)}
            okText="Xóa"
            cancelText="Hủy"
          >
            <Tooltip title="Xóa kỳ học">
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
          { title: <span className="cursor-pointer" onClick={() => navigate('/majors')}>Chuyên ngành</span> },
          { title: major.name },
        ]}
      />

      {/* Major Detail Header Card */}
      <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm relative overflow-hidden">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1.5">
            <div className="flex items-center gap-2">
              <Tag color="cyan" className="font-bold">Chuyên Ngành #{major.id}</Tag>
              {program && (
                <Tag
                  color="blue"
                  className="cursor-pointer font-medium"
                  onClick={() => navigate(`/programs/${program.id}`)}
                >
                  Hệ: {program.name}
                </Tag>
              )}
            </div>
            <h1 className="text-2xl font-bold text-slate-900 m-0 flex items-center gap-2">
              <Layers className="text-teal-600" size={28} /> {major.name}
            </h1>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            <Button
              type="default"
              icon={<Edit size={15} />}
              onClick={() => setIsMajorModalOpen(true)}
            >
              Sửa Chuyên Ngành
            </Button>
            <Popconfirm
              title="Xóa Chuyên Ngành?"
              onConfirm={() => {
                deleteMajor(major.id, {
                  onSuccess: () => navigate('/majors'),
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

      {/* Child Semesters Section */}
      <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 className="text-lg font-bold text-slate-800 m-0 flex items-center gap-2">
              <Calendar className="text-teal-600" size={20} /> Danh Sách Học Kỳ Thuộc Chuyên Ngành: {major.name}
            </h2>
            <p className="text-slate-500 text-xs mt-1">
              Hiển thị toàn bộ học kỳ thuộc chuyên ngành này. Bấm vào chi tiết để xem môn học.
            </p>
          </div>

          <Button
            type="primary"
            icon={<Plus size={15} />}
            className="bg-teal-600 hover:bg-teal-700 font-semibold text-xs rounded-xl h-10 px-4 flex items-center gap-1.5 shrink-0"
            onClick={handleOpenCreateSemester}
          >
            Thêm Học Kỳ Thuộc Chuyên Ngành Này
          </Button>
        </div>

        <Table
          columns={semesterColumns}
          dataSource={semesters}
          rowKey="id"
          loading={loadingSemesters}
          pagination={{ pageSize: 10 }}
        />
      </div>

      {/* Major Edit Modal */}
      <MajorFormModal
        open={isMajorModalOpen}
        onCancel={() => setIsMajorModalOpen(false)}
        isPending={isUpdatingMajor}
        initialValues={major}
        onSubmit={(data) => {
          updateMajor(
            { id: major.id, payload: data },
            { onSuccess: () => setIsMajorModalOpen(false) }
          );
        }}
      />

      {/* Semester Add/Edit Modal pre-filled with this major_id */}
      <SemesterFormModal
        open={isSemesterModalOpen}
        onCancel={() => setIsSemesterModalOpen(false)}
        isPending={isCreatingSemester || isUpdatingSemester}
        initialValues={editingSemester}
        fixedMajorId={major.id}
        onSubmit={handleSemesterSubmit}
      />
    </div>
  );
}
