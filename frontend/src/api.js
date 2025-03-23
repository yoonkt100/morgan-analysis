import axios from "axios";

const BASE_URL = "http://localhost:8000";

export const fetchSections = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/information`);
    return response.data;
  } catch (error) {
    console.error("❌ 데이터 요청 실패:", error);
    return { sections: [] };
  }
};
