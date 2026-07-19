import {
  Modal,
  Tabs,
  Spin,
  Empty,
  Card,
  Input,
  Button,
  Checkbox,
  Popconfirm,
  message,
} from "antd";
import {
  useArtifacts,
  ArtifactResponse,
  ArtifactVersion,
} from "../hooks/useLessons";
import { useSessionArtifacts } from "../../sessions/hooks/useSessions";
import { marked } from "marked";
import DOMPurify from "dompurify";
import { useRef, useEffect, useState } from "react";
import { Transformer } from "markmap-lib";
import { Markmap } from "markmap-view";
import { useQueryClient } from "@tanstack/react-query";
import { apiClient } from "../../../shared/api/base";
import { Trash2, Plus, Save, XCircle, Maximize2, Minimize2 } from "lucide-react";

interface RawGeneralQuizQuestion {
  question_content?: string;
  question?: string;
  question_text?: string;
  isCorrect?: string | number;
  answer_1?: string;
  answer_2?: string;
  answer_3?: string;
  answer_4?: string;
  explanation?: string;
  explanation_answer_1?: string;
  explanation_answer_2?: string;
  explanation_answer_3?: string;
  explanation_answer_4?: string;
  options?: Array<
    | {
        option_text?: string;
        is_correct?: boolean;
      }
    | string
  >;
  correct_option_index?: number;
}

interface RawQuizData {
  quiz?: RawGeneralQuizQuestion[];
  lesson_quiz?: RawGeneralQuizQuestion[];
  quiz_title?: string;
  quiz_description?: string;
  questions?: RawGeneralQuizQuestion[];
  practical_lab?: {
    title: string;
    objectives?: string[];
    description?: {
      inputs?: string;
      steps?: string[];
    };
    evaluation?: {
      checklist?: string[];
    };
  };
}

interface HomeworkExercise {
  index: number;
  level: string;
  folder_name: string;
  title: string;
  content: string;
  rubric: string;
}

interface ProjectEntryTest {
  title?: string;
  content?: string;
}

const transformer = new Transformer();

export const MarkmapComponent = ({ markmapData }: { markmapData: string }) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const mmRef = useRef<Markmap | null>(null);
  const [isFullscreen, setIsFullscreen] = useState(false);

  useEffect(() => {
    if (!svgRef.current) return;

    let cleanMd = markmapData.trim();
    if (cleanMd.startsWith("```")) {
      cleanMd = cleanMd.replace(/^```[a-zA-Z]*\r?\n/, "");
      cleanMd = cleanMd.replace(/\r?\n```$/, "");
      cleanMd = cleanMd.trim();
    }



    // Replace markdown image syntax with HTML img tags for inline rendering in Markmap
    cleanMd = cleanMd.replace(/!\[(.*?)\]\((.*?)\)/g, (_match, alt, src) => {
      return `<img src="${src}" alt="${alt}" style="max-height: 100px; max-width: 200px; display: block; margin: 6px auto; border-radius: 4px; border: 1px solid #e2e8f0; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);" />`;
    });

    const { root } = transformer.transform(cleanMd);

    if (!mmRef.current) {
      mmRef.current = Markmap.create(
        svgRef.current,
        {
          autoFit: true,
        },
        root,
      );
    } else {
      mmRef.current.setData(root);
      mmRef.current.fit();
    }
  }, [markmapData]);

  // Fit markmap when fullscreen toggles
  useEffect(() => {
    if (!mmRef.current) return;
    const timer = setTimeout(() => {
      mmRef.current?.fit();
    }, 150);
    return () => clearTimeout(timer);
  }, [isFullscreen]);

  // Handle escape key to exit fullscreen
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isFullscreen) {
        setIsFullscreen(false);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isFullscreen]);

  // Clean up on unmount
  useEffect(() => {
    return () => {
      if (mmRef.current) {
        mmRef.current.destroy();
        mmRef.current = null;
      }
    };
  }, []);

  const containerStyle = isFullscreen
    ? {
        position: "fixed" as const,
        top: 0,
        left: 0,
        width: "100vw",
        height: "100vh",
        backgroundColor: "#ffffff",
        zIndex: 99999,
        overflow: "hidden",
        padding: "20px",
        display: "flex",
        flexDirection: "column" as const,
      }
    : {
        position: "relative" as const,
        width: "100%",
        height: "65vh",
        border: "1px solid #e2e8f0",
        borderRadius: "8px",
        backgroundColor: "#f9fafb",
        overflow: "hidden",
        display: "flex",
        flexDirection: "column" as const,
      };

  return (
    <div style={containerStyle}>
      <div className="absolute top-3 right-3 z-10 flex gap-2">
        <button
          onClick={() => mmRef.current?.fit()}
          className="px-3 py-1.5 text-xs font-semibold bg-white hover:bg-gray-100 text-gray-700 rounded-md border border-gray-200 shadow-sm transition-all cursor-pointer flex items-center gap-1.5"
        >
          Thu phóng vừa màn hình
        </button>
        <button
          onClick={() => setIsFullscreen(!isFullscreen)}
          className="px-3 py-1.5 text-xs font-semibold bg-white hover:bg-gray-100 text-gray-700 rounded-md border border-gray-200 shadow-sm transition-all cursor-pointer flex items-center gap-1.5"
        >
          {isFullscreen ? <Minimize2 size={14} /> : <Maximize2 size={14} />}
          <span>{isFullscreen ? "Thu nhỏ lại" : "Toàn màn hình"}</span>
        </button>
      </div>
      <div className="flex-1 w-full h-full">
        <svg ref={svgRef} className="w-full h-full" />
      </div>
    </div>
  );
};

interface EditableQuestion {
  question_text: string;
  options: {
    option_text: string;
    is_correct: boolean;
  }[];
  explanation: string;
  optionExplanations: string[];
}

interface QuizEditorProps {
  artifact: ArtifactResponse;
  lessonId?: number | null;
  sessionId?: number | null;
}

