import { useState } from 'react';
import { Table, Button, Card, Popconfirm, Tag, Tooltip, Select } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { Plus, Eye, Edit, Trash2, Calendar } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useSemesters, useCreateSemester, useUpdateSemester, useDeleteSemester } from '../hooks/useSemesters';
import { useMajors } from '../../majors/hooks/useMajors';
import { SemesterResponse, SemesterCreate } from '../../../types/semester';
import { SemesterFormModal } from '../components/SemesterFormModal';

export default function SemesterListPage() {
  const navigate = useNavigate();
  const [selectedMajorId, setSelectedMajorId] = useState<number | undefined>(undefined);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingSemester, setEditingSemester] = useState<SemesterResponse | null>(null);

  const { data: majors } = useMajors();
  const { data: semesters, isLoading } = useSemesters(selectedMajorId);
  const { mutate: createSemester, isPending: isCreating } = useCreateSemester();
  const { mutate: updateSemester, isPending: isUpdating } = useUpdateSemester();
  const { mutate: deleteSemester } = useDeleteSemester();

  const handleOpenCreate = () => {
    setEditingSemester(null);
    setIsModalOpen(true);
  };

  const handleOpenEdit = (semester: SemesterResponse) => {
    setEditingSemester(semester);
    setIsModalOpen(true);
  };

  const handleSubmit = (data: SemesterCreate) => {
    if (editingSemester) {
      updateSemester(
        { id: editingSemester.id, payload: data },
        { onSuccess: () => setIsModalOpen(false) }
      );
    } else {
      createSemester(data, { onSuccess: () => setIsModalOpen(false) });
    }
  };

  const columns: ColumnsType<SemesterResponse> = [
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
      title: 'Chuyên ngành',
      dataIndex: 'major_id',
      render: (mId) => {
        const major = majors?.find((m) => m.id === mId);
        return (
          <Tag color="cyan" className="cursor-pointer" onClick={() => navigate(`/majors/${mId}`)}>
            {major?.name || `Chuyên ngành ID #${mId}`}
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
            title="Xóa Kỳ học này?"
            description="Các môn học liên quan sẽ bị ảnh hưởng."
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
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 tracking-tight flex items-center gap-2.5">
            <Calendar className="text-teal-600" size={26} /> Quản lý Kỳ Học
          </h1>
          <p className="text-slate-500 text-xs md:text-sm mt-1">
            Quản lý danh sách các học kỳ, lọc theo Chuyên ngành và quản lý môn học trong từng học kỳ.
          </p>
        </div>
        <div className="flex items-center gap-3 shrink-0">
          <Select
            allowClear
            placeholder="Lọc theo Chuyên Ngành"
            style={{ width: 220 }}
            value={selectedMajorId}
            onChange={(val) => setSelectedMajorId(val)}
            options={majors?.map((m) => ({ value: m.id, label: m.name }))}
          />
          <Button
            type="primary"
            size="large"
            icon={<Plus size={16} />}
            className="bg-teal-600 hover:bg-teal-700 shadow-md font-semibold text-sm rounded-xl h-11 px-5 flex items-center gap-1.5"
            onClick={handleOpenCreate}
          >
            Thêm Kỳ Học
          </Button>
        </div>
      </div>

      <Card bordered={false} className="shadow-sm rounded-2xl">
        <Table
          columns={columns}
          dataSource={semesters}
          rowKey="id"
          loading={isLoading}
          pagination={{ pageSize: 10, showSizeChanger: true }}
        />
      </Card>

      <SemesterFormModal
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        isPending={isCreating || isUpdating}
        initialValues={editingSemester}
        fixedMajorId={selectedMajorId}
        onSubmit={handleSubmit}
      />
    </div>
  );
}
