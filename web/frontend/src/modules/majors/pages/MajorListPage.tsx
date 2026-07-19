import { useState } from 'react';
import { Table, Button, Card } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { Plus } from 'lucide-react';
import { useMajors, useCreateMajor } from '../hooks/useMajors';
import { MajorResponse } from '../../../types/major';
import { MajorFormModal } from '../components/MajorFormModal';

export default function MajorListPage() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { data: majors, isLoading } = useMajors();
  const { mutate: createMajor, isPending } = useCreateMajor();

  const columns: ColumnsType<MajorResponse> = [
    { title: 'ID', dataIndex: 'id', width: 80 },
    { title: 'Tên chuyên ngành', dataIndex: 'name' },
    { title: 'Hệ đào tạo ID', dataIndex: 'program_id' },
  ];

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-gray-800">Quản lý Chuyên ngành</h2>
        </div>
        <Button type="primary" icon={<Plus size={16} />} onClick={() => setIsModalOpen(true)}>
          Thêm Chuyên ngành
        </Button>
      </div>
      <Card bordered={false} className="shadow-sm">
        <Table columns={columns} dataSource={majors} rowKey="id" loading={isLoading} />
      </Card>
      <MajorFormModal
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        isPending={isPending}
        onSubmit={(data) => createMajor(data, { onSuccess: () => setIsModalOpen(false) })}
      />
    </div>
  );
}
