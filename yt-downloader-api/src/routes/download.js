const express = require("express");
const ytdl = require("ytdl-core");
const router = express.Router();

router.get("/", async (req, res) => {
    const { url } = req.query;
    if (!url) return res.status(400).json({ error: "URL is required" });

    try {
        res.header("Content-Disposition", 'attachment; filename="video.mp4"');
        ytdl(url, { format: "mp4" }).pipe(res);
    } catch (error) {
        res.status(500).json({ error: "Download failed" });
    }
});

module.exports = router;
