import { useEffect, useState } from "react";
import { fetchSections } from "../api";
import Section from "./Section";

const Dashboard = () => {
  const [sections, setSections] = useState([]);

  useEffect(() => {
    fetchSections().then((data) => {
      setSections(data.sections);
    });
  }, []);

  return (
    <div className="dashboard">
      {sections.length > 0 ? (
        sections.map((section, index) => <Section key={index} section={section} sectionIndex={index} />)
      ) : (
        <p>⏳⏳ 데이터 로딩 중... ⏳⏳</p>
      )}
    </div>
  );
};

export default Dashboard;
