import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button, Table, Tag, Breadcrumb, Popconfirm, Tooltip, Spin, Alert } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { Plus, Eye, Edit, Trash2, GraduationCap, ArrowLeft, Layers } from 'lucide-react';
import { useProgram, useUpdateProgram, useDeleteProgram } from '../hooks/usePrograms';
import { useMajors, useCreateMajor, useUpdateMajor, useDeleteMajor } from '../../majors/hooks/useMajors';
import { MajorResponse, MajorCreate } from '../../../types/major';
import { ProgramFormModal } from '../components/ProgramFormModal';
import { MajorFormModal } from '../../majors/components/MajorFormModal';

export default function ProgramDetailPage() {
  const { programId } = useParams<{ programId: string }>();
  const idNum = programId ? parseInt(programId, 10) : null;
  const navigate = useNavigate();

  const { data: program, isLoading: loadingProgram } = useProgram(idNum);
  const { data: majors, isLoading: loadingMajors } = useMajors(idNum || undefined);

  // Modals state
  const [isProgramModalOpen, setIsProgramModalOpen] = useState(false);
  const [isMajorModalOpen, setIsMajorModalOpen] = useState(false);
  const [editingMajor, setEditingMajor] = useState<MajorResponse | null>(null);

  // Mutations
  const { mutate: updateProgram, isPending: isUpdatingProgram } = useUpdateProgram();
  const { mutate: deleteProgram } = useDeleteProgram();

  const { mutate: createMajor, isPending: isCreatingMajor } = useCreateMajor();
  const { mutate: updateMajor, isPending: isUpdatingMajor } = useUpdateMajor();
  const { mutate: deleteMajor } = useDeleteMajor();

  if (loadingProgram) {
    return (
      <div className="flex justify-center items-center min-h-[60vh]">
        <Spin size="large" tip="Đang tải chi tiết Hệ đào tạo..." />
      </div>
    );
  }

  if (!program) {
    return (
      <Alert
        type="error"
        message="Không tìm thấy Hệ đào tạo"
        description="Hệ đào tạo này không tồn tại hoặc đã bị xóa."
        action={
          <Button icon={<ArrowLeft size={14} />} onClick={() => navigate('/programs')}>
            Quay lại danh sách
          </Button>
        }
      />
    );
  }

  const handleOpenCreateMajor = () => {
    setEditingMajor(null);
    setIsMajorModalOpen(true);
  };

  const handleOpenEditMajor = (major: MajorResponse) => {
    setEditingMajor(major);
    setIsMajorModalOpen(true);
  };

  const handleMajorSubmit = (data: MajorCreate) => {
    if (editingMajor) {
      updateMajor(
        { id: editingMajor.id, payload: data },
        { onSuccess: () => setIsMajorModalOpen(false) }
      );
    } else {
      createMajor(data, { onSuccess: () => setIsMajorModalOpen(false) });
    }
  };

  const majorColumns: ColumnsType<MajorResponse> = [
    { title: 'ID', dataIndex: 'id', width: 70, render: (id) => <Tag color="cyan">#{id}</Tag> },
    {
      title: 'Tên chuyên ngành',
      dataIndex: 'name',
      render: (name, record) => (
        <div className="flex items-center gap-2">
          <Layers size={16} className="text-teal-600 shrink-0" />
          <span
            className="font-semibold text-slate-800 hover:text-teal-600 cursor-pointer"
            onClick={() => navigate(`/majors/${record.id}`)}
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
          <Tooltip title="Xem danh sách các học kỳ thuộc chuyên ngành này">
            <Button
              size="small"
              type="primary"
              className="bg-teal-600 hover:bg-teal-700 font-medium text-xs flex items-center gap-1"
              icon={<Eye size={13} />}
              onClick={() => navigate(`/majors/${record.id}`)}
            >
              Chi tiết
            </Button>
          </Tooltip>

          <Tooltip title="Sửa chuyên ngành">
            <Button
              size="small"
              type="default"
              className="text-amber-600 border-amber-300 hover:bg-amber-50 text-xs flex items-center gap-1"
              icon={<Edit size={13} />}
              onClick={() => handleOpenEditMajor(record)}
            >
              Sửa
            </Button>
          </Tooltip>

          <Popconfirm
            title="Xóa chuyên ngành này?"
            description="Các kỳ học và môn học thuộc chuyên ngành sẽ bị ảnh hưởng."
            onConfirm={() => deleteMajor(record.id)}
            okText="Xóa"
            cancelText="Hủy"
          >
            <Tooltip title="Xóa chuyên ngành">
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
          { title: <span className="cursor-pointer" onClick={() => navigate('/programs')}>Hệ đào tạo</span> },
          { title: program.name },
        ]}
      />

      {/* Program Detail Header Card */}
      <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm relative overflow-hidden">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1.5">
            <div className="flex items-center gap-2">
              <Tag color="teal" className="font-bold">Hệ Đào Tạo #{program.id}</Tag>
            </div>
            <h1 className="text-2xl font-bold text-slate-900 m-0 flex items-center gap-2">
              <GraduationCap className="text-teal-600" size={28} /> {program.name}
            </h1>
            <p className="text-slate-600 text-sm m-0">
              {program.description || 'Chưa có thông tin mô tả cho hệ đào tạo này.'}
            </p>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            <Button
              type="default"
              icon={<Edit size={15} />}
              onClick={() => setIsProgramModalOpen(true)}
            >
              Sửa Hệ Đào Tạo
            </Button>
            <Popconfirm
              title="Xóa Hệ Đào Tạo?"
              onConfirm={() => {
                deleteProgram(program.id, {
                  onSuccess: () => navigate('/programs'),
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

      {/* Child Majors Section */}
      <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 className="text-lg font-bold text-slate-800 m-0 flex items-center gap-2">
              <Layers className="text-teal-600" size={20} /> Danh Sách Chuyên Ngành Thuộc Hệ: {program.name}
            </h2>
            <p className="text-slate-500 text-xs mt-1">
              Hiển thị toàn bộ các chuyên ngành đang thuộc hệ đào tạo này. Bấm vào chi tiết để xem cây kỳ học.
            </p>
          </div>

          <Button
            type="primary"
            icon={<Plus size={15} />}
            className="bg-teal-600 hover:bg-teal-700 font-semibold text-xs rounded-xl h-10 px-4 flex items-center gap-1.5 shrink-0"
            onClick={handleOpenCreateMajor}
          >
            Thêm Chuyên Ngành Thuộc Hệ Này
          </Button>
        </div>

        <Table
          columns={majorColumns}
          dataSource={majors}
          rowKey="id"
          loading={loadingMajors}
          pagination={{ pageSize: 10 }}
        />
      </div>

      {/* Program Edit Modal */}
      <ProgramFormModal
        open={isProgramModalOpen}
        onCancel={() => setIsProgramModalOpen(false)}
        isPending={isUpdatingProgram}
        initialValues={program}
        onSubmit={(data) => {
          updateProgram(
            { id: program.id, payload: data },
            { onSuccess: () => setIsProgramModalOpen(false) }
          );
        }}
      />

      {/* Major Add/Edit Modal pre-filled with this program_id */}
      <MajorFormModal
        open={isMajorModalOpen}
        onCancel={() => setIsMajorModalOpen(false)}
        isPending={isCreatingMajor || isUpdatingMajor}
        initialValues={editingMajor}
        fixedProgramId={program.id}
        onSubmit={handleMajorSubmit}
      />
    </div>
  );
}