export const QuizEditor = ({
  artifact,
  lessonId,
  sessionId,
}: QuizEditorProps) => {
  const queryClient = useQueryClient();
  const [questionsList, setQuestionsList] = useState<EditableQuestion[]>([]);
  const [isDirty, setIsDirty] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  const [editingQuestionIdx, setEditingQuestionIdx] = useState<number | null>(
    null,
  );
  const [editingOption, setEditingOption] = useState<{
    qIdx: number;
    oIdx: number;
  } | null>(null);
  const [editingExplanation, setEditingExplanation] = useState<{
    qIdx: number;
    oIdx: number | "general";
  } | null>(null);

  useEffect(() => {
    if (!artifact?.content_json) {
      setQuestionsList([]);
      return;
    }
    const rawData = artifact.content_json as RawQuizData;
    let questions: EditableQuestion[] = [];

    const parseOptions = (q: RawGeneralQuizQuestion, isCorrectIdx?: number) => {
      const options: { option_text: string; is_correct: boolean }[] = [];

      if (Array.isArray(q.options)) {
        q.options.forEach((opt, idx) => {
          if (typeof opt === "object" && opt !== null) {
            options.push({
              option_text: opt.option_text || "",
              is_correct: !!opt.is_correct,
            });
          } else {
            options.push({
              option_text: String(opt),
              is_correct: idx === q.correct_option_index,
            });
          }
        });
      } else {
        options.push(
          { option_text: q.answer_1 || "", is_correct: isCorrectIdx === 1 },
          { option_text: q.answer_2 || "", is_correct: isCorrectIdx === 2 },
          { option_text: q.answer_3 || "", is_correct: isCorrectIdx === 3 },
          { option_text: q.answer_4 || "", is_correct: isCorrectIdx === 4 },
        );
      }
      return options.filter((o) => o.option_text !== "");
    };

    if (rawData.quiz && Array.isArray(rawData.quiz)) {
      questions = rawData.quiz.map((q) => {
        const isCorrectIdx = Number(q.isCorrect) || 1;
        const options = parseOptions(q, isCorrectIdx);
        return {
          question_text: q.question_content || q.question || "",
          options,
          explanation: q.explanation || "",
          optionExplanations: [
            q.explanation_answer_1 || "",
            q.explanation_answer_2 || "",
            q.explanation_answer_3 || "",
            q.explanation_answer_4 || "",
          ],
        };
      });
    } else if (rawData.lesson_quiz && Array.isArray(rawData.lesson_quiz)) {
      questions = rawData.lesson_quiz.map((q) => {
        const options = parseOptions(q);
        return {
          question_text: q.question || q.question_text || "",
          options,
          explanation: q.explanation || "",
          optionExplanations: [
            q.explanation_answer_1 || "",
            q.explanation_answer_2 || "",
            q.explanation_answer_3 || "",
            q.explanation_answer_4 || "",
          ],
        };
      });
    } else if (rawData.questions && Array.isArray(rawData.questions)) {
      questions = rawData.questions.map((q) => {
        const options = parseOptions(q);
        return {
          question_text: q.question_text || q.question || "",
          options,
          explanation: q.explanation || "",
          optionExplanations: [
            q.explanation_answer_1 || "",
            q.explanation_answer_2 || "",
            q.explanation_answer_3 || "",
            q.explanation_answer_4 || "",
          ],
        };
      });
    }

    setQuestionsList(questions);
    setIsDirty(false);
  }, [artifact]);

  const handleSave = async () => {
    if (!artifact?.content_json) return;
    setIsSaving(true);
    try {
      const rawData = artifact.content_json as RawQuizData;
      const updatedJson: RawQuizData = { ...rawData };

      if (rawData.quiz && Array.isArray(rawData.quiz)) {
        updatedJson.quiz = questionsList.map((eq) => {
          const correctIdx = eq.options.findIndex((o) => o.is_correct);
          const isCorrectVal = correctIdx !== -1 ? correctIdx + 1 : 1;
          return {
            question_content: eq.question_text,
            question: eq.question_text,
            answer_1: eq.options[0]?.option_text || "",
            answer_2: eq.options[1]?.option_text || "",
            answer_3: eq.options[2]?.option_text || "",
            answer_4: eq.options[3]?.option_text || "",
            isCorrect: isCorrectVal,
            explanation: eq.explanation,
            explanation_answer_1: eq.optionExplanations[0] || "",
            explanation_answer_2: eq.optionExplanations[1] || "",
            explanation_answer_3: eq.optionExplanations[2] || "",
            explanation_answer_4: eq.optionExplanations[3] || "",
          };
        });
      } else if (rawData.lesson_quiz && Array.isArray(rawData.lesson_quiz)) {
        updatedJson.lesson_quiz = questionsList.map((eq) => {
          const correctIdx = eq.options.findIndex((o) => o.is_correct);
          return {
            question: eq.question_text,
            options: eq.options.map((o) => ({
              option_text: o.option_text,
              is_correct: o.is_correct,
            })),
            correct_option_index: correctIdx !== -1 ? correctIdx : 0,
            explanation: eq.explanation,
            explanation_answer_1: eq.optionExplanations[0] || "",
            explanation_answer_2: eq.optionExplanations[1] || "",
            explanation_answer_3: eq.optionExplanations[2] || "",
            explanation_answer_4: eq.optionExplanations[3] || "",
          };
        });
      } else {
        updatedJson.questions = questionsList.map((eq) => {
          const correctIdx = eq.options.findIndex((o) => o.is_correct);
          return {
            question_text: eq.question_text,
            options: eq.options.map((o) => ({
              option_text: o.option_text,
              is_correct: o.is_correct,
            })),
            correct_option_index: correctIdx !== -1 ? correctIdx : 0,
            explanation: eq.explanation,
            explanation_answer_1: eq.optionExplanations[0] || "",
            explanation_answer_2: eq.optionExplanations[1] || "",
            explanation_answer_3: eq.optionExplanations[2] || "",
            explanation_answer_4: eq.optionExplanations[3] || "",
          };
        });
      }

      message.loading({
        content: "Đang lưu thay đổi...",
        key: "save-quiz",
        duration: 0,
      });
      await apiClient.put(`/artifacts/${artifact.id}`, {
        content_json: updatedJson,
      });

      queryClient.invalidateQueries({
        queryKey: lessonId
          ? ["artifacts", lessonId]
          : ["session_artifacts", sessionId],
      });
      message.success({
        content: "Đã lưu thay đổi quizz thành công!",
        key: "save-quiz",
        duration: 3,
      });
      setIsDirty(false);
    } catch (err) {
      console.error(err);
      message.error({
        content: "Lưu thay đổi thất bại!",
        key: "save-quiz",
        duration: 3,
      });
    } finally {
      setIsSaving(false);
    }
  };

  const addQuestion = () => {
    setQuestionsList([
      ...questionsList,
      {
        question_text: "Câu hỏi mới",
        options: [
          { option_text: "Lựa chọn A", is_correct: true },
          { option_text: "Lựa chọn B", is_correct: false },
          { option_text: "Lựa chọn C", is_correct: false },
          { option_text: "Lựa chọn D", is_correct: false },
        ],
        explanation: "Giải thích đáp án đúng",
        optionExplanations: ["", "", "", ""],
      },
    ]);
    setIsDirty(true);
  };

  const deleteQuestion = (index: number) => {
    const updated = [...questionsList];
    updated.splice(index, 1);
    setQuestionsList(updated);
    setIsDirty(true);
  };

  const editQuestionText = (index: number, text: string) => {
    const updated = [...questionsList];
    updated[index].question_text = text;
    setQuestionsList(updated);
    setIsDirty(true);
  };

  const addOption = (qIdx: number) => {
    const updated = [...questionsList];
    updated[qIdx].options.push({
      option_text: `Lựa chọn mới`,
      is_correct: false,
    });
    updated[qIdx].optionExplanations.push("");
    setQuestionsList(updated);
    setIsDirty(true);
  };

  const deleteOption = (qIdx: number, oIdx: number) => {
    const updated = [...questionsList];
    updated[qIdx].options.splice(oIdx, 1);
    if (updated[qIdx].optionExplanations.length > oIdx) {
      updated[qIdx].optionExplanations.splice(oIdx, 1);
    }
    setQuestionsList(updated);
    setIsDirty(true);
  };

  const editOptionText = (qIdx: number, oIdx: number, text: string) => {
    const updated = [...questionsList];
    updated[qIdx].options[oIdx].option_text = text;
    setQuestionsList(updated);
    setIsDirty(true);
  };

  const toggleCorrectOption = (qIdx: number, oIdx: number) => {
    const updated = [...questionsList];
    updated[qIdx].options.forEach((opt, idx) => {
      opt.is_correct = idx === oIdx;
    });
    setQuestionsList(updated);
    setIsDirty(true);
  };

  const editGeneralExplanation = (qIdx: number, text: string) => {
    const updated = [...questionsList];
    updated[qIdx].explanation = text;
    setQuestionsList(updated);
    setIsDirty(true);
  };

  const editOptionExplanation = (qIdx: number, oIdx: number, text: string) => {
    const updated = [...questionsList];
    while (updated[qIdx].optionExplanations.length <= oIdx) {
      updated[qIdx].optionExplanations.push("");
    }
    updated[qIdx].optionExplanations[oIdx] = text;
    setQuestionsList(updated);
    setIsDirty(true);
  };

  const originalQuizData = artifact.content_json as RawQuizData;
  const lab = originalQuizData?.practical_lab;

  return (
    <div className="max-h-[70vh] overflow-y-auto pr-2">
      <div className="flex justify-between items-center bg-gray-50 border border-gray-200 p-4 rounded-lg mb-6 sticky top-0 z-10 shadow-sm">
        <div className="flex items-center gap-2">
          <span className="font-bold text-gray-800 text-base">
            Trình chỉnh sửa Quizz (AI)
          </span>
          {isDirty && (
            <span className="px-2 py-0.5 bg-amber-100 text-amber-800 text-xs font-semibold rounded border border-amber-200 animate-pulse">
              Có thay đổi chưa lưu
            </span>
          )}
        </div>
        <div className="flex gap-3">
          <Button
            type="dashed"
            icon={<Plus size={16} className="inline mr-1 align-text-bottom" />}
            onClick={addQuestion}
            className="hover:border-blue-500 hover:text-blue-500 h-[36px] flex items-center justify-center"
          >
            Thêm câu hỏi
          </Button>
          <Button
            type="primary"
            disabled={!isDirty}
            loading={isSaving}
            icon={<Save size={16} className="inline mr-1 align-text-bottom" />}
            onClick={handleSave}
            className="bg-blue-600 hover:bg-blue-500 h-[36px] flex items-center justify-center"
          >
            Lưu thay đổi
          </Button>
        </div>
      </div>

      <div className="space-y-4!">
        {questionsList.map((q, qIdx) => (
          <Card
            key={qIdx}
            className="shadow-sm border-gray-200 relative group"
            title={
              <div className="flex items-center gap-3 w-full pr-2">
                <span className="font-bold text-gray-800 text-sm min-w-[55px]">
                  Câu {qIdx + 1}:
                </span>
                {editingQuestionIdx === qIdx ? (
                  <div className="flex-1 flex items-center gap-2">
                    <Input.TextArea
                      autoFocus
                      autoSize={{ minRows: 1, maxRows: 3 }}
                      value={q.question_text}
                      onChange={(e) => editQuestionText(qIdx, e.target.value)}
                      onBlur={() => setEditingQuestionIdx(null)}
                      className="font-medium text-gray-800"
                    />
                    <Button
                      size="small"
                      type="text"
                      onClick={() => setEditingQuestionIdx(null)}
                    >
                      ✓
                    </Button>
                  </div>
                ) : (
                  <div
                    className="flex-1 font-medium text-gray-800 cursor-pointer hover:bg-gray-100/70 p-1.5 rounded transition-all duration-200 border border-transparent hover:border-gray-200/50"
                    onClick={() => setEditingQuestionIdx(qIdx)}
                    title="Nhấp để chỉnh sửa câu hỏi"
                  >
                    {q.question_text || (
                      <span className="text-gray-400 italic">
                        Nhấp để chỉnh sửa nội dung câu hỏi
                      </span>
                    )}
                  </div>
                )}
              </div>
            }
            extra={
              <Popconfirm
                title="Xóa câu hỏi này?"
                description="Bạn có chắc chắn muốn xóa câu hỏi này khỏi danh sách?"
                onConfirm={() => deleteQuestion(qIdx)}
                okText="Xóa"
                cancelText="Hủy"
              >
                <Button
                  type="text"
                  danger
                  icon={<Trash2 size={16} />}
                  className="opacity-70 hover:opacity-100 transition-opacity"
                />
              </Popconfirm>
            }
          >
            <div className="space-y-4">
              <div className="space-y-4">
                {q.options.map((opt, oIdx) => {
                  const letter = String.fromCharCode(65 + oIdx);
                  return (
                    <div
                      key={oIdx}
                      className={`p-3 rounded border transition-all duration-200 ${
                        opt.is_correct
                          ? "bg-green-50/40 border-green-200"
                          : "bg-gray-50/30 border-gray-100"
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <Checkbox
                          checked={opt.is_correct}
                          onChange={() => toggleCorrectOption(qIdx, oIdx)}
                        >
                          <span className="font-bold text-gray-800 mr-1">
                            {letter}.
                          </span>
                        </Checkbox>

                        {editingOption?.qIdx === qIdx &&
                        editingOption?.oIdx === oIdx ? (
                          <div className="flex-1 flex gap-2 items-center">
                            <Input
                              autoFocus
                              value={opt.option_text}
                              onChange={(e) =>
                                editOptionText(qIdx, oIdx, e.target.value)
                              }
                              onBlur={() => setEditingOption(null)}
                              placeholder={`Nhập đáp án ${letter}...`}
                              className="flex-1 h-[36px]"
                            />
                            <Button
                              size="small"
                              type="text"
                              onClick={() => setEditingOption(null)}
                              className="h-[36px] w-[36px] flex items-center justify-center"
                            >
                              ✓
                            </Button>
                          </div>
                        ) : (
                          <div
                            className="flex-1 text-gray-700 cursor-pointer hover:bg-gray-100 px-3 h-[36px] flex items-center rounded transition-all duration-200 border border-transparent hover:border-gray-200/40"
                            onClick={() => setEditingOption({ qIdx, oIdx })}
                            title="Nhấp để chỉnh sửa đáp án"
                          >
                            {opt.option_text || (
                              <span className="text-gray-400 italic">
                                Nhấp để nhập câu trả lời
                              </span>
                            )}
                          </div>
                        )}

                        {q.options.length > 2 && (
                          <Popconfirm
                            title="Xóa đáp án này?"
                            onConfirm={() => deleteOption(qIdx, oIdx)}
                            okText="Xóa"
                            cancelText="Hủy"
                          >
                            <Button
                              type="text"
                              danger
                              size="small"
                              icon={<Trash2 size={14} />}
                              className="h-[36px] w-[36px] flex items-center justify-center"
                            />
                          </Popconfirm>
                        )}
                      </div>

                      {/* Explanations why correct or incorrect */}
                      <div className="mt-2 pl-6">
                        {editingExplanation?.qIdx === qIdx &&
                        editingExplanation?.oIdx === oIdx ? (
                          <div className="flex gap-2 w-full">
                            <Input
                              autoFocus
                              size="small"
                              placeholder={`Giải thích tại sao lựa chọn ${letter} là ${
                                opt.is_correct ? "đúng" : "sai"
                              }...`}
                              value={q.optionExplanations[oIdx] || ""}
                              onChange={(e) =>
                                editOptionExplanation(
                                  qIdx,
                                  oIdx,
                                  e.target.value,
                                )
                              }
                              onBlur={() => setEditingExplanation(null)}
                              className="text-xs text-gray-600 bg-gray-50/50 italic border-dashed flex-1"
                            />
                            <Button
                              size="small"
                              type="text"
                              onClick={() => setEditingExplanation(null)}
                            >
                              ✓
                            </Button>
                          </div>
                        ) : (
                          <div
                            className="text-xs text-gray-600 bg-gray-50/50 italic cursor-pointer hover:bg-gray-100 p-1.5 rounded transition-all duration-200 border border-transparent hover:border-gray-200/30 w-full"
                            onClick={() =>
                              setEditingExplanation({ qIdx, oIdx })
                            }
                            title="Nhấp để chỉnh sửa giải thích"
                          >
                            {q.optionExplanations[oIdx] || (
                              <span className="text-gray-400">
                                Nhấp để thêm giải thích tại sao{" "}
                                {opt.is_correct ? "đúng" : "sai"}...
                              </span>
                            )}
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>

              <div className="flex justify-start">
                <Button
                  type="dashed"
                  icon={
                    <Plus size={14} className="inline mr-1 align-text-bottom" />
                  }
                  onClick={() => addOption(qIdx)}
                  className="text-xs h-[36px] flex items-center justify-center"
                >
                  Thêm lựa chọn
                </Button>
              </div>

              {/* General Explanation */}
              <div className="mt-4 border-t pt-3">
                <div className="font-semibold text-gray-700 text-xs mb-1.5">
                  Giải thích chung:
                </div>
                {editingExplanation?.qIdx === qIdx &&
                editingExplanation?.oIdx === "general" ? (
                  <div className="flex flex-col gap-2">
                    <Input.TextArea
                      autoFocus
                      placeholder="Giải thích chung cho câu hỏi này..."
                      autoSize={{ minRows: 2, maxRows: 4 }}
                      value={q.explanation}
                      onChange={(e) =>
                        editGeneralExplanation(qIdx, e.target.value)
                      }
                      onBlur={() => setEditingExplanation(null)}
                      className="text-xs text-gray-600 bg-gray-50/30"
                    />
                    <div className="flex justify-end">
                      <Button
                        size="small"
                        type="text"
                        onClick={() => setEditingExplanation(null)}
                      >
                        ✓ Xong
                      </Button>
                    </div>
                  </div>
                ) : (
                  <div
                    className="text-xs text-gray-600 bg-gray-50/30 p-2.5 rounded cursor-pointer hover:bg-gray-100/50 transition-all duration-200 border border-transparent hover:border-gray-200/30 min-h-[40px]"
                    onClick={() =>
                      setEditingExplanation({ qIdx, oIdx: "general" })
                    }
                    title="Nhấp để chỉnh sửa giải thích chung"
                  >
                    {q.explanation || (
                      <span className="text-gray-400 italic">
                        Nhấp để thêm giải thích chung cho câu hỏi này...
                      </span>
                    )}
                  </div>
                )}
              </div>
            </div>
          </Card>
        ))}
      </div>

      {lab && (
        <Card
          title={
            <span className="text-blue-800 font-bold">
              Bài thực hành đi kèm: {lab.title}
            </span>
          }
          className="mt-8 border-blue-200 shadow-md bg-blue-50/10"
          headStyle={{
            backgroundColor: "#f0f7ff",
            borderBottom: "1px solid #bfdbfe",
          }}
        >
          <div className="space-y-4 text-sm text-gray-700">
            {lab.objectives && (
              <div>
                <h5 className="font-semibold text-gray-900 mb-1">
                  Mục tiêu bài thực hành:
                </h5>
                <ul className="list-disc pl-5 space-y-1">
                  {lab.objectives.map((obj: string, idx: number) => (
                    <li key={idx}>{obj}</li>
                  ))}
                </ul>
              </div>
            )}
            {lab.description?.steps && (
              <div>
                <h5 className="font-semibold text-gray-900 mb-1">
                  Các bước thực hiện:
                </h5>
                <ol className="list-decimal pl-5 space-y-1">
                  {lab.description.steps.map((step: string, idx: number) => (
                    <li key={idx}>{step}</li>
                  ))}
                </ol>
              </div>
            )}
          </div>
        </Card>
      )}
    </div>
  );
};

export const ArtifactVersionWrapper = ({
  artifact,
  lessonId,
  sessionId,
  exerciseIndex,
  children,
}: {
  artifact: ArtifactResponse;
  lessonId?: number | null;
  sessionId?: number | null;
  exerciseIndex?: number | null;
  children: (previewedArt: ArtifactResponse) => React.ReactNode;
}) => {
  const queryClient = useQueryClient();
  const [selectedVersionId, setSelectedVersionId] = useState<number | null>(
    null,
  );
  const [isRegenerating, setIsRegenerating] = useState(false);
  const [isSelecting, setIsSelecting] = useState(false);

  const versionsList = artifact.versions || [];

  // Find current active version in the list (or match by content)
  const activeVersion =
    versionsList.find(
      (v: ArtifactVersion) =>
        v.content === artifact.content &&
        JSON.stringify(v.content_json) ===
          JSON.stringify(artifact.content_json),
    ) || versionsList[versionsList.length - 1];

  const currentPreviewVersionId =
    selectedVersionId ?? activeVersion?.version_id ?? null;

  const previewedVersion = versionsList.find(
    (v: ArtifactVersion) => v.version_id === currentPreviewVersionId,
  );

  // Construct mock artifact with previewed version's content
  const previewedArtifact: ArtifactResponse = previewedVersion
    ? {
        ...artifact,
        content: previewedVersion.content,
        content_json: previewedVersion.content_json,
      }
    : artifact;

  const handleRegenerate = async () => {
    try {
      setIsRegenerating(true);
      message.loading({
        content: "Đang yêu cầu AI tạo lại tài nguyên...",
        key: "regenerate-artifact",
        duration: 0,
      });

      await apiClient.post(`/artifacts/${artifact.id}/regenerate`, {
        exercise_index: exerciseIndex || null,
      });
      message.success({
        content: "Đã kích hoạt tạo lại tài nguyên bằng AI!",
        key: "regenerate-artifact",
        duration: 3,
      });

      // Reset selected version so that the newest version will automatically be previewed when completed
      setSelectedVersionId(null);

      // Invalidate queries to refresh status
      queryClient.invalidateQueries({ queryKey: ["artifacts", lessonId] });
      queryClient.invalidateQueries({
        queryKey: ["session_artifacts", sessionId],
      });
    } catch (error) {
      console.error(error);
      message.error({
        content: "Gặp lỗi khi tạo lại tài nguyên.",
        key: "regenerate-artifact",
        duration: 3,
      });
    } finally {
      setIsRegenerating(false);
    }
  };

  const handleSelectVersion = async (versionId: number) => {
    try {
      setIsSelecting(true);
      message.loading({
        content: "Đang áp dụng phiên bản đã chọn...",
        key: "select-version",
        duration: 0,
      });

      await apiClient.post(`/artifacts/${artifact.id}/select-version`, {
        version_id: versionId,
      });
      message.success({
        content: "Đã lưu và áp dụng phiên bản thành công!",
        key: "select-version",
        duration: 3,
      });
      setSelectedVersionId(null);

      // Invalidate queries to refresh the active artifact content
      queryClient.invalidateQueries({ queryKey: ["artifacts", lessonId] });
      queryClient.invalidateQueries({
        queryKey: ["session_artifacts", sessionId],
      });
    } catch (error) {
      console.error(error);
      message.error({
        content: "Gặp lỗi khi lưu phiên bản.",
        key: "select-version",
        duration: 3,
      });
    } finally {
      setIsSelecting(false);
    }
  };

  const isCurrentActive = activeVersion?.version_id === currentPreviewVersionId;

  return (
    <div className="flex flex-col gap-4">
      {/* Version Control Header */}
      <div className="flex flex-wrap items-center justify-between gap-3 p-3.5 bg-slate-50 border border-slate-200/80 rounded-xl shadow-sm">
        <div className="flex items-center gap-3">
          <span className="text-xs font-bold text-slate-700 tracking-wide uppercase">
            Lịch sử phiên bản:
          </span>
          {versionsList.length === 0 ? (
            <span className="text-xs text-slate-400 italic">
              Chưa có phiên bản (Bấm Tạo lại để lưu phiên bản hiện tại và sinh
              bản mới)
            </span>
          ) : (
            <div className="flex items-center gap-2">
              {versionsList.map((v: ArtifactVersion) => {
                const isSelected = v.version_id === currentPreviewVersionId;
                const isActive = v.version_id === activeVersion?.version_id;

                let btnType: "primary" | "dashed" | "default" = "default";
                if (isSelected) btnType = "primary";

                let activeBorder = "";
                if (isActive)
                  activeBorder =
                    "ring-2 ring-emerald-500/40 border-emerald-500 hover:border-emerald-600";

                const displayTime = v.created_at
                  ? new Date(v.created_at).toLocaleTimeString("vi-VN", {
                      hour: "2-digit",
                      minute: "2-digit",
                    })
                  : "";

                return (
                  <Button
                    key={v.version_id}
                    size="small"
                    type={btnType}
                    onClick={() => setSelectedVersionId(v.version_id)}
                    className={`h-[30px] px-3 text-xs flex items-center gap-1.5 font-medium rounded-lg transition-all ${activeBorder}`}
                  >
                    V{v.version_id} {displayTime && `(${displayTime})`}
                    {isActive && (
                      <span
                        className="w-1.5 h-1.5 rounded-full bg-emerald-500 inline-block"
                        title="Phiên bản đang hoạt động"
                      />
                    )}
                  </Button>
                );
              })}
            </div>
          )}
        </div>

        <div className="flex items-center gap-2.5">
          {versionsList.length > 0 && !isCurrentActive && (
            <Button
              size="small"
              type="primary"
              className="bg-emerald-600 hover:bg-emerald-700 border-emerald-600 hover:border-emerald-700 h-[32px] px-4 text-xs font-semibold rounded-lg flex items-center shadow-sm"
              onClick={() =>
                currentPreviewVersionId &&
                handleSelectVersion(currentPreviewVersionId)
              }
              loading={isSelecting}
            >
              Xác nhận phiên bản V{currentPreviewVersionId}
            </Button>
          )}

          <Button
            size="small"
            type="primary"
            danger
            ghost
            className="h-[32px] px-4 text-xs font-semibold rounded-lg flex items-center hover:bg-red-50"
            onClick={handleRegenerate}
            loading={isRegenerating || artifact.status === "Pending"}
          >
            Tạo bản mới (AI)
          </Button>
        </div>
      </div>

      {/* Render the children with the previewed/active content */}
      <div className="flex-1">{children(previewedArtifact)}</div>
    </div>
  );
};

interface Props {
  open: boolean;
  lessonId?: number | null;
  sessionId?: number | null;
  title: string;
  onCancel: () => void;
  exerciseIndex?: number | null;
}

export const ArtifactPreviewModal = ({
  open,
  lessonId,
  sessionId,
  title,
  onCancel,
  exerciseIndex,
}: Props) => {
  const { data: lessonArtifacts, isLoading: isLessonLoading } = useArtifacts(
    lessonId || null,
  );
  const { data: sessionArtifacts, isLoading: isSessionLoading } =
    useSessionArtifacts(sessionId || null);

  const artifacts = lessonId ? lessonArtifacts : sessionArtifacts;
  const isLoading = lessonId ? isLessonLoading : isSessionLoading;

  const renderContent = (artifact: ArtifactResponse) => {
    if (artifact.status === "Pending") {
      return (
        <div className="flex flex-col justify-center items-center h-[400px] gap-4 bg-gray-50 rounded-lg border border-dashed border-gray-300">
          <Spin size="large" />
          <div className="text-gray-500 italic">
            Agent đang miệt mài viết phần {artifact.type}...
          </div>
        </div>
      );
    }

    if (artifact.status === "Failed") {
      return (
        <div className="flex flex-col justify-center items-center h-[400px] gap-4 bg-red-50 rounded-lg border border-dashed border-red-300">
          <XCircle size={36} className="text-red-500" />
          <div className="text-red-500 font-semibold">
            Gặp lỗi trong quá trình tự động sinh phần {artifact.type}.
          </div>
          <div className="text-gray-500 text-sm">
            Vui lòng bấm nút "Tạo AI" lại để hệ thống khôi phục từ checkpoint.
          </div>
        </div>
      );
    }

    if (
      (artifact.type === "quiz" ||
        artifact.type === "pre_quiz" ||
        artifact.type === "post_quiz") &&
      artifact.content_json
    ) {
      return (
        <QuizEditor
          artifact={artifact}
          lessonId={lessonId}
          sessionId={sessionId}
        />
      );
    }

    if (
      (artifact.type === "outline" || artifact.type === "session_mindmap") &&
      artifact.content
    ) {
      return <MarkmapComponent markmapData={artifact.content} />;
    }

    if (
      (artifact.type === "walkthrough" ||
        artifact.type === "project_srs" ||
        artifact.type === "project_mini_project") &&
      artifact.content
    ) {
      let markdown = artifact.content.trim();
      if (markdown.startsWith("```")) {
        markdown = markdown.replace(/^```[a-zA-Z]*\r?\n/, "");
        markdown = markdown.replace(/\r?\n```$/, "");
        markdown = markdown.trim();
      }

      const rawHtml = marked.parse(markdown) as string;
      const cleanHtml = DOMPurify.sanitize(rawHtml);

      let htmlRubric = "";
      if (artifact.type === "project_mini_project" && artifact.content_json?.rubric) {
        let rubricMd = artifact.content_json.rubric.trim();
        if (rubricMd.startsWith("```")) {
          rubricMd = rubricMd.replace(/^```[a-zA-Z]*\r?\n/, "");
          rubricMd = rubricMd.replace(/\r?\n```$/, "");
          rubricMd = rubricMd.trim();
        }
        htmlRubric = DOMPurify.sanitize(marked.parse(rubricMd) as string);
      }

      return (
        <div className="bg-white border rounded-lg p-6 h-[60vh] overflow-y-auto pr-2 space-y-6">
          <div
            className="markdown-content animate-fade-in"
            dangerouslySetInnerHTML={{ __html: cleanHtml }}
          />
          {htmlRubric && (
            <div>
              <div className="font-semibold text-gray-700 mb-2 border-l-4 border-green-500 pl-2">
                Tiêu chí chấm điểm (AI)
              </div>
              <div
                className="markdown-content text-gray-600 bg-green-50/10 p-4 rounded-lg border border-green-100"
                dangerouslySetInnerHTML={{ __html: htmlRubric }}
              />
            </div>
          )}
        </div>
      );
    }

    if (artifact.type === "project_entry_tests" && artifact.content_json?.entry_tests) {
      const allTests = (artifact.content_json.entry_tests || []) as ProjectEntryTest[];
      return (
        <div className="max-h-[60vh] overflow-y-auto pr-2 space-y-6">
          {allTests.map((test: ProjectEntryTest, idx: number) => {
            const htmlContent = DOMPurify.sanitize(
              marked.parse(test.content || "") as string,
            );
            return (
              <Card
                key={idx}
                title={
                  <div className="font-bold text-base text-gray-800">
                    Đề kiểm tra {idx + 1}: {test.title || `Bài kiểm tra đầu giờ ${idx + 1}`}
                  </div>
                }
                className="shadow-sm border-blue-100 hover:border-blue-200 transition-all duration-200"
                headStyle={{ backgroundColor: "#f8fafc" }}
              >
                <div className="space-y-4">
                  <div>
                    <div className="font-semibold text-gray-700 mb-2 border-l-4 border-indigo-500 pl-2">
                      Nội dung câu hỏi
                    </div>
                    <div
                      className="markdown-content text-gray-700 bg-gray-50/50 p-4 rounded-lg border border-gray-100"
                      dangerouslySetInnerHTML={{ __html: htmlContent }}
                    />
                  </div>
                </div>
              </Card>
            );
          })}
        </div>
      );
    }

    // Default render for HTML/Markdown
    return (
      <div className="bg-white border border-gray-200 rounded-lg h-[60vh]">
        <iframe
          srcDoc={artifact.content ?? undefined}
          className="w-full h-full border-0 rounded-lg"
          sandbox="allow-same-origin allow-scripts"
        />
      </div>
    );
  };

  const renderHomeworkContent = (
    artifact: ArtifactResponse,
    type: "levels" | "comprehensive" | "all",
  ) => {
    if (artifact.status === "Pending") {
      return (
        <div className="flex flex-col justify-center items-center h-[400px] gap-4 bg-gray-50 rounded-lg border border-dashed border-gray-300">
          <Spin size="large" />
          <div className="text-gray-500 italic">
            Agent đang miệt mài tạo bài tập...
          </div>
        </div>
      );
    }

    if (artifact.status === "Failed") {
      return (
        <div className="flex flex-col justify-center items-center h-[400px] gap-4 bg-red-50 rounded-lg border border-dashed border-red-300">
          <XCircle size={36} className="text-red-500" />
          <div className="text-red-500 font-semibold">
            Gặp lỗi trong quá trình tự động sinh bài tập.
          </div>
          <div className="text-gray-500 text-sm">
            Vui lòng bấm nút "Tạo AI" lại để hệ thống khôi phục từ checkpoint.
          </div>
        </div>
      );
    }

    if (!artifact.content_json) {
      return <Empty description="Không có dữ liệu bài tập" />;
    }

    const allExercises = (artifact.content_json.exercises ||
      []) as HomeworkExercise[];
    const exercises = allExercises.filter((ex) => {
      if (type === "levels") {
        return ex.index >= 1 && ex.index <= 5;
      } else if (type === "comprehensive") {
        return ex.index === 6;
      } else {
        return true;
      }
    });

    return (
      <div className="max-h-[70vh] overflow-y-auto pr-2 space-y-6">
        {type !== "all" && (
          <div className="bg-blue-50/50 p-4 rounded-lg border border-blue-100 mb-2">
            <h3 className="text-lg font-bold text-blue-900 mb-1">
              {type === "levels"
                ? "Danh sách bài tập tự luận phân tầng"
                : "Bài tập tổng hợp cuối khóa/cuối buổi"}
            </h3>
            <p className="text-xs text-blue-700/80 m-0">
              {type === "levels"
                ? "Tổng hợp 5 bài tập tự luận nâng cao năng lực lập trình từ Vận dụng cơ bản, Vận dụng chuyên sâu, Phân tích cho đến Sáng tạo."
                : "Bài tập tích hợp tổng hợp kiến thức toàn bộ buổi học giúp hệ thống hóa kỹ năng lập trình."}
            </p>
          </div>
        )}
        <div className="space-y-6">
          {exercises.map((ex: HomeworkExercise, i: number) => {
            const htmlContent = DOMPurify.sanitize(
              marked.parse(ex.content || "") as string,
            );
            const htmlRubric = DOMPurify.sanitize(
              marked.parse(ex.rubric || "") as string,
            );
            return (
              <Card
                key={i}
                title={
                  <div className="flex justify-between items-center w-full">
                    <span className="font-bold text-base text-gray-800">
                      Bài {ex.index}: {ex.title ? ex.title.replace(/<\/?[^>]+(>|$)/g, "").trim() : ""}
                    </span>
                    <span className="px-2.5 py-0.5 bg-blue-100 text-blue-800 text-xs font-semibold rounded-full uppercase tracking-wider">
                      {ex.level}
                    </span>
                  </div>
                }
                className="shadow-sm border-blue-100 hover:border-blue-200 transition-all duration-200"
                headStyle={{ backgroundColor: "#f8fafc" }}
              >
                <div className="space-y-4">
                  <div>
                    <div className="font-semibold text-gray-700 mb-2 border-l-4 border-indigo-500 pl-2">
                      Đề bài &amp; Yêu cầu
                    </div>
                    <div
                      className="markdown-content text-gray-700 bg-gray-50/50 p-4 rounded-lg border border-gray-100"
                      dangerouslySetInnerHTML={{ __html: htmlContent }}
                    />
                  </div>
                  {ex.rubric && (
                    <div>
                      <div className="font-semibold text-gray-700 mb-2 border-l-4 border-green-500 pl-2">
                        Tiêu chí chấm điểm (AI)
                      </div>
                      <div
                        className="markdown-content text-gray-600 bg-green-50/10 p-4 rounded-lg border border-green-100"
                        dangerouslySetInnerHTML={{ __html: htmlRubric }}
                      />
                    </div>
                  )}
                </div>
              </Card>
            );
          })}
        </div>
      </div>
    );
  };

  const renderSingleExercise = (
    artifact: ArtifactResponse,
    exIndex: number,
  ) => {
    if (artifact.status === "Pending") {
      return (
        <div className="flex flex-col justify-center items-center h-[400px] gap-4 bg-gray-50 rounded-lg border border-dashed border-gray-300">
          <Spin size="large" />
          <div className="text-gray-500 italic">
            Agent đang miệt mài tạo Bài {exIndex}...
          </div>
        </div>
      );
    }

    if (artifact.status === "Failed") {
      return (
        <div className="flex flex-col justify-center items-center h-[400px] gap-4 bg-red-50 rounded-lg border border-dashed border-red-300">
          <XCircle size={36} className="text-red-500" />
          <div className="text-red-500 font-semibold">
            Gặp lỗi trong quá trình tự động sinh Bài {exIndex}.
          </div>
          <div className="text-gray-500 text-sm">
            Vui lòng bấm nút "Tạo AI" lại để hệ thống khôi phục từ checkpoint.
          </div>
        </div>
      );
    }

    if (!artifact.content_json) {
      return <Empty description="Không có dữ liệu bài tập" />;
    }

    const allExercises = (artifact.content_json.exercises || []) as HomeworkExercise[];
    const ex = allExercises.find((e) => e.index === exIndex);

    if (!ex) {
      return <Empty description={`Không tìm thấy Bài ${exIndex}`} />;
    }

    const htmlContent = DOMPurify.sanitize(
      marked.parse(ex.content || "") as string,
    );
    const htmlRubric = DOMPurify.sanitize(
      marked.parse(ex.rubric || "") as string,
    );

    return (
      <div className="max-h-[70vh] overflow-y-auto pr-2 space-y-6">
        <Card
          title={
            <div className="flex justify-between items-center w-full">
              <span className="font-bold text-base text-gray-800">
                Bài {ex.index}: {ex.title ? ex.title.replace(/<\/?[^>]+(>|$)/g, "").trim() : ""}
              </span>
              <span className="px-2.5 py-0.5 bg-blue-100 text-blue-800 text-xs font-semibold rounded-full uppercase tracking-wider">
                {ex.level}
              </span>
            </div>
          }
          className="shadow-sm border-blue-100 hover:border-blue-200 transition-all duration-200"
          headStyle={{ backgroundColor: "#f8fafc" }}
        >
          <div className="space-y-4">
            <div>
              <div className="font-semibold text-gray-700 mb-2 border-l-4 border-indigo-500 pl-2">
                Đề bài &amp; Yêu cầu
              </div>
              <div
                className="markdown-content text-gray-700 bg-gray-50/50 p-4 rounded-lg border border-gray-100"
                dangerouslySetInnerHTML={{ __html: htmlContent }}
              />
            </div>
            {ex.rubric && (
              <div>
                <div className="font-semibold text-gray-700 mb-2 border-l-4 border-green-500 pl-2">
                  Tiêu chí chấm điểm (AI)
                </div>
                <div
                  className="markdown-content text-gray-600 bg-green-50/10 p-4 rounded-lg border border-green-100"
                  dangerouslySetInnerHTML={{ __html: htmlRubric }}
                />
              </div>
            )}
          </div>
        </Card>
      </div>
    );
  };

  const renderSingleEntryTest = (
    artifact: ArtifactResponse,
    testIndex: number,
  ) => {
    if (artifact.status === "Pending") {
      return (
        <div className="flex flex-col justify-center items-center h-[400px] gap-4 bg-gray-50 rounded-lg border border-dashed border-gray-300">
          <Spin size="large" />
          <div className="text-gray-500 italic">
            Agent đang miệt mài tạo Đề kiểm tra {testIndex}...
          </div>
        </div>
      );
    }

    if (artifact.status === "Failed") {
      return (
        <div className="flex flex-col justify-center items-center h-[400px] gap-4 bg-red-50 rounded-lg border border-dashed border-red-300">
          <XCircle size={36} className="text-red-500" />
          <div className="text-red-500 font-semibold">
            Gặp lỗi trong quá trình tự động sinh Đề kiểm tra {testIndex}.
          </div>
          <div className="text-gray-500 text-sm">
            Vui lòng bấm nút "Tạo AI" lại để hệ thống khôi phục từ checkpoint.
          </div>
        </div>
      );
    }

    if (!artifact.content_json || !artifact.content_json.entry_tests) {
      return <Empty description="Không có dữ liệu đề kiểm tra" />;
    }

    const allTests = (artifact.content_json.entry_tests || []) as ProjectEntryTest[];
    const test = allTests[testIndex - 1];

    if (!test) {
      return <Empty description={`Không tìm thấy Đề kiểm tra ${testIndex}`} />;
    }

    const htmlContent = DOMPurify.sanitize(
      marked.parse(test.content || "") as string,
    );

    return (
      <div className="max-h-[70vh] overflow-y-auto pr-2 space-y-6">
        <Card
          title={
            <div className="flex justify-between items-center w-full">
              <span className="font-bold text-base text-gray-800">
                Đề kiểm tra {testIndex}: {test.title || `Bài kiểm tra đầu giờ ${testIndex}`}
              </span>
            </div>
          }
          className="shadow-sm border-blue-100 hover:border-blue-200 transition-all duration-200"
          headStyle={{ backgroundColor: "#f8fafc" }}
        >
          <div className="space-y-4">
            <div>
              <div className="font-semibold text-gray-700 mb-2 border-l-4 border-indigo-500 pl-2">
                Nội dung câu hỏi
              </div>
              <div
                className="markdown-content text-gray-700 bg-gray-50/50 p-4 rounded-lg border border-gray-100"
                dangerouslySetInnerHTML={{ __html: htmlContent }}
              />
            </div>
          </div>
        </Card>
      </div>
    );
  };

  const getItems = () => {
    if (!artifacts || artifacts.length === 0) return [];

    const items: Array<{
      key: string;
      label: React.ReactNode;
      children: React.ReactNode;
    }> = [];

    // Friendly labels for artifact types
    const labelsMap: Record<string, string> = {
      reading: "Bài đọc (HTML)",
      outline: "Sơ đồ tư duy (MD)",
      quiz: "Quizz & Lab",
      video_script: "Kịch bản video",
      pre_quiz: "Quizz đầu giờ",
      post_quiz: "Quizz cuối giờ",
      session_mindmap: "Sơ đồ tổng hợp",
      session_reading: "Bài đọc tổng hợp",
      project_entry_tests: "Bài kiểm tra đầu giờ",
      project_srs: "Tài liệu đặc tả SRS",
      project_mini_project: "Đề bài Mini Project",
    };

    for (const art of artifacts) {
      if (art.type === "session_homework") {
        // Create tab "Bài tập" (exercises index 1-5)
        items.push({
          key: `${art.id}_homework`,
          label: <span className="font-semibold">Bài tập</span>,
          children: (
            <ArtifactVersionWrapper
              artifact={art}
              lessonId={lessonId}
              sessionId={sessionId}
            >
              {(previewedArt) => renderHomeworkContent(previewedArt, "all")}
            </ArtifactVersionWrapper>
          ),
        });
      } else {
        items.push({
          key: art.id.toString(),
          label: (
            <span className="font-semibold">
              {labelsMap[art.type] || art.type}
            </span>
          ),
          children: (
            <ArtifactVersionWrapper
              artifact={art}
              lessonId={lessonId}
              sessionId={sessionId}
            >
              {(previewedArt) => renderContent(previewedArt)}
            </ArtifactVersionWrapper>
          ),
        });
      }
    }

    return items;
  };

  return (
    <Modal
      title={
        <div className="flex items-center gap-2 text-lg">
          Tài nguyên học tập:{" "}
          <span className="font-semibold text-blue-600">{title}</span>
        </div>
      }
      open={open}
      onCancel={onCancel}
      width={1100}
      footer={null}
      destroyOnClose
    >
      <div className="mt-4 min-h-[400px]">
        {isLoading ? (
          <div className="flex justify-center items-center h-40">
            <Spin size="large" />
          </div>
        ) : artifacts?.length === 0 ? (
          <Empty
            description={
              lessonId
                ? "Bài học này chưa được AI sinh tài nguyên nào. Hãy bấm nút 'Tạo AI' để bắt đầu."
                : "Session này chưa được sinh tài nguyên nào. Hãy bấm nút 'Tạo AI Session' để bắt đầu."
            }
          />
        ) : exerciseIndex !== undefined && exerciseIndex !== null ? (
          <div className="space-y-6 animate-fade-in">
            {artifacts?.map((art) => {
              if (art.type === "session_homework") {
                return (
                  <ArtifactVersionWrapper
                    key={art.id}
                    artifact={art}
                    lessonId={lessonId}
                    sessionId={sessionId}
                    exerciseIndex={exerciseIndex}
                  >
                    {(previewedArt) => renderSingleExercise(previewedArt, exerciseIndex)}
                  </ArtifactVersionWrapper>
                );
              }
              if (art.type === "project_entry_tests") {
                return (
                  <ArtifactVersionWrapper
                    key={art.id}
                    artifact={art}
                    lessonId={lessonId}
                    sessionId={sessionId}
                    exerciseIndex={exerciseIndex}
                  >
                    {(previewedArt) => renderSingleEntryTest(previewedArt, exerciseIndex)}
                  </ArtifactVersionWrapper>
                );
              }
              return null;
            })}
          </div>
        ) : (
          <Tabs items={getItems()} type="card" />
        )}
      </div>
    </Modal>
  );
};
