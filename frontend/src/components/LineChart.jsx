import { Line } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const LineChart = ({ chartData }) => {
  const datasets = chartData.map((dataset, index) => ({
    label: dataset.legend_label,
    data: dataset.data,
    borderColor: `hsl(${index * 100}, 70%, 50%)`,
    backgroundColor: `hsla(${index * 100}, 70%, 50%, 0.5)`,
  }));

  return (
    <div className="chart-box">
      <Line
        data={{ labels: chartData[0].labels, datasets }}
        options={{
          maintainAspectRatio: true,  // ✅ 차트 크기 비율 유지
          responsive: true,
          elements: {
              point: {
                radius: 0, // 점 크기 줄이기 (기본값: 3~4)
                hoverRadius: 4, // 마우스 오버 시 크기
              },
          },
          plugins: {
              title: {
                display: true,
                text: chartData[0].legend_label,
                font: {
                  size: 30, // 글자 크기 조정
                  weight: "bold",
                },
                padding: {
                  top: 2,
                  bottom: 10,
                },
              },
          },
        }}
      />
    </div>
  );
};

export default LineChart;
