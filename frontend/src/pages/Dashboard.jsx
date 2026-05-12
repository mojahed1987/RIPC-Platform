import { useEffect, useState } from "react";

function Dashboard() {

  const [data, setData] = useState([]);

  useEffect(() => {

    fetch("http://127.0.0.1:8000/restrictions")
      .then((response) => response.json())
      .then((json) => {
        console.log(json);
        setData(json);
      });

  }, []);

  return (

    <div style={{ padding: "20px" }}>

      <h1>RIPC Restrictions Dashboard</h1>

      <table
        border="1"
        cellPadding="10"
        style={{
          borderCollapse: "collapse",
          width: "100%"
        }}
      >

        <thead>

          <tr>

            <th>ID</th>
            <th>Request ID</th>
            <th>Status</th>
            <th>HTTP Status</th>
            <th>Created At</th>

          </tr>

        </thead>

        <tbody>

          {data.map((row) => (

            <tr key={row.id}>

              <td>{row.id}</td>
              <td>{row.request_id}</td>
              <td>{row.status}</td>
              <td>{row.http_status}</td>
              <td>{row.created_at}</td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>

  );

}

export default Dashboard;