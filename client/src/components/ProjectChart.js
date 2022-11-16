import React, { useState, useEffect } from "react";
import { Chart } from "react-google-charts";
import axios from "axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

export default function ProjectChart({ repo = null, org = null }) {
  const [plotData, setPlotData] = useState([]);
  const [plotStackData, setPlotStackData] = useState([]);
  let config = {
    mode: "no-cors",
    headers: {
      "Content-Type": "text/json",
    },
    method: "GET",
  };
  const getData = () => {
    const commonData = [];
    let StackData = [];

    axios
      .get(process.env.REACT_APP_BACKEND + `data/${org}/${repo}`, config)
      .then((response) => {
        response.data["data"].forEach((item) => {
          commonData.push([
            item["dateStart"],
            item["open"],
            item["closed"],
            item["total"],
          ]);
          StackData.push({
            date: item["dateStart"],
            closed: item["closed"],
            total: item["total"],
          });
        });

        setPlotData([
          [`${org}-${repo}`, "open", "closed", "total"],
          ...commonData,
        ]);
        setPlotStackData(StackData);
        // {closed: 2, dateEnd: '2022-12-13', dateStart: '2022-11-13', open: 1, total: 3, …}
      });
  };

  useEffect(() => {
    getData();
    // eslint-disable-next-line
  }, []);
  if (plotData.length > 0)
    return (
      <>
        <div className="row">
          <div className="col s12 m6">
            <Chart
              chartType="LineChart"
              data={plotData}
              width="100%"
              height="600px"
              legendToggle
              options={{
                title: `${org}-${repo}`,
                curveType: "function",
                legend: { position: "bottom" },
              }}
            />
          </div>
          <div className="col s12 m6">
            <Chart
              chartType="BarChart"
              data={plotData.map((d) => d.slice(0, 3))}
              width="100%"
              height="600px"
              legendToggle
              options={{
                title: `${org}-${repo}`,
                curveType: "function",
                legend: { position: "bottom" },
                colors: ["#00FF00", "#A020F0"],
              }}
            />
          </div>
        </div>

        <div style={{ width: "100%", height: "400px" }}>
          <ResponsiveContainer>
            <BarChart
              width={500}
              height={300}
              data={plotStackData}
              margin={{
                top: 20,
                right: 30,
                left: 20,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="total" stackId="a" fill="#8884d8" />
              <Bar dataKey="closed" stackId="a" fill="#F4B400" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </>
    );
}
