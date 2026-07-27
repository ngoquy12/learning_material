import { useState } from 'react';
import { Table, Button, Card, Popconfirm, Tag, Tooltip, Select } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { Plus, Eye, Edit, Trash2, Layers } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useMajors, useCreateMajor, useUpdateMajor, useDeleteMajor } from '../hooks/useMajors';
import { usePrograms } from '../../programs/hooks/usePrograms';
import { MajorResponse, MajorCreate } from '../../../types/major';
import { MajorFormModal } from '../components/MajorFormModal';

export default function MajorListPage() {
  const navigate = useNavigate();
  const [selectedProgramId, setSelectedProgramId] = useState<number | undefined>(undefined);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingMajor, setEditingMajor] = useState<MajorResponse | null>(null);

  const { data: programs } = usePrograms();
  const { data: majors, isLoading } = useMajors(selectedProgramId);
  const { mutate: createMajor, isPending: isCreating } = useCreateMajor();
  const { mutate: updateMajor, isPending: isUpdating } = useUpdateMajor();
  const { mutate: deleteMajor } = useDeleteMajor();

  const handleOpenCreate = () => {
    setEditingMajor(null);
    setIsModalOpen(true);
  };

  const handleOpenEdit = (major: MajorResponse) => {
    setEditingMajor(major);
    setIsModalOpen(true);
  };

  const handleSubmit = (data: MajorCreate) => {
    if (editingMajor) {
      updateMajor(
        { id: editingMajor.id, payload: data },
        { onSuccess: () => setIsModalOpen(false) }
      );
    } else {
      createMajor(data, { onSuccess: () => setIsModalOpen(false) });
    }
  };

  const columns: ColumnsType<MajorResponse> = [
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
      title: 'Hệ đào tạo',
      dataIndex: 'program_id',
      render: (pId) => {
        const prog = programs?.find((p) => p.id === pId);
        return (
          <Tag color="blue" className="cursor-pointer" onClick={() => navigate(`/programs/${pId}`)}>
            {prog?.name || `Hệ ID #${pId}`}
          </Tag>
        );
      },
    },
    {
      title: 'Hành động',
      key: 'action',
      width: 220,
      render: (_, record) => (
        <div className="flex items-center gap-1.5">
          <Tooltip title="Xem danh sách kỳ học thuộc chuyên ngành này">
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
            title="Xóa Chuyên ngành này?"
            description="Các kỳ học và môn học liên quan sẽ bị ảnh hưởng."
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
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 tracking-tight flex items-center gap-2.5">
            <Layers className="text-teal-600" size={26} /> Quản lý Chuyên Ngành
          </h1>
          <p className="text-slate-500 text-xs md:text-sm mt-1">
            Quản lý các chuyên ngành đào tạo, lọc theo Hệ đào tạo và xem cấu trúc kỳ học chi tiết.
          </p>
        </div>
        <div className="flex items-center gap-3 shrink-0">
          <Select
            allowClear
            placeholder="Lọc theo Hệ Đào Tạo"
            style={{ width: 220 }}
            value={selectedProgramId}
            onChange={(val) => setSelectedProgramId(val)}
            options={programs?.map((p) => ({ value: p.id, label: p.name }))}
          />
          <Button
            type="primary"
            size="large"
            icon={<Plus size={16} />}
            className="bg-teal-600 hover:bg-teal-700 shadow-md font-semibold text-sm rounded-xl h-11 px-5 flex items-center gap-1.5"
            onClick={handleOpenCreate}
          >
            Thêm Chuyên Ngành
          </Button>
        </div>
      </div>

      <Card bordered={false} className="shadow-sm rounded-2xl">
        <Table
          columns={columns}
          dataSource={majors}
          rowKey="id"
          loading={isLoading}
          pagination={{ pageSize: 10, showSizeChanger: true }}
        />
      </Card>

      <MajorFormModal
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        isPending={isCreating || isUpdating}
        initialValues={editingMajor}
        fixedProgramId={selectedProgramId}
        onSubmit={handleSubmit}
      />
    </div>
  );
}
