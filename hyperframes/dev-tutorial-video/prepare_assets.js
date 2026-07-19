import fs from "fs";
import path from "path";
import { execSync } from "child_process";
import { fileURLToPath } from "url";

// Tái tạo lại biến __dirname trong môi trường ES Module
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Thông tin API ElevenLabs chính xác
const ELEVENLABS_API_KEY =
  "d5663f484bf69915d3dc6cc35b22b5856365a9ba68f64b2f6e1067e80cc70c52";
const ELEVENLABS_VOICE_ID = "6adFm46eyy74snVn6YrT"; // Đã cập nhật Voice ID mới của bạn
const BASE_URL = "https://api.elevenlabs.io";

// Kịch bản trích xuất từ file gốc, đã được bọc chuẩn hóa Unicode NFC chống lỗi dấu trên Mac
const scenes = [
  {
    id: "scene_01",
    text: "Ok, Xin chào tất cả các bạn! Trong bài học ngày hôm nay, chúng ta sẽ tìm hiểu về cấu trúc dữ liệu List trong Python. Hãy tưởng tượng, bạn phải quản lý danh sách sinh viên của một lớp học. Nếu suy nghĩ và sử dụng logic thông thường, bạn sẽ phải tạo ra hàng chục, thậm chí hàng trăm biến riêng lẻ như student 1, student 2. Điều này làm code cực kỳ rối và khó quản lý. Giải pháp ở đây là sử dụng List. List giống như một chiếc tủ đồ nhiều ngăn, cho phép bạn nhét tất cả dữ liệu có liên quan vào chung một chỗ, chỉ với một cái tên duy nhất. Và lúc này, thay vì chúng ta phải tạo ra hàng trăm biến, toàn bộ dữ liệu về sinh viên đã có thể lưu trữ trong 1 biến có cấu trúc duy nhất, cực kỳ gọn gàng và dễ dàng.",
  },
  {
    id: "scene_02",
    text: "Vậy tóm lại, List là gì? Nếu bạn đã từng tiếp xúc với các ngôn ngữ lập trình khác như C++, Java hay JavaScript, bạn sẽ thấy nó chính là khái niệm Mảng, hay Array. Sứ mệnh của cấu trúc dữ liệu này rất đơn giản: Giúp chúng ta nhóm và quản lý các đối tượng có tính chất tương đồng nhau cùng một chỗ - Chính là List, từ đó có thể sử dụng các phương thức có sẵn hoặc thuật toán để làm việc với các đối tượng trong List đó một cách cực kỳ đơn giản và dễ dàng. Cú pháp khai báo List sẽ cực kỳ ngắn gọn như sau: Bạn chỉ cần đặt một tên biến tương ứng với danh sách cần lưu trữ và quản lý, tiếp theo mở cặp ngoặc vuông, và đưa các giá trị, đối tượng có tính chất tương đồng nhau vào bên trong cặp ngoặc vuông đó. Vậy là xong! Mà nhớ giúp mình là mỗi một giá trị sẽ cách nhau bởi dấu phẩy nhé.",
  },
  {
    id: "scene_03",
    text: "Tiếp theo, để làm việc với List một cách hiệu quả, chắc chắn các bạn phải nhớ và lưu ý về 3 thuật ngữ sau. Thứ nhất là Element, tức là 'Phần tử', đại diện cho từng món đồ, từng giá trị được chứa ở bên trong List. Thứ hai là Index, tức là 'Chỉ số', nó giống như là số nhà, giúp xác định vị trí của từng phần tử trong List. Và cuối cùng là Length, tức là 'Độ dài', cho biết tổng số lượng phần tử đang có mặt bên trong List hay danh sách đó.",
  },
  {
    id: "scene_04",
    text: "Giờ hãy đặt 3 khái niệm đó vào lại trong danh sách sinh viên ban nãy mà chúng ta vừa lấy làm ví dụ. Bằng mắt thường, ta có thể nhìn thấy luôn là List này sẽ có 5 cái tên, vậy Độ dài - Length của nó sẽ là 5. Mỗi cái tên như 'An', 'Bình' là một phần tử hay một Element. Và cuối cùng, điều quan trọng nhất: Vị trí Index. Trong lập trình, chúng ta không bắt đầu đếm từ 1. Vị trí đầu tiên của danh sách luôn được đánh số là 0. Do đó, bạn An nằm ở Index số 0, và bạn Bình nằm ở Index số 1.",
  },
  {
    id: "scene_05",
    text: "Và cuối cùng, sau khi đã nắm rõ về các khái niệm, cách thức khai báo list rồi, chúng ta sẽ tiếp tục thử dùng lệnh 'print' để in toàn bộ biến students ra màn hình console và quan sát xem, Python sẽ in ra kết quả như thế nào nhé. Và boom! Toàn bộ danh sách đều được hiển thị ra màn hình console một cách hết sức tường minh, đơn giản và dễ dàng rồi nha. Và nếu các bạn muốn kiểm tra xem List này có bao nhiêu phần tử bằng code, chỉ cần dùng hàm built-in là 'len()', viết tắt của chữ length. Hàm này lập tức trả về kết quả cho chúng ta.",
  },
  {
    id: "scene_06",
    text: "Tổng kết lại, List là cấu trúc dữ liệu linh hoạt và được dùng nhiều nhất trong Python. Nhớ kỹ luật đếm từ 0 và các hàm cơ bản nhé. Hãy thử mở trình soạn thảo code lên và tạo ngay một List danh sách các món ăn yêu thích của bạn. Hẹn gặp lại trong bài học tiếp theo!",
  },
];

