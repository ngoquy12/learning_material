import { useState } from 'react';
import { Table, Button, Card, Popconfirm, Tag, Tooltip } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { Plus, Eye, Edit, Trash2, GraduationCap } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { usePrograms, useCreateProgram, useUpdateProgram, useDeleteProgram } from '../hooks/usePrograms';
import { ProgramResponse, ProgramCreate } from '../../../types/program';
import { ProgramFormModal } from '../components/ProgramFormModal';

export default function ProgramListPage() {
  const navigate = useNavigate();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingProgram, setEditingProgram] = useState<ProgramResponse | null>(null);

  const { data: programs, isLoading } = usePrograms();
  const { mutate: createProgram, isPending: isCreating } = useCreateProgram();
  const { mutate: updateProgram, isPending: isUpdating } = useUpdateProgram();
  const { mutate: deleteProgram } = useDeleteProgram();

  const handleOpenCreate = () => {
    setEditingProgram(null);
    setIsModalOpen(true);
  };

  const handleOpenEdit = (program: ProgramResponse) => {
    setEditingProgram(program);
    setIsModalOpen(true);
  };

  const handleSubmit = (data: ProgramCreate) => {
    if (editingProgram) {
      updateProgram(
        { id: editingProgram.id, payload: data },
        { onSuccess: () => setIsModalOpen(false) }
      );
    } else {
      createProgram(data, { onSuccess: () => setIsModalOpen(false) });
    }
  };

  const columns: ColumnsType<ProgramResponse> = [
    { title: 'ID', dataIndex: 'id', width: 70, render: (id) => <Tag color="blue">#{id}</Tag> },
    {
      title: 'Tên hệ đào tạo',
      dataIndex: 'name',
      render: (name, record) => (
        <div className="flex items-center gap-2">
          <GraduationCap size={16} className="text-teal-600 shrink-0" />
          <span
            className="font-semibold text-slate-800 hover:text-teal-600 cursor-pointer"
            onClick={() => navigate(`/programs/${record.id}`)}
          >
            {name}
          </span>
        </div>
      ),
    },
    { title: 'Mô tả', dataIndex: 'description', render: (desc) => desc || <span className="text-slate-400 italic">Chưa có mô tả</span> },
    {
      title: 'Hành động',
      key: 'action',
      width: 220,
      render: (_, record) => (
        <div className="flex items-center gap-1.5">
          <Tooltip title="Xem danh sách chuyên ngành thuộc hệ này">
            <Button
              size="small"
              type="primary"
              className="bg-teal-600 hover:bg-teal-700 font-medium text-xs flex items-center gap-1"
              icon={<Eye size={13} />}
              onClick={() => navigate(`/programs/${record.id}`)}
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
            title="Xóa Hệ đào tạo này?"
            description="Lưu ý: Các chuyên ngành liên quan cũng sẽ bị ảnh hưởng."
            onConfirm={() => deleteProgram(record.id)}
            okText="Xóa"
            cancelText="Hủy"
          >
            <Tooltip title="Xóa hệ đào tạo">
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
            <GraduationCap className="text-teal-600" size={26} /> Quản lý Hệ Đào Tạo
          </h1>
          <p className="text-slate-500 text-xs md:text-sm mt-1">
            Quản lý các hệ đào tạo chính quy, liên thông, văn bằng 2 và cây cấu trúc môn học liên quan.
          </p>
        </div>
        <Button
          type="primary"
          size="large"
          icon={<Plus size={16} />}
          className="bg-teal-600 hover:bg-teal-700 shadow-md font-semibold text-sm rounded-xl h-11 px-5 flex items-center gap-1.5 shrink-0"
          onClick={handleOpenCreate}
        >
          Thêm Hệ Đào Tạo
        </Button>
      </div>

      <Card bordered={false} className="shadow-sm rounded-2xl">
        <Table
          columns={columns}
          dataSource={programs}
          rowKey="id"
          loading={isLoading}
          pagination={{ pageSize: 10, showSizeChanger: true }}
        />
      </Card>

      <ProgramFormModal
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        isPending={isCreating || isUpdating}
        initialValues={editingProgram}
        onSubmit={handleSubmit}
      />
    </div>
  );
}
