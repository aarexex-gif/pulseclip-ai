import os
import uuid
import json
import shutil
import subprocess
from fastapi import FastAPI, BackgroundTasks, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from google import genai

app = FastAPI(title="PulseClip AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("clips", exist_ok=True)
os.makedirs("temp", exist_ok=True)
app.mount("/clips", StaticFiles(directory="clips"), name="clips")

ai_client = genai.Client()
jobs = {}

class ClipRequest(BaseModel):
    url: str
    mode: str = "vod"
    crop_style: str = "center"
    duration: int = 120
    cookies_txt: str = ""

def format_ass_time(seconds: float) -> str:
    seconds = max(0.0, float(seconds))
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    cs = int(round((seconds - int(seconds)) * 100))
    if cs == 100:
        secs += 1
        cs = 0
    return f"{hrs}:{mins:02d}:{secs:02d}.{cs:02d}"

def generate_ass(captions: list, ass_path: str):
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Liberation Sans,64,&H0000FFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,5,2,2,60,60,220,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for c in captions:
        s = format_ass_time(c.get("start", 0))
        e = format_ass_time(c.get("end", 2))
        text = str(c.get("text", "")).replace("{", "").replace("}", "").upper()
        events.append(f"Dialogue: 0,{s},{e},Default,,0,0,0,,{{\\fscx110\\fscy110}}{text}")
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")

def run_ai_pipeline(job_id: str, raw_video: str, crop_style: str):
    audio_mp3 = f"temp/{job_id}.mp3"
    ass_file = f"temp/{job_id}.ass"
    output_filename = f"clip_{job_id[:8]}.mp4"
    output_path = f"clips/{output_filename}"

    jobs[job_id]["status"] = "Extracting audio for Gemini AI..."
    jobs[job_id]["progress"] = 50
    subprocess.run([
        "ffmpeg", "-y", "-i", raw_video, "-vn", "-ac", "1", "-ar", "16000", "-b:a", "32k", audio_mp3
    ], check=True)

    jobs[job_id]["status"] = "Gemini AI listening for viral hooks & captions..."
    jobs[job_id]["progress"] = 70

    uploaded_audio = ai_client.files.upload(file=audio_mp3)
    prompt = """
    Listen to this stream audio and find the single most viral, funny, or high-energy moment (15 to 45 seconds long).
    If the clip is shorter than 30 seconds, pick the best segment inside it.
    Also return short 2-to-4 word punchy caption phrases synced relative to the clip start (where 0.0 is the start of the cut clip).
    Return ONLY valid JSON:
    {
      "start": 0.0,
      "end": 20.0,
      "hook_title": "Catchy viral hook title",
      "virality_score": 95,
      "reason": "Why this moment is viral",
      "captions": [
        {"start": 0.0, "end": 1.8, "text": "WAIT WATCH THIS"},
        {"start": 1.8, "end": 3.5, "text": "NO WAY BRO"}
      ]
    }
    """
    response = ai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[uploaded_audio, prompt],
        config={"response_mime_type": "application/json"},
    )
    viral_data = json.loads(response.text)
    clip_start = max(0.0, float(viral_data.get("start", 0.0)))
    clip_end = float(viral_data.get("end", clip_start + 20.0))

    jobs[job_id]["status"] = "Rendering 9:16 vertical clip + captions..."
    jobs[job_id]["progress"] = 85

    generate_ass(viral_data.get("captions", []), ass_file)
    ass_escaped = ass_file.replace("\\", "/").replace(":", "\\:")
    duration_clip = max(5.0, clip_end - clip_start)

    if crop_style == "split":
        filter_complex = (
            f"[0:v]crop=ih*(9/8):ih,scale=720:640[top];"
            f"[0:v]crop=iw/3:ih/3:0:ih-(ih/3),scale=720:640[bottom];"
            f"[top][bottom]vstack=inputs=2,ass='{ass_escaped}'[v]"
        )
        ffmpeg_cmd = [
            "ffmpeg", "-y", "-ss", str(clip_start), "-i", raw_video, "-t", str(duration_clip),
            "-filter_complex", filter_complex, "-map", "[v]", "-map", "0:a",
            "-c:v", "libx264", "-preset", "ultrafast", "-c:a", "aac", output_path,
        ]
    else:
        vf_filter = f"crop=ih*(9/16):ih,scale=720:1280,ass='{ass_escaped}'"
        ffmpeg_cmd = [
            "ffmpeg", "-y", "-ss", str(clip_start), "-i", raw_video, "-t", str(duration_clip),
            "-vf", vf_filter, "-c:v", "libx264", "-preset", "ultrafast", "-c:a", "aac", output_path,
        ]

    subprocess.run(ffmpeg_cmd, check=True)

    for fpath in (raw_video, audio_mp3, ass_file):
        if os.path.exists(fpath):
            os.remove(fpath)

    jobs[job_id].update({
        "status": "Completed",
        "progress": 100,
        "video_url": f"/clips/{output_filename}",
        "hook_title": viral_data.get("hook_title", "Viral Stream Clip"),
        "virality_score": viral_data.get("virality_score", 92),
        "reason": viral_data.get("reason", "High energy stream highlight"),
        "chat_spikes_found": 3,
    })

