from src.collectors.project_discovery_collector import collector
from src.pipeline.intelligence_pipeline import pipeline

# Register Discord console notification
import src.notifications.discord.discord_console


event = collector.execute()

pipeline.process(event)