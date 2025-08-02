const mic = require("mic");
const fs = require("fs");
const fetch = require("node-fetch");
const FormData = require("form-data");

const expectedPhrase = "Hello";
const outputPath = "./recorded.wav";
const SERVER_URL = "http://127.0.0.1:5000";
const RECORD_DURATION_MS = 5000;

const deleteFile = true;

console.log("🎙️ Starting microphone recording for 5 seconds...");

const micInstance = mic({
  rate: "16000", // Sample rate for Vosk model
  channels: "1",
  bitwidth: "16",
  encoding: "signed-integer",
  fileType: "wav",
});

const micInputStream = micInstance.getAudioStream();
const outputFileStream = fs.WriteStream(outputPath);

micInputStream.pipe(outputFileStream);

// Handle errors
micInputStream.on("error", (err) => {
  console.error("❌ Mic error:", err);
});

micInstance.start();

setTimeout(() => {
  micInstance.stop();
  console.log("✅ Recording finished. Sending to /check-voice...");

  const form = new FormData();
  form.append("expected", expectedPhrase);
  form.append("audio", fs.createReadStream(outputPath), "recorded.wav");

  fetch(`${SERVER_URL}/check-voice`, {
    method: "POST",
    body: form,
    headers: form.getHeaders(),
  })
    .then((res) => res.json())
    .then((data) => {
      console.log("🎯 Match Check Response:");
      console.log(data);

      // Clean up the file
      if (deleteFile) {
        fs.unlink(outputPath, (err) => {
          if (err) console.error("❌ Failed to delete file:", err);
          else console.log("🧹 Temporary audio file deleted.");
        });
      }
    })
    .catch((err) => {
      console.error("❌ Fetch Error:", err.message);
    });
}, RECORD_DURATION_MS);
