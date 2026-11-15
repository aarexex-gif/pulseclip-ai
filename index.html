<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
  <meta name="theme-color" content="#09090b" />
  <title>PulseClip AI — Live Stream Auto-Clipper</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-zinc-950 text-zinc-100 min-h-screen font-sans selection:bg-yellow-400 selection:text-black">

  <header class="border-b border-zinc-800 bg-zinc-900/80 backdrop-blur sticky top-0 z-10">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between">
      <div class="flex items-center gap-2.5">
        <div class="w-3 h-3 rounded-full bg-red-500 animate-pulse"></div>
        <h1 class="text-lg sm:text-xl font-bold tracking-tight">PulseClip <span class="text-yellow-400">AI</span></h1>
      </div>
      <span class="text-[11px] bg-zinc-800 text-zinc-300 px-3 py-1 rounded-full border border-zinc-700">
        Cloud 9:16 Auto-Clipper
      </span>
    </div>
  </header>

  <main class="max-w-5xl mx-auto px-4 sm:px-6 py-6 sm:py-10">
    <div class="grid md:grid-cols-12 gap-6 sm:gap-8">

      <div class="md:col-span-7 space-y-6">
        <div class="bg-zinc-900 border border-zinc-800 rounded-2xl p-5 sm:p-6 shadow-xl">
          <h2 class="text-base sm:text-lg font-semibold mb-1">Paste Stream Link or Upload Video</h2>
          <p class="text-xs sm:text-sm text-zinc-400 mb-5">Finds the #1 viral hook with Gemini AI, reframes to 9:16, and burns word-by-word pop-up captions.</p>

          <div class="space-y-4">
            <div>
              <label class="block text-xs uppercase tracking-wider text-zinc-400 mb-2">Option 1: Stream / Video Link (Twitch, Kick, YouTube)</label>
              <input id="streamUrl" type="url" placeholder="https://..." 
                class="w-full bg-zinc-950 border border-zinc-800 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-yellow-400 transition" />
            </div>

            <div class="relative flex py-1 items-center">
              <div class="flex-grow border-t border-zinc-800"></div>
              <span class="flex-shrink mx-3 text-xs text-zinc-500 uppercase">OR</span>
              <div class="flex-grow border-t border-zinc-800"></div>
            </div>

            <div>
              <label class="block text-xs uppercase tracking-wider text-zinc-400 mb-2">Option 2: Upload Video From Phone / PC (Bypasses YouTube IP Blocks)</label>
              <input id="videoFile" type="file" accept="video/*"
                class="w-full bg-zinc-950 border border-zinc-800 rounded-xl px-4 py-2.5 text-sm text-zinc-300 file:mr-4 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-bold file:bg-yellow-400 file:text-black hover:file:bg-yellow-300" />
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-xs uppercase tracking-wider text-zinc-400 mb-2">9:16 Framing Style</label>
                <select id="cropStyle" class="w-full bg-zinc-950 border border-zinc-800 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-yellow-400">
                  <option value="center">Center Crop (IRL / Podcast)</option>
                  <option value="split">Split-Screen (Gameplay + Facecam)</option>
                </select>
              </div>

              <div>
                <label class="block text-xs uppercase tracking-wider text-zinc-400 mb-2">Watch Buffer (Seconds)</label>
                <input id="duration" type="number" value="120" min="30" max="900"
                  class="w-full bg-zinc-950 border border-zinc-800 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-yellow-400" />
              </div>
            </div>

            <details class="bg-zinc-950 border border-zinc-800 rounded-xl p-3 text-xs text-zinc-400">
              <summary class="cursor-pointer font-medium text-zinc-300">Advanced: Paste YouTube Cookies (if YouTube blocks cloud IP)</summary>
              <textarea id="cookiesTxt" rows="3" placeholder="Paste Netscape cookies.txt content here if YouTube asks to sign in..."
                class="w-full mt-2 bg-zinc-900 border border-zinc-800 rounded-lg p-2 text-xs text-zinc-200 focus:outline-none focus:border-yellow-400"></textarea>
            </details>

            <button onclick="startClipping()" id="submitBtn"
              class="w-full bg-yellow-400 hover:bg-yellow-300 active:scale-[0.99] text-black font-bold py-3.5 rounded-xl transition shadow-lg shadow-yellow-400/10">
              ⚡ Launch AI Clipper Bot
            </button>
          </div>
        </div>

        <div id="statusCard" class="hidden bg-zinc-900 border border-zinc-800 rounded-2xl p-5 sm:p-6">
          <div class="flex items-center justify-between mb-3">
            <span id="statusText" class="text-sm font-medium text-yellow-400 animate-pulse">Initializing...</span>
            <span id="progressPercent" class="text-xs font-mono text-zinc-400">0%</span>
          </div>
          <div class="w-full bg-zinc-950 h-2.5 rounded-full overflow-hidden border border-zinc-800">
            <div id="progressBar" class="bg-yellow-400 h-full transition-all duration-500" style="width: 0%"></div>
          </div>
        </div>
      </div>

      <div class="md:col-span-5">
        <div class="bg-zinc-900 border border-zinc-800 rounded-2xl p-5 sm:p-6 flex flex-col items-center justify-center min-h-[420px]">
          <div id="emptyState" class="text-center space-y-3 px-4">
            <div class="w-14 h-14 rounded-2xl bg-zinc-800 flex items-center justify-center mx-auto text-2xl">📱</div>
            <p class="text-sm text-zinc-400">Your edited 9:16 viral clip with word-by-word pop-up captions will appear here ready to save to your phone.</p>
          </div>

          <div id="resultCard" class="hidden w-full space-y-4">
            <div class="flex items-center justify-between gap-2">
              <span class="text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded bg-green-500/20 text-green-400 border border-green-500/30">
                Virality: <span id="viralScore">95</span>/100
              </span>
              <span class="text-xs font-medium px-2.5 py-1 rounded bg-yellow-500/15 text-yellow-300 border border-yellow-500/30">
                9:16 Vertical HD
              </span>
            </div>

            <h3 id="clipTitle" class="font-bold text-base text-white"></h3>
            <p id="clipReason" class="text-xs text-zinc-400"></p>

            <video id="videoPreview" controls playsinline class="w-full rounded-xl border border-zinc-800 bg-black aspect-[9/16] max-h-[380px] mx-auto"></video>

            <a id="downloadBtn" href="#" download
              class="block text-center w-full bg-white hover:bg-zinc-200 text-black font-bold py-3.5 rounded-xl transition">
              ⬇️ Save Ready-to-Post Clip (.MP4)
            </a>
          </div>
        </div>
      </div>

    </div>
  </main>

  <script>
    let pollInterval = null;

    async function startClipping() {
      const url = document.getElementById("streamUrl").value.trim();
      const fileInput = document.getElementById("videoFile");
      const crop_style = document.getElementById("cropStyle").value;
      const duration = parseInt(document.getElementById("duration").value);
      const cookies_txt = document.getElementById("cookiesTxt").value.trim();

      if (!url && (!fileInput.files || fileInput.files.length === 0)) {
        alert("Please paste a stream URL or choose a video file from your device.");
        return;
      }

      document.getElementById("submitBtn").disabled = true;
      document.getElementById("submitBtn").innerText = "🤖 AI Bot Working...";
      document.getElementById("statusCard").classList.remove("hidden");
      document.getElementById("statusText").className = "text-sm font-medium text-yellow-400 animate-pulse";
      document.getElementById("emptyState").classList.remove("hidden");
      document.getElementById("resultCard").classList.add("hidden");

      try {
        let res;
        if (fileInput.files && fileInput.files.length > 0) {
          const formData = new FormData();
          formData.append("file", fileInput.files[0]);
          formData.append("crop_style", crop_style);
          res = await fetch("/api/upload", { method: "POST", body: formData });
        } else {
          res = await fetch("/api/clip", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url, mode: "vod", crop_style, duration, cookies_txt })
          });
        }
        const data = await res.json();
        pollStatus(data.job_id);
      } catch (err) {
        alert("Server connection failed. Check if your cloud server is awake.");
        resetButton();
      }
    }

    function pollStatus(jobId) {
      pollInterval = setInterval(async () => {
        try {
          const res = await fetch(`/api/status/${jobId}`);
          const job = await res.json();

          document.getElementById("statusText").innerText = job.status;

          if (job.progress >= 0) {
            document.getElementById("progressPercent").innerText = `${job.progress}%`;
            document.getElementById("progressBar").style.width = `${job.progress}%`;
          } else {
            clearInterval(pollInterval);
            document.getElementById("statusText").className = "text-sm font-medium text-red-400";
            resetButton();
          }

          if (job.progress === 100) {
            clearInterval(pollInterval);
            resetButton();
            showResult(job);
          }
        } catch (e) {
          console.error("Polling error:", e);
        }
      }, 2000);
    }

    function showResult(job) {
      document.getElementById("emptyState").classList.add("hidden");
      document.getElementById("resultCard").classList.remove("hidden");
      document.getElementById("viralScore").innerText = job.virality_score;
      document.getElementById("clipTitle").innerText = job.hook_title;
      document.getElementById("clipReason").innerText = job.reason;

      const video = document.getElementById("videoPreview");
      video.src = job.video_url;
      video.load();

      const dlBtn = document.getElementById("downloadBtn");
      dlBtn.href = job.video_url;
    }

    function resetButton() {
      const btn = document.getElementById("submitBtn");
      btn.disabled = false;
      btn.innerText = "⚡ Launch AI Clipper Bot";
    }
  </script>
</body>
</html>
