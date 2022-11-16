import React, { useState, useEffect } from "react";
import { Chart } from "react-google-charts";
import axios from "axios";

export default function MainChart() {
  const [plotdata, setPlotData] = useState([]);
  let dataToSet = [];
  let config = {
    mode: "no-cors",
    headers: {
      "Content-Type": "text/json",
    },
    method: "GET",
  };
  const getData = () => {

    axios
    .get(process.env.REACT_APP_BACKEND + "data", config)
        .then((response) => {
          dataToSet = response.data["data"].map((item) => {
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
