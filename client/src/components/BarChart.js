import React, { useState, useEffect } from "react";
import { Chart } from "react-google-charts";

export default function BarChart() {
  const [plotdata, setPlotData] = useState([]);
  let dataToSet = [];
  const getData = () => {
    fetch(`/data`, {
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        dataToSet = data["data"].map((item) => {
          return [item["url"].split("/").pop(), item["stars"], item["forks"]];
        });

        setPlotData([["star and forks", "stars", "forks"], ...dataToSet]);
      });
  };

  useEffect(() => {
    getData();
    // eslint-disable-next-line
  }, []);
  if (plotdata.length > 0)
    return (
      <div>
        <Chart
          chartType="Bar"
          data={plotdata}
          width="100%"
          height="400px"
          legendToggle
        />
      </div>
    );
}
