import { Modal, Button, Input, Table, Alert } from "antd";
import { Save, Sparkles, Maximize2, Minimize2 } from "lucide-react";
import { PMRow, useReviewPM, useAutoFixPM } from "../hooks/useCourses";
import { useState, useEffect } from "react";
import type { ColumnsType } from "antd/es/table";
import { marked } from "marked";
import DOMPurify from "dompurify";

interface Props {
  open: boolean;
  courseId: number;
  onCancel: () => void;
  onConfirm: (data: PMRow[]) => void;
  isConfirming: boolean;
  initialData: PMRow[];
}

export const PMPreviewModal = ({
  open,
  courseId,
  onCancel,
  onConfirm,
  isConfirming,
  initialData,
}: Props) => {
  const [data, setData] = useState<PMRow[]>([]);
  const [reviewResult, setReviewResult] = useState<string | null>(null);
  const [expandedColumns, setExpandedColumns] = useState<boolean>(false);

  const { mutate: reviewPM, isPending: isReviewing } = useReviewPM();
  const { mutate: autoFixPM, isPending: isAutoFixing } = useAutoFixPM();

  useEffect(() => {
    setData(initialData);
    setReviewResult(null);
    setExpandedColumns(false);
  }, [initialData, open]);

  const updateRow = (index: number, field: keyof PMRow, value: string) => {
    const newData = [...data];
    newData[index] = { ...newData[index], [field]: value };
    setData(newData);
  };

  const handleReview = () => {
    reviewPM(
      { courseId, payload: data },
      {
        onSuccess: (res) => {
          setReviewResult(res.review_content);
        },
      },
    );
  };

  const handleAutoFix = () => {
    if (!reviewResult) return;
    autoFixPM(
      { courseId, payload: data, reviewReport: reviewResult },
      {
        onSuccess: (fixedData) => {
          setData(fixedData);
          setReviewResult(null);
        },
      }
    );
  };

  const columns: ColumnsType<PMRow> = [
    {
      title: "Session",
      dataIndex: "session_val",
      key: "session_val",
      width: expandedColumns ? 160 : "12%",
      render: (text, _, index) => (
        <Input
          value={text}
          onChange={(e) => updateRow(index, "session_val", e.target.value)}
        />
      ),
    },
    {
      title: "Chủ đề",
      dataIndex: "content_val",
      key: "content_val",
      width: expandedColumns ? 350 : "20%",
      render: (text, _, index) => (
        <Input.TextArea
          autoSize={{ minRows: 1, maxRows: 6 }}
          value={text}
          onChange={(e) => updateRow(index, "content_val", e.target.value)}
        />
      ),
    },
    {
      title: "Lesson",
      dataIndex: "lesson_val",
      key: "lesson_val",
      width: expandedColumns ? 140 : "10%",
      render: (text, _, index) => (
        <Input
          value={text}
          onChange={(e) => updateRow(index, "lesson_val", e.target.value)}
        />
      ),
    },
    {
      title: "Chi tiết (Details / Prompt)",
      dataIndex: "details_val",
      key: "details_val",
      width: expandedColumns ? 650 : "38%",
      render: (text, _, index) => (
        <Input.TextArea
          autoSize={{ minRows: 1, maxRows: 6 }}
          value={text}
          onChange={(e) => updateRow(index, "details_val", e.target.value)}
        />
      ),
    },
    {
      title: "Output mong muốn",
      dataIndex: "output_val",
      key: "output_val",
      width: expandedColumns ? 500 : "20%",
      render: (text, _, index) => (
        <Input.TextArea
          autoSize={{ minRows: 1, maxRows: 6 }}
          value={text}
          onChange={(e) => updateRow(index, "output_val", e.target.value)}
        />
      ),
    },
  ];

  return (
    <Modal
      title={
        <div className="flex items-center gap-2 text-lg">
          Duyệt trước cấu trúc Khóa học (Raw PM Data)
        </div>
      }
      open={open}
      onCancel={onCancel}
      width={1300}
      footer={
        <div className="flex justify-between mt-4">
          <div className="flex gap-2">
            <Button
              icon={<Sparkles size={16} />}
              type="dashed"
              className="text-purple-600 border-purple-600 font-semibold"
              onClick={handleReview}
              loading={isReviewing}
              disabled={isAutoFixing}
            >
              {isReviewing ? "Senior đang đọc..." : "Nhờ AI Review PM"}
            </Button>
            {reviewResult && (
              <Button
                icon={<Sparkles size={16} />}
                type="primary"
                className="bg-purple-600 hover:bg-purple-700 text-white font-semibold border-none"
                onClick={handleAutoFix}
                loading={isAutoFixing}
                disabled={isReviewing}
              >
                AI Tự Sửa PM
              </Button>
            )}
            <Button
              icon={expandedColumns ? <Minimize2 size={16} /> : <Maximize2 size={16} />}
              onClick={() => setExpandedColumns(!expandedColumns)}
              className="font-medium"
              disabled={isAutoFixing || isReviewing}
            >
              {expandedColumns ? "Thu gọn cột (Vừa màn hình)" : "Giãn rộng cột (Cuộn ngang)"}
            </Button>
          </div>
          <div className="flex gap-2">
            <Button onClick={onCancel} disabled={isConfirming || isReviewing || isAutoFixing}>
              Hủy
            </Button>
            <Button
              type="primary"
              icon={<Save size={16} />}
              loading={isConfirming}
              onClick={() => onConfirm(data)}
              disabled={isAutoFixing || isReviewing}
            >
              Xác nhận Lưu vào DB
            </Button>
          </div>
        </div>
      }
      destroyOnClose
    >
      <div className="mt-4 flex flex-col gap-4">
        {reviewResult && (
          <Alert
            message="Đánh giá từ Senior Academic Director"
            description={
              <div 
                className="text-sm [&_ul]:list-disc [&_ul]:pl-5 [&_ol]:list-decimal [&_ol]:pl-5 [&_li]:mb-1 [&_h3]:text-base [&_h3]:font-bold [&_h3]:mt-2 [&_h3]:mb-1 [&_p]:mb-2"
                dangerouslySetInnerHTML={{ 
                  __html: DOMPurify.sanitize(marked.parse(reviewResult) as string) 
                }} 
              />
            }
            type="info"
            showIcon
            closable
            onClose={() => setReviewResult(null)}
          />
        )}

        <Table
          columns={columns}
          dataSource={data}
          rowKey={(_, index) => index as number}
          pagination={false}
          scroll={{ x: expandedColumns ? 1800 : "100%", y: reviewResult ? 300 : 500 }}
          size="small"
          bordered
        />
      </div>
    </Modal>
  );
};

