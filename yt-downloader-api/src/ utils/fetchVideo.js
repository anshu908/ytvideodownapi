const ytdl = require("ytdl-core");

async function fetchVideo(url) {
    const info = await ytdl.getInfo(url);
    return {
        title: info.videoDetails.title,
        duration: info.videoDetails.lengthSeconds,
        thumbnail: info.videoDetails.thumbnails.pop().url,
        formats: info.formats.map(f => ({ quality: f.qualityLabel, url: f.url }))
    };
}

module.exports = fetchVideo;
