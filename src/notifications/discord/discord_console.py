from src.event_bus.event_bus import event_bus


class DiscordConsoleNotification:

    def send(self, profile):

        print("\n========== DISCORD ==========")

        print(f"Project : {profile.project_name}")

        print(f"Confidence : {profile.confidence_score}%")

        print(f"Signals : {profile.signal_count}")

        print(profile.ai_summary)

        print("=============================\n")


discord_console = DiscordConsoleNotification()

event_bus.subscribe(
    "intelligence_event",
    discord_console.send,
)