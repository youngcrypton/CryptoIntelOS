from src.intelligence.detectors.change_detector import (
    change_detector,
)

from src.intelligence.normalizers.website_normalizer import (
    website_normalizer,
)

from src.intelligence.extractors.website_extractor import (
    website_extractor,
)

from src.intelligence.engine.registry import (
    intelligence_registry,
)

from src.services.website_snapshot_service import (
    website_snapshot_service,
)

from src.services.event_service import (
    event_service,
)

from src.intelligence.rules.rule_engine import (
    rule_engine,
)


class WebsiteIntelligenceService:
    """
    Handles all website intelligence.
    """

    def process(
        self,
        project,
        result,
    ):

        payload = result.payload

        print(f"Title       : {payload.title}")
        print(f"Description : {payload.description}")
        print(f"HTML Size   : {len(payload.html):,} characters")

        # ------------------------------------------
        # Normalize Website
        # ------------------------------------------

        current_data = website_normalizer.normalize(
            payload
        )

        previous_snapshot = (
            website_snapshot_service.get_latest_snapshot(
                project.name
            )
        )

        previous_data = None

        if previous_snapshot:

            previous_data = {
                "url": previous_snapshot.url,
                "title": previous_snapshot.title,
                "description": previous_snapshot.description,
                "html_hash": previous_snapshot.html_hash,
            }

        # ------------------------------------------
        # Detect Website Changes
        # ------------------------------------------

        changes = change_detector.compare(
            previous_data,
            current_data,
        )

        if changes:

            print("\n========== Website Changes ==========\n")

            for change in changes:

                print(change["field"])
                print(f"Old : {change['old']}")
                print(f"New : {change['new']}\n")

        # ------------------------------------------
        # Save Website Snapshot
        # ------------------------------------------

        changed = website_snapshot_service.save_snapshot(
            project.name,
            payload,
        )

        # ------------------------------------------
        # Record Website Event
        # ------------------------------------------

        if changed:

            event_service.record_event(
                project=result.project,
                source=result.collector,
                signal_type=result.signal_type,
                title=result.title,
                summary=result.summary,
                priority="Medium",
                confidence=result.confidence,
                evidence=result.evidence,
            )

        # ------------------------------------------
        # Extract Structured Website Profile
        # ------------------------------------------

        print("\n========== Website Extraction ==========\n")

        profile = website_extractor.extract(
            payload
        )

        print(f"Title         : {profile.title}")
        print(f"Description   : {profile.description}")
        print(f"Token         : {profile.token}")
        print(f"Users         : {profile.users}")
        print(f"Daily Volume  : {profile.daily_volume}")
        print(f"Max TPS       : {profile.max_tps}")
        print(f"Block Time    : {profile.block_time}")
        print(f"GitHub Links  : {len(profile.github)}")
        print(f"Docs          : {len(profile.docs)}")
        print(f"Audits        : {len(profile.audits)}")
        print(f"Whitepapers   : {len(profile.whitepapers)}")

        print()

        # ------------------------------------------
        # Rule Engine
        # ------------------------------------------

        print("\n========== Rule Engine ==========\n")

        findings = rule_engine.run(
            profile
        )

        if not findings:

            print("No intelligence findings.\n")

        else:

            for finding in findings:

                print(f"[{finding.severity}] {finding.title}")
                print(f"Summary : {finding.summary}")
                print(f"Confidence : {finding.confidence}%")
                print()

                event_service.record_event(
                    project=result.project,
                    source="Rule Engine",
                    signal_type="Website Finding",
                    title=finding.title,
                    summary=finding.summary,
                    priority=finding.severity,
                    confidence=finding.confidence,
                    evidence=finding.evidence,
                )


website_intelligence_service = WebsiteIntelligenceService()

intelligence_registry.register(
    "Website Collector",
    website_intelligence_service,
)