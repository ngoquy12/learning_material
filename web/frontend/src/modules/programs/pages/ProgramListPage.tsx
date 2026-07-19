import { useState } from 'react';
import { Table, Button, Card } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { Plus } from 'lucide-react';
import { usePrograms, useCreateProgram } from '../hooks/usePrograms';
import { ProgramResponse } from '../../../types/program';
import { ProgramFormModal } from '../components/ProgramFormModal';

export default function ProgramListPage() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { data: programs, isLoading } = usePrograms();
  const { mutate: createProgram, isPending } = useCreateProgram();

  const columns: ColumnsType<ProgramResponse> = [
    { title: 'ID', dataIndex: 'id', width: 80 },
    { title: 'Tên hệ đào tạo', dataIndex: 'name' },
    { title: 'Mô tả', dataIndex: 'description' },
  ];

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-gray-800">Quản lý Hệ đào tạo</h2>
        </div>
        <Button type="primary" icon={<Plus size={16} />} onClick={() => setIsModalOpen(true)}>
          Thêm Hệ đào tạo
        </Button>
      </div>
      <Card bordered={false} className="shadow-sm">
        <Table columns={columns} dataSource={programs} rowKey="id" loading={isLoading} />
      </Card>
      <ProgramFormModal
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        isPending={isPending}
        onSubmit={(data) => createProgram(data, { onSuccess: () => setIsModalOpen(false) })}
      />
    </div>
  );
}