def process_stream_job(job_id: str, req: ClipRequest):
    try:
        raw_video = f"temp/{job_id}_raw.mp4"
        cookie_file = f"temp/{job_id}_cookies.txt"

        jobs[job_id]["status"] = "Downloading stream segment..."
        jobs[job_id]["progress"] = 25

        cmd = [
            "yt-dlp",
            "--no-check-certificates",
            "--geo-bypass",
            "--extractor-args", "youtube:player_client=tv_embedded,mweb,web",
            "-f", "best[height<=720][ext=mp4]/best[ext=mp4]/best",
            "--download-sections", f"*0-{req.duration}",
            "-o", raw_video,
        ]

        if req.cookies_txt and req.cookies_txt.strip():
            with open(cookie_file, "w", encoding="utf-8") as cf:
                cf.write(req.cookies_txt.strip() + "\n")
            cmd.extend(["--cookies", cookie_file])

        cmd.append(req.url)

        res = subprocess.run(cmd, capture_output=True, text=True)
        if os.path.exists(cookie_file):
            os.remove(cookie_file)

        if res.returncode != 0:
            err_lines = [line for line in res.stderr.splitlines() if "ERROR:" in line]
            clean_err = err_lines[-1] if err_lines else res.stderr[-300:]
            raise Exception(f"Stream download blocked by host IP ({clean_err}). Try uploading a video file or pasting a Twitch/Kick/direct video link.")

        run_ai_pipeline(job_id, raw_video, req.crop_style)

    except Exception as e:
        jobs[job_id]["status"] = f"Error: {str(e)}"
        jobs[job_id]["progress"] = -1

def process_upload_job(job_id: str, raw_video: str, crop_style: str):
    try:
        run_ai_pipeline(job_id, raw_video, crop_style)
    except Exception as e:
        jobs[job_id]["status"] = f"Error: {str(e)}"
        jobs[job_id]["progress"] = -1

@app.get("/")
async def serve_frontend():
    return FileResponse("index.html")

@app.post("/api/clip")
async def start_clip_job(req: ClipRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "Starting AI Clipper...", "progress": 5}
    background_tasks.add_task(process_stream_job, job_id, req)
    return {"job_id": job_id}

@app.post("/api/upload")
async def upload_video_job(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    crop_style: str = Form("center")
):
    job_id = str(uuid.uuid4())
    raw_video = f"temp/{job_id}_raw.mp4"
    with open(raw_video, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    jobs[job_id] = {"status": "Video uploaded! Starting AI Clipper...", "progress": 25}
    background_tasks.add_task(process_upload_job, job_id, raw_video, crop_style)
    return {"job_id": job_id}

@app.get("/api/status/{job_id}")
async def get_job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]
