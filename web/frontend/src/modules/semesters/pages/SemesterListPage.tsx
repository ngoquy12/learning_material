import { useState } from 'react';
import { Table, Button, Card } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { Plus } from 'lucide-react';
import { useSemesters, useCreateSemester } from '../hooks/useSemesters';
import { SemesterResponse } from '../../../types/semester';
import { SemesterFormModal } from '../components/SemesterFormModal';

export default function SemesterListPage() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { data: semesters, isLoading } = useSemesters();
  const { mutate: createSemester, isPending } = useCreateSemester();

  const columns: ColumnsType<SemesterResponse> = [
    { title: 'ID', dataIndex: 'id', width: 80 },
    { title: 'Tên kỳ học', dataIndex: 'name' },
    { title: 'Chuyên ngành ID', dataIndex: 'major_id' },
  ];

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-gray-800">Quản lý Kỳ học</h2>
        </div>
        <Button type="primary" icon={<Plus size={16} />} onClick={() => setIsModalOpen(true)}>
          Thêm Kỳ học
        </Button>
      </div>
      <Card bordered={false} className="shadow-sm">
        <Table columns={columns} dataSource={semesters} rowKey="id" loading={isLoading} />
      </Card>
      <SemesterFormModal
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        isPending={isPending}
        onSubmit={(data) => createSemester(data, { onSuccess: () => setIsModalOpen(false) })}
      />
    </div>
  );
}
