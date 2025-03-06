const express = require("express");
const cors = require("cors");
require("dotenv").config();

const app = express();
app.use(cors());

app.use("/download", require("./routes/download"));
app.use("/info", require("./routes/info"));

app.listen(3000, () => console.log("Server running on port 3000"));
