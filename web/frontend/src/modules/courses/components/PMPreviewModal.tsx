import { Modal, Button, Input, Table, Alert, Select, Tag } from "antd";
import {
  Save,
  Sparkles,
  Maximize2,
  Minimize2,
  Table as TableIcon,
  Trash2,
} from "lucide-react";
import { PMRow, useReviewPM, useAutoFixPM } from "../hooks/useCourses";
import { useState, useEffect } from "react";
import type { ColumnsType } from "antd/es/table";
import { marked } from "marked";
import DOMPurify from "dompurify";

import { GeneratePMModal } from "./GeneratePMModal";

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
  const [expandedColumns, setExpandedColumns] = useState<boolean>(true);
  const [generateModalOpen, setGenerateModalOpen] = useState<boolean>(false);
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([]);

  const handleBatchDeleteRows = () => {
    if (selectedRowKeys.length === 0) return;
    Modal.confirm({
      title: "Xác Nhận Xóa Hàng Loạt Dòng PM",
      content: `Bạn có chắc chắn muốn xóa ${selectedRowKeys.length} dòng bài học đã chọn khỏi bảng cấu trúc PM không? Thao tác này sẽ cập nhật bảng xem trước (chưa lưu vào DB cho đến khi bạn xác nhận).`,
      okText: `Xóa ${selectedRowKeys.length} Dòng Đã Chọn`,
      okType: "danger",
      cancelText: "Hủy",
      onOk: () => {
        const newData = data.filter((_, idx: number) => !selectedRowKeys.includes(idx));
        setData(newData);
        setSelectedRowKeys([]);
      },
    });
  };

  const { mutate: reviewPM, isPending: isReviewing } = useReviewPM();
  const { mutate: autoFixPM, isPending: isAutoFixing } = useAutoFixPM();

  useEffect(() => {
    // Normalize data to ensure 10 columns exist with fallbacks
    const normalized = (initialData || []).map((row) => ({
      session_id: row.session_id || row.session_val || "",
      session_type_vn: row.session_type_vn || row.form || "Lý thuyết",
      session_code: row.session_code || "THEORY",
      session_title: row.session_title || row.content_val || "",
      lesson_title: row.lesson_title || row.lesson_val || "",
      details: row.details || row.details_val || "",
      expected_outcome: row.expected_outcome || row.output_val || "",
      forbidden_scope: row.forbidden_scope || "",
      allowed_scope: row.allowed_scope || "",
      tech_stack: row.tech_stack || "",
    }));
    setData(normalized);
    setReviewResult(null);
    setExpandedColumns(true);
  }, [initialData, open]);

  const updateRow = (index: number, field: keyof PMRow, value: string) => {
    const newData = [...data];
    newData[index] = { ...newData[index], [field]: value };
    setData(newData);
  };

  const getSessionRowSpan = (list: PMRow[], index: number): number => {
    if (index === undefined || index === null || !list[index]) return 1;

    const getSessionKey = (r: PMRow) =>
      (
        r.session_id ||
        r.session_val ||
        r.session_title ||
        r.content_val ||
        ""
      ).trim();
    const currentKey = getSessionKey(list[index]);

    if (!currentKey) return 1;

    // If previous row has the exact same session key, return 0 to merge/hide cell
    if (index > 0) {
      const prevKey = getSessionKey(list[index - 1]);
      if (prevKey === currentKey) {
        return 0;
      }
    }

    // Count how many consecutive rows share this session key
    let count = 1;
    for (let i = index + 1; i < list.length; i++) {
      if (getSessionKey(list[i]) === currentKey) {
        count++;
      } else {
        break;
      }
    }
    return count;
  };

  const updateSessionGroupField = (
    index: number,
    field: keyof PMRow,
    value: string,
  ) => {
    const getSessionKey = (r: PMRow) =>
      (
        r.session_id ||
        r.session_val ||
        r.session_title ||
        r.content_val ||
        ""
      ).trim();
    const targetKey = getSessionKey(data[index]);
    const newData = [...data];

    if (targetKey) {
      for (let i = 0; i < newData.length; i++) {
        if (getSessionKey(newData[i]) === targetKey) {
          newData[i] = { ...newData[i], [field]: value };
        }
      }
    } else {
      newData[index] = { ...newData[index], [field]: value };
    }
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
          const normalized = fixedData.map((row) => ({
            session_id: row.session_id || row.session_val || "",
            session_type_vn: row.session_type_vn || row.form || "Lý thuyết",
            session_code: row.session_code || "THEORY",
            session_title: row.session_title || row.content_val || "",
            lesson_title: row.lesson_title || row.lesson_val || "",
            details: row.details || row.details_val || "",
            expected_outcome: row.expected_outcome || row.output_val || "",
            forbidden_scope: row.forbidden_scope || "",
            allowed_scope: row.allowed_scope || row.output_val || "",
            tech_stack: row.tech_stack || "",
          }));
          setData(normalized);
          setReviewResult(null);
        },
      },
    );
  };

  const columns: ColumnsType<PMRow> = [
    {
      title: "Session",
      dataIndex: "session_id",
      key: "session_id",
      width: expandedColumns ? 120 : 95,
      onCell: (_, index) => ({
        rowSpan: getSessionRowSpan(data, index ?? 0),
      }),
      render: (text, _, index) => (
        <Input
          size="small"
          className="font-bold text-xs rounded-md bg-slate-50 text-slate-800"
          value={text}
          placeholder="Session 01"
          onChange={(e) =>
            updateSessionGroupField(index, "session_id", e.target.value)
          }
        />
      ),
    },
    {
      title: "Loại Session",
      dataIndex: "session_type_vn",
      key: "session_type_vn",
      width: expandedColumns ? 135 : 115,
      onCell: (_, index) => ({
        rowSpan: getSessionRowSpan(data, index ?? 0),
      }),
      render: (text, _, index) => (
        <Select
          size="small"
          className="w-full text-xs"
          value={text || "Lý thuyết"}
          onChange={(val) =>
            updateSessionGroupField(index, "session_type_vn", val)
          }
          options={[
            { value: "Định hướng", label: "Định hướng" },
            { value: "Lý thuyết", label: "Lý thuyết" },
            { value: "Thực hành", label: "Thực hành" },
            { value: "Mini Project", label: "Mini Project" },
            { value: "Capstone Project", label: "Capstone Project" },
          ]}
        />
      ),
    },
    {
      title: "Mã Session",
      dataIndex: "session_code",
      key: "session_code",
      width: expandedColumns ? 145 : 125,
      onCell: (_, index) => ({
        rowSpan: getSessionRowSpan(data, index ?? 0),
      }),
      render: (text, _, index) => (
        <Select
          size="small"
          className="w-full text-xs font-mono"
          value={text || "THEORY"}
          onChange={(val) =>
            updateSessionGroupField(index, "session_code", val)
          }
          options={[
            {
              value: "ORIENTATION",
              label: (
                <Tag color="blue" className="m-0">
                  ORIENTATION
                </Tag>
              ),
            },
            {
              value: "THEORY",
              label: (
                <Tag color="cyan" className="m-0">
                  THEORY
                </Tag>
              ),
            },
            {
              value: "PRACTICE",
              label: (
                <Tag color="purple" className="m-0">
                  PRACTICE
                </Tag>
              ),
            },
            {
              value: "MINI_PROJECT",
              label: (
                <Tag color="orange" className="m-0">
                  MINI_PROJECT
                </Tag>
              ),
            },
            {
              value: "FINAL_PROJECT",
              label: (
                <Tag color="magenta" className="m-0">
                  FINAL_PROJECT
                </Tag>
              ),
            },
          ]}
        />
      ),
    },
    {
      title: "Tiêu Đề Session",
      dataIndex: "session_title",
      key: "session_title",
      width: expandedColumns ? 260 : "12%",
      onCell: (_, index) => ({
        rowSpan: getSessionRowSpan(data, index ?? 0),
      }),
      render: (text, _, index) => (
        <Input.TextArea
          autoSize={{ minRows: 2, maxRows: 6 }}
          size="small"
          className="text-xs rounded-md font-bold text-slate-800 bg-slate-50"
          value={text}
          placeholder="Session Title..."
          onChange={(e) =>
            updateSessionGroupField(index, "session_title", e.target.value)
          }
        />
      ),
    },
    {
      title: "Tên Lesson",
      dataIndex: "lesson_title",
      key: "lesson_title",
      width: expandedColumns ? 240 : "12%",
      render: (text, _, index) => (
        <Input.TextArea
          autoSize={{ minRows: 1, maxRows: 4 }}
          size="small"
          className="text-xs rounded-md font-medium"
          value={text}
          placeholder="Bài 01: ..."
          onChange={(e) => updateRow(index, "lesson_title", e.target.value)}
        />
      ),
    },
    {
      title: "Nội Dung Chi Tiết (Lesson Scope)",
      dataIndex: "details",
      key: "details",
      width: expandedColumns ? 360 : "18%",
      render: (text, _, index) => (
        <Input.TextArea
          autoSize={{ minRows: 2, maxRows: 6 }}
          size="small"
          className="text-xs rounded-md"
          value={text}
          placeholder="Mô tả chi tiết prompt context cho AI..."
          onChange={(e) => updateRow(index, "details", e.target.value)}
        />
      ),
    },
    {
      title: (
        <span className="text-teal-700 font-bold flex items-center gap-1">
          Kết Quả Mong Đợi (Outcome)
        </span>
      ),
      dataIndex: "expected_outcome",
      key: "expected_outcome",
      width: expandedColumns ? 340 : "18%",
      render: (text, _, index) => (
        <Input.TextArea
          autoSize={{ minRows: 2, maxRows: 6 }}
          size="small"
          className="text-xs rounded-md border-teal-200 bg-teal-50/20 text-teal-900 font-medium"
          value={text}
          placeholder="Sản phẩm / Năng lực sinh viên tự làm/viết được..."
          onChange={(e) => updateRow(index, "expected_outcome", e.target.value)}
        />
      ),
    },
    {
      title: (
        <span className="text-rose-700 font-bold flex items-center gap-1">
          Phạm Vi CẤM DÙNG
        </span>
      ),
      dataIndex: "forbidden_scope",
      key: "forbidden_scope",
      width: expandedColumns ? 300 : "16%",
      render: (text, _, index) => (
        <Input.TextArea
          autoSize={{ minRows: 1, maxRows: 5 }}
          size="small"
          className="text-xs rounded-md border-rose-200 bg-rose-50/30 text-rose-900"
          value={text}
          placeholder="Chưa dùng OOP, chưa dùng Database..."
          onChange={(e) => updateRow(index, "forbidden_scope", e.target.value)}
        />
      ),
    },
    {
      title: (
        <span className="text-emerald-700 font-bold flex items-center gap-1">
          Phạm Vi ĐÃ HỌC (Output)
        </span>
      ),
      dataIndex: "allowed_scope",
      key: "allowed_scope",
      width: expandedColumns ? 300 : "16%",
      render: (text, _, index) => (
        <Input.TextArea
          autoSize={{ minRows: 1, maxRows: 5 }}
          size="small"
          className="text-xs rounded-md border-emerald-200 bg-emerald-50/30 text-emerald-900"
          value={text}
          placeholder="Cú pháp căn bản print, input, if-else..."
          onChange={(e) => updateRow(index, "allowed_scope", e.target.value)}
        />
      ),
    },
    {
      title: "Tech Stack",
      dataIndex: "tech_stack",
      key: "tech_stack",
      width: expandedColumns ? 150 : 100,
      render: (text, _, index) => (
        <Input
          size="small"
          className="text-xs rounded-md font-mono"
          value={text}
          placeholder="python/core"
          onChange={(e) => updateRow(index, "tech_stack", e.target.value)}
        />
      ),
    },
  ];

  return (
    <Modal
      title={
        <div className="flex items-center gap-2 text-lg font-bold text-slate-800">
          <TableIcon className="text-teal-600" size={22} /> Cấu Trúc Khóa Học
        </div>
      }
      open={open}
      onCancel={onCancel}
      width={expandedColumns ? "96vw" : "94vw"}
      style={{ top: 15 }}
      footer={
        <div className="flex flex-col sm:flex-row justify-between gap-3 mt-4">
          <div className="flex flex-wrap gap-2">
            <Button
              icon={<Sparkles size={16} />}
              className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-bold border-none hover:from-indigo-700 hover:to-purple-700 shadow-sm"
              onClick={() => setGenerateModalOpen(true)}
              disabled={isAutoFixing || isReviewing}
            >
              AI Sinh PM 10 Cột Tự Động
            </Button>
            <Button
              icon={<Sparkles size={16} />}
              type="dashed"
              className="text-teal-700 border-teal-600 font-semibold hover:bg-teal-50"
              onClick={handleReview}
              loading={isReviewing}
              disabled={isAutoFixing}
            >
              {isReviewing ? "Đang thẩm định..." : "AI Review PM"}
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
                AI Tự Sửa PM Sư Phạm
              </Button>
            )}
            {selectedRowKeys.length > 0 && (
              <Button
                danger
                type="primary"
                icon={<Trash2 size={16} />}
                onClick={handleBatchDeleteRows}
                disabled={isAutoFixing || isReviewing}
                className="font-semibold shadow-sm animate-pulse"
              >
                Xóa {selectedRowKeys.length} Dòng Đã Chọn
              </Button>
            )}
            <Button
              icon={
                expandedColumns ? (
                  <Minimize2 size={16} />
                ) : (
                  <Maximize2 size={16} />
                )
              }
              onClick={() => setExpandedColumns(!expandedColumns)}
              className="font-medium text-xs border-teal-300 text-teal-800 hover:bg-teal-50"
              disabled={isAutoFixing || isReviewing}
            >
              {expandedColumns ? "Co gọn vừa màn hình" : "Mở rộng"}
            </Button>
          </div>
          <div className="flex gap-2">
            <Button
              onClick={onCancel}
              disabled={isConfirming || isReviewing || isAutoFixing}
            >
              Hủy
            </Button>
            <Button
              type="primary"
              icon={<Save size={16} />}
              loading={isConfirming}
              onClick={() => onConfirm(data)}
              disabled={isAutoFixing || isReviewing}
              className="bg-teal-600 hover:bg-teal-700 font-semibold"
            >
              Xác Nhận Nhập Vào DB & PM Excel
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
                  __html: DOMPurify.sanitize(
                    marked.parse(reviewResult) as string,
                  ),
                }}
              />
            }
            type="warning"
            showIcon
            closable
            onClose={() => setReviewResult(null)}
            className="rounded-xl border-amber-200 bg-amber-50/60"
          />
        )}

        <Table
          columns={columns}
          dataSource={data}
          rowKey={(_, index) => index as number}
          rowSelection={{
            selectedRowKeys,
            onChange: (newSelectedKeys) => setSelectedRowKeys(newSelectedKeys),
          }}
          pagination={false}
          scroll={{
            x: expandedColumns ? 2450 : "100%",
            y: reviewResult ? 280 : 520,
          }}
          size="small"
          bordered
          className="rounded-xl overflow-hidden border border-slate-200"
        />
      </div>

      <GeneratePMModal
        open={generateModalOpen}
        onCancel={() => setGenerateModalOpen(false)}
        onSuccess={(generatedRows) => {
          setData(generatedRows);
          setReviewResult(null);
        }}
      />
    </Modal>
  );
};
