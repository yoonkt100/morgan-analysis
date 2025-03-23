import LineChart from "./LineChart";
import "../App.css";

const Section = ({ section, sectionIndex }) => {
  return (
    <div className={`section section-${sectionIndex + 1}`}>
      <div className="section-title">{section.text}</div>
      <div className="graph-container">
        {section.graphs.map((graph) => (
          <LineChart key={graph.id} chartData={graph.data} />
        ))}
      </div>
    </div>
  );
};

export default Section;
