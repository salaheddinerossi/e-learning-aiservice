
from fastapi import APIRouter, HTTPException

from app.services.summary_service import analyze_and_summarize_transcription
from app.services.video_conversion_service import download_video, convert_video_to_audio
from pydantic import BaseModel

router = APIRouter()


class VideoRequest(BaseModel):
    url: str

# @router.post("/convert-and-transcribe/")
# def convert_and_transcribe_video(request_body: VideoRequest):
#     try:
#         video_path = download_video(request_body.url)
#         audio_path = convert_video_to_audio(video_path)
#         transcribed_text = transcribe_audio_to_text_with_openai_api(audio_path)
#         return {"message": "Conversion and transcription successful", "audio_path": audio_path, "transcribed_text": transcribed_text}
#     except Exception as e:
#         print(f"Error in convert_and_transcribe_video: {e}")
#         raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-transcription/")
def analyze_transcription(request_body: VideoRequest):
    try:
        video_path = download_video(request_body.url)
        audio_path = convert_video_to_audio(video_path)
        transcribed_text = "Git, a system for keeping track of changes that happen across a set of files. Open a directory on your local system with an editor like VS Code. Then run git init from the command line. You just created a git repository or repo. It lives in this hidden git directory and keeps track of all the changes that happen to these files. As you work on a codebase, you take snapshots or commits of the current state of these files. Every commit has a unique ID and is linked to its parent, and this means we can travel back in time to a previous version of our files. Notice how our source control icon is lit up. Currently, all of our files are untracked because we need to add them to the repo. Run git add to include or stage these files in the repo. Then create a snapshot of their current state by running git commit along with a message about what you did to these files. Congratulations, you just created the first commit on the head of the master branch in this repo. The changed files disappeared and you're now on a clean working directory. The head represents the most recent commit. If we make some changes, commit them to the repo, the head moves forward, but we still have a reference to our previous commit so we can always go back to it. But the thing about software is that it's developed in a nonlinear fashion. You might have multiple teams working on different features for the same codebase simultaneously. Git makes that possible by branching. Create one by running git branch, and then run git checkout to move into that branch. You can now safely work on your feature in this branch without affecting the code or files in the master branch. The commits you make here live in an alternate universe with its own unique history. At some point though, you'll likely want to merge this history with the history in the master branch. When you're ready, go back to the master branch by running git checkout. Then run git merge on your alternate universe. The tip of your feature branch now becomes the head of the master branch. Or in other words, our fragmented universe has become one. Unless you ran into a merge conflict, in which case you'll just have to wait for the sequel. This has been Git Explained in 100 seconds. If you want to see more short videos like this, make sure to hit the like button, subscribe, and let me know what you think in the comments. Thanks for watching and I will see you in the next one."
        analysis_result = analyze_and_summarize_transcription(transcribed_text)

        return {
            "message": "Analysis successful",
            # "audio_path": audio_path,
            "analysis_result": analysis_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



