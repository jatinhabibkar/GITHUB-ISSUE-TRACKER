import "./App.css";
import { useEffect, useState } from "react";
import MainChart from "./components/MainChart";
import ProjectChart from "./components/ProjectChart";
import axios from "axios";

function App() {
  const [options, setoptions] = useState([]);

  let config = {
    mode: "no-cors",
    headers: {
      "Content-Type": "text/json",
    },
    method: "GET",
  };

  useEffect(() => {
    axios
      .get(process.env.REACT_APP_BACKEND + "allUrl", config)
      .then((response) => {
        setoptions(response["data"]["data"]);
      });
    // eslint-disable-next-line
  }, []);

  return (
    <div className="App">
      <div className="container">
        <br />
        <br />
        <MainChart />
        {options.length > 0 &&
          options.map((urls, index) => {
            let urlsSplit = urls.split("/");
            let repo = urlsSplit.pop();
            let org = urlsSplit.pop();

            return (
              <div
                key={index}
                style={{
                  borderColor: "grey",
                  borderStyle: "solid",
                  margin: "10px",
                }}
              >
                <h5 style={{ textAlign: "center" }}>{org + "/" + repo}</h5>
                <ProjectChart repo={repo} org={org} />
              </div>
            );
          })}
      </div>
    </div>
  );
}

export default App;
