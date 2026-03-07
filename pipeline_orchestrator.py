"""
Pipeline Orchestrator
Controls the entire AI Shorts Factory pipeline
"""

from logging.logger import logger

# Trend analysis
from trend_analysis.youtube_trends import YouTubeTrends
from trend_analysis.google_trends import GoogleTrends
from trend_analysis.trend_ranker import TrendRanker
from trend_analysis.trend_selector import TrendSelector

# Discovery
from discovery.youtube_search import YouTubeSearch
from discovery.keyword_expander import KeywordExpander

# Downloader
from downloader.video_downloader import VideoDownloader

# Processing
from video_processing.normalize_video import NormalizeVideo
from video_processing.fps_sampler import FPSSampler
from video_processing.frame_extractor import FrameExtractor
from video_processing.audio_extractor import AudioExtractor

# Analysis
from analysis.transcription import Transcription
from analysis.scene_detection import SceneDetection
from analysis.audio_analysis import AudioAnalysis

# Hook detection
from hook_detection.hook_generator import HookGenerator

# Scoring
from scoring.viral_score import ViralScore
from scoring.clip_ranker import ClipRanker

# Clip selection
from clip_selection.clip_selector import ClipSelector

# Pacing
from pacing_engine.pacing_optimizer import PacingOptimizer

# Editing
from editing.clip_extractor import ClipExtractor
from editing.portrait_crop import PortraitCrop
from editing.jump_cut_engine import JumpCutEngine

# Effects
from effects.zoom_effects import ZoomEffects
from effects.motion_effects import MotionEffects
from effects.emphasis_effects import EmphasisEffects

# Subtitles
from subtitles.subtitle_engine import SubtitleEngine

# Metadata
from metadata.caption_generator import CaptionGenerator
from metadata.hashtag_generator import HashtagGenerator

# Quality
from quality_control.quality_filter import QualityFilter

# Export
from export.shorts_exporter import ShortsExporter
from export.thumbnail_generator import ThumbnailGenerator

# Upload
from upload.youtube_uploader import YouTubeUploader
from upload.tiktok_uploader import TikTokUploader


class PipelineOrchestrator:

    def run(self):

        logger.info("Starting RXG Shorts Pipeline")

        # =========================
        # 1. Trend Analysis
        # =========================

        yt_trends = YouTubeTrends().get_trends()
        google_trends = GoogleTrends().get_trending()

        ranked = TrendRanker().rank(yt_trends + google_trends)

        topic = TrendSelector().select(ranked)[0]

        logger.info(f"Selected topic: {topic}")

        # =========================
        # 2. Keyword Expansion
        # =========================

        keywords = KeywordExpander().expand(topic)

        # =========================
        # 3. Video Discovery
        # =========================

        videos = YouTubeSearch().search(keywords)

        if not videos:
            logger.warning("No videos found")
            return

        video_url = videos[0]

        logger.info(f"Selected video: {video_url}")

        # =========================
        # 4. Download
        # =========================

        video_path = VideoDownloader().download(video_url)

        # =========================
        # 5. Preprocessing
        # =========================

        video_path = NormalizeVideo().process(video_path)

        for _ in FPSSampler().sample(video_path):
    pass

        frames = FrameExtractor().extract_multiple(video_path,[1,3,5])

        audio = AudioExtractor().extract(video_path)

        # =========================
        # 6. Analysis
        # =========================

        transcript = Transcription().run(audio)

        scenes = SceneDetection().detect(video_path)

        audio_events = AudioAnalysis().analyze(audio)

        # =========================
        # 7. Hook Detection
        # =========================

        hooks = HookGenerator().generate(
            transcript,
            scenes,
            audio
        )

        # =========================
        # 8. Viral Scoring
        # =========================

        scored_clips = ViralScore().score(hooks)

        ranked_clips = ClipRanker().rank(scored_clips)

        # =========================
        # 9. Clip Selection
        # =========================

        selected_clip = ClipSelector().select(ranked_clips)

        # =========================
        # 10. Pacing Optimization
        # =========================

        paced_clip = PacingOptimizer().optimize(selected_clip)

        # =========================
        # 11. Editing
        # =========================

        clip_file = ClipExtractor().extract(video_path, paced_clip)

        clip_file = PortraitCrop().apply(clip_file)

        clip_file = JumpCutEngine().apply(clip_file)

        # =========================
        # 12. Effects
        # =========================

        clip_file = ZoomEffects().apply(clip_file)

        clip_file = MotionEffects().apply(clip_file)

        clip_file = EmphasisEffects().apply(clip_file)

        # =========================
        # 13. Subtitles
        # =========================

        clip_file = SubtitleEngine().generate(
            clip_file,
            transcript
        )

        # =========================
        # 14. Metadata
        # =========================

        caption = CaptionGenerator().generate(topic)

        hashtags = HashtagGenerator().generate()

        full_caption = f"{caption}\n\n{hashtags}"

        # =========================
        # 15. Quality Control
        # =========================

        passed = QualityFilter().filter([clip_file])

        if not passed:
            logger.warning("Video failed quality check")
            return

        # =========================
        # 16. Export
        # =========================

        final_video = ShortsExporter().export(clip_file)

        ThumbnailGenerator().generate(final_video)

        # =========================
        # 17. Upload
        # =========================

        YouTubeUploader().upload_video(
            final_video,
            caption=caption
        )

        TikTokUploader().upload_video(
            final_video,
            caption=full_caption
        )

        logger.info("Pipeline finished successfully")