const ttsDir = path.join(__dirname, "courses/fundamental_python/assets/tts");
if (!fs.existsSync(ttsDir)) fs.mkdirSync(ttsDir, { recursive: true });

async function downloadTTS() {
  let durationMap = {};
  console.log("🚀 Bắt đầu quá trình tải 6 file audio...");

  for (const scene of scenes) {
    console.log(`\n⏳ Đang xử lý: ${scene.id}...`);
    const outputPath = path.join(ttsDir, `${scene.id}.mp3`);

    try {
      const response = await fetch(
        `${BASE_URL}/v1/text-to-speech/${ELEVENLABS_VOICE_ID}`,
        {
          method: "POST",
          headers: {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text: scene.text.normalize("NFC"), // Đảm bảo xử lý chuẩn hóa ký tự dựng sẵn tiếng Việt
            model_id: "eleven_v3", // Cấu hình chạy đúng Model v3 mới nhất
            voice_settings: {
              stability: 0.45, // Giữ độ ổn định tốt để tránh vấp từ
              similarity_boost: 0.65, // Tăng nhẹ để bám chuẩn sắc thái đặc trưng của giọng mẫu
              use_speaker_boost: true,
            },
          }),
        },
      );

      if (!response.ok) {
        const errorMsg = await response.text();
        console.error(
          `❌ Lỗi tải ${scene.id} - Mã lỗi: ${response.status} - Chi tiết: ${errorMsg}`,
        );
        continue;
      }

      const buffer = Buffer.from(await response.arrayBuffer());
      fs.writeFileSync(outputPath, buffer);

      // Bỏ grep đi để quét toàn bộ output, bắt cả chữ sec hoặc seconds
      const afinfoOut = execSync(`afinfo "${outputPath}"`).toString();
      const durationMatch = afinfoOut.match(/duration:\s*([\d.]+)\s*sec/i);
      const duration = durationMatch ? parseFloat(durationMatch[1]) : 0;

      durationMap[scene.id] = Math.round(duration * 100) / 100;
      console.log(
        `✅ Hoàn tất tải: ${scene.id}.mp3 | Thời lượng: ${durationMap[scene.id]} giây.`,
      );
    } catch (error) {
      console.error(`❌ Lỗi ngoại lệ tại ${scene.id}:`, error.message);
    }
  }

  const jsonPath = path.join(ttsDir, "durations.json");
  fs.writeFileSync(jsonPath, JSON.stringify(durationMap, null, 2));
  console.log(
    `\n🎉 Xong! Toàn bộ file âm thanh và file đo thời lượng đã được lưu tại: ${jsonPath}`,
  );
}

downloadTTS();
